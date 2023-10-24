# GenAI-Platform

## GenAI-Platform简介

GenAI-Platform 是一个提供多种API功能的平台，包括但不限于chatbot交互、用户管理和支付处理。该平台使用Sanic为主框架，并提供了一套完整的API接口供开发者调用。

## 项目介绍

`GenAI-Platform` 是一个基于 RAG（Retrieval Augmented Generation, 检索增强生成）框架的应用程序。RAG 是一个结合了大规模语言模型(LLM)与外部知识源的工程框架，目的是为了提升问答系统的能力。

![RAG架构示意图](genaipf/static/RAG.jpg)

### 为什么选择 RAG?

#### LLM的知识更新难题

- LLM 的训练数据集是固定的，因此一旦训练完成，很难再通过继续训练来更新其知识。
- LLM 参数量庞大，任何时候进行 fine-tuning 都需要消耗大量的资源且耗时。
- 无法直接查询或编辑 LLM 中编码的数百亿参数中的知识。
  
因此,为了让 LLM 拥有持续学习和获取新知识的能力, RAG 应运而生。

#### RAG 的工作原理

1. **知识索引**: 对文本数据进行处理,通过词嵌入等技术进行向量化，并存入数据库中，形成可检索的向量索引。
2. **知识检索**: 当有一个输入问题时, RAG 会检索知识库以找到与问题最相关的文档。
3. **生成答案**: RAG 会提供问题和检索到的文档给 LLM，允许 LLM 融合这些外部知识，并生成答案。

这使得 LLM 能够利用外部知识库，无需修改其参数。当知识库更新时，新知识也可以实时注入到 LLM 中。

#### RAG 的优点

- 利用大规模外部知识增强 LLM 的推理和事实性。
- 快速实现原型。
- 知识索引阶段能做到知识的实时更新。
- 生成的答案具有强大的可解释性。

#### RAG 的缺点

- 知识检索阶段有可能检索到与问题不太相关的文档。
- 在生成答案时，可能缺乏一些基本的世界知识。
- 向量数据库在处理大量数据时面临挑战。
- 推理时的预处理和向量化增加了计算成本。
- 更新外部知识库需要大量资源。

### 总结

在这个 `GenAI-Platform` 项目中，我们使用 RAG 架构来构建一个强大、实时更新且具有高度可解释性的问答系统，虽然它也带有一些技术上的挑战，但其优势使得该项目能够提供更为智能和高效的服务。


## 项目主要功能与特点

### 功能：

1.**智能聊天机器人**: 基于OpenAI的GPT模型，结合qdrant-client向量数据库预处理为用户提供实时、准确的智能回复。

2.**用户管理**: 提供完整的用户注册、登录、注销功能，并支持验证码和邮箱验证。

3.**消息管理**: 用户可以获取、分享、删除消息和消息组，支持流式处理。

4.**支付系统**: 集成支付功能，用户可以查询支付卡信息、订单检查和账户查询。

5.**多语言模型链接**: 通过langchain工具，链接不同的语言模型并将其集成到项目功能中。

### 特点：

1.**高性能**: 使用sanic网络框架，支持异步请求处理，确保快速响应。

2.**安全性**: 集成了多种安全措施，如密码加密、验证码验证和令牌验证。

3.**扩展性**: 基于模块化设计，易于添加新功能和模块。

4.**跨平台**: 使用Python开发，支持多种操作系统和平台。

5.**数据处理**: 强大的数据处理能力，结合pandas、numpy等工具进行数据清洗、分析和操作。

6.**与区块链集成**: 通过web3库，实现与Ethereum区块链的交互，为未来的区块链应用提供可能。

## 项目安装和运行

1. **安装项目**：

```bash
cd GenAI-Platform
pip install -e .
```

2. **加载向量数据库内容**：

```bash
cd GenAI-Platform
python app.py -a
```

3. **运行平台**：

```bash
cd GenAI-Platform
python app.py
```

## API接口介绍

| 类别          | API路由             | 方法    | 功能描述                               |
|--------------|--------------------|--------|--------------------------------------|
| **Chatbot**  | `/mpcbot/sendchat_gpt4` | POST   | GPT-4版本的chatbot交互                     |
| **GPT**      | `api/getMessageList`    | GET    | 获取消息列表                             |
|              | `api/getMsgGroupList`   | GET    | 获取消息组列表                           |
|              | `api/delMsgGroupList`   | POST   | 删除消息组                               |
|              | `api/sendStremChat`     | POST   | 发送流式聊天内容                           |
| **UserRate** | `api/userRate`          | POST   | 用户评价                                 |
|              | `api/delMessages`       | POST   | 根据编码删除消息                           |
|              | `api/shareMessages`     | POST   | 分享消息                                 |
|              | `api/getShareMessages`  | POST   | 获取分享的消息                            |
| **User**     | `api/userLogin`         | POST   | 用户登录                                 |
|              | `api/checkLogin`        | GET    | 检查登录状态                              |
|              | `api/register`          | POST   | 用户注册                                 |
|              | `api/loginOut`          | GET    | 用户登出                                 |
|              | `api/sendVerifyCode`    | POST   | 发送验证码                               |
|              | `api/sendEmailCode`     | POST   | 发送电子邮件验证码                         |
|              | `api/getCaptcha`        | GET    | 获取验证码图像                             |
|              | `api/testVerifyCode`    | POST   | 验证验证码                                |
|              | `api/modifyPassword`    | POST   | 修改密码                                 |
| **Pay**      | `api/pay/cardInfo`      | GET    | 查询支付卡信息                            |
|              | `api/pay/orderCheck`    | GET    | 检查订单                                 |
|              | `api/pay/account`       | GET    | 查询用户账户                              |
|              | `api/pay/callback`      | POST   | 支付成功回调                              |

## 项目目录结构

以下是 `GenAI-Platform` 中 `genaipf` 主要目录结构和它们的功能描述：

-**conf**: 包含项目的各种配置文件，如服务器端口、数据库连接等设置。

-**constant**: 存放项目中使用的常量定义，如错误代码、消息常量等。

-**controller**: 负责处理API请求，与前端的交互，以及返回响应。API接口定义如`sendchat_gpt4`和`userLogin`都在这里定义。

-**dispatcher**: 负责API的调度逻辑，如将特定请求路由到相应的控制器或处理器。

-**exception**: 该目录包含自定义的异常处理逻辑以及自定义异常类的定义。

-**interfaces**: 定义与外部系统或其他项目模块交互的接口。

-**middlewares**: 用于处理API请求和响应的中间件。这些中间件可以执行诸如认证、日志记录等预处理和后处理任务。

-**routers**: 这里定义了所有API的路由，确保每个请求被正确地导向适当的控制器。

-**services**: 包含项目的核心业务逻辑以及与数据库的交互代码。

-**static**: 用于存放项目的静态资源，如CSS、JavaScript文件和图片等。

-**utils**: 该目录提供了各种实用程序和辅助功能，如日期转换、字符串操作等。

以上就是 `genaipf` 的目录结构和它们的功能描述。

## 技术栈介绍

以下是`GenAI-Platform`的主要技术栈及其在项目中的作用：

-**sanic (23.3.0)**: 一个高效、轻量级的Web服务器框架，支持异步请求处理，为项目提供了主要的Web服务。

-**qdrant-client (1.4.0)**: 向量数据库客户端，用于高效地存储和检索向量数据。

-**openai (0.27.4)**: OpenAI的Python客户端，用于调用GPT系列等模型来实现语言智能回复功能。

-**langchain (0.0.314)**: 链接语言模型与项目功能的工具，为项目中的语言处理部分提供支持。

-**pymysql (1.1.0)**: MySQL数据库的Python客户端，用于数据存储和检索。

-**redis (3.5.3)**: 高性能的键-值存储系统，用于缓存、会话管理等功能。

-**web3 (6.2.0)**: Ethereum区块链的Python客户端，用于实现与区块链的交互。

-**aiohttp (3.8.4)**: 异步HTTP客户端/服务器框架，用于处理异步网络请求。

-**APScheduler (3.10.1)**: 一个任务调度库，用于定时执行任务或定期运行某些代码片段。

其余的库和工具为项目提供了各种辅助功能和增强性能，确保项目的高效、稳定运行。

## 许可证信息

此项目使用 `Apache 2.0` 许可证，这意味着您可以自由地使用、修改和分发代码，但需要给出原始代码的适当归属。

## 联系方式与社区

我们非常重视社区的反馈和建议。

- **GitHub社区**: 如有任何疑问、建议或问题，欢迎在GitHub社区中提问或留言。
- **电子邮件**: 如果您需要进一步的支持或有特殊的需求，可以直接发送电子邮件至：[contact@mountainlion.ai](mailto:contact@mountainlion.ai)

我们会尽快回复并为您提供帮助。
