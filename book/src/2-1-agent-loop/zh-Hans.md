读这一章，只需要你用过写代码的 AI agent，比如 Copilot 的 agent 模式。

## 一句话 {#in-one-sentence}

agent 就是一个循环：模型决定要做什么，外面的程序替它做，结果回到模型面前，模型再决定下一步。这个循环上有四个地方可以改，agent 出错时先判断该改哪一处，再考虑换模型或者加 prompt。

## 写给管理者 {#for-leaders}

- **要拍板的事**：agent 出了问题，先问该改四个地方里的哪一个（它读什么、有哪些工具、调用之前的检查、调用之后的检查），再考虑换更贵的模型或者写更长的 prompt。
- **风险**：循环本身很少出问题，出问题的通常是它周围这四样。写在 prompt 里的规则只是请求，模型不一定照做；循环什么时候停，看的是模型还要不要工具，不看活有没有真的做完，所以 agent 说“做完了”不能直接当真。
- **做对的代价**：主要是配置的时间。最便宜的是改 agent 读什么，写几行规则就够；调用前后的检查是代码，要有人维护。
- **可以问团队**：“上一次结果不好，我们修的是上下文、工具清单，还是加了一道模型之外的检查？”

## agent 出错，别急着怪模型 {#problem}

agent 犯错的时候，人会觉得是背后的大模型出了错，于是就继续在 prompt 里加很多句子去规避这种风险，比如“小心”“不要做 XX”，或者换一个更聪明的模型，比如从 Sonnet 换到 Opus，把 thinking effort 开到最高。这些有的时候管用，但是这并不是根因，因为 agent 最后做出什么事，不光看模型，还要看模型读到了什么、手里有哪些工具、调用工具的前后有没有检查，这些都在模型外面，换一个模型也改变不了。

AI agent 其实包括两部分：模型（LLM）和工具（Tool Calling）。用户发出 prompt，模型进行思考，但是模型本身就是一个大脑，它没有手，那它怎么来触碰你的本地系统呢（比如查文件、改文件、运行一个终端命令、访问浏览器，或者直接进行 Computer Use 来全程操作你的电脑）？这就是靠 Tool Calling。模型思考以后决定要做什么操作，通过提供给它的工具接口发出调用，外面的程序（Claude Code、Copilot 的 agent 模式都是这样的程序）真正去运行，返回一个结果作为下一段输入，模型拿到以后就继续思考，决定下一步是继续调用工具，还是认为任务已经完成，然后返回给用户一段结果，这就是你看到的答案。

上面这个流程，就是我们所谓的 **Agent Loop**（循环）。

这个循环上有四个地方可以改：模型读到什么、给它哪些工具、调用工具之前的检查、调用之后的检查。这一章我想教你看懂这个循环，以后 agent 出错时，先判断该改哪一处，再考虑换模型或者加 prompt。

## 循环怎么转，四个地方怎么改 {#how-it-works}

::: figure 2-1-loop

### 每一轮，模型都要重新读一遍 prompt

绕循环走一圈，这本书叫一**轮**：程序把 prompt 拼好发给模型，模型写回一段文本，可能还带着一个或几个工具调用，程序运行这些工具、记下结果，再决定要不要继续。VS Code 团队讲 Copilot 的循环时也是这么分的，他们叫 round，并且说 prompt 在每一轮都重新构建一次（[The Coding Harness Behind GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode)）。模型在两轮之间什么都不记得，这一轮的 prompt 里没有的东西，对它来说就不存在，所以系统指令、规则、你说的话、之前每一轮的工具调用和结果，每一轮都要重新放进去。读文档的时候要注意，Claude Code 和 Copilot 的文档说 turn，一般指你发一条消息到它给出回答这一整段，里面可以有很多轮。

从这个过程能得出两件事。第一，agent 的每个动作都是一次工具调用，模型没有别的办法做事，而工具是模型外面的程序运行的，所以运行之前可以拦下来。**hook** 就放在这个位置，它是你写的一个小程序，平台在固定的时机运行它，比如每次工具调用之前和之后（[硬性规则放在哪？用 hook](2-2-hooks.html)）。第二，模型只看得到 prompt 里的文本，你的屏幕、你的磁盘它都看不到，它以为项目是什么样子，全看上下文里写了什么，而上下文有大小上限（[为什么不能把所有规则都塞给 Agent？](3-1-context-budget.html)）。

hook 能不能管住所有调用，要看平台。Claude Code 的文档写明了，子 agent 里的工具调用和 MCP 工具都会触发同样的 hook（[Hooks reference](https://code.claude.com/docs/en/hooks)）。Copilot 的文档只说子 agent 里触发的 hook 输入会多几个字段，列出来的工具名都是内置工具，没有提 MCP（[GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference)），我在 Copilot 上见过内置工具和子 agent 的调用都经过 hook，MCP 工具没有测过。另外有两样东西不走这条路。一样是服务端工具，它们在提供方那边运行，中间没有你的代码（[Agent 用不好工具，先看工具的描述和报错](1-2-tool-calling.html)）。另一样是 Claude Code 里用 `@` 引用的文件，默认直接放进上下文，不经过工具调用，所以拦读文件的 hook 不会触发。

### 模型不再要工具，循环就停了

循环正常结束的条件只有一个：模型这一轮没有要工具。在 Anthropic 的 API 上，只要 `stop_reason` 是 `tool_use` 就接着转，模型写完回答，`stop_reason` 变成 `end_turn`，循环就退出（[How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)）。Copilot 也一样，这一轮没有工具调用，这段文本就是最后的回答。所以循环停下来，只说明模型觉得做完了，不说明活真的做完了，中间没有任何东西替你检查过结果。

另外两种停法不是模型决定的。一种是你自己按停止，VS Code 的文档说得很清楚，停止不会撤销已经做完的动作，也不会撤销对外部服务的改动（[Build with AI in VS Code](https://code.visualstudio.com/docs/agents/overview)）。另一种是平台的上限，VS Code 的 `chat.agent.maxRequests` 限制 agent 能发多少次请求，默认是 25（[AI settings reference](https://code.visualstudio.com/docs/agents/reference/ai-settings)）。

还有一种情况正好相反，模型想停，被挡了回去。Copilot 的 `agentStop` 和 Claude Code 的 `Stop` 是模型写完回答时运行的 hook，它可以返回 `block` 和一个原因，这个原因会当作新的 prompt 送回模型，循环就接着转。这个位置很有用，模型说做完了，hook 可以去看待办清单或者跑一遍测试，没通过就说“还没完，第 4 步没做”，agent 不用你守着也能把一长串清单做完（[别跟风瞎用子 Agent](2-3-subagents.html)）。代价是它可能一直停不下来，而每转一轮都要花钱，所以 Copilot CLI 和 Claude Code 都设了保险，连续挡 8 次以后强制结束，hook 自己也能从 `stop_hook_active` 这个字段看出，这一轮已经是被挡回来的（[GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference)、[Hooks reference](https://code.claude.com/docs/en/hooks)）。

### 循环上有四个地方可以改

模型怎么思考你改变不了，你能改的是它周围的四样东西。

1. **它读什么**。规则文件、skill、你指给它看的文件，都是放进上下文的文本，这是用得最多、也最便宜的办法，写几行规则就能告诉它自己猜不到的事（[规则写太多，Agent 反而记不住](3-3-instructions-and-skills.html)）。短板是这些文本只是请求，模型可能不照做，而且对话长了，VS Code 和 Claude Code 都会把前面的内容压缩成摘要，早期的细节和指令可能就丢了。
2. **有哪些工具**。模型只能调用给了它的工具，工具的描述和报错也是它了解工具的唯一途径（[Agent 用不好工具，先看工具的描述和报错](1-2-tool-calling.html)）。想给一个角色固定一份更短的工具清单，就用自定义 agent（[什么时候才需要自定义 Agent？](2-4-custom-agents.html)）。短板是工具的能力常常比名字大，你拿掉了改文件的工具，只要还留着终端，它照样可以用命令改文件。
3. **调用之前的检查**。工具运行之前，hook 能看到工具名和参数，可以放行，也可以拒绝并说明原因，原因会送回给模型。hook 是平台运行的，模型跳不过去，所以这里的规则是会运行的代码，不是请求。用代码守规则也不只有 hook 这一种，工具清单、自查用的命令都算，只是覆盖的范围更窄（[为什么 Agent 不听 prompt 里的规则？](4-1-requests-and-rules.html)）。平台自带的审批规则也在这个位置，比如 VS Code 按命令文本匹配的自动批准规则。短板是它看到的只是调用的文本，命令运行起来做了什么它看不到，VS Code 的文档也说 hook 不能替代强制执行的权限、沙箱或者企业管控（[Security](https://code.visualstudio.com/docs/agents/run/security)）。
4. **调用之后的检查**。工具运行之后，hook 能看到结果，可以留一条记录，可以给模型加一段话，Copilot 和 Claude Code 还能改写模型读到的结果。短板是已经发生的事它撤销不了，VS Code 的文档也是这么写的（[Hooks](https://code.visualstudio.com/docs/agent-customization/hooks)），所以要挡住的动作只能放在调用之前。

这四处里，第 1、4 处改变模型知道什么，第 2、3 处改变它能做什么。只写在规则文件里的东西，改变的只是它知道什么。

沙箱是另一类，它不看调用，限制的是命令运行起来以后能碰什么，所以我没把它算进这四样（[不要开放全部的权限或使用沙箱](4-5-least-privilege.html)）。

### 常见的错，先看该改哪一处

循环本身很少出问题，Anthropic 的文档说它的标准写法就是一个按 `stop_reason` 判断的 `while` 循环，没几行代码。出问题的基本都在上面这四处。下面这张表是我自己用 agent 时攒下来的，记的是我见过的情况，不是统计数据。

| 你看到的 | 通常的原因 | 先改哪里 |
| --- | --- | --- |
| 它改了不该改的 | 它想的是怎么把活干完，不是被不被允许 | 调用之前的检查，或者收紧工具清单 |
| 它忘了前面说过的事 | 上下文被压缩了，或者对话太长了 | 它读什么：要紧的东西放进文件，不留在对话里（[对话越久，Agent 越笨](3-2-long-sessions.html)） |
| 它检查自己的活，说没问题 | 同一个模型、同样的推理，有同样的盲区 | 换一个视角来查：另一个 agent 或者一条命令（[别跟风瞎用子 Agent](2-3-subagents.html)） |
| 它不停重试一个被拒绝的操作 | 它想把任务做完 | 拒绝的原因写清楚该改做什么（[“先问我”为什么挡不住 Agent？](4-2-ask-vs-refuse.html)） |
| 它说“做完了”，其实没有 | 循环只看模型还要不要工具，模型又倾向于报告成功 | 停止时的检查，让它自己跑测试（[让 Agent 自己跑测试](5-4-self-checks.html)） |

第三条和最后一条不只是我见过，Anthropic 也写过。他们发现 agent 给自己的活打分时总是偏高，质量一般也会很有信心地夸（[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)），Claude 也有没好好测就把功能标成完成的倾向（[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)）。这几条的原因很少是模型不够聪明，所以换模型要放到这些都查过以后（[选模型，别只看 token 单价](1-1-models-and-cost.html)）。

### 自己看一次循环怎么转

想亲眼看循环怎么转，什么都不用装。在 agent 的对话里问一句“读一下 README，告诉我这个项目是做什么的”，回答出来之前你会看到一行类似“Read README.md”的字，这就是一次工具调用，VS Code 默认把细节折叠起来，展开就能看到它的输入和输出（[Use tools with agents](https://code.visualstudio.com/docs/agents/run/tools)）。再问一个要读三个文件的问题，你会看到三个调用，它们可能挤在同一轮里，这些结果现在都留在上下文里了。想看模型每次到底收到了什么，在 VS Code 里运行 **Developer: Show Chat Debug View**，它按每次模型交互列出系统提示、prompt、上下文、回答和工具的输入输出，一次一次翻过去，就能看到每一轮多了什么（[Debug chat interactions](https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view)）。这个视图里有你的代码和文件路径，分享之前要先看一遍。

## 循环越转越贵，而且它不是一份计划 {#costs-and-traps}

循环的钱主要花在重读上。每转一轮，模型都要把整个上下文再读一遍，里面还多了上一轮的结果，所以读的量比轮数涨得快，用[选模型，别只看 token 单价](1-1-models-and-cost.html)那个算例的数字，10 轮一共读 325,000 个 token，20 轮就是 1,150,000 个，约 3.5 倍。prompt 缓存能让重读便宜很多，Anthropic 读缓存的价格在大多数模型上是输入价的十分之一，在 Opus 5.5 和 Sonnet 5.5 上是二十分之一（[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)），但是缓存省的只是钱，这些内容照样占着上下文窗口，照样分走模型的注意力，Anthropic 说上下文是“边际收益递减的有限资源”（[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)）。

这段文本里最少有人盯着的是工具结果。prompt 是你写的，里面有什么你心里有数，可是 agent 读的文件、命令打印的日志，你可能从来没见过，它们照样占着窗口，模型也可能照着里面的文字去行动（[Agent 读到的网页和文件，可能在给它下命令](4-6-untrusted-input.html)）。它们能占多少，Anthropic 有一个数，在一个 100 轮的网页搜索评测里，快到上限时自动清掉过期的工具结果，token 用量降了 84%（[Managing context on the Claude Developer Platform](https://claude.com/blog/context-management)）。

让模型自己决定下一步，本身也有代价。Anthropic 说 agent 是拿延迟和成本去换更好的任务表现，建议先找最简单的办法，需要时才增加复杂度（[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)）。如果一件事的步骤从来不变，一个在固定位置调用模型的脚本可能比 agent 更适合你，它更便宜，也更好预测。

还有一个坑是把循环当成一份计划。模型不是先想好整条路再照着走，它每一轮根据这一轮的 prompt 决定下一步，就算它一开始写了一份计划，那也只是上下文里的一段文本。所以它走上错路，通常是前面某一轮的结果把它带过去的，而那个结果还留在上下文里，后面每一轮都会再读到。

## 平台自带了，就可以删掉自己的 hook {#when-to-delete-it}
{status: industry}

只要 agent 还是靠调用工具来工作，这个循环和这四个地方就不会过时，会过时的是我自己写的那部分。我今天用 hook 挡调用、催 agent 接着做，是因为平台留给我的就是这些位置，如果平台提供了原生的办法来强制执行规则、预算或者停止条件，我会改用它，不再用自己的 hook。这件事已经开始了，VS Code 的 Autopilot 会批准所有工具，并且推着 agent 一直做到任务完成，打开 `chat.autopilot.advanced.enabled` 以后，还会由另一个模型来判断请求完成了没有（[Security](https://code.visualstudio.com/docs/agents/run/security)、[AI settings reference](https://code.visualstudio.com/docs/agents/reference/ai-settings)），Claude Code 的 `/goal` 就是一个内置的停止 hook（[Hooks reference](https://code.claude.com/docs/en/hooks)）。

## 在你自己的环境里试试 {#try-it}

::: prompt
读这个项目的指令文件和设置。你找到的每条规则或限制，告诉我它在四个地方里的哪一个起作用：agent 读什么、有哪些工具、工具调用前的检查、工具调用后的检查。把只是写下来的请求、没有模型之外的东西来强制执行的规则，每一条都标出来。列出五条一旦被破坏影响最大的规则。不要修改任何文件。
:::

## 延伸阅读 {#go-deeper}

- Anthropic：[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，它把 agent 定义为“在循环里自主使用工具的 LLM”
- Anthropic：[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)，讲什么时候固定的 workflow 就够了
- Anthropic 文档：[How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)，循环的标准写法
- VS Code 博客：[The Coding Harness Behind GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode)
- Claude Code 文档：[How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- VS Code 文档：[Set up a context engineering flow in VS Code](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)

## 在 harness 里探索 {#explore}

循环在哪里都一样，但是在我的 harness 里，你可以从旁边看每一轮往上下文里放了什么，hook 看到了哪次调用、回答了什么。

::: prompt
/harness-rookie-wondering 我读完了“Agent 到底是怎么干活的？”这一章。请教我这个 harness 是怎么站在循环的四个地方的：它往上下文里放了什么、允许哪些工具，以及它的 hook 在调用前后做什么。带我打开真实的文件，并画出一轮是怎么穿过它们的。
:::
