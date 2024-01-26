from typing import List, Optional, Dict
from dataclasses import dataclass, field
from genaipf.utils.time_utils import get_format_time_YYYY_mm_dd
import requests
import re


@dataclass
class Result:
    """A class representing a search result.

    Attributes:
        title (str): The title of the search result.
        url (str): The URL of the search result.
        id (str): The temporary ID for the document.
        score (float, optional): A number from 0 to 1 representing similarity between the query/url and the result.
        published_date (str, optional): An estimate of the creation date, from parsing HTML content.
        author (str, optional): If available, the author of the content.
    """
    title: str
    url: str
    id: str
    score: Optional[float] = None
    published_date: Optional[str] = None
    author: Optional[str] = None
    extract: Optional[str] = None

    def __init__(self, title: str, url: str, id: str, score: Optional[float] = None,
                 published_date: Optional[str] = None, author: Optional[str] = None, extract: Optional[str] = None, **kwargs):
        self.title = title
        self.url = url
        self.score = score
        self.id = id
        self.published_date = published_date
        self.author = author
        self.extract = extract

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"URL: {self.url}\n"
                f"ID: {self.id}\n"
                f"Score: {self.score}\n"
                f"Published Date: {self.published_date}\n"
                f"Author: {self.author}\n"
                f"Extract: {self.extract}")


@dataclass
class DocumentContent:
    """A class representing the content of a document.

    Attributes:
        id (str): The ID of the document.
        url (str): The URL of the document.
        title (str): The title of the document.
        extract (str): The first 1000 tokens of content in the document.
        author (str, optional): If available, the author of the content.
    """
    id: str
    url: str
    title: str
    extract: str
    author: Optional[str] = None

    def __init__(self, id: str, url: str, title: str, extract: str, author: Optional[str] = None, **kwargs):
        self.id = id
        self.url = url
        self.title = title
        self.extract = extract
        self.author = author

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"URL: {self.url}\n"
                f"Title: {self.title}\n"
                f"Extract: {self.extract}"
                f"Author: {self.author}")


@dataclass
class GetContentsResponse:
    """A class representing the response for getting contents of documents.

    Attributes:
        contents (List[DocumentContent]): A list of document contents.
    """
    contents: List[DocumentContent]

    def __str__(self):
        return "\n\n".join(str(content) for content in self.contents)


@dataclass
class SearchResponse:
    """A class representing the response for a search operation.

    Attributes:
        results (List[Result]): A list of search results.
    """
    contents: List[Result]
    autoprompt_string: Optional[str] = None
    api: Optional['Bing'] = field(default=None, init=False)

    def get_contents(self):
        return self.contents

    def __str__(self):
        output = "\n\n".join(str(content) for content in self.contents)
        if self.autoprompt_string:
            output += f"\n\nAutoprompt String: {self.autoprompt_string}"
        return output


class Bing:
    """A client for interacting with Bing Search API.

        Attributes:
            base_url (str): The base URL for the Bing Search API.
            headers (dict): The headers to include in API requests.
        """

    def __init__(self, subscription_key: str, base_url: str = "https://api.bing.microsoft.com/v7.0"):
        """Initialize the Bing client with the provided API key and optional base URL and user agent.

        Args:
            subscription_key (str): The API key for authenticating with the Bing API.
            base_url (str, optional): The base URL for the Bing API. Defaults to "https://api.bing.microsoft.com/v7.0".
        """
        self.headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        self.base_url = base_url

    def search(self, query: str, text_format: Optional[str] = "HTML", freshness: Optional[str] = None,
               offset: Optional[int] = 0, count: Optional[int] = 5):
        params = {
            "q": query,
            "textDecorations": False,
            "textFormat": text_format,
            "offset": offset,
            "count": count
        }
        if freshness is not None and freshness != "":
            params['freshness'] = freshness
        # else:
        #     pattern = re.compile(r'最新|最近|当前|现在|即时|此刻|即刻|目前')
        #     if pattern.search(query):
        #         params['freshness'] = get_format_time_YYYY_mm_dd()
        response = requests.get(f"{self.base_url}/search", headers=self.headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        results = []
        if search_results.get('webPages') is not None and search_results.get('webPages').get('value') is not None:
            results = [Result(page.get('name'), page.get('url'), page.get('id'), 0,
                              page.get('datePublished')[:10] if page.get('datePublished') and len(
                                  page.get('datePublished')) > 10 else "", None, page.get('snippet')) for page in
                       search_results.get('webPages').get('value')]
        search_response = SearchResponse(contents=results)
        return search_response
