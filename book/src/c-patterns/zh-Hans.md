这个附录是一个小模式的书架。每个模式有一行问题，几行做法，一个可以照着抄的、来自我的 harness 的真实文件，以及讲道理的那一章。它们是拿来改的例子，不是拿来粘贴的。这些文件是钉住的 tag 上的真实文件，所以比你的第一版应有的样子更长、更具体。抄过去之后，要在你自己的环境里逐个检查。如果不知道从哪里开始，先看安全类的模式（拒绝一条命令、审批留给人），再看省上下文的，最后看长任务用的。每个模式都有一行**局限**，取自它所链接的那一章。

## 把核心限制放在一页上 {#core-limits}

**问题。** agent 乱猜路径和命令，或者把你改的文件“整理”掉。

**做法。** 保留一页简短的、始终加载的规则。只放没有它模型就会做错的内容，并放在最前面。开头有两条限制就够了。

::: code harness AGENTS.md L44-L45 "随 harness 发布的规则页里的两条核心限制：先看再动手，保留用户自己的改动。"

**局限。** 变长的页面就没人读了；每一行都要有存在的理由。

更多内容见[指令与 skill：只加载需要的](3-3-instructions-and-skills.html)和[30 分钟搭一个最小 harness](0-2-minimal-harness.html)。

## 规则只为它适用的文件加载 {#rules-by-file}

**问题。** 一条只对某一类文件要紧的规则，在每个对话里都占地方。

**做法。** 把规则放进带 `applyTo` 匹配模式的指令文件。agent 处理匹配的文件时才加载，其余时候不占任何空间。

::: code harness .github/instructions/skills.instructions.md L1-L4 "按文件加载的指令的头部：一段描述和一个 applyTo 匹配模式。"

**局限。** 这是对模型的请求，不是平台强制执行的规则。

更多内容见[指令与 skill：只加载需要的](3-3-instructions-and-skills.html)。

## 所有时机只用一个 hook 入口 {#one-hook-entry}

**问题。** 好几个 hook 脚本，各有各的超时和 shell，很难保持一致。

**做法。** 让配置文件只说明在哪些时机调用，并让每个时机都指向同一个程序。做什么由这个程序决定。设一个时间限制，并记住这个文件是在窗口启动时读取的。

::: code harness .github/hooks/harness.json L40-L51 "工具运行之前那个时机的入口：它只写出程序的名字和时间限制。"

**局限。** 超时的 hook 会被当作通过，所以要让它快。

更多内容见[Hook：每次调用都会经过的执行点](2-2-hooks.html)和[把执行层当软件来设计](4-4-enforcement-design.html)。

## 拒绝危险命令，并给出理由 {#refuse-with-reason}

**问题。** 造成的损害无法挽回的命令，比如递归删除根目录或主目录，永远不该运行。

**做法。** 为每一条写一个匹配模式和一句 `why`。agent 会读这个理由，所以要写清这条命令会做什么。匹配模式要窄，因为一次误拒就是一个卡住的任务。它拦得住常见的写法，拦不住所有的写法。

::: code harness .harness/policies/gate.json L59-L62 "一条真实的拒绝规则：对根目录、主目录或当前文件夹做递归强制删除，附上 agent 读得懂的理由。"

**局限。** 这是个减速带，不是边界：它只拦常见的写法。对那些绝不能碰的东西，不要交出去（[有些东西根本不给](4-5-least-privilege.html)）。

更多内容见[询问不是限制](4-2-ask-vs-refuse.html)和[Hook：每次调用都会经过的执行点](2-2-hooks.html)。

## 审批留在人的终端里 {#person-only-commands}

**问题。** 如果 agent 能运行审批命令，审批就没有意义。

**做法。** 在同一个 hook 里，拒绝每一条授予权限的命令。理由告诉 agent，请人到自己的终端里去运行。测一下：让 agent 运行其中一条。

::: code harness .harness/policies/gate.json L83-L86 "对只有人才能运行的命令的拒绝：审批、豁免、打开无人值守模式。"

**局限。** 只有在 hook 运行、并且它的文件受到保护的时候才有效。

更多内容见[两道门：人在哪里审批](5-3-two-approvals.html)和[保护规则本身的文件](4-3-guardrails.html)。

## 标出只有人才能启动的 skill {#user-only-skill}

**问题。** 一个会花钱或者会交出权限的 skill，不该因为模型觉得合适就启动。

**做法。** 设置 `disable-model-invocation: true`，并在描述里写明 agent 不得调用它。这限制的是谁来启动这个 skill，不限制它启动之后做什么。

::: code harness .github/skills/harness-autorun/SKILL.md L1-L8 "只有用户才能启动的 skill 的开头：头部的标志，和描述里的那句话。"

**局限。** 它限制谁来启动 skill，不限制 skill 做什么。

更多内容见[指令与 skill：只加载需要的](3-3-instructions-and-skills.html)和[无人值守：什么时候必须停](5-7-when-to-stop.html)。

## 只读的帮手 {#read-only-helper}

**问题。** 你想让一个 agent 大量阅读，却不能改任何东西。

**做法。** 建一个自定义 agent，它的 `tools` 列表里只有读和搜索，也不能调用别的 agent。工具列表才是限制；正文里的“不要……”是请求。在正文里写明这个帮手必须交回什么。

::: code harness .github/agents/mapper.agent.md L1-L8 "一个只读的帮手：工具列表只有读和搜索，也不调用别的 agent。"

**局限。** 每个帮手都从空白的上下文开始，所以几个帮手的成本是单个 agent 的好几倍。

更多内容见[自定义 agent：固定模型和工具的角色](2-4-custom-agents.html)和[慎用子 agent](2-3-subagents.html)。

## 给帮手一份它能独立使用的任务说明 {#helper-brief}

**问题。** 帮手看不到你的对话，所以含糊的调用只会得到含糊的回答。

**做法。** 写明问题、要读的范围和要交回的条目，附上长度限制，并要求每个结论都给出来源。

::: code harness .github/skills/generic-mapreduce/templates/brief.md L5-L18 "给只读帮手的任务说明：问题、范围、要交回什么、长度和来源。"

更多内容见[慎用子 agent](2-3-subagents.html)。

## 只回答 PASS 或 FAIL 的检查者 {#pass-fail-checker}

**问题。** 一个写长篇大论的检查者，既没给人留下可数的东西，也没给脚本留下可读的东西。

**做法。** 把第一行固定为 PASS 或 FAIL。每条发现都写明文件、行号和违反的规则。不提建议，不给修复，有长度限制。这样脚本就能数通过的次数，并丢掉哪里都没指向的发现。

::: code harness .github/agents/reviewer.agent.md L58-L76 "独立检查者的固定输出：一行结论、带文件和行号的发现、长度上限。"

**局限。** 模型当检查者仍然会出错；一次误报的 FAIL 会让作者去追一个不存在的问题。

更多内容见[让“通过”可信](5-5-counted-checks.html)和[模型能检查模型吗](5-6-model-checks-model.html)。

## 把需求写在一页上，并让人确认 {#requirement-page}

**问题。** 请求含糊，还会变来变去，事后没人说得清当时约定了什么。

**做法。** agent 写一页，写明要做什么、不做什么、什么时候算完成，以及一份诚实的“还不清楚”清单。顶上有一行，记录人是否确认过。

::: code harness .harness/contracts/templates/task/en/REQ.md L1-L42 "需求页：要做什么、不做什么、做到什么算完成、还不清楚的事，以及是谁确认的。"

更多内容见[需求由 agent 写，人确认](5-2-requirements.html)。

## 给下一个会话的交接文件 {#handover-file}

**问题。** 新对话对旧对话里做过的工作一无所知。

**做法。** 留一个简短的文件，新会话先读它：状态、正在做什么、下一步、该读什么，以及人做过的决定。每次停下之前都更新。不要盲目相信它：它是 agent 写的。

::: code harness .harness/contracts/templates/task/en/TASK.md L1-L23 "任务的交接文件：状态、正在做、下一步、要读的文件、决定、未解决的问题。"

**局限。** 它是 agent 写的，所以可能有错；要紧的内容要对照源头检查。

更多内容见[管任务，不管对话](5-1-tasks.html)和[跨会话的长任务](5-8-long-work.html)。

## 把人知道的调用关系写下来 {#known-uses}

**问题。** 模型或脚本生成的代码地图看起来没问题，你却没办法知道它之后有没有丢东西。

**做法。** 在抽取器还不存在的时候，由人写下几条他知道确实存在的调用关系，一行一条。每次生成地图，都必须把它们全部找出来。

::: code harness .harness/examples/kb-toolkits/spring/facts.jsonl L4-L8 "Spring 示例里五条已知的调用关系：一个对象、调用的类型、另一个对象。"

**局限。** 一份短清单只能说明地图找得到某些调用关系，不能说明它全都找得到。

更多内容见[Toolkit：用脚本画出代码的地图](8-2-kb-toolkit.html)。

## 每次都用同样的格式汇报一次抽查 {#audit-report}

**问题。** 对模型输出的检查，最后写成了一段文字，两次抽查没法比较。

**做法。** 一份固定的报告：通过还是失败，每种类型一个分数，每处差异附上文件和行号，出现的规律，以及被纠正过的读法。

::: code harness .github/skills/generic-kb-toolkit-audit/templates/audit.md L1-L36 "抽查报告模板：结果、每种类型的分数、漏掉的、误报的调用关系、规律、被纠正的读法。"

**局限。** 样本小，只看得出大的缺口。

更多内容见[地图对不对：盲抽查](8-3-kb-audit.html)。

## 让每次停下都自己说明原因 {#stop-reason}

**问题。** 无人值守的运行以“遇到了问题”停下，留给人去弄清发生了什么。

**做法。** 告诉 agent 什么时候该停、什么时候不该停，以及理由里必须有什么：哪一步卡住了、为什么、人要决定什么。能用事实判断出来的停止，仍然由 hook 来判断。

::: code harness .github/skills/harness-autorun/references/when-to-stop.md L11-L36 "什么时候该自己停、什么时候不该停，以及怎么给回来的人写理由。"

更多内容见[无人值守：什么时候必须停](5-7-when-to-stop.html)。
