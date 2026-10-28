读这一章，需要你知道什么是工具。如果不知道，先读[Tool calling，以及怎么给 agent 设计工具](1-2-tool-calling.html)。

## 一句话 {#in-one-sentence}

MCP 不是什么新的能力。它是工具的一个标准插头，会把别人的代码、权限和文本带进你的 agent。

## 写给管理者 {#for-leaders}

- **要拍板的事**：把每个 MCP server 都当成一个要你批准的依赖，就像一个不是你写的库；如果一条普通命令就能完成任务，优先用命令。
- **风险**：server 会带进来别人的代码、别人的权限，以及模型会读、会听从的文本。它的工具清单，在你批准之后也可能变。hook 能不能像管内置工具那样管 MCP 工具，我没有测过。
- **做对的代价**：每个 server 做一次简短的审查（谁写的、能碰什么、凭据放在哪），再定期重读一遍工具清单。
- **可以问团队**：“现在连着哪些 server？每个是谁批准的？每个能碰什么？”

## 问题 {#problem}

agent 有多大用处，取决于它有哪些工具。你可能想让自己的 agent 读你的问题跟踪系统、查数据库，或者操作浏览器。这些工具得有人来写，而每个平台（VS Code Copilot、Claude Code、Codex）接收工具的方式都不一样。

没有共同的标准，工作量会成倍增加。三个平台、三个工具，可能需要九个单独的连接器。每个连接器都是有人要写、要持续更新的代码，每多一个平台或工具，就多一行或一列。

::: figure 1-3-mcp-plug

**Model Context Protocol**（MCP）就是解决这个问题的标准。一个工具只写一次，写成一个 **MCP server**。一个平台只学一次这个协议。此后，任何 server 都能和任何支持 MCP 的平台配合。可以想想 USB 接口：插头是标准，它不管你插的是什么。

### 先说三个词

- **MCP server** 是一个以标准方式向 agent 提供能力的程序。它可以运行在你的机器上，也可以在别处。
- **MCP host** 是 AI 应用，比如 VS Code。它为每个连上的 server 建一个 **client**。client 负责保持连接。
- **协议**是一种约定好的发消息的方式，这样不同人写的两个程序可以配合工作。

这一章始终围绕一个想法。MCP 通常不会给 agent 一个它本来拿不到的能力（带自己登录的远程服务是个例外：它能提供你没有别的办法获得的访问）。它改变的是工具*怎么接上去*。后面几节的内容，都是由此而来的。

## 原理 {#how-it-works}

### server 能提供什么

协议定义了 server 可以对外提供的三样东西。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）

- **工具（Tools）**：agent 可以调用来做事的函数：文件操作、API 调用、数据库查询。多数人说 MCP，指的就是这个，它和[Tool calling，以及怎么给 agent 设计工具](1-2-tool-calling.html)里的工具是同一种。
- **资源（Resources）**：agent 可以读来当上下文的数据，比如文件内容或数据库记录。
- **提示（Prompts）**：可复用的模板，帮助组织一次对话，比如系统 prompt 或少样本示例。

agent 这一侧先问 server 有什么（对工具来说，是一个 `tools/list` 请求），拿回每个工具的名字、描述和它接受的参数。模型要求调用时，host 会向对应的 server 发一个 `tools/call`，并把答案作为文本放回对话。从模型的角度看，这和别的工具没什么两样。

### 本地和远程

server 有两种运行方式。

- **本地（stdio）**。host 在你的机器上把 server 作为一个程序启动，通过它的标准输入和输出（每个命令行程序都有的纯文本管道）和它通信。通常只有一个 host 在用它。
- **远程（Streamable HTTP）**。server 运行在别的地方，host 通过普通的网络请求（HTTP）和它通信，通常要登录。一个远程 server 可以服务很多用户。

两种方式的协议是一样的。区别对安全很要紧：本地 server 是以你的权限在你电脑上运行的代码，而远程 server 是别人的服务，你要把数据发给它。

### 接上一个，你就把什么带了进来

这是本章的重点。server 不是一个你打开的功能；它是一个**依赖**，像一个不是你写的库。随它而来的有四样东西。

::: figure 1-3-what-comes-in

1. **别人的代码**。本地 server 运行在你的机器上。VS Code 自己的文档说：“本地 MCP server 可以在你的机器上运行代码，工具可以用你的权限访问外部服务。”（[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)）
2. **别人的权限**。server 以你给它的任何访问权限行事：你的数据库登录、你的问题跟踪系统的 token。agent 现在通过这个 server，拥有了这些权限。
3. **别人的话，变成了指令**。server 的工具描述，是模型会读并当真的文本。而工具返回的内容（一个 issue 的正文、一个网页），是写它的人写的文本。模型读到的文本里，可能含有给它的命令。[agent 读到的文字可能在指挥它](4-6-untrusted-input.html)讲的就是这件事。
4. **一笔固定的开销**。每个工具的名字、描述和参数，每次调用都要发给模型。一个有很多工具、你却很少用的 server，每一轮照样花 token，工具一多，模型也更难选（[Tool calling，以及怎么给 agent 设计工具](1-2-tool-calling.html)）。协议自己的文档提到，连了很多 server 的 client，可以用渐进式的工具发现，而不是一开始就把所有工具都加载进来。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）Anthropic 的文章 [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) 把工具定义撑爆上下文窗口当作一个问题，并介绍了只加载所需工具，或者让 agent 通过代码来调用 server 的办法。这里我只是指个路。这笔开销有多大，取决于你连了多少工具，所以数一数你自己的。

### 加之前要检查什么

四个问题，按我会问的顺序。

- **谁写的，谁在持续更新？** VS Code 的建议是，在安装或启动 server 之前，先审查“发布者、命令或端点，以及它请求的访问权限”。
- **它能碰什么？** 优先选只限于任务所需的 server。一个读 issue 的 server，不该拿着一个能删仓库的 token。
- **凭据放在哪？** 不要放在对话里，也不要提交进你的项目。VS Code 警告过，不要把凭据贴进对话，也不要提交。
- **它返回的东西可信吗？** 如果文本来自外部（公开的网页、任何人都能提的工单），就当成不可信的。

### 用 MCP，还是一条命令就够？

不是每个工具都需要 server。agent 需要的很多东西，本来就以命令行程序的形式存在：`git`、测试运行器、云平台的命令行工具。能用终端的 agent，不需要任何 server 就能用上它们。

| 选 | 什么时候 |
| --- | --- |
| 命令行程序 | 它已经有了，在本地运行，输出又短又清楚。活动部件更少 |
| MCP server | 你想在多个平台上用同一个工具，或者它需要结构化的输入、可发现的能力清单，或者要登录一个远程服务 |

我倾向于先用命令，因为它给你的配置加进来的代码和权限都更少。等共用的插头开始值回多出来的那个依赖，再换成 MCP。

### 我没测过的

在你测过之前，别指望 hook 能保护你不受 MCP 工具的影响。我自己的 harness 没有搭任何 MCP server。公司会为自己的环境配置它们，有些公司的环境还禁止非官方的 server。MCP 工具调用是不是像内置工具调用那样经过 hook，hook 能不能看到它们的完整参数，我**没有测过**。如果你靠 hook 来守 MCP 工具，先用一个无害的 server 测一下。

### 测一测你自己的配置

对你连上的每个 server，问**三个问题**：

1. 我知道它是谁写的、能碰什么吗？
2. 命令行程序能做同样的事吗？
3. 它的工具里，我真正用到的有几个？

**一个不用安装任何东西的检查**。列出你的 agent 现在有的工具（多数编辑器在对话的工具选择器里显示；去哪找请查你编辑器的文档）。数一数。然后问问哪些是你上周用过的。其余的就是有成本、有风险，却没有收益。

## 代价和坑 {#costs-and-traps}

**插头越多，攻击面越大**。每个 server 都是外部文本和外部代码通向你的 agent 的一条路。你为了试点东西加上、后来又忘了的 server，仍然在那里。

**“官方”不等于对你安全**。一个受人尊敬的公司发布的 server，仍然会拿到你的凭据，仍然会返回别人的文本。

**server 的工具清单会变**。协议允许 server 告诉 client，它的工具变了。你审查时没问题的工具，下个月可能就不是那一个了。server 还可以在你批准之后改某个工具的描述，而描述是模型会听从的文本（这类攻击常被叫作 rug pull 或工具投毒；[agent 读到的文字可能在指挥它](4-6-untrusted-input.html)讲了这个想法）。时不时重读一遍清单，能固定 server 的版本就固定。

**共用标准不等于行为一致**。各平台支持协议的哪些部分、怎么请求审批、把设置存在哪里，都不一样。请查你所用平台的当前文档。

## 业界怎么说 {#industry}
{status: industry}

- **协议自己的文档**把 MCP 描述为一个交换上下文的协议，并说它“不规定 AI 应用如何使用 LLM，也不规定如何管理所提供的上下文”。加载什么、怎么问你，由 host 决定。（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）
- **VS Code** 把 server 当成要审查的代码：看发布者和请求的访问权限，只批准你理解的操作。（[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)）

两者对分工的看法一致：协议让接入变容易，而决定接入什么，仍然是你的事。

## 什么时候可以删掉 {#when-to-delete-it}
{status: industry}

不再用某个 server 的工具了，或者一条普通命令就能完成任务了，就把它移除。如果平台开始默认给 server 加沙箱，让坏的 server 干不了多大的坏事，这份谨慎也可以放松一点。我还是会在添加之前检查发布者和访问权限。

## 在你自己的环境里试试 {#try-it}

不用装 harness。在你自己的仓库里打开 agent，粘贴：

::: prompt
找出为这个项目或编辑器配置的每一个 MCP server（看编辑器和项目的设置，以及所有 MCP 配置文件）。每一个，告诉我：谁发布的、在本地还是远程运行、用什么凭据以及存在哪里、暴露了多少个工具、一个普通的命令行程序能不能做同样的事。把存在已提交文件里的凭据标出来。不要打印任何密钥的值，也不要修改任何文件。
:::

## 延伸阅读 {#go-deeper}

- Model Context Protocol：[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)
- VS Code 文档：[MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- Anthropic：[Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

## 在 harness 里探索 {#explore}

我的 harness 给 agent 三类工具：内置的、它自己的命令行工具，以及可选的 MCP。它自己没有搭任何 MCP server。harness 可以带你看 MCP 会接在哪里、其他工具是怎么分类的，配上真实的文件。按上面的说明准备好之后，输入：

::: prompt
/harness-rookie-wondering 我读完了“MCP server：接工具的标准接口”这一章。请教我这个 harness 里的三类工具，以及 MCP 放在哪里。带我打开真实的文件，让我看工具名是怎么分到各类里的。
:::

它一次只教一小块，停下来确认你跟上了，再和你一起打开文件。
