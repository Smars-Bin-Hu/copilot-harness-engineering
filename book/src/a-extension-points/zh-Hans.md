这个附录是一张查找表。你想知道“这个东西放哪里、agent 什么时候能看到、能不能强制”，就在这里找到那一行，再顺着链接去看讲道理的那一章。

## 先读这个 {#read-first}

**核对日期：2026-10-27。** 那天我读了 VS Code、Claude Code 和 Codex 的官方文档。名称、文件夹、设置和预览版标签经常变，所以这一页会过期。以文档为准，不要以这张表为准，并看一下日期。

看各行之前，先知道两件事。

- **VS Code 现在要你先选一个 harness。** VS Code 文档说，你选的 harness（比如 Copilot harness 或本地 harness）决定哪些格式和位置有效：“创建了文件，不等于所选的 harness 能加载或运行它。”下面有几行写“仅限本地 harness”，就是这个原因。
- **这里的“强制执行”只有一个意思。** 平台让 agent 必须服从，模型没法选择不照做，才算强制执行。几乎每一行都只是对模型的请求。例外是拒绝调用的 hook，和把工具去掉的工具列表。为什么这很要紧，是[提示里的规则只是请求](4-1-requests-and-rules.html)这一章的主题。

在官方页面上确认不了对应功能的地方，格子里写“未确认”。我没有猜。

各行的简要指引：

- 每个任务都适用的规则：始终开启的指令。
- 只对某些文件适用的规则：按文件的指令。
- 合适时由 agent 自己启动的做事方式：skill。
- 一组不同的工具，或者一个只读的帮手：自定义 agent。
- 必须拒绝的事：hook，或者把工具拿掉。

## VS Code Copilot {#copilot}

| 扩展点 | 是什么 | 什么时候加载 | 强制执行吗？ | 章节 |
| --- | --- | --- | --- | --- |
| 指令，始终开启 | 仓库根目录的 `.github/copilot-instructions.md` 和 `AGENTS.md`。`CLAUDE.md` 只有本地 harness 会读，且要打开 `chat.useClaudeMdFile`。 | 自动加入 agent 的上下文。嵌套的 `AGENTS.md` 是实验功能，默认关闭（本地 harness）。 | 不。是请求。文档说适用的来源是叠加的，所以不要靠顺序来解决冲突。 | [指令与 skill：只加载需要的](3-3-instructions-and-skills.html) |
| 指令，按文件 | `.github/instructions` 里的 `*.instructions.md`（Claude 格式：`.claude/rules`）。 | `applyTo` 通配符匹配到正在修改的文件时附上；或者 `description` 与任务匹配时按需加载。 | 不。是请求。 | [指令与 skill：只加载需要的](3-3-instructions-and-skills.html) |
| Prompt 文件 | `.github/prompts`（或你的用户配置）里的 `*.prompt.md`。一个保存下来的 prompt，头部可以带可选的 `agent`、`model` 和 `tools`。 | 只在你运行它的时候：输入 `/` 和它的名字。只限聊天视图里的本地 harness 会话。不会自动应用。 | 不。它就是个 prompt。不过它的 `tools` 列表优先于它指定的 agent 的工具列表。 | 没有章节讲 prompt 文件。请读你所用工具的官方文档。 |
| Skill | 一个带 `SKILL.md` 的文件夹，放在 `.github/skills/`、`.claude/skills/` 或 `.agents/skills/`（以及主目录下的同名位置）。 | 三层：先是名称和描述；请求匹配或你输入 `/name` 时加载正文；其他文件只在正文指到它们时才加载。 | 不。由模型决定用不用。`disable-model-invocation: true` 能阻止模型启动它，这限制的是谁来启动，不是它做什么。 | [指令与 skill：只加载需要的](3-3-instructions-and-skills.html)、[把团队的做法写成 skill](3-4-skills-and-workflows.html) |
| 自定义 agent | `.github/agents`（Claude 格式：`.claude/agents`）里的 `*.agent.md`，有头部和一段指令正文。 | 你在 Agent 下拉框里选它的时候，或者另一个 agent 把它当子 agent 运行的时候。在 Copilot harness 里，它的指令会加到你的自定义指令上，冲突时它说了算。 | `tools` 列表是强制的：文档说“只有这些工具可用”。正文，比如“不要做 X”，是请求。 | [自定义 agent：固定模型和工具的角色](2-4-custom-agents.html)、[慎用子 agent](2-3-subagents.html) |
| Hook | `.github/hooks/` 里的 JSON 文件，或者设置文件里的 `hooks` 映射。事件包括 `sessionStart`、`userPromptSubmitted`、`preToolUse`、`postToolUse`、`subagentStart`、`subagentStop`、`agentStop`。 | 由平台在这些时刻运行。在本地 harness 里，`chat.useHooks` 控制是否执行。窗口启动时读取。 | 是，对它看得到的范围：`preToolUse` 可以返回拒绝并附上原因。超时则回到正常的权限流程。文档里标为预览版。 | [Hook：每次调用都会经过的执行点](2-2-hooks.html)、[把执行层当软件来设计](4-4-enforcement-design.html) |
| MCP server | 增加工具的 server。个人的：`~/.copilot/mcp-config.json`。共享的：项目根目录的 `.mcp.json`（需要打开实验设置 `chat.mcp.workspaceRootConfig.enabled`）。较早的：`.vscode/mcp.json`。 | 按用户或工作区配置。文档没有细说 server 什么时候启动；登录和工具审批出现时，由你来审查。 | 对 server 做什么，不。你的组织可以限制哪些 server 可用。 | [MCP server：接工具的标准接口](1-3-mcp.html) |
| 工具集和工具列表 | 聊天里的工具选择器（Copilot harness：自定义编辑器的 Tools 标签页；本地 harness：Configure Tools）。输入 `#` 可以点名一个工具。一次请求最多可以有 128 个工具。 | 按配置档或按请求选择。 | 没启用的工具调用不了。但启用一个工具，并不会跳过它的审批。 | [Tool calling，以及怎么给 agent 设计工具](1-2-tool-calling.html)、[自定义 agent：固定模型和工具的角色](2-4-custom-agents.html) |
| 设置 | 打开或关闭上面各项的 VS Code 设置，比如 `chat.useHooks`、`chat.useAgentsMdFile`、`chat.useClaudeMdFile`、`chat.includeApplyingInstructions`、`chat.useCustomizationsInParentRepositories`。 | 由 VS Code 读取。Copilot CLI 和 Copilot 应用不继承编辑器的设置，所以文档建议不要依赖自定义位置的设置。 | 设置是宿主的配置。企业管控可以打开或关闭 hook；适用企业托管的 Copilot 设置时，Claude 和 Codex 的 harness 会被禁用。 | [30 分钟搭一个最小 harness](0-2-minimal-harness.html) |

关于工具集的一点说明。VS Code 文档说，用户自定义的工具集（`.jsonc` 文件）已弃用，Copilot harness 不支持。想要一个可复用的工具选择，文档推荐用带 `tools` 列表的自定义 agent。我把工具集当作遗留功能。

## Claude Code 和 Codex 里的对应项 {#counterparts}

| 扩展点 | Claude Code | Codex |
| --- | --- | --- |
| 指令，始终开启 | `CLAUDE.md`（项目、用户、组织）。也可以读仓库的 `AGENTS.md` 来代替 `CLAUDE.md`。文档称它是“上下文，不是强制执行的配置”。 | 从项目根目录到当前文件夹，每个目录一份 `AGENTS.md`；需要替换某一份时，用 `AGENTS.override.md`。每次运行构建一次；合并后的大小上限是 `project_doc_max_bytes`（默认 32 KiB）。 |
| 指令，按文件 | 带 `paths` 头部的 `.claude/rules/*`。 | 离工作更近的嵌套 `AGENTS.md`。文件模式的头部：未确认。 |
| Prompt 文件 | `.claude/commands/*.md` 仍然可用，但命令已经并入 skill。同名的 skill 优先。 | `~/.codex/prompts/` 里有自定义 prompt，但已弃用，改用 skill。以 `/prompts:name` 运行。不通过仓库共享。 |
| Skill | `.claude/skills/<name>/SKILL.md`（项目）、`~/.claude/skills/`（个人）。描述始终在上下文里；正文在调用时加载。 | `.agents/skills`（仓库，从当前文件夹一直到根目录）、`$HOME/.agents/skills`、`/etc/codex/skills`。同样的三层加载。`agents/openai.yaml` 里的 `allow_implicit_invocation: false` 会关闭由模型启动的用法。 |
| 自定义 agent | `.claude/agents/*.md`，带 `tools`（允许名单）、`disallowedTools` 和 `model`。 | `.codex/agents/*.toml`（项目）或 `~/.codex/agents/`，每个文件一个 agent，有 `name`、`description`、`developer_instructions` 和可选的模型设置。子 agent 继承父级的沙箱、审批策略和 MCP server。每个 agent 单独的工具允许名单：未确认。 |
| Hook | `.claude/settings.json`、`.claude/settings.local.json` 或 `~/.claude/settings.json` 里的 `hooks`。退出码 2，或者 JSON 里 `permissionDecision` 为 `deny`，会在 `PreToolUse` 上拦截。默认情况下，失败或超时的 hook 不会拦截。 | `~/.codex/` 或 `<repo>/.codex/` 里的 `hooks.json`，或 `config.toml` 里的 `[hooks]`。`PreToolUse` 可以拒绝。项目 hook 只在受信任的项目里加载，而且必须先审查。文档称 hook 是护栏，不是完整的强制边界。hook 超时会怎样：未确认。 |
| MCP server | 项目里的 `.mcp.json`（共享）、`~/.claude.json`（本地和用户范围）。项目里的 server 在交互会话中要先审批。 | `~/.codex/config.toml` 里的 `[mcp_servers.<name>]`，或者受信任项目的 `.codex/config.toml`。`codex mcp add` 和 `codex mcp list`。 |
| 工具集 | 未确认有单独的这个功能。我找到的最接近的是子 agent 的 `tools` 允许名单。 | 未确认。 |
| 设置 | `settings.json`（用户、项目、本地，以及托管策略）。我只查了 hook 相关的部分。 | `~/.codex/config.toml` 和 `.codex/config.toml`，有 `approval_policy` 和 `sandbox_mode`。在托管的机器上，`requirements.toml` 可以限制它们。 |

## 怎么用这一页 {#how-to-use}

两个习惯，会让这张表有用。

- **规则放在够用的、最轻的那个点上。** 始终开启的指令每一轮都占地方；skill 只在用到时占地方；hook 要花代码。顺序和道理见[上下文是一份预算](3-1-context-budget.html)和[提示里的规则只是请求](4-1-requests-and-rules.html)。
- **先查 harness，再查文件。** 如果一个文件似乎被忽略了，先问一问你选的 harness 到底能不能加载这类文件。[排错](b-troubleshooting.html)从症状出发。

本书的例子来自 Copilot 一侧的同一套配置。Claude Code 和 Codex 那两列我自己没有跑过；它们来自上面那个日期各厂商的文档。
