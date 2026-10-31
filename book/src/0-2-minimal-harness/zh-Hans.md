读这一章，需要你在自己的项目里用过 Copilot 的 agent 模式，并且读过[什么是 Harness Engineering？](0-1-the-gap-and-the-map.html)，或者知道“harness”这个词。

## 一句话 {#in-one-sentence}

先写一页规则，加一个 skill，再写一个拦截危险命令的 hook，别的功能等遇到真实的痛点再加。

## 写给管理者 {#for-leaders}

- **要拍板的事**：先搭最小的一套（一页规则、一个 skill、一个拦截危险命令的 hook），以后每加一样功能，都要说得出它解决的是哪个真实的痛点。
- **风险**：一口气搭出来的大 harness 维护成本高，也说不清哪一部分起了作用。最小的这一套也不是万无一失：规则和 skill 只是请求，模型可以不照做；hook 模型绕不过去，但它只拦得住它认得的命令写法。
- **做对的代价**：如果已经在 VS Code 里打开了项目，一个人大约半小时能搭完。之后团队要像审代码一样审规则文件和 hook 文件。
- **可以问团队**：“我们的配置里，哪些部分来自真实的失败，哪些是从模板抄来的？”

## 不要一开始就想完美 {#problem}

读完上一章的七层架构，很容易让人想一次性搭建全部的功能：任务看板、知识库、human in the loop（review 和 approve）、子 agent、围栏（guardrails）、权限管理、沙箱……你其实不需要一口气吃成个大胖子，我个人的经验是先从一个最小的功能开始迭代，一点点遇到问题或者痛点，再考虑是否要加功能，而且我也遇到过伪需求，比如有一些功能一开始加上去，后面发现是错误的伪需求，所以后面还删除过。

Anthropic 给做 agent 的团队的建议也是这样：“先找尽可能简单的方案，只在需要时才增加复杂度”，而且“只有在它明显改善了结果时”才值得加。（[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)）

总之，跟着这篇文章，先学会搭建一个最小的 demo，然后了解 harness 到底是什么。这篇文章，我想教你先设计一页规则 `.md` 文件，再添加一个 skill，最后写一个 hook，感受一下这三层。如果你已经在 VS Code 里打开了项目，全部搭完大约要半小时。

## 三步搭出最小的一套 {#how-it-works}

::: figure 0-2-grow-by-pain

### 为什么先规则，再 skill，最后 hook

这三样约束 agent 的力度一样比一样紧，搭起来的成本也一样比一样高，所以从最便宜的开始。

常见的规则文件就是 `AGENTS.md`（比如 Codex、Copilot）、`CLAUDE.md`（Claude Code）或者 `.github/copilot-instructions.md`（Copilot），前两个一般在你的项目仓库根目录下创建就好了，第三个放在 `.github/` 文件夹里。规则只要写几分钟，不用写代码，就能告诉 agent 它自己猜不到的事：项目怎么搭、测试怎么跑、什么东西不能碰。每次会话开始，agent 都会自动查找有没有这个文件，如果有的话，就会加载到上下文里。它只是请求，模型可以不理；按我的经验，写下来的东西它大多数时候会照做，但是如果上下文过长，有的时候模型就会忽略一些规则，所以规则文件不能 100% 保证。

skill 是一个文件夹，Copilot 放在 `.github/skills/` 下面，Claude Code 放在 `.claude/skills/` 下面，Codex 放在 `.agents/skills/` 下面，里面有一个 `SKILL.md`，开头写名字和描述，下面写某一类活的具体步骤，比如怎么发版、怎么加一张数据库表。这些长的操作步骤不适合放进规则文件，因为规则文件每次都要整份加载，步骤一多，每次都要为它付 token（[规则写太多，Agent 反而记不住](3-3-instructions-and-skills.html)），放进 skill 以后，agent 平时只看到每个 skill 的名字和描述，需求对得上了才去读全文。它的短板是比规则多了一层不确定：除了同样只是请求，用不用这个 skill 也是 agent 自己判断的，描述写得不好，它就想不起来用。

hook 是平台在固定时机调用的一个你自己写的小程序，比如每次运行工具之前，平台会把这次调用的内容（用哪个工具、参数是什么）交给它，由它决定放行还是拒绝。规则和 skill 都是写给模型看的，模型可以不照做，hook 不一样，做判断的是模型外面的程序，它说不，模型绕不过去，所以那几件绝对不能发生的事要交给它。它放在最后，是因为它是代码，要写、要测、要维护，而且它只看得到这一次调用，看不到命令运行起来之后做了什么（[硬性规则放在哪？用 hook](2-2-hooks.html)），所以只拦得住它认得的写法，同一条命令换一种写法就可能漏过去。

### 第 1 步：写一页规则（约 10 分钟）

在项目根目录建一个 `AGENTS.md`，如果你不确定用哪个文件，就用它，因为 Copilot 和 Codex 都读，Claude Code 在没有 `CLAUDE.md` 的时候也读。文件里只写模型会搞错或者会漏掉的东西，也就是你项目自己的命令、限制和坑，它本来就懂的不用写，比如在你用的语言里怎么写循环。规则越短越好，第一版写五到十行就够了，Claude Code 的文档也建议每个文件控制在 200 行以内，因为文件越长，占的上下文越多，模型照做得也越差（[How Claude remembers your project](https://code.claude.com/docs/en/memory)）。

有一行值得早点加上：改完之后要跑的命令（测试、lint），再加一句“通过之前不许说做完了”，这是最便宜的检查（[让 Agent 自己跑测试](5-4-self-checks.html)）。

我配置里的真实文件要长一些，核心的两条限制是这样的：

::: code harness AGENTS.md L44-L45 "自带规则文件里的两条核心限制：动手之前先看，保留用户自己的改动。"

写完要确认它生效了。开一个新对话，问一个只有你的规则才答得出的问题，比如“这个项目里怎么跑测试？”，它照着规则回答，说明文件加载了，如果它在猜，就检查文件名和位置。在 VS Code 里也可以展开回答下面的 References，或者在命令面板里运行 **Chat: Open Customizations**，看这个文件在不在列表里。

### 第 2 步：加一个 skill（约 10 分钟）

挑一件你给 agent 解释过不止一次的活，在 `.github/skills/` 下面给它建一个文件夹，里面放一个 `SKILL.md`，开头写名字和描述。名字只能用小写字母、数字和连字符，并且要和文件夹同名，描述最多 1024 个字符。

最要紧的是描述，因为 agent 平时只看得到这一段，能不能在该用的时候想起这个 skill，全看它写得好不好。VS Code 的建议是把“做什么”和“什么时候用”都写具体，我还会写上用户可能会说的词。

::: code harness .github/skills/generic-code-standards/SKILL.md L1-L6 "一个真实 skill 的开头：agent 最先看到的，是名字和描述。"

开头下面写步骤，步骤后面列一小段坑，也就是 agent 通常会出错的地方。以后每看到它失败一次就加一条，这是我知道的写 skill 最有用的习惯（[怎么写一个真正好用的 skill？](3-4-skills-and-workflows.html)）。

写完同样要确认。在对话框里输入 `/`，这个 skill 应该出现在列表里，然后提一个符合描述、但不点名这个 skill 的需求，看 agent 会不会用上它。如果它一直不选这个 skill，问题通常出在描述上。

### 第 3 步：写一个拦截危险命令的 hook（约 10 分钟）

终端是 agent 手里最厉害的工具，所以第一个 hook 就从这里下手，拦那些损害无法撤销的命令，比如递归删除一个文件夹，或者下载一个脚本后一行命令直接运行。

hook 分两部分，配置文件告诉平台在哪个事件上调用哪个程序，程序负责判断。VS Code 从仓库的 `.github/hooks/*.json` 读配置，我的配置里，每个事件都指向同一个程序：

::: code harness .github/hooks/harness.json L40-L51 "工具运行之前那个时机的配置：它只是写明了要调用哪个程序。"

每次运行工具之前，平台把这次调用交给程序，如果命令符合你要拦的某个模式，程序就返回拒绝（把 `permissionDecision` 设成 `deny`），并附上原因。原因要写明应该改做什么，因为 agent 看得到它，不写的话 agent 还会再试同样的事（[“先问我”为什么挡不住 Agent？](4-2-ask-vs-refuse.html)）。下面是我的一个模式，写得这么长，是因为同一条命令有很多种写法，你第一天不需要这么大的文件，先写三四个模式就够了。

::: code harness .harness/policies/gate.json L59-L62 "一条真实的拒绝规则：对根目录、主目录或当前文件夹做递归强制删除，附上 agent 看得懂的原因。"

测试 hook 不能拿真正危险的命令。先加一条无害的规则，比如拒绝命令 `echo hook-test`，再让 agent 去跑，你应该会看到一个带着你写的原因的拒绝，测完把这条规则删掉。

hook 有三个坑，我都踩过：

- hook 程序启动不了（比如找不到解释器），这次调用会被当作拒绝，GitHub 的文档也是这么写的：preToolUse 的命令出错，就拒绝这次工具调用。结果是 agent 一个工具都用不了，屏幕上却只显示 hook 出错，所以在依赖它之前先测一次。
- hook 超时（我的配置设的是 30 秒），平台就当它没表态，按正常的权限规则处理这次调用。如果这条命令平时是自动批准的，它就照常运行，等于没有 hook，所以程序要快。
- 在我的配置里，hook 的配置是窗口启动时读的，改完要重新加载 VS Code 窗口。

### 你需要多大的 harness？

这三样够不够，取决于 agent 出错时谁会受影响。

| 你是 | 大概够用的 | 原因 |
| --- | --- | --- |
| 在自己的项目上单干的一个人 | 上面这三样 | 每处改动你都看得到，出错的代价只有你自己担 |
| 在共享仓库上的小团队 | 这三样，规则文件和 hook 文件像代码一样审，再加一个记录 agent 做了什么的地方 | 别人会承接 agent 的错误，而“谁改了规则”会成为一个问题（[怎么把 Agent 配置推广到整个团队？](7-4-rollout-and-governance.html)） |
| 大团队，或者有合规义务的代码 | 以上这些，再按你的风险需要加[审批点](5-3-two-approvals.html)、[可计数的检查](5-5-counted-checks.html)和报告 | 出错的代价由别人承担，而且你得拿得出发生了什么 |

大多数读者属于第一行，两道审批、任务看板这些都可以以后再说。

### 接下来按痛点加什么

三样都搭好以后，不用把这本书从头读到尾，哪里疼了，再去读对应的那一章。

| 痛点 | 读 |
| --- | --- |
| agent 一次又一次无视某条规则 | [4.1](4-1-requests-and-rules.html) |
| 一条命令弹了一百次审批，你不看就点“允许” | [4.2](4-2-ask-vs-refuse.html) |
| 它说“做完了”，测试却是失败的 | [5.4](5-4-self-checks.html) |
| 长对话越聊越差，它还忘事 | [3.2](3-2-long-sessions.html) |
| 账单比预想的高 | [1.1](1-1-models-and-cost.html) |
| 你想把工作分给多个 agent | [2.3](2-3-subagents.html) |
| 你说不清它做了什么 | [6.1](6-1-observe.html) |

### 怎么知道变好了没有？

每加一样东西，你都想知道它有没有用，但是感觉靠不住。办法是挑几个你知道正确答案的任务，每次改动前后各跑一遍，用同样的方式打分（方法见[第 6 部分](6-3-eval-tasks.html)）。粗糙的版本也比猜强：五个任务，加一张运行之前就写好的“什么算对”的清单，每个任务多跑几次，因为一次运行的结果可能只是运气（[同一个任务跑两次，结果不一样](6-4-variance.html)）。

## 规则文件会越写越长，hook 会让人放心过头 {#costs-and-traps}

规则文件最先出问题。每出一次事故就加一行，过一阵它就很长了，有些条目还互相矛盾，模型也就不再照做了，所以要定期删减，让每条规则只出现在一个地方。

hook 的问题更隐蔽，它让人放心过头。因为它只拦它认得的写法，所以别说“agent 删不了东西”，要说“agent 跑不了这几条具体的命令”。

## 什么时候可以把每一样删掉 {#when-to-delete-it}
{status: industry}

这套入门配置里的每一样，平台都在慢慢自带。等平台自己的权限系统开箱就能拒绝同样的危险命令，就删掉你的 hook；等它自己学会了你项目的命令，就缩短你的规则文件。每次大的模型升级之后，都重读一遍规则（[换了新模型，旧规则该删了](6-5-model-upgrades.html)），因为为旧模型写的那些行，可能已经成了累赘。

## 在你自己的环境里试试 {#try-it}

::: prompt
对照一套三部分的最小配置，检查这个仓库：一页简短的规则、一个 skill、一个拦截的 hook。每一部分，说明它在不在、在哪、有没有用。对规则，列出又长、又过期或者互相矛盾的行，并指出缺了哪些模型猜不到的命令和限制。对 hook，列出哪些不可逆的命令（比如递归删除）没有任何东西拦着。不要修改任何文件。
:::

## 延伸阅读 {#go-deeper}

- Anthropic：[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- VS Code 文档：[Create and manage agent customizations](https://code.visualstudio.com/docs/copilot/customization/overview)
- VS Code 文档：[Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)、[Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- VS Code 文档：[Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- Claude Code 文档：[How Claude remembers your project](https://code.claude.com/docs/en/memory)

## 在 harness 里探索 {#explore}

我自己的配置，就是这一章的成熟版：一页规则、许多 skill，还有一个守着每次工具调用的 hook。harness 可以从内部带你逐个看，也能帮你配置你自己的。

::: prompt
/harness-rookie-wondering 我读完了“30 分钟搭一个最小 harness”这一章。请教我这个 harness 的规则页、skill 和 hook 是怎么做的。带我打开真实的文件，让我看 hook 是怎么拒绝一条命令的，并帮我看清哪些东西我可以抄进自己的项目。
:::
