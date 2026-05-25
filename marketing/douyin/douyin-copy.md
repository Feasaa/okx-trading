# OKX Trading 抖音发布文案

## 版本 1：项目展示型

标题：
我写了一个 AI + OKX 的量化交易系统

口播：
我最近做了一个开源项目，叫 OKX Trading。它不是一个简单的回测脚本，而是把 AI 生成策略、Ta4j 回测、风险评分、OKX 实盘执行和交易提醒串成了一条完整链路。

你可以用自然语言描述一个策略，比如“双均线加 RSI”，系统会生成 Java/Ta4j 策略代码，然后进入回测框架，计算收益、回撤、胜率、夏普、VaR、CVaR 等指标。通过回测后，还可以接 OKX WebSocket 和 REST API 做实盘策略运行。

后端是 Java 21 + Spring Boot，配 MySQL、Redis、Kafka、Docker，前端用 cryptoquantx。目前 GitHub 已经 90 多星。

这个项目只做技术研究，不是投资建议。感兴趣可以去 GitHub 搜 okx-trading。

文案：
一个人的量化交易系统可以做到什么程度？

我把 AI 策略生成、Ta4j 回测、风险评分、OKX 实盘执行、交易提醒、MySQL/Redis/Kafka 数据管道做成了一套完整闭环。

不是承诺收益，只是把 AI + 量化交易的工程化链路跑通。

GitHub：ralph-wren/okx-trading

#AI量化 #量化交易 #Java #SpringBoot #OKX #程序员 #开源项目

## 版本 2：强钩子型

标题：
我让 AI 写策略，再拿去回测和实盘

口播：
很多人说 AI 写交易策略不靠谱，我同意，直接实盘肯定不靠谱。

所以我做的是一套验证链路：先让 AI 根据自然语言生成 Java/Ta4j 策略，再动态编译，然后用历史 K 线跑回测，算 33 个风险指标，最后才允许进入 OKX 实盘策略引擎。

这个项目里已经有 250 多个策略，支持批量回测、动态评分、订单记录、交易提醒，也接了 MySQL、Redis、Kafka 和 Docker。

重点不是“AI 一夜暴富”，而是“AI 生成想法，人用工程系统验证它”。

文案：
AI 生成交易策略，真正难的不是生成，而是验证。

我的做法：
1. 自然语言生成策略
2. 动态编译 Java/Ta4j 代码
3. 历史 K 线回测
4. 33 个风险指标评分
5. 小资金/模拟实盘验证
6. 通知和日志持续监控

项目已开源：ralph-wren/okx-trading

仅技术研究，不构成投资建议。

#AI编程 #量化系统 #回测 #OKX #开源 #交易系统

## 版本 3：程序员技术型

标题：
Java 后端写量化系统，能有多完整？

口播：
这个项目后端是 Java 21 + Spring Boot 3.2.5，核心分几层：

Controller 层提供策略、回测、行情、交易、账户接口；
Service 层接 DeepSeek、Ta4j、OKX API、通知服务；
数据层用 MySQL 存策略、K 线、回测结果和订单；
Redis 做缓存，Kafka 做 K 线数据缓冲；
前端用 cryptoquantx 做策略工厂、回测分析和实盘交易页面。

最有意思的是策略链路：AI 生成代码，Janino 或 Java Compiler API 动态编译，Ta4j 跑回测，指标系统打分，然后再进入实盘策略管理。

文案：
这不是一个量化脚本，而是一套 Spring Boot 量化交易后端。

技术栈：
Java 21 / Spring Boot 3.2.5 / Ta4j / DeepSeek / OKX WebSocket / MySQL / Redis / Kafka / Docker / Swagger

项目：ralph-wren/okx-trading

风险提示：只做技术研究，不是投资建议。

#Java #SpringBoot #系统架构 #量化交易 #开源项目 #后端开发

## 版本 4：封面标题备选

- 我写了一个 AI 炒币系统
- AI 写策略，系统跑回测
- 250+ 策略自动回测
- 90+ Stars 的量化项目
- 从一句话到 OKX 实盘
- Java 写量化系统能有多完整？
- AI + 量化，不是玄学，是工程
- 33 个风险指标筛策略

## 评论区置顶

项目地址：github.com/ralph-wren/okx-trading

风险提示：这个项目只用于技术研究、回测和自动化交易系统学习，不构成任何投资建议。实盘交易请先模拟盘/小资金验证。
