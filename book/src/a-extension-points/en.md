This appendix is a lookup table for the moment you wonder "where does this go, when does the agent see it, and can it be forced?" Find the row here, then follow its link to the chapter that explains why.

## Before you rely on a row {#read-first}

**Checked: 2026-10-27.** That is the day I read the official docs of VS Code, Claude Code and Codex for this page. Names, folders, settings and preview labels change often, so the page will go stale. That is why the date is here: check it before you lean on a row. If the table and the docs disagree, the docs win.

Two more things decide how you read the rows.

- **VS Code now asks you to choose a harness first.** Here "harness" is VS Code's own name for the option you pick, such as the Copilot harness or the Local harness, and according to the VS Code docs that choice decides which formats and locations work. In their words, "Creating a file doesn't mean the selected harness can load or run it." That is why some rows below say "Local harness only".
- **"Enforced" has one meaning here.** A thing is enforced if the platform makes the agent obey it, so that the model cannot choose otherwise. By that measure almost every row is a request to the model. The exceptions are a hook that refuses a call and a tool list that removes tools. Why the difference matters is the subject of [A rule in a prompt is a request](4-1-requests-and-rules.html).

If you know what you want but not which row it belongs to, start here:

- A rule for every task: always-on instructions.
- A rule for some files: instructions by file.
- A way of working the agent starts when it fits: a skill.
- A different set of tools or a read-only helper: a custom agent.
- Something that must be refused: a hook, or taking the tool away.

## VS Code Copilot {#copilot}

Each row answers the opening question in order: what the thing is, when the agent sees it, and whether it can be forced.

| Extension point | What it is | When it loads | Enforced? | Chapter |
| --- | --- | --- | --- | --- |
| Instructions, always on | `.github/copilot-instructions.md` and `AGENTS.md` at the repository root. `CLAUDE.md` is read by the Local harness only, when `chat.useClaudeMdFile` is on. | Added to the agent's context automatically. Nested `AGENTS.md` files are experimental and off by default (Local harness). | No, it is a request. The docs say applicable sources are additive, so do not rely on order to settle a conflict. | [Instructions and skills](3-3-instructions-and-skills.html) |
| Instructions, by file | `*.instructions.md` in `.github/instructions` (Claude format: `.claude/rules`). | Attached when the `applyTo` glob matches a file being changed, or loaded on demand when the `description` matches the task. | No, it is a request. | [Instructions and skills](3-3-instructions-and-skills.html) |
| Prompt files | `*.prompt.md` in `.github/prompts` (or your user profile). A saved prompt with optional `agent`, `model` and `tools` in its header. | Only when you run it: type `/` and its name. Local harness sessions in the Chat view only. Not applied automatically. | No, it is a prompt. Its `tools` list does take priority over the tool list of the agent it names. | No chapter covers prompt files. See the official docs of your tool. |
| Skills | A folder with a `SKILL.md`, in `.github/skills/`, `.claude/skills/` or `.agents/skills/` (and the same under your home folder). | Three levels: name and description first, the body when the request matches or you type `/name`, other files only when the body points to them. | No, the model decides whether to use it. `disable-model-invocation: true` stops the model from starting it, which is a limit on who starts, not on what it does. | [Instructions and skills](3-3-instructions-and-skills.html), [Skills as workflows](3-4-skills-and-workflows.html) |
| Custom agents | `*.agent.md` in `.github/agents` (Claude format: `.claude/agents`), with a header and a body of instructions. | When you pick it in the Agent dropdown, or when another agent runs it as a subagent. In the Copilot harness its instructions are added to your custom instructions and win conflicts. | The `tools` list is enforced: the docs say "only those tools are available". The body, such as "do not do X", is a request. | [Custom agents](2-4-custom-agents.html), [Use subagents sparingly](2-3-subagents.html) |
| Hooks | JSON files in `.github/hooks/`, or a `hooks` map in settings files. Events include `sessionStart`, `userPromptSubmitted`, `preToolUse`, `postToolUse`, `subagentStart`, `subagentStop`, `agentStop`. | Run by the platform at those moments. In the Local harness `chat.useHooks` controls execution. Hook files are read when the window starts. | Yes, for what it sees: `preToolUse` can return a deny with a reason. A timeout falls through to normal permissions. Labelled Preview in the docs. | [Hooks](2-2-hooks.html), [Enforcement design](4-4-enforcement-design.html) |
| MCP servers | Servers that add tools. Personal: `~/.copilot/mcp-config.json`. Shared: `.mcp.json` at the project root (needs the experimental `chat.mcp.workspaceRootConfig.enabled`). Older: `.vscode/mcp.json`. | Configured per user or workspace. The docs do not detail when a server starts; you review sign-in and tool approvals as they appear. | Not for what a server does, though your organization can restrict which servers are available. | [MCP servers](1-3-mcp.html) |
| Tool sets and the tool list | A tool picker in the chat (Copilot harness: Customizations editor, Tools tab; Local harness: Configure Tools). Type `#` to name a tool. A request can have at most 128 tools. | Chosen per profile or per request. | Yes: a tool that is not enabled cannot be called. Enabling a tool, though, does not skip its approval. | [Tool calling](1-2-tool-calling.html), [Custom agents](2-4-custom-agents.html) |
| Settings | VS Code settings that switch the above on or off, such as `chat.useHooks`, `chat.useAgentsMdFile`, `chat.useClaudeMdFile`, `chat.includeApplyingInstructions`, `chat.useCustomizationsInParentRepositories`. | Read by VS Code. Copilot CLI and the Copilot app do not inherit editor settings, so the docs advise against relying on custom location settings. | Not a rule for the model. Settings are host configuration. Enterprise controls can switch hooks on or off, and the Claude and Codex harnesses are disabled when enterprise-managed Copilot settings apply. | [A minimal harness](0-2-minimal-harness.html) |

One more note, on tool sets. The VS Code docs say user-defined tool sets (`.jsonc` files) are deprecated and not supported in the Copilot harness. When you want a reusable choice of tools, they recommend a custom agent with a `tools` list instead. So I treat tool sets as legacy.

## The same points in Claude Code and Codex {#counterparts}

If you also work in Claude Code or Codex, these are the same rows on their side. Where I could not confirm a counterpart on the official pages, the cell says "not confirmed" instead of a guess. I have not run these two columns myself, because every example in this book comes from one setup on the Copilot side. What they say rests on the vendors' docs as they stood on the date above.

| Extension point | Claude Code | Codex |
| --- | --- | --- |
| Instructions, always on | `CLAUDE.md` (project, user, organization). It can also read a repository's `AGENTS.md` in place of `CLAUDE.md`. The docs call it "context, not enforced configuration". | `AGENTS.md` per directory from the project root down to the current folder, and `AGENTS.override.md` where you need to replace one. Built once per run; combined size capped at `project_doc_max_bytes` (32 KiB by default). |
| Instructions, by file | `.claude/rules/*` with a `paths` header. | Nested `AGENTS.md` files closer to the work. A file-pattern header: not confirmed. |
| Prompt files | `.claude/commands/*.md` still works, but commands have been merged into skills. A skill with the same name wins. | Custom prompts in `~/.codex/prompts/` exist but are deprecated in favour of skills. Run as `/prompts:name`. Not shared through the repository. |
| Skills | `.claude/skills/<name>/SKILL.md` (project), `~/.claude/skills/` (personal). Descriptions are always in context; the body loads when invoked. | `.agents/skills` (repository, from the current folder up to the root), `$HOME/.agents/skills`, `/etc/codex/skills`. Same three-level loading. `allow_implicit_invocation: false` in `agents/openai.yaml` turns off model-started use. |
| Custom agents | `.claude/agents/*.md`, with `tools` (an allowlist), `disallowedTools` and `model`. | `.codex/agents/*.toml` (project) or `~/.codex/agents/`, one agent per file, with `name`, `description`, `developer_instructions` and optional model settings. Subagents inherit the parent's sandbox, approval policy and MCP servers. A tool allowlist per agent: not confirmed. |
| Hooks | `hooks` in `.claude/settings.json`, `.claude/settings.local.json` or `~/.claude/settings.json`. Exit code 2, or a JSON `permissionDecision` of `deny`, blocks on `PreToolUse`. By default a hook that fails or times out does not block. | `hooks.json` or `[hooks]` in `config.toml`, in `~/.codex/` or `<repo>/.codex/`. `PreToolUse` can deny. Project hooks load only for a trusted project and must be reviewed first. The docs call hooks a guardrail, not a complete enforcement boundary. What happens when a hook times out: not confirmed. |
| MCP servers | `.mcp.json` in the project (shared), `~/.claude.json` (local and user scopes). Project servers ask for approval in interactive sessions. | `[mcp_servers.<name>]` in `~/.codex/config.toml`, or `.codex/config.toml` for a trusted project. `codex mcp add` and `codex mcp list`. |
| Tool sets | Not confirmed as a separate feature. The nearest I found is a subagent's `tools` allowlist. | Not confirmed. |
| Settings | `settings.json` (user, project, local, and managed policy). I checked it only for hooks. | `~/.codex/config.toml` and `.codex/config.toml`, with `approval_policy` and `sandbox_mode`. `requirements.toml` can restrict them on managed machines. |

## How to use this page {#how-to-use}

Two habits make this table useful.

- **Put a rule in the lightest point that is enough.** Always-on instructions cost room every turn, a skill costs room only when it is used, and a hook costs code. The order and the reasoning are in [Context is a budget](3-1-context-budget.html) and [A rule in a prompt is a request](4-1-requests-and-rules.html).
- **Check the harness before the file.** If a file seems to be ignored, first ask whether the harness you selected can load that kind of file at all. If the harness is not the cause, [Troubleshooting](b-troubleshooting.html) starts from the symptom you see.
