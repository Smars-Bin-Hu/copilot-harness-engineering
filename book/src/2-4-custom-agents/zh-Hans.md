读这一章，需要你读过[慎用子 agent](2-3-subagents.html)，或者至少知道什么是子 agent。

## 一句话 {#in-one-sentence}

只有在必须换模型、或者缩小工具范围时，才去建自定义 agent。要改的是它知道什么、怎么干活，一个 skill 或一个指令文件就够了。

## 写给管理者 {#for-leaders}

- **要拍板的事**：自定义 agent 只在它改变了别的办法共享不了的东西时才批：它的工具、它的模型，或者一份不能让它看到调用方推理过程的上下文。
- **风险**：一个只是换了语气、加了点专业知识的角色，是戏服：多一个要同步维护的文件，平台并不强制执行它。在我早期的配置里，三个按岗位分工的 agent，在四个小任务上（每个只跑了一次），用量约是一个 agent 的 4.5 倍，结果并没有更好。
- **做对的代价**：每一个真实的限制，对应一个 agent 文件，像任何规则一样通过代码审查来改。我的配置里只留了一个只读的帮手和一个检查者。
- **可以问团队**：“这个 agent 文件里列了工具或模型吗？如果没有，为什么它不是一个 skill？”

## 问题 {#problem}

[慎用子 agent](2-3-subagents.html)问的是，要不要把工作分给多个 agent。这一章问的是一个更小的问题：你想要一个不一样的 agent 时，到底要搭什么？

很多配置一上来就搭角色：“SQL 专家”“代码 reviewer”“文档撰写者”，每个都是一个 agent 文件。这让人觉得井井有条。但看看 agent 文件里装的是什么，你会发现大部分内容，都可以用别的办法交给默认的 agent。一个只是换了语气、加了点专业知识的角色，就是戏服。它多出一样要维护的东西，却没有任何平台强制执行的内容。

先说两个词。

- **自定义 agent** 是为 agent 定义一个角色的文件。在 VS Code Copilot 里，它是以 `.agent.md` 结尾的文件。它有一小段头部（名字、描述、设置）和一段正文指令。
- **默认 agent** 是你什么都不选时，与你对话的那个普通 agent。

## 原理 {#how-it-works}

### agent 文件里有什么

头部有几项设置。下面这些是要紧的，来自 VS Code 的文档和我自己的文件：

- **名字和描述**。描述告诉模型什么时候该调用这个 agent。要写给调用方看：说明这个 agent 是做什么的，需要被告知什么。子 agent 从空白的上下文开始（[慎用子 agent](2-3-subagents.html)），所以含糊的调用消息，让它无从下手。
- **工具清单**。文件里给了清单，这个 agent 就只有清单上的工具。
- **模型**，可选。它可以是一份按偏好排序的列表：第一个用不了，就试下一个。
- **谁可以调用它**。有两个设置，作用不同。`user-invocable: false` 让这个 agent 不出现在下拉列表里（VS Code 文档叫它选择器里的可见性）。另一个单独的设置 `disable-model-invocation`，管的是模型能不能把它当子 agent 调用。见下面的“隐藏不等于禁止”。

正文是文本：这个角色是干什么的、怎么干、不能做什么、交回什么。

### 只有 agent 文件才能做到的

::: figure 2-4-what-differs

把这些设置并排放在一起，然后问：哪些东西，我可以用别的办法交给默认 agent？

- **怎么干活、知道什么**。指令文件和 skill 对任何 agent 都有效。SQL 风格指南、检查清单、这里的命名方式：放进 skill 或指令文件（[指令与 skill：只加载需要的](3-3-instructions-and-skills.html)）。这样默认 agent 就能干这份活，不需要新的 agent。
- **有哪些工具**。这没法用别的办法给。一个 agent 有它的文件里列出的那些工具，平台会强制执行这份清单。没有编辑工具的 agent，无论你怎么要求，都编辑不了。这是 agent 文件能给你的硬性限制。（写在文件正文里的规则，比如“不要改文件”，和别的规则一样是请求。）
- **用哪个模型**。同样只有 agent 文件能做到。简单的活用便宜的模型，难的思考用强的。人可以在下拉列表里切换默认 agent 的模型，但子 agent 的模型是在它的文件里设的。
- **独立的上下文**。作为子 agent 运行时，它从空白的上下文开始，只有它的报告会回来。这不是文件的属性，而是子 agent 这个身份的属性。想要独立检查时，这是搭一个的理由，[慎用子 agent](2-3-subagents.html)讲了这一点。

所以我用的规则很短。**这几样里至少有一样没法共享时，才建自定义 agent：工具不同、模型不同，或者你需要一份不能让它看到调用方推理过程的上下文。** 其他情况，都用默认 agent，把专业知识写下来。一个快速的检验：如果你能把它说成“做 X 的时候，这样做”，它就是 skill。如果你能把它说成“这份活不能有工具 Y”或者“这份活要用模型 Z 来跑”，它就是 agent。

加一个之前，我问两个问题：它防的是哪种故障？默认 agent 为什么做不到同样的事？

VS Code 的上下文工程指南把 agent 用在“遵循多轮流程、使用特定工具的 workflow”上，它的示例规划 agent 有一份简短的只读工具清单，和一条不要去实现的指令。这是同样的形状：工具清单是限制，指令是请求。

### 一个例子：reviewer

在我的配置里，有一个自定义 agent，是我比其他所有都更想保留的：reviewer。它是一个检查者，只看需求和结果。下面是它文件的开头：

::: code harness .github/agents/reviewer.agent.md L1-L8 "reviewer 的头部：tools 那一行是限制，model 那一行是备选列表，description 是对调用它的模型的请求。"

`tools` 那一行给了它读、搜索和运行命令的工具，没有改文件的。所以它没法“顺手修一下”。`agents: []` 表示它不能再启动别的子 agent。模型是一份备选列表，第一个用不了，就用下一个。每一项选择的理由，在[慎用子 agent](2-3-subagents.html)里。这里要紧的是：头部里每一行会改变行为的，要么是工具限制，要么是模型，要么是上下文的边界。描述只是在请求。正文主要说该看什么、该交回什么。

### 我踩过的三个坑

**“隐藏”不等于“禁止”**。让一个 agent 不出现在下拉列表里的设置，拦不住另一个 agent 把它当子 agent 来调用。让模型不去使用它的那个设置，也拦不住。如果“谁可以调用谁”很要紧，要由 hook 来决定（[Hook：每次调用都会经过的执行点](2-2-hooks.html)），不能靠这两个设置。

**hook 看不到当前是哪个 agent**。hook 收到的事件里，没有主 agent 的名字（[Hook：每次调用都会经过的执行点](2-2-hooks.html)），所以不能把权限交给“admin agent”：任何 agent 都可以冒充它。权限只能跟着会话走，比如在我的配置里，admin 开关是由人在终端里打开的（[保护规则本身的文件](4-3-guardrails.html)）。我曾经有过一个 admin agent，后来撤掉了。

**比调用方更高一级的模型，可能被悄悄跳过**。这个我见过一次，之后没再测过：当子 agent 的模型比主模型高一个级别时，平台不会运行它，也不吭声。所以“检查到底有没有发生”，必须由模型之外的东西来确认，比如一个把 reviewer 的回答存到磁盘上的 hook。一道检查如果对你要紧，就留一份它运行过的记录。

### 测一测你自己的配置

拿你有的一个角色 agent（“SQL 专家”“文档撰写者”）。它的文件里列了工具或模型吗？都没有的话，把它的正文挪进一个 skill（[指令与 skill：只加载需要的](3-3-instructions-and-skills.html)），把同一个任务交给默认 agent，一次带这个 skill，一次不带，对比一下。如果看不出差别，这个 agent 就是戏服。每种多跑几次，再相信你看到的。

## 代价和坑 {#costs-and-traps}

**agent 越多，要同步维护的越多**。每个文件里都有模型名、工具清单和一段会过期的正文。模型名会变。和下拉列表对不上的名字，会让 agent 坏掉。agent 文件设定的是限制，所以在团队里，像任何规则一样通过代码审查来改。

**切换可能丢掉对话**。VS Code 文档说，选定的 agent 会作用于你的请求，直到你切换。对于一次单纯的切换，对话历史会怎么样，文档没有说，我也没测过。要紧的东西放在文件里（[长对话会变差](3-2-long-sessions.html)）。

**角色可能让人觉得是限制，其实只是请求**。正文写着“不要做 X”，agent 照样做了 X。只有工具清单才是限制。

**角色比你以为的要少**。在我早期的配置里，我有三个按岗位分工的 agent（一个协调、一个开发、一个检查）。在四个小任务上，它们的用量约是一个 agent 的 4.5 倍，结果并没有更好（[慎用子 agent](2-3-subagents.html)）。我只留下了检查者。那是四个任务、每个一次：是薄弱的证据，不是结果。Anthropic 在另一个量级上报告了同样的方向：在他们的研究系统里，agent 用的 token 约是聊天的 4 倍，多 agent 系统约是 15 倍（[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)）。我的数字和他们的，衡量的是不同的东西，所以只比较方向。

## 什么时候可以删掉 {#when-to-delete-it}
{status: industry}

只要 agent 文件强制执行了 skill 做不到的东西：工具清单或模型，它就留着。有些平台已经让 skill 带上工具设置。在 Claude Code 里，skill 的 `allowed-tools` 只是预先批准某些工具，并不限制，而另一个单独的 `disallowed-tools`，会在 skill 生效期间移除工具（[Skills](https://code.claude.com/docs/en/skills)）。这样的设置在你的平台上是不是强制执行的，要自己去查。如果是，很多 agent 文件就不再需要了。而任何内容只是“表现得像 X 领域专家”的 agent，今天就可以删。

## 在你自己的环境里试试 {#try-it}

不用装 harness。在你自己的仓库里打开 agent，粘贴：

::: prompt
找出这个项目里每一个自定义 agent 文件。每一个，报告：它的头部是限制了工具、设置了模型，还是都没有；描述写得是否让调用方知道什么时候该用、该说什么；以及正文里哪些行只是请求。把没有工具限制、也没有模型设置的 agent，都标为疑似戏服，并说明哪个 skill 或指令文件可以替代它。不要修改任何文件。
:::

## 延伸阅读 {#go-deeper}

- VS Code 文档：[Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- VS Code 文档：[Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- Anthropic：[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [指令与 skill：只加载需要的](3-3-instructions-and-skills.html)：改变 agent 行为的另一条路

## 在 harness 里探索 {#explore}

harness 里的自定义 agent 特意只有很小的一组：一个只读的帮手和一个检查者。你可以打开这两个文件，把每一行和上面的表对照。按上面的说明准备好之后，输入：

::: prompt
/harness-rookie-wondering 我读完了“自定义 agent”这一章。请教我这个 harness 的 agent 文件里有什么：工具清单、模型列表，以及哪些行会改变行为、哪些只是请求。带我打开真实的文件，并让我看看为什么 agent 这么少。
:::

它一次只教一小块，停下来确认你跟上了，再和你一起打开文件。
