读这一章，需要你知道什么是工具调用。如果不知道，先读[Agent 用不好工具，先看工具的描述和报错](1-2-tool-calling.html)。

## 一句话 {#in-one-sentence}

MCP 是把工具接到 agent 上的标准协议，它一般不会让 agent 多出新本事，但是每接一个 server，别人的代码、你的权限、别人写的文本和一笔 token 开销都会跟着进来，所以接之前先看一条命令够不够，接了就当成依赖来管。

## 写给管理者 {#for-leaders}

- **要拍板的事**：把每个 MCP server 都当成一个要批准的依赖，就像一个不是你们写的库；一条普通命令能做到的事，优先用命令。
- **风险**：server 会带进来别人的代码、你们的权限，以及模型会当真的文本，而且批准之后它还可能变，npm 上就出过前 15 个版本都正常、到 1.0.16 才加后门的 server。hook 能不能管住 Copilot 里的 MCP 工具，文档没有写，我也没有测过。
- **做对的代价**：每个 server 做一次简短的审查（谁写的、能碰什么、凭据放在哪、版本固定了没有），再隔一段时间重读一遍工具清单。
- **可以问团队**：“现在连着哪些 server？每个是谁批准的，能碰什么，版本固定了吗？”

## 没有 MCP，每个工具要给每个平台写一遍 {#problem}

这篇文章，我想教你在接 MCP server 之前想清楚三件事：它到底改变了什么，接上以后有什么东西跟着进来，什么时候一条命令就够了。

agent 能做多少事，取决于它手里有哪些工具，迟早你会想让它读问题跟踪系统、查数据库或者操作浏览器，而这些工具总得有人来写。每个平台（VS Code Copilot、Claude Code、Codex）自己接工具的方式都不一样，所以没有共同标准的话，三个平台、三个工具可能就要九个连接器，每多一个平台或者一个工具，要写和要维护的代码都按乘法往上涨。

::: figure 1-3-mcp-plug

**Model Context Protocol**（MCP）就是解决这件事的标准，Anthropic 在 2024 年 11 月开源了它。它规定 AI 应用和工具之间用什么格式发消息，这样一个工具只要写一次，写成一个 **MCP server**，一个平台也只要实现一次这个协议，之后任何 server 都能接到任何支持 MCP 的平台上，九个连接器就变成了三加三，官方文档打的比方是 USB-C 接口。现在 VS Code、Claude Code、Codex、Cursor 和 ChatGPT 都支持它。（[What is the Model Context Protocol (MCP)?](https://modelcontextprotocol.io/docs/getting-started/intro)）

协议里还有两个角色要知道。**MCP host** 是 AI 应用本身，比如 VS Code 或者 Claude Code，host 每连一个 server 就建一个 **MCP client**，由这个 client 维持和这个 server 的连接。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）

你可能会觉得接上 MCP，agent 就多了新本事，其实一般没有，MCP 改变的是工具怎么接上去，server 能做的事，agent 用一条命令或者调一个 API 多半也能做。例外是托管在厂商那边、自带登录的远程 server，它可能给你别的办法拿不到的访问。所以接 server 的时候，不用先想它能多给你什么，要先想除了工具，还有什么跟着进来了。

## 接上一个 server，到底接进来了什么 {#how-it-works}

接上一个 server，等于给你的配置加了一个不是你写的依赖，它有自己的代码和更新节奏，用着你给的权限，还往模型的上下文里写东西。

### server 能提供三样东西

协议定义了 server 可以提供的三样东西，区别在于由谁决定用。**工具**（Tools）是模型自己决定调用的函数，比如操作文件、调 API、查数据库，多数人说 MCP，指的就是它。**资源**（Resources）是只读的数据，比如文件内容或者数据库 schema，由应用决定放不放进上下文。**提示**（Prompts）是可复用的模板，由用户明确调用。（[Understanding MCP servers](https://modelcontextprotocol.io/docs/learn/server-concepts)）

host 连上 server 以后发一个 `tools/list` 请求，拿回每个工具的名字、描述和参数，再把所有 server 的工具合成一张表交给模型，模型要用某个工具时，host 向对应的 server 发一个 `tools/call`，再把结果放回对话。所以在模型看来，MCP 工具和内置工具没有区别，它还是只能靠名字、描述和报错来用工具，上一章的规则全都适用，只不过这些文字现在是别人写的。

### 本地 server 跑在你的机器上，远程 server 跑在别人那里

server 有两种运行方式，用的是同一套消息。**本地** server 走 stdio 传输，host 在你的机器上启动一个进程，通过它的标准输入和输出通信，所以配置里写的其实就是一条启动命令，比如 VS Code 文档里 Playwright 的例子是 `npx -y @playwright/mcp@latest`。**远程** server 走 Streamable HTTP 传输，运行在别人的机器上，host 通过 HTTP 和它通信，通常要登录，同一个 server 通常服务很多用户，比如 Sentry 官方的 server。

这个区别决定了你要防什么，本地 server 是用你的权限、在你电脑上运行的代码，要防的是它在你机器上做什么，远程 server 是别人的服务，要防的是你发给它的数据，和你交给它的账号权限。

### 接上一个 server，有四样东西跟着进来

::: figure 1-3-what-comes-in

1. 别人的代码。本地 server 就是运行在你机器上的一个程序，一启动就在运行，不用等模型调用工具。VS Code 的文档说得很直接：“本地 MCP server 可以在你的机器上运行代码，工具可以用你的权限访问外部服务。”（[Add MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)）
2. 你的权限。server 用你给它的访问权限做事，比如你的数据库账号、你在问题跟踪系统里的 token，agent 通过这个 server 也就拿到了这些权限，所以 token 的范围有多大，agent 出错或者被骗的时候，损失就可能有多大。
3. 别人写的文本。工具的描述是别人写的，模型会读、会当真，工具返回的内容（一个 issue 的正文、一个网页）也是别人写的，这些文本里可能藏着给模型的命令（[Agent 读到的网页和文件，可能在给它下命令](4-6-untrusted-input.html)）。
4. 一笔固定的 token 开销。工具的名字、描述和参数都算模型的输入，如果 host 把它们全发给模型，每次请求都要带上，缓存能让钱少花一些，但是占的上下文窗口一点都不少，工具一多，模型也更容易选错。

第四样的开销可以很大。Anthropic 举过一个五个 server 的例子，GitHub 的 35 个工具约 26K token，Slack 的 11 个约 21K，再加上 Sentry、Grafana 和 Splunk，一共 58 个工具，对话还没开始就占了约 55K token（[Introducing advanced tool use for Claude](https://www.anthropic.com/engineering/advanced-tool-use)）。host 这边的办法是工具搜索，先不把工具定义发给模型，只给它一个搜索工具，用到的时候才加载完整定义。Claude Code 默认就这么做，会话开始时只加载工具名和 server 的说明（[Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)）。VS Code 在 Claude Sonnet 4.5、Opus 4.5 以上的模型上也默认打开，只留读写文件、运行命令这样一小组核心工具常驻，它的团队做过线上实验，用 Claude 模型时，中位用户一整个会话的 token 用量降了约 18%（[Improving token efficiency for GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/06/17/improving-token-efficiency-in-github-copilot)）。所以这笔开销到底有多大，要看你用的 host、模型和连了多少工具，最好数一数你自己的。

### 先看一条命令够不够

agent 需要的很多东西本来就是命令行程序，比如 `git`、`gh`、测试运行器、云平台的命令行工具，只要 agent 能用终端，不接任何 server 就能用上它们。我倾向于先用命令，因为它给你的配置加进来的代码和权限都更少，等多个平台共用一个工具的好处抵得过多出来的那个依赖，再换成 MCP 也不迟。

工具的厂商自己也这么建议。VS Code 的文档开头就说，现有工具够用的话就不需要再加 server。Claude Code 的文档建议优先用 `gh`、`aws`、`gcloud` 这些命令行工具，因为它们不会往上下文里加工具清单（[Manage costs effectively](https://code.claude.com/docs/en/costs)）。微软的 Playwright MCP 的 README 也告诉用 coding agent 的读者，CLI 加 skill 可能更合适，MCP 留给需要保持浏览器状态的长循环（[Playwright MCP](https://github.com/microsoft/playwright-mcp)）。

不过省多少 token 要看具体的活。Checkly 的 Stefan Judis 在 2026 年 7 月用 Claude Code 把同一个浏览器任务各跑了三遍，用 Playwright MCP 结束时的上下文约 48K 到 50K，用 `playwright-cli` 约 45K 到 48K，差别很小，他的解释是工具定义现在是延迟加载的（[CLIs are more token-efficient than MCP. Or are they?](https://www.checklyhq.com/blog/mcp-vs-cli-token-efficiency/)）。所以在有工具搜索的 host 上，命令的好处主要是依赖和权限更少，不在 token 上。

MCP 也有命令比不了的地方。它的每个工具都有名字和参数 schema，host 可以按工具来批准，而 agent 一旦能用终端，就能跑任何命令，hook 读到的也只是命令的文本（[硬性规则放在哪？用 hook](2-2-hooks.html)）。所以给一个写操作很多的内部系统做接口时，几个窄的 MCP 工具可能比一个什么都能做的命令行更好管。

| 选 | 什么时候 |
| --- | --- |
| 命令行程序 | 它已经有了，在本地运行，输出又短又清楚，agent 又能用终端 |
| MCP server | 你想在多个平台上共用同一个工具，需要结构化的输入，要登录一个远程服务，想按工具来批准，或者 agent 运行的地方没有终端 |

### 接之前问五个问题

既然 server 是依赖，对任何依赖该问的问题，对它也都该问，下面五个按我会问的顺序排。

- 谁写的，谁在持续更新？VS Code 的建议是，在安装或启动之前先看“发布者、命令或端点，以及它请求的访问权限”（[Add MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)）。上架了也不等于审查过，MCP 官方的 Registry 只存元数据、验证发布者的命名空间，安全扫描交给 npm 这样的包仓库和下游的市场（[The MCP Registry](https://modelcontextprotocol.io/registry/about)）。
- 它能碰什么？优先选只限于任务所需的 server，比如一个读 issue 的 server，就不该拿着一个能删仓库的 token。
- 凭据放在哪？别放在对话里，也别提交进项目，VS Code 的文档还提醒，个人配置文件也不是存密钥的地方（[MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)）。
- 版本固定了吗？启动命令里写着 `@latest` 的话，包一更新，之后启动跑的就可能是新代码，所以要写死一个看过的版本。
- 它返回的东西可信吗？如果文本来自外部，比如公开的网页、任何人都能提的工单，就当成不可信的。

### hook 管不管得住 MCP 工具，各家不一样

Claude Code 的文档写明了，MCP 工具在 `PreToolUse`、`PostToolUse` 这些事件里和普通工具一样出现，名字是 `mcp__<server>__<tool>`（[Hooks reference](https://code.claude.com/docs/en/hooks)）。Copilot 这边没有写，GitHub 的 hook 参考只说 `preToolUse` 在“每个工具运行之前”触发，列出来的工具名都是内置工具，VS Code 的 hook 文档也没有提 MCP（[GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference)）。我自己的 harness 没有搭任何 MCP server，这类 server 是公司按自己的环境配的，有的公司还禁止非官方的，所以 MCP 工具在 Copilot 上是不是经过 hook、hook 能不能看到完整的参数，我没有测过。

想靠 hook 的话，先用一个无害的 server 测一次，写一个只记录输入的 hook，调用一次 MCP 工具，看记录里有没有这次调用、参数全不全。就算经过了 hook，它看到的也只是这次调用的参数，server 收到以后做了什么，它看不到。

### 接上以后怎么查

已经连上的 server 也要回头看，对每一个问三个问题：

1. 我知道它是谁写的、能碰什么吗？
2. 命令行程序能做同样的事吗？
3. 它的工具里，我真正用到的有几个？

第三个问题不用安装任何东西就能回答。在 VS Code 里打开 **Chat: Open Customizations** 的 Tools 页，能看到每组工具启用了几个、一共几个，在 Claude Code 里用 `/context` 看是什么在占上下文。数完再想想上周用过其中哪些，其余的都是有成本、有风险，却没有收益的，可以把工具关掉，或者把整个 server 停用。

## 官方的 server 也会出事，审查过的 server 也会变 {#costs-and-traps}

每个 server 都是外部文本和外部代码通向 agent 的一条路，接得越多，能出问题的地方越多，而且不光是在用的才算，当初为了试试加上、后来忘掉的 server 也一直在那里。

名气大也不是跳过审查的理由。Invariant Labs 在 2025 年 5 月公开过一个例子，攻击者在一个公开仓库里提一个 issue，里面藏着给 agent 的指令，用户只是让 agent 看看这个仓库的 issue，而 agent 连着官方的 GitHub MCP server，又有权限读用户的私有仓库，结果它把私有仓库的内容写进了公开仓库的一个 pull request。Invariant 说这不是 server 代码的缺陷，GitHub 光改 server 修不好，他们的建议是收窄权限，比如一个会话只让 agent 碰一个仓库（[GitHub MCP Exploited](https://invariantlabs.ai/blog/mcp-github-vulnerability)）。不可信的文本、私有数据和对外的出路，这三样在这里全凑齐了（[Agent 读到的网页和文件，可能在给它下命令](4-6-untrusted-input.html)）。“官方”只告诉你代码是谁写的，它拿着你的凭据，照样会读到别人写的文本。

就算是你仔细审查过的 server，也可能在你不知情的时候变了，变的地方有三处。

- 工具清单变了。协议允许 server 更新工具，再通知 client 重新拉取清单，所以 server 可以在你批准之后改掉某个工具的描述，这种做法叫 rug pull。描述里能藏什么，Invariant Labs 演示过，叫工具投毒（tool poisoning），一个看起来只做加法的 `add` 工具，描述里藏着一段话，让模型读 `~/.ssh/id_rsa`，再把内容放进一个参数发回去（[Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)）。
- 代码变了。npm 上的 `postmark-mcp` 冒用 Postmark 的名字，前 15 个版本都正常，到 1.0.16 才加上后门，把邮件偷偷密送到外部服务器（[Security Alert: Malicious 'postmark-mcp' npm Package](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package)）。
- 配置变了。VS Code 里工作区的 `.mcp.json` 和 `.vscode/mcp.json` 跟着 Workspace Trust 走，在受信任的工作区里，配置改了也不会再单独问你，而配置里写的是一条会运行的命令，所以改这些文件的 pull request 要当成改代码来审（[Manage and troubleshoot MCP servers](https://code.visualstudio.com/docs/agents/run/manage-mcp-servers)）。

所以要隔一段时间重读一遍工具清单，能固定版本就固定。

另一个坑是以为标准一样，行为也就一样。协议只统一了 host 和 server 之间的消息，配置放在哪、支持协议的哪些部分、怎么批准，都是各家自己定的，光 VS Code 就有两种配置格式，顶层键一个是 `mcpServers`，一个是 `servers`，不能直接互相复制，各家的配置放在哪，可以查[扩展点速查表](a-extension-points.html)。协议本身也还在变，当前版本是 2026-07-28，这一版去掉了连接时的握手和会话，还把 sampling、roots 和 logging 标成了废弃，距离上一版只有八个月（[Key Changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog)）。只是用别人的 server，这些变化你多半感觉不到，自己写 server 的话，就要留出跟版本的工夫。

## 协议和 VS Code 都把决定权留给了你 {#industry}
{status: industry}

协议的文档说，MCP 只管交换上下文，“不规定 AI 应用如何使用 LLM，也不规定如何管理所提供的上下文”（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）。规范要求 host 调用任何工具之前都要得到用户明确的同意，同时也承认 MCP 自己没法在协议层面强制这些原则（[Specification](https://modelcontextprotocol.io/specification/latest)）。VS Code 就是这样一个 host，它让你看发布者和请求的访问权限，只批准你理解的操作，给组织的是 `ChatMCP` 策略，可以把 server 限制在一份 registry 里，不过这个策略管不到 Copilot 运行时自己发现的 server（[Secure AI-assisted development in VS Code](https://code.visualstudio.com/docs/agents/run/security)）。所以两边的分工是一致的，协议让接入变容易，决定接入什么仍然是你的事。

## 什么时候可以删掉一个 server {#when-to-delete-it}
{status: industry}

不再用某个 server 的工具了，或者一条普通命令就能完成任务了，就把它移除。

这份谨慎什么时候能放松，要看平台。如果平台默认把本地 server 关进沙箱，坏的 server 能做的事就少很多，但是写这一章的时候还没到这一步，VS Code 的 Copilot 会话沙箱默认是关的，打开以后也默认不拦出站网络（[Sandbox Copilot agent sessions](https://code.visualstudio.com/docs/agents/run/agent-sandboxing)）。沙箱也只管得住 server 这个进程，管不了你交给它的远程账号，也管不了它返回给模型的文本，所以即便有了沙箱，我还是会在添加之前检查发布者和访问权限。

## 在你自己的环境里试试 {#try-it}

::: prompt
找出为这个项目或编辑器配置的每一个 MCP server（看编辑器和项目的设置，以及所有 MCP 配置文件）。每一个，告诉我：谁发布的、在本地还是远程运行、启动命令有没有固定版本、用什么凭据以及存在哪里、暴露了多少个工具、一个普通的命令行程序能不能做同样的事。把存在已提交文件里的凭据标出来。不要打印任何密钥的值，也不要修改任何文件。
:::

## 延伸阅读 {#go-deeper}

- Model Context Protocol：[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)、[Specification](https://modelcontextprotocol.io/specification/latest)、[Client Best Practices](https://modelcontextprotocol.io/docs/develop/clients/client-best-practices)、[Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- VS Code 文档：[Add MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)、[Manage and troubleshoot MCP servers](https://code.visualstudio.com/docs/agents/run/manage-mcp-servers)、[MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)
- Anthropic：[Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)，让 agent 写代码来调用 server，中间结果不进模型的上下文，代价是要有一个安全的沙箱
- Invariant Labs：[Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)、[GitHub MCP Exploited](https://invariantlabs.ai/blog/mcp-github-vulnerability)

## 在 harness 里探索 {#explore}

我的 harness 给 agent 三类工具：内置工具、它自己的命令行工具，还有可选的 MCP，它自己没有搭任何 MCP server。harness 可以和你一起打开真实的文件，带你看 MCP 会接在哪里，其他工具又是怎么分类的。

::: prompt
/harness-rookie-wondering 我读完了“接 MCP server 之前，要想清楚什么？”这一章。请教我这个 harness 里的三类工具，以及 MCP 放在哪里。带我打开真实的文件，让我看工具名是怎么分到各类里的。
:::
