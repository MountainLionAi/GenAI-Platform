# GenAI Platform: RAG-Based Intelligent Chatbot Backend Suite

<div align="center">
  <img src="genaipf/static/GenAI%20Platform.jpg" alt="GenAI Platform Image" />
</div>

<div align="center">
  <p>
    <a href="https://github.com/MountainLionAi/GenAI-Platform">
        <img alt="stars" src="https://img.shields.io/github/stars/MountainLionAi/GenAI-Platform?style=social" />
    </a>
    <a href="https://github.com/MountainLionAi/GenAI-Platform">
        <img alt="forks" src="https://img.shields.io/github/forks/MountainLionAi/GenAI-Platform?style=social" />
    </a>
    <a href="https://opensource.org/licenses/Apache-2.0">
      <img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" />
    </a>
    <a href="https://github.com/MountainLionAi/GenAI-Platform/releases">
      <img alt="Release Notes" src="https://img.shields.io/github/release/MountainLionAi/GenAI-Platform.svg" />
    </a>
    <a href="https://github.com/MountainLionAi/GenAI-Platform/issues">
      <img alt="Open Issues" src="https://img.shields.io/github/issues-raw/MountainLionAi/GenAI-Platform" />
    </a>
  </p>
  <p>
    <a href="https://codespaces.new/MountainLionAi/GenAI-Platform">
      <img alt="Open in GitHub Codespaces" src="https://github.com/codespaces/badge.svg" />
    </a>
  </p>
  <p>
    <a href="https://www.mlion.ai/#/">mlion.ai</a> has built on this platform technology
  </p>

[**简体中文**](README_zh.md)
</div>

## Latest Mlion.ai Update: Enhanced AI One-Click Trading

Mlion.ai has recently launched a major update to its "AI One-Click Trading" feature in the AI trading section, significantly improving user experience and trading convenience. This update introduces the following new features:

- **AI Automated Trading with Multiple Order Types**: Support for market orders, limit orders, and cross-chain limit orders through natural language commands
- **Multi-Scenario Trading Support**: Provides wallet operations, multi-round dialogues, insufficient balance notifications, exchange range limitations, and unsupported currency exchange scenarios
- **Natural Language Trading Examples**: Users can directly trade using natural language such as "buy $15 worth of BNB" or "sell 0.03 BNB when BNB rises to $800"
- **Extensive Currency Support**: Supports BTC, ETH (ERC20, BSC, Polygon), BNB (BSC), POL (Polygon), USDT (ERC20, BSC, Polygon), and more
- **Agent Workflow Visualization**: The entire coin recommendation process is clearly displayed to users, providing transparent insight into the Agent's underlying selection logic

For more details and demonstration videos, visit: [https://x.com/MLion_AI](https://x.com/MLion_AI)

## Contents
- [Introduction to GenAI Platform](#introduction-to-genai-platform)
- [Core Features](#core-features)
- [Why Choose RAG?](#why-choose-rag)
- [GenAI Platform RAG](#genai-platform-rag)
- [Multi Agent](#multi-agent)
- [Subsystems in the Project](#subsystems-in-the-project)
- [Project Installation and Running](#project-installation-and-running)
- [API Interface Introduction](#api-interface-introduction)
- [Project Directory Structure](#project-directory-structure)
- [Technology Stack Introduction](#technology-stack-introduction)
- [Project Application Scenarios](#project-application-scenarios)
- [Applications Developed Using GenAI Platform](#applications-developed-using-genai-platform)
- [License Information](#license-information)
- [Developer Advantages](#developer-advantages)
- [Contact and Community](#contact-and-community)

## Introduction to GenAI-Platform

`GenAI Platform` is an open-source project designed to offer a comprehensive backend solution based on the Retrieval-Augmented Generation (RAG) architecture, enabling developers to build and deploy intelligent chatbots for specific vertical domains. This platform integrates the latest large language model technologies, allowing developers to seamlessly merge various sources of information. With a carefully designed scheduling system, efficient query transformation, and routing mechanisms, it provides accurate and relevant responses to users. Furthermore, `GenAI Platform` supports multi-agent cooperation using Microsoft's open-source AutoGen framework, enhancing the system's ability to handle complex queries and tasks.

## Core Features

- **Integration of Diverse Information Sources**: `GenAI Platform` supports cloud-based internet searches, database storage, and vector storage, enabling chatbots to access and process data from multiple information sources.

- **Intelligent Scheduler**: The platform's innovatively developed scheduler uses embedding models to process user queries, employing function filtering and matching to identify effective information sources and select the most appropriate functions to construct the final prompt for generating answers.

- **Efficient Query Processing**: Through query transformation and routing, `GenAI Platform` can convert user queries into a list of queries, then choose the most suitable tool to provide answers.

- **Flexible Agent Selection**: The platform's built-in agent selection mechanism supports various query processing agents, such as LlamaIndex and Langchain, offering more processing options for user queries. The integration of the AutoGen framework further facilitates cooperation among multiple agents, ensuring comprehensive and precise responses.

- **Support for Multi-Model Integration and Switching**: `GenAI Platform` allows linking multiple large language models (LLMs) and provides easy switching between them, enhancing the flexibility and adaptability of the system.

- **One-Stop Backend Services**: `GenAI Platform` provides comprehensive backend support, including user management, payment systems, message management, and system log management.

- **Good Scalability**: Based on a modular design, it is easy for developers to add new features and modules.

- **Support for Web Asynchronous Response**: Using the sanic web framework, it supports asynchronous request processing, ensuring quick responses.

`GenAI-Platform` is an application based on the RAG (Retrieval Augmented Generation) framework. RAG supports generating answers by retrieving data from sources beyond LLMs. RAG = search + LLM prompts, where LLMs use search algorithms to obtain contextual information from external data sources based on user queries. Finally, the query and retrieved context are combined and fed into LLM prompts, providing highly accurate and contextually relevant responses.

## Why Choose RAG?

### The Knowledge Update Challenge of LLMs

- The training dataset of an LLM is fixed, making it difficult to update its knowledge through further training once training is completed.
- LLMs have a vast number of parameters, and fine-tuning at any time requires significant resources and is time-consuming.
- It is impossible to directly query or edit the knowledge encoded in the billions of parameters of an LLM.
  
Therefore, to enable LLMs to continuously learn and acquire new knowledge, RAG was developed.

### How RAG Works

1. **Knowledge Indexing**: Text data is processed, vectorized through techniques such as word embedding, and stored in a database to create a searchable vector index.
2. **Knowledge Retrieval**: When a question is inputted, RAG searches the knowledge base to find documents most relevant to the question.
3. **Generating Answers**: RAG provides the question and retrieved documents to the LLM, allowing the LLM to integrate this external knowledge and generate answers.

This enables LLMs to utilize external knowledge bases without altering their parameters. When the knowledge base is updated, new knowledge can also be injected into the LLM in real-time.

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## GenAI-Platform RAG

<div align="center">
  <img src="genaipf/static/ChatBot%20Workflow.png" alt="Chatbot Workflow Image" />
</div>

In the `GenAI Platform RAG` system, the entire query processing workflow is accomplished through a series of carefully designed components. Here is an overview of the system:

The user's query and chat history first enter the Embedding Model module, which processes and encodes the input. The processed data then enters the Dispatcher module. The dispatcher uses the Function Filter to select the appropriate GPT Function, which is executed by calling the OpenAI API. 

In the dispatcher, after the function is selected, the Final Prompt is generated according to the Match Prompt, and then sent to the Agent module. The agent module performs Query Transformation and Query Routing, using tools (such as Llamaindex and Langchain) to transform the query into a suitable information request and determine the best path for the query. 

The Information Source module includes Internet search (such as Bing, Metaphor, Perplexity), DB Storage and Vector Storage. Agents retrieve data from these sources and return relevant information to the scheduler module through Fusion Retrieval. 

Finally, the scheduler sends the processed data and generated prompts to the LLM for generation, and the generated answers are returned to the user to complete the entire query processing process. This process ensures that users get accurate and detailed answers by effectively utilizing multiple sources of information and advanced query processing techniques.

![RAG Architecture Diagram](genaipf/static/RAG.jpg)

In the `GenAI Platform RAG` system, the entire query processing workflow is accomplished through a series of carefully designed components. Here are the main parts of the process and their functions:

### Dispatcher

- **Embedding Model**: Utilizes embedding models to process queries, converting queries and chat histories into vector form for subsequent retrieval and matching.

- **Function Filter**: This component filters possible GPT functions using a vector database, effectively addressing the potential limitation in the number of GPT functions.

- **Function Choice**: At this stage, the system leverages GPT's function call capability, allowing interaction with the language model to determine the context and intent of user queries. GPT functions primarily classify the user’s input into scenarios. For example, a function named "Currency News" might be defined to handle “news about a specific thing, media information about a specific thing, recent updates about a specific thing.” Once the GPT function determines the scenario, it specifies the sources of reference materials needed to answer the question, such as databases, APIs, search engines, etc. If a user’s question cannot be well answered, the scenario is summarized, and a new function is added to address it.

- **Vector Databases**: The dispatcher can specify multiple vector databases tailored to different domains, ensuring that the system can retrieve and match the most relevant information for a wide range of questions.

- **Final Prompt Generation**: Once the function is selected, the dispatcher generates the Final Prompt according to the Match Prompt. This prompt is then sent to the Agent module for further processing.

By incorporating these components, the dispatcher ensures that the system accurately classifies queries, selects the appropriate functions and information sources, and prepares the query for effective processing by the agent module.

![Dispatch Diagram](genaipf/static/Dispatch.jpg)

### Information Source

- **Web Search Tools**: Utilizing cloud technology, the system can perform internet searches to obtain a wide range of real-time information, providing rich data support for generated answers. Tools that may be used in this process include Bing, Metaphor, Google, etc.

- **DB Storage**: Stores structured data, providing necessary historical information and factual data for queries.

- **Vector Storage**: Stores feature vectors used for fast retrieval and comparison of information, accelerating the query processing process.

### Agent

- **Agent Choice**: After determining the function to be executed, the agent selection step comes into play. This step is specifically designed for complex questions that require a deeper understanding and analysis. Agents in LlamaIndex interact with the language model to choose the correct tool for processing the question. The function of this agent is to interact multiple times with different information sources within the system, aggregating and synthesizing information to produce a more precise and in-depth answer.Through multiple interactions between agent selection and tools, the system can analyze questions deeply, combining multiple data points and considering different information sources to optimize the answer. This ensures that even in the face of complex queries, `GenAI Platform` can provide answers that are both deep and high-quality, reflecting not only the accuracy of data but also a profound understanding of the intent behind user queries.

- **Query Transformation**: Transforms the original query into a form suitable for processing, which may include restructuring or expanding the query.

- **Query Routing**: Determines which information source or tool the transformed query should be sent to for processing.

- **Fusion Retrieval**: Combines data from multiple information sources for query processing, enhancing the accuracy and relevance of the answers.

### Search Engine Integration

<div align="center">
  <img src="genaipf/static/RAG%20with%20Search%20Engine.jpg" alt="Search Engine Diagram" />
</div>

- **Query Evaluation**: When a user submits a query, the system evaluates whether the query requires a combined approach of Retrieval Augmented Generation (RAG) and external search capabilities.

- **Asynchronous Task Execution**: If a combined approach is deemed necessary, the query is routed to an asynchronous task module that executes both RAG processes and search engine queries.

- **Search Engine Utilization**: The system leverages search engines (such as Serper, Exa, or Google) to obtain relevant sources, search results, and related queries.

- **Information Integration**: The acquired information is fed back into the system, where it undergoes prompt engineering processing.

- **Final Response Generation**: The Large Language Model (LLM) uses the integrated information to generate the final response to the user.

- **Direct Query Processing**: If the query does not require a combined RAG and search engine approach, it is directed straight to the prompt engineering module, after which the LLM generates a response.

This process allows the system to flexibly select the appropriate processing pipeline based on query requirements, ensuring the delivery of accurate and comprehensive responses. By integrating RAG methodologies with external search capabilities, the system can provide users with more thorough and precise information.

### Final Answer Generation

- **Match Prompt**: Matches an appropriate prompt template based on the results of function selection and information retrieval.

- **Final Prompt**: Combines the matched prompt with retrieved information to generate the final prompt for the language model.

- **Large Language Model (LLM)**: Uses the final prompt to generate the answer to the user's query through a large language model.

### Summary

The complete retrieval-enhanced process of `GenAI-Platform` ensures that the generation of answers is based not only on directly queried data but also on inputs from intelligently selected function processing and agent tools, thereby providing high-quality, personalized, and accurate answers.

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## Multi Agent

We have introduced Microsoft's open-source project AutoGen as the framework for our Multi Agent system, enabling multiple AI agents to collaborate on complex tasks. Here is an overview of AutoGen and its integration into our system:

AutoGen is an open-source programming framework for building AI agents and facilitating cooperation among multiple agents to solve tasks. AutoGen aims to streamline the development and research of agentic AI, much like PyTorch does for Deep Learning. It offers features such as:

- **Agent Cooperation**: AutoGen enables agents to interact with each other to collaboratively solve tasks.
- **Multi-Model Support**: Facilitates the use of various large language models (LLMs) and tool use support.
- **Flexible Workflows**: Supports both autonomous and human-in-the-loop workflows.
- **Conversation Patterns**: Supports multi-agent conversation patterns for complex workflows.
- **Enhanced LLM Inference**: Provides utilities like API unification and caching, and advanced usage patterns such as error handling, multi-config inference, and context programming.

<div align="center">
  <img src="genaipf/static/Multi_Agent.png" alt="Multi_Agent Diagram" />
</div>

AutoGen simplifies the orchestration, automation, and optimization of complex LLM workflows, maximizing the performance of LLM models and overcoming their weaknesses. It supports diverse conversation patterns for complex workflows. With customizable and conversable agents, developers can use AutoGen to build a wide range of conversation patterns concerning conversation autonomy, the number of agents, and agent conversation topology.

Our implementation uses AutoGen to manage and coordinate multiple agents, enhancing the system's ability to handle complex queries and tasks. This allows us to provide more comprehensive and precise responses by leveraging the strengths of different AI agents.

The integration of AutoGen into our system is illustrated in the `examples` folder, specifically in the `multi_agent_t001.py` file. The core functionalities are encapsulated in the `genaipf` folder under the `agent` directory in the `autogen.py` file.

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## Subsystems in the Project
![Subsystems in the Project](genaipf/static/System.jpg)

1. **Intelligent Chatbot**: Based on OpenAI's GPT model, this subsystem is the core of `GenAI Platform`, providing users with an intelligent interactive chat experience. Through the `GenAI Platform RAG` system, it can handle large-scale and complex queries while maintaining quick response times and high accuracy. Additionally, the system now supports integration with Telegram, allowing users to interact with the chatbot through Telegram bots, facilitating project traction and enhancing user engagement.

2. **User Management System**: This subsystem handles all functionalities related to user accounts. It supports basic user registration, login, and logout functions, along with security measures such as captcha and email verification, ensuring users can safely access their accounts and protecting the platform from unauthorized access.

3. **Message Management System**: Allows users to manage their communications efficiently and orderly. Users can retrieve historical messages, share important information, and even delete conversations that are no longer needed. Additionally, the system supports streaming to ensure timely interaction of messages with the frontend.

4. **Payment System**: Integrates payment functionalities, allowing users to inquire about payment card information, order checks, and account queries.

5. **System Log Management System**: This subsystem is responsible for recording and managing system logs, crucial for monitoring system operation, debugging, and security auditing. It tracks user activities, system performance, and any potential anomalies or security events, providing valuable information for system administrators.

6. **Telegram Bot Integration**: This new functionality allows the integration of the intelligent chatbot with Telegram, providing an additional platform for user interaction. By leveraging Telegram bots, users can engage with the chatbot directly through the Telegram app, making it easier for users to access the platform's services and increasing the project's reach.

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## Project Installation and Running

1. **Install the Project**:

```bash
cd GenAI-Platform
pip install -e .
```

2. **Load Vector Database Content**:

```bash
cd GenAI-Platform
python app.py -a
```

3. **Run the Platform**:

```bash
cd GenAI-Platform
python app.py
```
<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## API Interface Introduction (v1 API Version Control)

| Category      | API Route                  | Method | Function Description                  |
|---------------|----------------------------|--------|---------------------------------------|
| **GPT**       | `api/v1/sendChat`          | POST   | Send chat content                     |
|               | `api/v1/getMessageList`    | GET    | Retrieve message list                 |
|               | `api/v1/getMsgGroupList`   | GET    | Retrieve message group list           |
|               | `api/v1/delMsgGroupList`   | POST   | Delete message group                  |
|               | `api/v1/sendStreamChat`    | POST   | Send streaming chat content           |
|               | `api/v1/sendOneshotChat`   | POST   | Send one-shot chat content            |
|               | `api/v1/sendRawChatStream` | POST   | Send raw chat stream                  |
|               | `api/v1/sendStylizedRequest`| POST  | Send stylized chat request            |
| **UserRate**  | `api/v1/userRate`          | POST   | User rating                           |
|               | `api/v1/delMessages`       | POST   | Delete messages by code               |
|               | `api/v1/shareMessages`     | POST   | Share messages                        |
|               | `api/v1/getShareMessages`  | POST   | Retrieve shared messages              |
| **Assistant** | `api/v1/assistantChat`     | POST   | Interaction with the assistant        |
|               | `api/v1/getAssistantHistory`| POST  | Retrieve assistant chat history       |
| **User**      | `api/v1/userLogin`         | POST   | User login                            |
|               | `api/v1/checkLogin`        | GET    | Check login status                    |
|               | `api/v1/register`          | POST   | User registration                     |
|               | `api/v1/loginOut`          | GET    | User logout                           |
|               | `api/v1/sendVerifyCode`    | POST   | Send verification code                |
|               | `api/v1/sendEmailCode`     | POST   | Send email verification code          |
|               | `api/v1/getCaptcha`        | GET    | Retrieve captcha image                |
|               | `api/v1/testVerifyCode`    | POST   | Verify the verification code          |
|               | `api/v1/modifyPassword`    | POST   | Modify password                       |
|               | `api/v1/newsbot`           | GET    | Retrieve news                         |
|               | `api/v1/userLoginOther`    | POST   | User login with other methods         |
|               | `api/v1/addFeedback`       | POST   | Add user feedback                     |
| **Pay**       | `api/v1/pay/cardInfo`      | GET    | Query payment card information        |
|               | `api/v1/pay/orderCheck`    | GET    | Check orders                          |
|               | `api/v1/pay/account`       | GET    | Query user account                    |
|               | `api/v1/pay/callback`      | POST   | Callback for successful payment       |

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## Project Directory Structure

Here is the main directory structure of `GenAI-Platform` in `genaipf` and their function descriptions:

- **agent**: Contains various agent functionalities, including integrations with AutoGen and LlamaIndex, providing the framework for multi-agent cooperation and task handling.

- **bot**: Contains code for connecting the project inputs and outputs to Telegram bots, facilitating interaction with the chatbot through Telegram.

- **conf**: Contains various configuration files of the project, such as server port, database connections, etc.

- **constant**: Stores constant definitions used in the project, such as error codes, message constants, etc.

- **controller**: Responsible for handling API requests, interacting with the frontend, and returning responses. API interface definitions like `sendchat_gpt4` and `userLogin` are defined here.

- **dispatcher**: Handles the logic for API dispatching, routing specific requests to the corresponding controller or handler.

- **exception**: This directory contains custom exception handling logic and the definitions of custom exception classes.

- **interfaces**: Defines interfaces for interaction with external systems or other project modules.

- **middlewares**: Middleware for processing API requests and responses. These middlewares can perform tasks such as authentication, logging, etc., for preprocessing and postprocessing.

- **routers**: Defines all API routes, ensuring each request is correctly directed to the appropriate controller.

- **services**: Contains the core business logic of the project and the code for database interactions.

- **static**: Stores the project's static resources, such as CSS, JavaScript files, and images.

- **tools**: Provides various tools for internet information queries (currently includes Bing, Metaphor, Preplexity).

- **utils**: Offers various utilities and helper functions, such as date conversion, string manipulation, etc.

In addition to the `genaipf` folder, there is also an `examples` directory, which includes example code demonstrating the integration of multiple AI agents using AutoGen and LlamaIndex. This directory provides practical use cases and templates for implementing multi-agent cooperation within the system.

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## Technology Stack Introduction

Here is the main technology stack of `GenAI-Platform` and their roles in the project:

- **sanic (23.3.0)**: An efficient, lightweight web server framework supporting asynchronous request processing, providing the main web services for the project.

- **sanic_session (0.8.0)**: Session management for the Sanic web framework.

- **qdrant-client (1.4.0)**: Vector database client for efficiently storing and retrieving vector data.

- **openai (1.7.1)**: OpenAI's Python client for calling models like the GPT series for language intelligence reply functions.

- **langchain (0.0.314)**: A tool linking language models with project functionality, supporting the language processing part of the project.

- **langchain-anthropic (0.1.4)**: Extension for LangChain to support Anthropics models.

- **llama-index (0.9.30)**: Similarly, a tool linking language models with project functionality, providing powerful Agent-related features for the project.

- **pymysql (1.1.0)**: A Python client for MySQL databases, used for data storage and retrieval.

- **redis (3.5.3)**: A high-performance key-value store system used for caching, session management, etc.

- **web3 (6.2.0)**: Python client for Ethereum blockchain, for implementing interactions with the blockchain.

- **aiohttp (3.8.4)**: Asynchronous HTTP client/server framework for handling asynchronous network requests.

- **APScheduler (3.10.1)**: A task scheduling library, for executing tasks at a scheduled time or periodically running certain code snippets.

- **aiosmtplib (2.0.2)**: Async SMTP client for sending emails.

- **async-cache (1.1.1)**: Asynchronous caching library.

- **aiocache (0.12.2)**: Caching library for async operations.

- **aiomysql (0.2.0)**: Async MySQL client for Python.

- **selenium (4.21.0)**: Browser automation framework for testing web applications.

- **autogen (1.0.16)**: An open-source programming framework for building AI agents and facilitating cooperation among multiple agents to solve tasks. It streamlines the development and research of agentic AI, much like PyTorch does for Deep Learning, and supports multi-agent conversation patterns and enhanced LLM inference.

Other libraries and tools provide various auxiliary functions and enhance performance, ensuring the project's efficient and stable operation.

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## Project Application Scenarios

- **Chatbots for Vertical Domains**: For specific industries or fields such as law, healthcare, or customer support, the platform can provide deeply customized solutions.

- **Knowledge-Intensive Applications**: In scenarios that require handling vast amounts of information and providing knowledgeable answers, `GenAI Platform RAG` architecture offers robust support.

- **Multi-Channel Deployment**: Supports access via various communication channels, such as web, mobile apps, or third-party service platforms, offering flexible access options for users.

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## Applications Developed Using GenAI Platform
### MountainLion: Your Personal GenAI Assistant for the Web3 Industry
  ![moutainlion](genaipf/static/moutainlion.webp)

  `MountainLion` is an intelligent assistant developed on the `GenAI Platform`, focusing on the in-depth exploration of the Web3 industry. Serving as your personal assistant, MountainLion harnesses the advanced AI analytical capabilities to provide extensive information on areas such as blockchain, cryptocurrencies, decentralized finance (DeFi), and non-fungible tokens (NFTs). Whether you are a beginner or an expert in the Web3 field, MountainLion aims to assist you in maintaining a leading edge in industry insights.

  To learn more about MountainLion or to experience the product, please visit this [link](https://www.mlion.ai/#/).

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## Developer Advantages

- **Open Source Collaboration**: As an open-source project, `GenAI Platform` encourages collaboration and contributions from the developer community, driving the platform's development and innovation.

- **Customization and Scalability**: The platform's modular design allows developers to easily add or modify functionalities as needed.

- **Documentation and Support**: Provides comprehensive documentation and community support to help developers quickly get started and resolve issues during development.

### Contributors Wall
<a href="https://github.com/MountainLionAi/GenAI-Platform/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MountainLionAi/GenAI-Platform&max=200" />
</a>

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## License Information

This project is licensed under the `Apache 2.0` license, which means you can freely use, modify, and distribute the code, but you must give appropriate attribution to the original source.

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>

## Contact and Community

We highly value feedback and suggestions from our community.

- **GitHub Community**: If you have any questions, suggestions, or issues, you are welcome to ask or leave a message in the GitHub community.
- **Email**: If you need further support or have specific requirements, you can directly email: [contact@mountainlion.ai](mailto:contact@mountainlion.ai)

We will respond promptly and provide assistance.

<div align="right">
    <a href="#contents">↑ Back to Contents ↑</a>
</div>
