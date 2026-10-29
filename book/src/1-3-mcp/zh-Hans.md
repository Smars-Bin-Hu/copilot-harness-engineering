读这一章，需要你知道什么是工具。如果不知道，先读[Tool calling，以及怎么给 agent 设计工具](1-2-tool-calling.html)。

## 一句话 {#in-one-sentence}

MCP 不是什么新的能力，而是工具的一个标准插头；插上它，别人的代码、权限和文本也跟着进了你的 agent。

## 写给管理者 {#for-leaders}

- **要拍板的事**：把每个 MCP server 都当成一个要你批准的依赖，就像一个不是你写的库；一条普通命令就能完成的事，优先用命令。
- **风险**：server 会带进来别人的代码、别人的权限，以及模型会读、会照做的文本，而且你批准之后，它的工具清单还可能变。hook 能不能像管内置工具那样管住 MCP 工具，我没有测过。
- **做对的代价**：每个 server 做一次简短的审查（谁写的、能碰什么、凭据放在哪），再隔一段时间重读一遍工具清单。
- **可以问团队**：“现在连着哪些 server？每个是谁批准的？每个能碰什么？”

## 工具为什么需要一个标准插头？ {#problem}

agent 有多大用处，取决于它手里有哪些工具。早晚有一天，你会想让它读你的问题跟踪系统、查数据库，或者操作浏览器，而这些工具都得有人来写。麻烦在于，每个平台（VS Code Copilot、Claude Code、Codex）接收工具的方式都不一样。

所以，没有一个共同的标准，工作量就会成倍增加。三个平台、三个工具，可能就要九个单独的连接器，每一个都是有人要写、写完还要持续更新的代码。每多一个平台，就多一行；每多一个工具，就多一列。

::: figure 1-3-mcp-plug

**Model Context Protocol**（MCP）就是解决这个问题的标准。它给两头定了同一套**协议**，也就是一种约定好的发消息的方式。有了它，不同人写的两个程序也能配合工作。这样一来，一个工具只要写一次，写成一个 **MCP server**；一个平台也只要学一次这个协议。之后，任何 server 都能和任何支持 MCP 的平台配合。可以想想 USB 接口：插头是标准，至于你插的是什么，它一概不管。

在工具这一头，MCP server 是一个以标准方式向 agent 提供能力的程序，可以运行在你的机器上，也可以在别处。另一头是 **MCP host**，也就是 AI 应用，比如 VS Code。它为每个连上的 server 建一个 **client**，由这个 client 保持连接。

那么，一个标准插头会不会让 agent 多出新的本事？一般不会（自带登录的远程服务是个例外，它能提供你没有别的办法获得的访问）。MCP 改变的是工具*怎么接上去*。既然只改了接法，真正要问的就是：随着工具一起，还有什么从这个插头进来了。

## 你接进来的到底是什么 {#how-it-works}

### server 能提供什么

要看清进来了什么，先得知道 server 能往这边送些什么。协议定义了 server 可以对外提供的三样东西。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）多数人说 MCP，指的是其中的**工具**（Tools），也就是 agent 可以调用来做事的函数，比如文件操作、API 调用、数据库查询，它和[Tool calling，以及怎么给 agent 设计工具](1-2-tool-calling.html)里的工具是同一种。除了工具，server 还可以提供**资源**（Resources），即 agent 可以读来当上下文的数据，比如文件内容或数据库记录；以及**提示**（Prompts），即可复用的模板，用来帮着组织一次对话，比如系统 prompt 或少样本示例。

用到这些之前，agent 这一侧会先问 server 有什么。对工具来说，这是一个 `tools/list` 请求，拿回来的是每个工具的名字、描述和它接受的参数。之后模型要求调用某个工具，host 就向对应的 server 发一个 `tools/call`，再把答案作为文本放回对话。所以在模型看来，MCP 工具和别的工具没什么两样。

### 本地和远程

server 有两种运行方式，两种用的是同一个协议。**本地（stdio）** server 由 host 在你的机器上作为一个程序启动，host 通过它的标准输入和输出（每个命令行程序都有的纯文本管道）和它通信。通常也只有这一个 host 在用它。**远程（Streamable HTTP）** server 运行在别的地方，host 通过普通的网络请求（HTTP）和它通信，通常要登录。一个远程 server 可以服务很多用户。

这个区别对安全很要紧，因为本地 server 是以你的权限、在你电脑上运行的代码；远程 server 则是别人的服务，你得把数据发给它。

### 接上一个，就带进来什么

不过，不管本地还是远程，server 都不是打开就行的功能，而是一个**依赖**，就像一个不是你写的库。接上它，会带进来四样东西。

::: figure 1-3-what-comes-in

1. 它带进来别人的代码，因为本地 server 就运行在你的机器上。VS Code 自己的文档说：“本地 MCP server 可以在你的机器上运行代码，工具可以用你的权限访问外部服务。”（[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)）
2. 它带进来别人的权限。server 以你给它的访问权限行事，比如你的数据库登录、你在问题跟踪系统里的 token，于是 agent 通过这个 server，也拿到了这些权限。
3. 它带进来别人的话，而模型会把这些话当成指令。server 的工具描述，是模型会读、会当真的文本；工具返回的内容（一个 issue 的正文、一个网页），也是写它的人写的文本。模型读到的文本里，可能藏着给它的命令，[agent 读到的文字可能在指挥它](4-6-untrusted-input.html)讲的就是这件事。
4. 它带进来一笔固定的开销。每个工具的名字、描述和参数，每次调用都要发给模型，所以一个工具很多、你却很少用的 server，每一轮照样花 token；工具一多，模型也更难选（[Tool calling，以及怎么给 agent 设计工具](1-2-tool-calling.html)）。绕开的办法是有的，我在这里只点到为止。协议自己的文档提到，连了很多 server 的 client，可以用渐进式的工具发现，而不是一开始就把所有工具都加载进来（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）。Anthropic 的文章 [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) 则把工具定义撑爆上下文窗口当作一个问题，并介绍了只加载所需工具，或者让 agent 通过代码来调用 server 的办法。这笔开销有多大，取决于你连了多少工具，所以数一数你自己的。

### 加之前要检查什么

既然 server 是一个依赖，对任何依赖该问的问题，对它也都该问。下面是四个，按我会问的顺序排。

- 谁写的，谁在持续更新？VS Code 的建议是，在安装或启动 server 之前，先审查“发布者、命令或端点，以及它请求的访问权限”。
- 它能碰什么？优先选只限于任务所需的 server，比如一个读 issue 的 server，就不该拿着一个能删仓库的 token。
- 凭据放在哪？别放在对话里，也别提交进项目，VS Code 的文档也是这样提醒的。
- 它返回的东西可信吗？如果文本来自外部，比如公开的网页、任何人都能提的工单，就当成不可信的。

### 用 MCP，还是一条命令就够？

在这四个问题之前，其实还有一个问题：这个工具真的需要一个 server 吗？agent 需要的很多东西，本来就以命令行程序的形式存在，比如 `git`、测试运行器、云平台的命令行工具。只要 agent 能用终端，不需要任何 server 就能用上它们。

| 选 | 什么时候 |
| --- | --- |
| 命令行程序 | 它已经有了，在本地运行，输出又短又清楚。活动部件更少 |
| MCP server | 你想在多个平台上用同一个工具，或者它需要结构化的输入、可发现的能力清单，或者要登录一个远程服务 |

我倾向于先用命令，因为它给你的配置加进来的代码和权限都更少。等共用插头的好处开始抵得过多出来的那个依赖，再换成 MCP 也不迟。

### hook 管得住 MCP 工具吗？

你也许指望，hook 能像拦下一次糟糕的内置工具调用那样，拦下一次糟糕的 MCP 调用。这一点我没法给你打包票。我自己的 harness 没有搭任何 MCP server（这类 server 是公司按自己的环境配的，有的公司还禁止非官方的），所以 MCP 工具调用是不是像内置工具调用那样经过 hook、hook 能不能看到它们的完整参数，我**没有测过**。在你自己用一个无害的 server 测过之前，别指望 hook 能替你守住 MCP 工具。

### 怎么检查你自己的配置

已经连上的 server，也值得回头看一看。对每一个，问三个问题：

1. 我知道它是谁写的、能碰什么吗？
2. 命令行程序能做同样的事吗？
3. 它的工具里，我真正用到的有几个？

第三个问题，不用安装任何东西就能回答。列出你的 agent 现在有的工具（多数编辑器在对话的工具选择器里显示，具体在哪要看编辑器，查一下它的文档），数一数，再问问自己上周用过其中哪些。其余的，就是有成本、有风险，却没有收益。

## 插头多了，会在哪里出问题 {#costs-and-traps}

风险先从 server 本身说起。每个 server 都是外部文本和外部代码通向你的 agent 的一条路，所以每多接一个插头，攻击面就大一圈。而且不光是在用的才算，那些当初为了试试加上、后来忘掉的 server，也一直在那里。

名气大，也不是跳过审查的理由。一个受人尊敬的公司发布的 server 是“官方”的，可它照样会拿到你的凭据，照样会返回别人写的文本。官方不等于对你安全。

就算是你仔细审查过的 server，也可能在你不知情的时候变了。协议允许 server 告诉 client，它的工具变了，所以你审查时没问题的工具，下个月可能就不是那一个了。server 还可以在你批准之后改某个工具的描述，而描述是模型会照做的文本（这类攻击常被叫作 rug pull 或工具投毒，[agent 读到的文字可能在指挥它](4-6-untrusted-input.html)讲了这个想法）。所以要时不时重读一遍清单，能固定 server 的版本就固定。

最后一个坑，是以为标准一样，行为也就一样。各平台支持协议的哪些部分、怎么请求审批、把设置存在哪里，都不一样，所以请查你所用平台的当前文档。

## 协议和 VS Code 也这么看吗？ {#industry}
{status: industry}

协议自己的文档把 MCP 描述为一个交换上下文的协议，并说它“不规定 AI 应用如何使用 LLM，也不规定如何管理所提供的上下文”。换句话说，加载什么、怎么问你，由 host 决定。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）VS Code 就是这样一个 host，它把 server 当成要审查的代码：看发布者和它请求的访问权限，只批准你理解的操作。（[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)）

所以两者对分工的看法是一致的。协议让接入变容易，而决定接入什么，仍然是你的事。

## 什么时候可以删掉一个 server {#when-to-delete-it}
{status: industry}

决定接入什么，也包括决定拔掉什么。不再用某个 server 的工具了，或者一条普通命令就能完成任务了，就把它移除。如果平台开始默认给 server 加沙箱，让坏的 server 干不了多大的坏事，这份谨慎本身也可以放松一点。即便如此，我还是会在添加之前检查发布者和访问权限。

## 在你自己的环境里试试 {#try-it}

::: prompt
找出为这个项目或编辑器配置的每一个 MCP server（看编辑器和项目的设置，以及所有 MCP 配置文件）。每一个，告诉我：谁发布的、在本地还是远程运行、用什么凭据以及存在哪里、暴露了多少个工具、一个普通的命令行程序能不能做同样的事。把存在已提交文件里的凭据标出来。不要打印任何密钥的值，也不要修改任何文件。
:::

## 延伸阅读 {#go-deeper}

- Model Context Protocol：[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)
- VS Code 文档：[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- Anthropic：[Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

## 在 harness 里探索 {#explore}

我的 harness 给 agent 三类工具：内置的、它自己的命令行工具，以及可选的 MCP。它自己没有搭任何 MCP server。harness 可以和你一起打开真实的文件，带你看 MCP 会接在哪里、其他工具又是怎么分类的。

::: prompt
/harness-rookie-wondering 我读完了“MCP server：接工具的标准接口”这一章。请教我这个 harness 里的三类工具，以及 MCP 放在哪里。带我打开真实的文件，让我看工具名是怎么分到各类里的。
:::
