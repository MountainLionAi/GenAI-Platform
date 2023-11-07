# GenAI-Platform

## Introduction to GenAI-Platform

GenAI-Platform is a multi-API platform, offering a range of functionalities including chatbot interactions, user management, and payment processing. It leverages Sanic as the primary framework, providing a comprehensive set of APIs for developers.

## Project Description

`GenAI-Platform` is an application based on the Retrieval Augmented Generation (RAG) framework. RAG combines large language models (LLM) with external knowledge sources to enhance the capabilities of question-answering systems.

![RAG Architecture Diagram](genaipf/static/RAG.jpg)

### Why Choose RAG?

#### Challenges with Knowledge Update in LLMs

- The training datasets of LLMs are static, making it challenging to update their knowledge base post-training.
- The sheer size of LLM parameters makes fine-tuning a resource-intensive and time-consuming process.
- Directly querying or editing the knowledge encoded within the billions of parameters in LLM is impractical.

As a solution, RAG was introduced to enable continuous learning and knowledge acquisition for LLMs.

#### How RAG Works

1. **Knowledge Indexing**: Text data is processed, vectorized using techniques like word embedding, and stored in a database to form a searchable vector index.
2. **Knowledge Retrieval**: Upon receiving a query, RAG searches the knowledge base to find the most relevant documents.
3. **Answer Generation**: RAG feeds the query and retrieved documents to the LLM, allowing it to integrate this external knowledge and generate responses.

This allows LLMs to utilize an external knowledge base without altering their parameters. With the knowledge base being updated, new knowledge can be injected into LLMs in real-time.

#### Advantages of RAG

- Enhances LLM reasoning and factual capabilities with a vast external knowledge base.
- Facilitates rapid prototyping.
- Knowledge indexing allows for real-time knowledge updates.
- The generated responses are highly interpretable.

#### Disadvantages of RAG

- Possible retrieval of irrelevant documents during the knowledge retrieval phase.
- Generated responses may lack some fundamental world knowledge.
- The vector database faces challenges in handling vast amounts of data.
- Preprocessing and vectorization in inference add computational overhead.
- Updating the external knowledge base requires significant resources.

### Summary

In the `GenAI-Platform` project, we use the RAG framework to build a powerful, real-time updated, and highly interpretable question-answering system. While there are technical challenges, the advantages make the project capable of providing smarter and more efficient services.

## Key Features and Highlights of the Project

### Features:

1. **Intelligent Chatbot**: Based on OpenAI's GPT model and combined with a qdrant-client vector database for preprocessing, it provides real-time, accurate intelligent responses.
2. **User Management**: Offers complete functionalities for user registration, login, logout, and supports captcha and email verification.
3. **Message Management**: Allows users to retrieve, share, delete messages and message groups, supporting streaming processing.
4. **Payment System**: Integrates payment functionalities, enabling users to check payment card information, order inspection, and account queries.
5. **Multilingual Model Linking**: Utilizes the langchain tool to link different language models and integrate them into the project's features.

### Highlights:

1. **Performance**: Powered by the Sanic web framework, it supports asynchronous request handling for rapid response.
2. **Security**: Incorporates various security measures, such as password hashing, captcha validation, and token authentication.
3. **Scalability**: Designed with modularity in mind, allowing for the easy addition of new features and modules.
4. **Cross-Platform Compatibility**: Developed in Python, supporting various operating systems and platforms.
5. **Data Handling**: Equipped with strong data processing capabilities, using tools like pandas and numpy for data cleaning, analysis, and operations.
6. **Blockchain Integration**: Facilitates interactions with the Ethereum blockchain via the web3 library, opening avenues for future blockchain applications.

## Installation and Execution

1. **Project Installation**:

```bash
cd GenAI-Platform
pip install -e .
```

2. **Load Vector Database Content:**:

```bash
cd GenAI-Platform
python app.py -a .
```

3. **Run the Platform:**:

```bash
cd GenAI-Platform
python app.py .
```

## API Interface Introduction

| Category     | API Route               | Method | Function Description                          |
| ------------ | ----------------------- | ------ | --------------------------------------------- |
| **Chatbot**  | `/mpcbot/sendchat_gpt4` | POST   | Interaction with the GPT-4 version of chatbot |
| **GPT**      | `api/getMessageList`    | GET    | Retrieve message list                         |
|              | `api/getMsgGroupList`   | GET    | Retrieve message group list                   |
|              | `api/delMsgGroupList`   | POST   | Delete message group                          |
|              | `api/sendStremChat`     | POST   | Send streaming chat content                   |
| **UserRate** | `api/userRate`          | POST   | User rating                                   |
|              | `api/delMessages`       | POST   | Delete messages by code                       |
|              | `api/shareMessages`     | POST   | Share messages                                |
|              | `api/getShareMessages`  | POST   | Retrieve shared messages                      |
| **User**     | `api/userLogin`         | POST   | User login                                    |
|              | `api/checkLogin`        | GET    | Check login status                            |
|              | `api/register`          | POST   | User registration                             |
|              | `api/loginOut`          | GET    | User logout                                   |
|              | `api/sendVerifyCode`    | POST   | Send verification code                        |
|              | `api/sendEmailCode`     | POST   | Send email verification code                  |
|              | `api/getCaptcha`        | GET    | Get captcha image                             |
|              | `api/testVerifyCode`    | POST   | Verify verification code                      |
|              | `api/modifyPassword`    | POST   | Modify password                               |
| **Pay**      | `api/pay/cardInfo`      | GET    | Query payment card information                |
|              | `api/pay/orderCheck`    | GET    | Check order                                   |
|              | `api/pay/account`       | GET    | Query user account                            |
|              | `api/pay/callback`      | POST   | Payment success callback                      |

## Project Directory Structure

Below is the main directory structure of `GenAI-Platform` in `genaipf` and their function descriptions:

- **conf**: Contains various configuration files of the project, like server port, database connections, etc.
- **constant**: Stores constant definitions used in the project, such as error codes, message constants, etc.
- **controller**: Responsible for handling API requests, interactions with the front end, and returning responses. API interface definitions like `sendchat_gpt4` and `userLogin` are defined here.
- **dispatcher**: In charge of API dispatching logic, like routing specific requests to the appropriate controller or handler.
- **exception**: This directory contains custom exception handling logic and definitions of custom exception classes.
- **interfaces**: Defines interfaces for interactions with external systems or other project modules.
- **middlewares**: Middleware for processing API requests and responses. They can perform tasks like authentication, logging, etc., as pre-processing and post-processing.
- **routers**: Defines all API routes, ensuring each request is correctly directed to the appropriate controller.
- **services**: Contains the core business logic of the project and the code for interacting with the database.
- **static**: For storing static resources of the project like CSS, JavaScript files, and images.
- **utils**: Provides various utilities and helper functions, such as date conversion, string manipulation, etc.

## Technology Stack Introduction

Below is the main technology stack of `GenAI-Platform` and its role in the project:

- **sanic (23.3.0)**: An efficient, lightweight Web server framework that supports asynchronous request processing, providing the main Web services for the project.
- **qdrant-client (1.4.0)**: A vector database client for efficiently storing and retrieving vector data.
- **openai (0.27.4)**: OpenAI's Python client for calling models like GPT for intelligent language response capabilities.
- **langchain (0.0.314)**: A tool linking language models to project functionalities, supporting the language processing part of the project.
- **pymysql (1.1.0)**: A Python client for MySQL databases for data storage and retrieval.
- **redis (3.5.3)**: A high-performance key-value store for caching, session management, etc.
- **web3 (6.2.0)**: A Python client for the Ethereum blockchain, for implementing interactions with the blockchain.
- **aiohttp (3.8.4)**: An asynchronous HTTP client/server framework for handling asynchronous network requests.
- **APScheduler (3.10.1)**: A job scheduling library for periodically running certain snippets of code or scheduled tasks.

The rest of the libraries and tools provide various auxiliary functions and enhance performance, ensuring the project runs efficiently and stably.

## License Information

This project uses the `Apache 2.0` license, which means you are free to use, modify, and distribute the code, but you must give proper attribution to the original code.

## Contact Information and Community

We value the community's feedback and suggestions.

- **GitHub Community**: If you have any questions, suggestions, or issues, feel free to ask or leave a message in the GitHub community.
- **Email**: For further support or special requests, you can directly email: [contact@mountainlion.ai](mailto:contact@mountainlion.ai)

We will respond promptly and provide assistance.
