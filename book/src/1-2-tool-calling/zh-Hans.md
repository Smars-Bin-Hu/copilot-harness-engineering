读这一章，只需要知道写代码的 AI agent 能读文件、跑命令。

## 一句话 {#in-one-sentence}

模型只提出工具调用，真正运行工具的是它外面的程序，而模型只能靠工具的名字、描述和报错信息来用工具，所以这些文字写得好不好，决定了工具能不能被用好。

## 写给管理者 {#for-leaders}

- **要拍板的事**：把给 agent 的工具当成产品来做，描述和报错信息都要有人负责；还要决定哪些固定的步骤做成命令，不写进 prompt。
- **风险**：模型只能根据工具的名字和描述去猜，含糊的工具会被用错，或者根本没人用。写在 prompt 里的规则只是请求，而由命令完成的步骤，走这条路径就跳不过去。
- **做对的代价**：重写描述和报错信息花不了多少。命令是代码，要有人维护和测试。
- **可以问团队**：“如果只看每个工具的名字和描述，你能知道什么时候该用它吗？它的报错信息又是怎么说的？”

## 模型自己碰不到你的文件 {#problem}

看着 agent 改文件，你会觉得是模型改的，其实模型只是一个读文本、写文本的程序，它自己打不开文件，也运行不了命令。它能做的是写出一段结构化的请求，意思是“调用工具 `read_file`，路径是 `src/app.py`”，这就是一次**工具调用**（tool call）。模型外面的程序（[什么是 Harness Engineering？](0-1-the-gap-and-the-map.html)里第一种意思的 harness）读到这个请求，真的去读文件，再把读到的内容作为**工具结果**放回对话，模型读完再决定下一步。读文件、搜索、改文件、运行命令、抓取网页，这些 agent 能要求做的动作都叫**工具**。

这件事有两个后果。第一，agent 的每个动作都要经过一次调用，而调用是在模型外面执行的，所以程序可以检查、拒绝或者修改它，这是你能对 agent 强制执行规则的基础。第二，模型用工具的时候，手里只有工具的名字、描述和参数列表，它不是一个看过文档、能问同事的程序员，而是一个靠这几行字来猜的用户，所以这几行字写得好不好，直接决定工具能不能被用好。

### 一次来回

::: figure 1-2-tool-call

以 Anthropic 的 API 为例，模型要用工具时，回复的 `stop_reason` 是 `tool_use`，里面带着写明工具名和参数的 `tool_use` 块，你的代码运行这个工具，再用 `tool_result` 块把结果送回去（[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)）。这种在你这边运行的叫客户端工具，编辑器里的 agent 做的大部分事都是这样在你的机器上运行的。还有一类**服务端工具**，比如 Anthropic 的 `web_search`，是在提供方那边运行的，结果直接返回，中间没有你的代码，所以你没法在它运行之前或之后插手。

## 能在哪里插手，工具又该怎么写 {#how-it-works}

### 你能在哪里插手

用客户端工具的时候，程序夹在请求和动作之间，所以有两个地方可以插手。工具运行之前，程序可以放行、拒绝或者修改这次调用，常用的办法是 hook，拒绝时给出的原因会送回给 agent（[硬性规则放在哪？用 hook](2-2-hooks.html)）。工具运行之后，程序可以在模型读到结果之前，把结果精简、过滤或者补充一下。放在这里的规则是会运行的代码，而写在 prompt 里的规则只是请求（[为什么 Agent 不听 prompt 里的规则？](4-1-requests-and-rules.html)）。但是 hook 只能判断模型已经发出的调用，模型能不能把调用发对，取决于它调用之前看到了什么、调用之后拿回了什么，这两样都是你写的文字。

### 模型只能靠你写的文字来用工具

人用命令行，可以看文档、问同事，还能察觉到哪里不对劲。模型手里只有工具的名字、一段描述和参数列表，它靠这些决定什么时候用，靠上下文去猜参数，工具没告诉它的事它一概不知道，返回的结果它也都当普通文本读，结果有多大，就占掉多少上下文窗口。所以它会猜错，Anthropic 的文档举的例子是，`get_weather` 需要地点，你问“天气怎么样？”却没说在哪，Opus 更可能回头问你，Sonnet 可能自己填一个 New York（[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)）。

反过来，改这几行字的回报很高。Anthropic 说“哪怕对工具描述做很小的改进，也能带来显著的提升”，Claude Sonnet 3.5 在 SWE-bench Verified 评测上拿到当时最好的成绩，就是在精确地改了工具描述之后（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。下面五条规则按一次调用经过的顺序排。

### 1. 描述要写得像给新员工的交接说明

调用之前，描述是模型了解一个工具用途的唯一地方，所以要写清楚这个工具做什么、什么时候用、什么时候不用，写得含糊，工具就会被用错，或者没人用。参数的名字也一样，Anthropic 的例子是别叫 `user`，要叫 `user_id`，因为 `user` 可能是名字，也可能是邮箱或者 ID。如果两个工具看起来很像，每个工具的描述里都要说清它和另一个有什么不同。

### 2. 报错信息要写给 agent 看

调用出了错，模型接下来读到的就是报错。人看到堆栈会停下来想一想，模型是拿到文本就接着往下走，如果报错是 `Error 400`，它就只能猜，往往又猜回同一个错的值，如果报错说明了哪里不对、接下来该试什么，它就能把调用改对。拒绝也一样，要说明应该改做什么（[“先问我”为什么挡不住 Agent？](4-2-ask-vs-refuse.html)）。

### 3. 输出要短，还要能分页

调用成功了，模型读到的是输出。工具返回的所有东西都会放进上下文窗口（[为什么不能把所有规则都塞给 Agent？](3-1-context-budget.html)），而且之后每一轮都要再读一遍（[选模型，别只看 token 单价](1-1-models-and-cost.html)），所以如果 agent 只想要一行，工具却把一个大文件整个返回，不光浪费 token，还可能把有用的东西挤出窗口。办法是给结果设限制，比如默认的上限、分页、范围选择或者过滤器。Claude Code 默认把工具的响应限制在 25,000 个 token 以内，不管上限定在哪里，截短的时候都要说一声，并告诉 agent 怎么缩小查询范围。Anthropic 还有一个做法是加一个 `response_format` 参数，让 agent 自己选简洁还是详细，他们的例子里详细回复是 206 个 token，简洁回复是 72 个，只有三分之一（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。

### 4. 工具少，选得更准

多一个工具不是没坏处。工具只要加载了，它的名字、描述和参数每次调用都要发给模型，工具越多，token 花得越多，选错的机会也越多，功能重叠的时候尤其如此。Claude Code 和 VS Code（Claude Sonnet 4.5、Opus 4.5 以上）默认用工具搜索，一部分工具先不加载，用到时才搜出来，这能省下定义占的 token，但是模型还是要靠名字和描述才搜得到它（[接 MCP server 之前，要想清楚什么？](1-3-mcp.html)）。VS Code 还有一个硬上限，一次请求最多启用 128 个工具，用不上的可以在工具选择器里关掉（[Agent tools](https://code.visualstudio.com/docs/copilot/agents/agent-tools)）。所以优先用一小组明显不同的工具，能合并的就合并，Anthropic 的例子是做一个 `search_contacts` 而不是 `list_contacts`，做一个 `schedule_event` 把查空闲和建日程合在一起。工具很多的时候，把相关的工具归到同一个名字前缀下也能帮 agent 分清楚，不过前缀和后缀哪种好，Anthropic 说不同模型效果不一样，要用自己的评测来定（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。

### 5. 固定的步骤做成命令，不写进 prompt

这是五条里我最想强调的一条。有些活的步骤每次都一样，而且有对错之分，比如给新任务建文件夹、复制文件、算一个哈希、写入记录、写回之前检查一切就绪。你可以把这些步骤写进指令让 agent 照着做，它大多数时候也会照做，但是也可以一次性写成一个**命令**，也就是 agent 当作工具来运行的一个小程序，由命令自己完成这些步骤、检查前置条件，最后返回一个简短的结果。走命令这条路径时，agent 跳不过任何一步，也写不出错误的状态，因为状态根本不是它写的。

::: figure 1-2-prompt-vs-command

这适合不需要判断的步骤，如果某一步需要 agent 拿主意，就把那部分留给它，命令只做周围那些固定的事。我的 harness 就是这么做的，一个命令行工具负责建任务文件夹（[一个任务一个文件夹](5-1-tasks.html)）、取文件、算 diff、统计检查，模型只要运行命令、读结果。进度是最好的例子，任务清单读的是命令写入的数据文件，不是 agent 手写的 Markdown 笔记，因为手写的进度会漏打勾，也会写错。

命令的输出最好能说明下一步做什么，这样 agent 就不用猜了。同一个命令既有人在终端里看，也有脚本通过管道读，所以可以在终端里打印对齐的文本，接到管道上时打印 JSON，两种输出的字段一样。

命令的短板是 agent 真去用它才有用，而且它只守得住经过它的东西，如果 agent 能用别的办法做同样的事，比如手动改文件，命令就只是图个方便，算不上限制（[为什么 Agent 不听 prompt 里的规则？](4-1-requests-and-rules.html)）。

### 怎么检查你自己的工具

对你给 agent 的任何一个工具，先问三个问题。只看名字和描述，你知道什么时候该用、什么时候不该用吗？它失败的时候，信息有没有告诉 agent 接下来做什么？它的输出最大能有多大，如果很大，上下文会怎么样？

最快的实验什么都不用装：让 agent 用一种你明知不对的方式调用你的某个工具，看看返回了什么，假如你就是那个 agent，这条信息能不能让你知道该怎么办，如果不能，要重写的就是这条信息。

如果你自己做工具，Anthropic 的方法是同一个想法的放大版：根据真实的使用场景写出任务，运行它们，读原始记录（调用和结果，不只是最终答案），然后在 agent 出错的地方改描述和报错信息。他们还把这些记录贴给 Claude Code 让它来改工具，文章里的大部分建议就是这么来的（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。

## 好工具也有代价，模型选的参数也不能全信 {#costs-and-traps}

描述写得再好也要花 token，因为工具只要加载了，描述每次调用都要发一遍，所以只写模型选择和使用这个工具需要的内容，长的说明书放进文件里，让 agent 需要时再读。命令的代价不一样，它是要维护的代码，项目一变就可能出错，而且是 prompt 不会有的那种错，所以每个命令都要保持小，并且写测试。

工具调用也不能当成用户的意愿，因为参数是模型选的，而它选之前读到的文本可能来自任何地方（[Agent 读到的网页和文件，可能在给它下命令](4-6-untrusted-input.html)）。Anthropic 的 API 上加 `strict: true` 能保证调用符合工具的 schema，但这只保证格式，值还是模型选的（[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)）。

还有一个很实际的坑，工具名在不同版本之间会变，如果你的规则或 hook 按工具名来匹配，就把这份对应关系放在一个地方，改名时只改一处。

## 模型提供方也把工具的文字当接口 {#industry}
{status: industry}

Anthropic 的两份资料说的是同一件事：工具是一个接口，它的文字也是接口的一部分。讲怎么写工具的那篇把工具设计当成工作的一部分，认为描述和报错信息值得像代码一样测试（[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)）。工具使用文档说客户端工具由你的应用运行，再把结果送回去，还提醒模型“可能会猜出你没提供的值”（[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)）。

## 什么时候可以删掉命令 {#when-to-delete-it}
{status: industry}

最可能过时的是命令，因为检查前置条件的命令是围着模型的弱点搭起来的脚手架，如果模型在遵循多步指令上变得足够可靠，命令也许就不再比一个好的 prompt 强。即便到了那一天，那些每次都必须完全一样、或者需要留下记录的事，我还是会用命令。描述和报错信息的道理不一样，只要模型还在读文本，它就一直成立。

## 在你自己的环境里试试 {#try-it}

::: prompt
找出这个仓库里每一个预期由 agent 运行的工具、命令或脚本（看 agent 文件、脚本、任务运行器和指令文件）。每一个从四方面判断：名字和描述是否说清了什么时候该用、什么时候不该用；报错信息有没有说明接下来做什么；输出最大能有多大；指令里描述的某个固定的多步流程，是否应该改成命令。列出最差的三个，并说明各自怎么修。不要修改任何文件。
:::

## 延伸阅读 {#go-deeper}

- Anthropic：[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Anthropic 文档：[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- VS Code 文档：[Agent tools](https://code.visualstudio.com/docs/copilot/agents/agent-tools)

## 在 harness 里探索 {#explore}

我的 harness 给了 agent 一个命令行工具，用来做那些必须确定的步骤，还有一个守在每次工具调用门口的 hook。harness 可以和你一起打开真实的文件，从内部带你看这两样。

::: prompt
/harness-rookie-wondering 我读完了“Agent 用不好工具，先看工具的描述和报错”这一章。请教我这个 harness 给了 agent 哪些工具：内置的，和它自己的命令行工具。带我打开真实的文件，让我看一次拒绝和它的原因，并画出一次工具调用是怎么走的。
:::
