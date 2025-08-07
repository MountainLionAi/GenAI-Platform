"""
Intelligent Search Tool
Analyzes chat history using Claude Sonnet 4 to break down complex queries
into simple search tasks, then executes them using Serper and CoinGecko APIs.
"""

import asyncio
import json
import os
import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from functools import wraps
import logging
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import anthropic
from dotenv import load_dotenv
import backoff
import pytz

# Load environment variables
load_dotenv()

# Configure structured logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Custom JSON formatter for structured logs
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
        }
        if hasattr(record, 'extra_data'):
            log_obj.update(record.extra_data)
        return json.dumps(log_obj)

# Apply JSON formatter
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.handlers = [handler]


@dataclass
class SearchQuery:
    """Represents a single search query with metadata"""
    query: str
    api_type: str  # 'serper' or 'coingecko'
    endpoint: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1
    description: str = ""


@dataclass
class APIConfig:
    """Configuration for API keys and settings"""
    anthropic_api_key: str
    serper_api_key: str
    coingecko_api_key: str
    max_retries: int = 3
    timeout: int = 30
    max_concurrent_requests: int = 6


class IntelligentSearchTool:
    """Main class for intelligent search functionality"""
    
    def __init__(self):
        # Load API keys from environment
        self.config = APIConfig(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            serper_api_key=os.getenv("GOOGLE_SERPER_API_KEY"),
            coingecko_api_key=os.getenv("COINGECKO_API_KEY")
        )
        
        # Validate API keys
        if not all([self.config.anthropic_api_key, self.config.serper_api_key, self.config.coingecko_api_key]):
            raise ValueError("Missing required API keys in .env file")
        
        # Initialize Anthropic client
        self.claude_client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
        
        # Get system timezone
        self.system_timezone = self._get_system_timezone()
        self.current_time = datetime.now(self.system_timezone)
        
        # Semaphore for rate limiting
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
    
    def _get_system_timezone(self) -> timezone:
        """Get current system timezone"""
        try:
            # Try to get local timezone
            local_tz = datetime.now().astimezone().tzinfo
            return local_tz
        except:
            # Fallback to UTC
            return timezone.utc
    
    @backoff.on_exception(
        backoff.expo,
        (anthropic.RateLimitError, anthropic.APITimeoutError),
        max_tries=3,
        jitter=backoff.full_jitter
    )
    def _analyze_chat_with_claude(self, chat_history: List[Dict[str, str]]) -> List[SearchQuery]:
        """Use Claude Sonnet 4 to analyze chat history and generate search queries"""
        
        # Create the tool definition for structured output
        tools = [{
            "name": "generate_search_queries",
            "description": "Generate structured search queries based on the conversation",
            "input_schema": {
                "type": "object",
                "properties": {
                    "queries": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "The search query string"},
                                "api_type": {"type": "string", "enum": ["serper", "coingecko"], "description": "Which API to use"},
                                "endpoint": {"type": "string", "description": "API endpoint to use"},
                                "parameters": {"type": "object", "description": "Additional parameters for the API call"},
                                "priority": {"type": "integer", "minimum": 1, "maximum": 5, "description": "Priority level (1=highest)"},
                                "description": {"type": "string", "description": "Why this search is needed"}
                            },
                            "required": ["query", "api_type", "endpoint", "priority", "description"]
                        },
                        "maxItems": 6
                    }
                },
                "required": ["queries"]
            }
        }]
        
        # Build the prompt
        system_prompt = f"""You are an intelligent search query generator. Current time: {self.current_time.isoformat()}
System timezone: {self.system_timezone}

Analyze the conversation and break down complex questions into simple, specific search queries (maximum 6).

For each query, determine:
1. Use 'serper' API for: general web searches, news, images, shopping, places, academic content
2. Use 'coingecko' API for: cryptocurrency prices, market data, trading volumes, historical crypto data

Serper endpoints:
- /search (general web)
- /news (recent news)
- /images (image search)
- /shopping (product search)
- /places (location-based)
- /scholar (academic)

For Serper searches, ALWAYS include time range in parameters when relevant:
- "tbs": "qdr:h" for 1 hour (breaking news, real-time events)
- "tbs": "qdr:d" for 24 hours (recent news, daily updates)
- "tbs": "qdr:w" for 1 week (weekly trends, recent developments)
- "tbs": "qdr:m" for 1 month (monthly reports, recent changes)
- "tbs": "qdr:y" for 1 year (annual data, yearly trends)

Query string "q" should include current time context when relevant:
- Add "2025" for current year searches
- Include "this week", "today", "recent" when asking for latest info
- Use "August 2025" for current month when relevant

CoinGecko endpoints:
- /simple/price (current prices)
- /coins/markets (market overview)
- /coins/{id}/market_chart (historical data)
- /coins/{id}/ohlc (OHLC data)

Consider time constraints and prioritize queries by importance."""

        # Format chat history
        formatted_history = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in chat_history
        ])
        
        user_message = f"""<conversation_history>
{formatted_history}
</conversation_history>

Analyze this conversation and generate appropriate search queries to answer the user's questions comprehensively.

IMPORTANT GUIDELINES:
1. For time-sensitive queries, include current date/time context in the "q" parameter
2. Always set appropriate "tbs" parameter for Serper searches based on query urgency:
   - Use "qdr:h" for breaking news or real-time events
   - Use "qdr:d" for recent news, today's events, daily updates
   - Use "qdr:w" for weekly trends, "this week" queries
   - Use "qdr:m" for monthly data, recent developments
   - Use "qdr:y" for annual trends, yearly comparisons

3. Enhance query strings with temporal context:
   - Add "August 2025" for current month
   - Include "recent", "latest", "this week" when asking for current info
   - Use specific year "2025" for current year searches

4. Prioritize queries by user intent and recency requirements.

Focus on the most recent messages and ensure queries are specific and actionable."""

        try:
            # Call Claude with tool use
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
                tools=tools,
                tool_choice={"type": "tool", "name": "generate_search_queries"}
            )
            
            # Extract tool use response
            for content in response.content:
                if content.type == "tool_use" and content.name == "generate_search_queries":
                    queries_data = content.input.get("queries", [])
                    search_queries = []
                    
                    for q in queries_data:
                        search_query = SearchQuery(
                            query=q["query"],
                            api_type=q["api_type"],
                            endpoint=q["endpoint"],
                            parameters=q.get("parameters", {}),
                            priority=q["priority"],
                            description=q["description"]
                        )
                        search_queries.append(search_query)
                    
                    # Sort by priority
                    search_queries.sort(key=lambda x: x.priority)
                    
                    logger.info(f"Generated {len(search_queries)} search queries", 
                              extra={'extra_data': {'query_count': len(search_queries)}})
                    
                    return search_queries
            
            # Fallback if no tool use
            return []
            
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}", 
                        extra={'extra_data': {'error_type': type(e).__name__}})
            raise
    
    async def _execute_serper_search(self, session: aiohttp.ClientSession, query: SearchQuery) -> Dict[str, Any]:
        """Execute a single Serper API search"""
        
        # Map endpoints to Serper URLs
        endpoint_map = {
            "/search": "https://google.serper.dev/search",
            "/news": "https://google.serper.dev/news",
            "/images": "https://google.serper.dev/images",
            "/shopping": "https://google.serper.dev/shopping",
            "/places": "https://google.serper.dev/places",
            "/scholar": "https://google.serper.dev/scholar"
        }
        
        url = endpoint_map.get(query.endpoint, "https://google.serper.dev/search")
        
        # Build request payload
        payload = {
            "q": query.query,
            "gl": query.parameters.get("gl", "us"),
            "hl": query.parameters.get("hl", "en"),
            "num": query.parameters.get("num", 10)
        }
        
        # Add time-based search if specified
        if "tbs" in query.parameters:
            payload["tbs"] = query.parameters["tbs"]
        
        headers = {
            "X-API-KEY": self.config.serper_api_key,
            "Content-Type": "application/json"
        }
        
        try:
            async with session.post(url, json=payload, headers=headers, timeout=self.config.timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "query": query.query,
                        "api": "serper",
                        "endpoint": query.endpoint,
                        "description": query.description,
                        "results": data
                    }
                elif response.status == 429:
                    # Rate limited
                    retry_after = int(response.headers.get("Retry-After", 60))
                    await asyncio.sleep(retry_after)
                    return await self._execute_serper_search(session, query)
                else:
                    error_text = await response.text()
                    logger.error(f"Serper API error: {response.status} - {error_text}")
                    return {
                        "query": query.query,
                        "api": "serper",
                        "error": f"HTTP {response.status}: {error_text}"
                    }
                    
        except asyncio.TimeoutError:
            return {
                "query": query.query,
                "api": "serper",
                "error": "Request timeout"
            }
        except Exception as e:
            logger.error(f"Serper search error: {str(e)}")
            return {
                "query": query.query,
                "api": "serper",
                "error": str(e)
            }
    
    async def _execute_coingecko_search(self, session: aiohttp.ClientSession, query: SearchQuery) -> Dict[str, Any]:
        """Execute a single CoinGecko API search"""
        
        base_url = "https://pro-api.coingecko.com/api/v3"
        
        # Handle different endpoints
        if query.endpoint == "/simple/price":
            url = f"{base_url}/simple/price"
            params = {
                "ids": query.parameters.get("ids", query.query.lower().replace(" ", "-")),
                "vs_currencies": query.parameters.get("vs_currencies", "usd"),
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
                "include_last_updated_at": "true"
            }
        elif query.endpoint == "/coins/markets":
            url = f"{base_url}/coins/markets"
            params = {
                "vs_currency": query.parameters.get("vs_currency", "usd"),
                "order": query.parameters.get("order", "market_cap_desc"),
                "per_page": query.parameters.get("per_page", 20),
                "page": query.parameters.get("page", 1),
                "sparkline": "false"
            }
        elif "/market_chart" in query.endpoint:
            coin_id = query.parameters.get("coin_id", query.query.lower().replace(" ", "-"))
            url = f"{base_url}/coins/{coin_id}/market_chart"
            params = {
                "vs_currency": query.parameters.get("vs_currency", "usd"),
                "days": query.parameters.get("days", 7)
            }
        else:
            # Default to simple price
            url = f"{base_url}/simple/price"
            params = {"ids": query.query.lower().replace(" ", "-"), "vs_currencies": "usd"}
        
        headers = {
            "x-cg-pro-api-key": self.config.coingecko_api_key,
            "Content-Type": "application/json"
        }
        
        try:
            async with session.get(url, params=params, headers=headers, timeout=self.config.timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "query": query.query,
                        "api": "coingecko",
                        "endpoint": query.endpoint,
                        "description": query.description,
                        "results": data
                    }
                elif response.status == 429:
                    # Rate limited
                    await asyncio.sleep(60)  # CoinGecko typically requires 1 minute wait
                    return await self._execute_coingecko_search(session, query)
                else:
                    error_text = await response.text()
                    logger.error(f"CoinGecko API error: {response.status} - {error_text}")
                    return {
                        "query": query.query,
                        "api": "coingecko",
                        "error": f"HTTP {response.status}: {error_text}"
                    }
                    
        except asyncio.TimeoutError:
            return {
                "query": query.query,
                "api": "coingecko",
                "error": "Request timeout"
            }
        except Exception as e:
            logger.error(f"CoinGecko search error: {str(e)}")
            return {
                "query": query.query,
                "api": "coingecko",
                "error": str(e)
            }
    
    async def _execute_searches_parallel(self, search_queries: List[SearchQuery]) -> List[Dict[str, Any]]:
        """Execute all search queries in parallel"""
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for query in search_queries:
                async with self.semaphore:  # Limit concurrent requests
                    if query.api_type == "serper":
                        #task = self._execute_serper_search(session, query)
                        continue
                    elif query.api_type == "coingecko":
                        task = self._execute_coingecko_search(session, query)
                    else:
                        continue
                    
                    tasks.append(task)
            
            # Execute all tasks in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Search task {i} failed: {str(result)}")
                    processed_results.append({
                        "query": search_queries[i].query if i < len(search_queries) else "unknown",
                        "error": str(result)
                    })
                else:
                    processed_results.append(result)
            
            return processed_results
    
    def _format_results(self, search_results: List[Dict[str, Any]]) -> str:
        """Format search results into a clean string output"""
        
        formatted_output = []
        formatted_output.append(f"Search Results - Generated at {self.current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")
        formatted_output.append("=" * 80 + "\n")
        
        for i, result in enumerate(search_results, 1):
            formatted_output.append(f"\n### Search {i}: {result.get('query', 'Unknown Query')}")
            formatted_output.append(f"API: {result.get('api', 'Unknown')} | Purpose: {result.get('description', 'N/A')}\n")
            
            if "error" in result:
                formatted_output.append(f"❌ Error: {result['error']}\n")
                continue
            
            if result.get('api') == 'serper':
                # Format Serper results
                serper_data = result.get('results', {})
                
                # Answer box (most important)
                answer_box = serper_data.get('answerBox', {})
                if answer_box:
                    formatted_output.append("💡 Quick Answer:")
                    formatted_output.append(f"  {answer_box.get('answer', answer_box.get('snippet', 'No answer'))}")
                    if answer_box.get('source'):
                        formatted_output.append(f"  Source: {answer_box.get('source')}")
                    formatted_output.append("")
                
                # Knowledge graph
                kg = serper_data.get('knowledgeGraph', {})
                if kg:
                    formatted_output.append("📊 Knowledge Graph:")
                    formatted_output.append(f"  Title: {kg.get('title', 'No title')}")
                    if kg.get('type'):
                        formatted_output.append(f"  Type: {kg.get('type')}")
                    formatted_output.append(f"  Description: {kg.get('description', 'No description')[:300]}...")
                    if kg.get('attributes'):
                        formatted_output.append("  Key Info:")
                        for attr in list(kg.get('attributes', {}).items())[:3]:
                            formatted_output.append(f"    • {attr[0]}: {attr[1]}")
                    formatted_output.append("")
                
                # News results (prioritize recent news)
                news = serper_data.get('news', [])
                if news:
                    formatted_output.append("📰 Latest News:")
                    for i, item in enumerate(news[:5], 1):
                        title = item.get('title', 'No title')
                        date = item.get('date', 'No date')
                        source = item.get('source', 'Unknown')
                        snippet = item.get('snippet', '')
                        
                        formatted_output.append(f"  {i}. {title}")
                        formatted_output.append(f"     📅 {date} | 🏢 {source}")
                        if snippet:
                            formatted_output.append(f"     📝 {snippet[:200]}...")
                        formatted_output.append(f"     🔗 {item.get('link', 'No link')}")
                        formatted_output.append("")
                
                # Organic results
                organic = serper_data.get('organic', [])
                if organic:
                    formatted_output.append("📄 Web Results:")
                    for j, item in enumerate(organic[:6], 1):  # Show top 6 results
                        title = item.get('title', 'No title')
                        link = item.get('link', 'No link')
                        snippet = item.get('snippet', 'No description')
                        date = item.get('date', '')
                        
                        formatted_output.append(f"  {j}. {title}")
                        if date:
                            formatted_output.append(f"     📅 {date}")
                        formatted_output.append(f"     📝 {snippet[:250]}...")
                        formatted_output.append(f"     🔗 {link}")
                        formatted_output.append("")
                
                # Related searches for additional context
                related = serper_data.get('relatedSearches', [])
                if related:
                    formatted_output.append("🔍 Related Searches:")
                    for rel in related[:4]:  # Show top 4 related searches
                        formatted_output.append(f"  • {rel.get('query', '')}")
                    formatted_output.append("")
                
                # People also ask
                people_also_ask = serper_data.get('peopleAlsoAsk', [])
                if people_also_ask:
                    formatted_output.append("❓ People Also Ask:")
                    for paa in people_also_ask[:3]:
                        question = paa.get('question', '')
                        answer = paa.get('snippet', '')
                        formatted_output.append(f"  Q: {question}")
                        if answer:
                            formatted_output.append(f"  A: {answer[:150]}...")
                        formatted_output.append("")
                
                # Videos if present
                videos = serper_data.get('videos', [])
                if videos:
                    formatted_output.append("🎥 Videos:")
                    for video in videos[:3]:
                        formatted_output.append(f"  • {video.get('title', 'No title')}")
                        formatted_output.append(f"    Channel: {video.get('channel', 'Unknown')}")
                        if video.get('duration'):
                            formatted_output.append(f"    Duration: {video.get('duration')}")
                        formatted_output.append(f"    🔗 {video.get('link', 'No link')}")
                        formatted_output.append("")
            
            elif result.get('api') == 'coingecko':
                # Format CoinGecko results
                cg_data = result.get('results', {})
                
                if isinstance(cg_data, dict) and not cg_data.get('error'):
                    # Simple price data
                    for coin, data in cg_data.items():
                        if isinstance(data, dict) and 'usd' in data:
                            formatted_output.append(f"💰 {coin.upper()} Price Data:")
                            formatted_output.append(f"  • Current Price: ${data.get('usd', 'N/A'):,.2f}")
                            formatted_output.append(f"  • Market Cap: ${data.get('usd_market_cap', 0):,.0f}")
                            formatted_output.append(f"  • 24h Volume: ${data.get('usd_24h_vol', 0):,.0f}")
                            formatted_output.append(f"  • 24h Change: {data.get('usd_24h_change', 0):.2f}%")
                            
                            if 'last_updated_at' in data:
                                update_time = datetime.fromtimestamp(data['last_updated_at'])
                                formatted_output.append(f"  • Last Updated: {update_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                elif isinstance(cg_data, list):
                    # Market data
                    formatted_output.append("📈 Market Overview:")
                    for coin in cg_data[:5]:  # Top 5 coins
                        formatted_output.append(f"  • {coin.get('name', 'Unknown')} ({coin.get('symbol', '').upper()})")
                        formatted_output.append(f"    Price: ${coin.get('current_price', 0):,.2f}")
                        formatted_output.append(f"    24h Change: {coin.get('price_change_percentage_24h', 0):.2f}%")
                        formatted_output.append(f"    Market Cap Rank: #{coin.get('market_cap_rank', 'N/A')}\n")
        
        formatted_output.append("=" * 80)
        formatted_output.append("\nSearch completed successfully.")
        
        return "\n".join(formatted_output)
    
    async def search(self, chat_history: List[Dict[str, str]]) -> str:
        """
        Main entry point for intelligent search.
        
        Args:
            chat_history: List of message dictionaries with 'role' and 'content' keys
            
        Returns:
            Formatted string with all search results
        """
        
        start_time = time.time()
        
        try:
            # Step 1: Analyze chat with Claude to generate search queries
            logger.info("Analyzing chat history with Claude Sonnet 4...")
            search_queries = self._analyze_chat_with_claude(chat_history)
            
            if not search_queries:
                return "No search queries generated. Please provide more context in the conversation."
            
            # Log generated queries
            logger.info(f"Generated queries: {json.dumps([q.query for q in search_queries])}")
            
            # Step 2: Execute searches in parallel
            logger.info(f"Executing {len(search_queries)} searches in parallel...")
            search_results = await self._execute_searches_parallel(search_queries)
            
            # Step 3: Format results
            formatted_results = self._format_results(search_results)
            
            # Log completion
            elapsed_time = time.time() - start_time
            logger.info(f"Search completed in {elapsed_time:.2f} seconds", 
                      extra={'extra_data': {'elapsed_time': elapsed_time, 'query_count': len(search_queries)}})
            
            return search_results, formatted_results
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}", 
                        extra={'extra_data': {'error_type': type(e).__name__, 'error_details': str(e)}})
            return f"Search failed due to an error: {str(e)}"


# Thread-safe singleton instance
_search_tool_instance = None
_instance_lock = asyncio.Lock()


async def get_search_tool() -> IntelligentSearchTool:
    """Get or create the singleton search tool instance"""
    global _search_tool_instance
    
    if _search_tool_instance is None:
        async with _instance_lock:
            if _search_tool_instance is None:
                _search_tool_instance = IntelligentSearchTool()
    
    return _search_tool_instance


async def intelligent_search(chat_history: List[Dict[str, str]]) -> str:
    """
    Main function to be imported and called by other modules.
    
    Args:
        chat_history: List of message dictionaries with 'role' and 'content' keys
        Example: [
            {"role": "user", "content": "What's the current price of Bitcoin?"},
            {"role": "assistant", "content": "I'll help you find Bitcoin's current price."},
            {"role": "user", "content": "Also, what are the latest AI developments this week?"}
        ]
    
    Returns:
        Formatted string containing all search results
    """
    
    # Validate input
    if not chat_history or not isinstance(chat_history, list):
        return "Error: chat_history must be a non-empty list of message dictionaries"
    
    # Get search tool instance
    search_tool = await get_search_tool()
    
    # Execute search
    return await search_tool.search(chat_history)


# Example usage when running directly
if __name__ == "__main__":
    # Example chat history with time-sensitive queries
    example_chat = [
        {"role": "user", "content": "What's the current price of Bitcoin and Ethereum?"},
        {"role": "assistant", "content": "I'll help you find the current cryptocurrency prices."},
        {"role": "user", "content": "Also, what are the latest AI developments and news this week in August 2025?"}
    ]
    
    # Run the search
    async def main():
        result = await intelligent_search(example_chat)
        print(result)
    
    # Execute
    asyncio.run(main())