读这一章，需要你读过[别跟风瞎用子 Agent](2-3-subagents.html)，或者至少知道什么是子 agent。

## 一句话 {#in-one-sentence}

只有在必须换模型、或者缩小工具范围时，才去建自定义 agent。如果要改的只是它知道什么、怎么干活，一个 skill 或一个指令文件就够了。

## 写给管理者 {#for-leaders}

- **要拍板的事**：自定义 agent 只在它改变了别的办法共享不了的东西时才批：它的工具、它的模型，或者一份用来做独立检查的独立上下文。
- **风险**：一个只改了语气和专业知识的角色 agent，不过是多出一个要同步维护的文件，里面却没有一样是平台强制执行的。角色各自作为独立的 agent 运行时，用量也会涨，Anthropic 就测过，他们的多 agent 研究系统用的 token 约是聊天的 15 倍。
- **做对的代价**：每一个真实的限制对应一个 agent 文件，像任何规则一样通过代码审查来改。我的配置里只留了一个只读的帮手和一个检查者。
- **可以问团队**：“这个 agent 文件里列了工具或模型吗？如果没有，为什么它不是一个 skill？”

## 想要一个不一样的 agent，到底要搭什么？ {#problem}

[别跟风瞎用子 Agent](2-3-subagents.html)问的是，要不要把工作分给多个 agent。真想要一个不一样的 agent 时，很多配置接下来的做法是搭角色，“SQL 专家”“代码 reviewer”“文档撰写者”，每个都是一个 agent 文件，让人觉得是在整理。可这到底算不算整理，得先弄清这种文件是什么。**自定义 agent** 是为 agent 定义一个角色的文件，在 VS Code Copilot 里就是以 `.agent.md` 结尾的文件：上面一小段头部（名字、描述、设置），下面一段正文指令。和它相对的是**默认 agent**，也就是你什么都不选时，与你对话的那个普通 agent。

可是再看看这种文件里装的是什么，你会发现大部分内容，其实都可以用别的办法交给默认 agent。说白了，一个只是换了语气、加了点专业知识的角色，就是戏服：它多出一样要维护的东西，里面却没有一样是平台强制执行的。那么，除了戏服，文件里还有什么？

## agent 文件里，哪些东西不只是戏服？ {#how-it-works}

### agent 文件里有什么

这个答案，要从头部找起，因为设置都在那里。按 VS Code 的文档和我自己的文件来看，要紧的只有几项。

名字和描述是写给调用方看的。描述告诉模型什么时候该调用这个 agent，所以里面要说清这个 agent 是做什么的、需要被告知什么。子 agent 从空白的上下文开始（[别跟风瞎用子 Agent](2-3-subagents.html)），调用消息一含糊，它就无从下手。

其余的设置，决定这个 agent 用什么干活、谁可以调用它。头部如果给了一份工具清单，这个 agent 就只有清单上的工具。模型是可选的，也可以是一份按偏好排序的列表，第一个用不了，就试下一个。谁可以调用它，由两个设置来管，作用各不相同。`user-invocable: false` 让这个 agent 不出现在下拉列表里（VS Code 文档叫它选择器里的可见性）；另一个单独的设置 `disable-model-invocation`，管的是模型能不能把它当子 agent 调用。它们各有拦不住的调用，见后面的“隐藏不等于禁止”。

头部下面的正文就是文本，写的是这个角色是干什么的、怎么干、不能做什么、交回什么。

### 只有 agent 文件才能做到的

::: figure 2-4-what-differs

把这些设置并排放在一起，一项一项地问：这样东西，默认 agent 能不能用别的办法拿到？

知道什么、怎么干活，这些默认 agent 都能拿到。指令文件和 skill 对任何 agent 都有效，所以 SQL 风格指南、检查清单、这里的命名方式，都可以放进 skill 或指令文件（[规则写太多，Agent 反而记不住](3-3-instructions-and-skills.html)）。这样默认 agent 就能干这份活，用不着新的 agent。

工具就不一样了，它没法用别的办法给。一个 agent 有的就是它的文件里列出的那些工具，平台会强制执行这份清单，所以没有编辑工具的 agent，无论你怎么要求，都编辑不了。而写在文件正文里的规则，比如“不要改文件”，就没有这样的效力。它和别的规则一样，只是请求。

同样，模型也只能在 agent 文件里定，不管是给简单的活配一个便宜的模型，还是给难的思考配一个强的。人可以在下拉列表里切换默认 agent 的模型，但子 agent 的模型是在它的文件里设的。

工具和模型都写在文件里。独立的上下文不一样，它根本不写在文件里。作为子 agent 运行时，它从空白的上下文开始，只有它的报告会回来，这来自“作为子 agent 运行”这件事，而不是文件里写了什么。想要独立检查时，这是搭一个的理由，[别跟风瞎用子 Agent](2-3-subagents.html)讲的就是这种情况。

所以我用的规则很短。**这几样里至少有一样没法共享时，才建自定义 agent：工具不同、模型不同，或者你需要一份不能让它看到调用方推理过程的上下文**。其他情况，都用默认 agent，把专业知识写下来。

有一个快速的检验，能让这条规则更好用。如果你能把它说成“做 X 的时候，这样做”，它就是 skill；如果你能把它说成“这份活不能有工具 Y”或者“这份活要用模型 Z 来跑”，它就是 agent。真要加一个之前，我还是会问两个问题：它防的是哪种故障？默认 agent 为什么做不到同样的事？

VS Code 的上下文工程指南也是这样划线的。它把 agent 用在“遵循多轮流程、使用特定工具的 workflow”上，它的示例规划 agent 正好符合这一点：那份简短的只读工具清单是限制，那条不要去实现的指令是请求。

### 一个例子：reviewer

在我的配置里，有一个自定义 agent 是我最想留下的，那就是 reviewer。它是一个只看需求和结果的检查者，下面是它文件的开头：

::: code harness .github/agents/reviewer.agent.md L1-L8 "reviewer 的头部：tools 那一行是限制，model 那一行是备选列表，description 是对调用它的模型的请求。"

`tools` 那一行给了它读、搜索和运行命令的工具，却没有改文件的，所以它没法“顺手修一下”。`agents: []` 表示它不能再启动别的子 agent，模型则是一份备选列表。（每一项选择的理由，在[别跟风瞎用子 Agent](2-3-subagents.html)里。）这里要紧的是，头部里每一行会改变行为的，要么是工具限制，要么是模型，要么是上下文的边界。相比之下，描述只是在请求，正文则主要说该看什么、该交回什么。

不过，我碰到的事并不都这么干净利落。

### 我踩过的三个坑

第一个坑是，“隐藏”不等于“禁止”。让一个 agent 不出现在下拉列表里的设置，拦不住另一个 agent 把它当子 agent 来调用；让模型不去使用它的那个设置，同样拦不住。如果“谁可以调用谁”很要紧，就得由 hook 来决定（[硬性规则放在哪？用 hook](2-2-hooks.html)），不能靠这两个设置。

可 hook 自己也有盲区：它看不到当前是哪个 agent。hook 收到的事件里没有主 agent 的名字（[硬性规则放在哪？用 hook](2-2-hooks.html)），所以权限不能交给“admin agent”：任何 agent 都可以冒充它。权限只能跟着会话走，比如在我的配置里，admin 开关是由人在终端里打开的（[别让 Agent 改自己的规则](4-3-guardrails.html)）。我曾经有过一个 admin agent，后来撤掉了。

最后一个坑是，检查可能被悄悄跳过：子 agent 的模型比主模型高一个级别时，平台不会运行它，也不吭声。这种情况我只见过一次，可正因为它一声不吭，“检查到底有没有发生”，必须由模型之外的东西来确认，比如一个把 reviewer 的回答存到磁盘上的 hook。

### 测一测你自己的配置

现在回到那条规则，拿它来测一测你自己的角色 agent。挑你有的一个，比如“SQL 专家”或“文档撰写者”，看它的文件里有没有列工具或模型。都没有的话，把它的正文挪进一个 skill（[规则写太多，Agent 反而记不住](3-3-instructions-and-skills.html)），再把同一个任务交给默认 agent，一次带这个 skill，一次不带，对比一下。如果看不出差别，这个 agent 就是戏服；不过每种都多跑几次，再相信你看到的。

## 多留一个 agent 要付出什么 {#costs-and-traps}

最直接的代价是维护。每个文件里都有模型名、工具清单和一段会过期的正文。就拿模型名来说，它会变，而和下拉列表对不上的名字，会让 agent 坏掉。agent 文件设定的是限制，所以在团队里，它也应该像任何规则一样通过代码审查来改。

还有，切换 agent 可能会丢掉对话。VS Code 文档说，选定的 agent 会作用于你的请求，直到你切换为止；至于单纯切换一次之后对话历史会怎么样，文档没有说，所以要紧的东西，放在文件里（[对话越久，Agent 越笨](3-2-long-sessions.html)）。

最后是用量。算下来，你需要的角色其实比你以为的少。每个作为独立 agent 运行的角色，都要自己读、自己写，这些加起来有多少，Anthropic 在他们的研究系统里量过：agent 用的 token 约是聊天的 4 倍，多 agent 系统约是 15 倍（[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)）。在我早期的配置里，我有三个按岗位分工的 agent，一个协调、一个开发、一个检查，最后只留下了检查者，为什么见[别跟风瞎用子 Agent](2-3-subagents.html)。

## 什么时候可以删掉 agent 文件 {#when-to-delete-it}
{status: industry}

只要 agent 文件还强制执行着 skill 做不到的东西，也就是工具清单或模型，它就值得留着。有些平台已经让 skill 带上工具设置。在 Claude Code 里，skill 的 `allowed-tools` 只是预先批准某些工具，并不限制它们；移除工具靠的是另一个单独的设置 `disallowed-tools`，它会在 skill 生效期间把工具拿掉（[Skills](https://code.claude.com/docs/en/skills)）。这样的设置在你的平台上是不是强制执行的，要自己去查，如果是，很多 agent 文件就不再需要了。至于那些内容只是“表现得像 X 领域专家”的 agent，今天就可以删。

## 在你自己的环境里试试 {#try-it}

::: prompt
找出这个项目里每一个自定义 agent 文件。每一个，报告：它的头部是限制了工具、设置了模型，还是都没有；描述写得是否让调用方知道什么时候该用、该说什么；以及正文里哪些行只是请求。把没有工具限制、也没有模型设置的 agent，都标为疑似戏服，并说明哪个 skill 或指令文件可以替代它。不要修改任何文件。
:::

## 延伸阅读 {#go-deeper}

- VS Code 文档：[Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- VS Code 文档：[Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- Anthropic：[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [规则写太多，Agent 反而记不住](3-3-instructions-and-skills.html)：改变 agent 行为的另一条路

## 在 harness 里探索 {#explore}

harness 里的自定义 agent 是特意只留了很小的一组：一个只读的帮手和一个检查者。你可以打开这两个文件，把每一行和上面的表对照。

::: prompt
/harness-rookie-wondering 我读完了“自定义 agent”这一章。请教我这个 harness 的 agent 文件里有什么：工具清单、模型列表，以及哪些行会改变行为、哪些只是请求。带我打开真实的文件，并让我看看为什么 agent 这么少。
:::
