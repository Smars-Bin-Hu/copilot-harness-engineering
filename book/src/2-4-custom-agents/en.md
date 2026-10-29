This chapter assumes you have read [Use subagents sparingly](2-3-subagents.html), or at least know what a subagent is.

## In one sentence {#in-one-sentence}

Build a custom agent only when you must change the model or shrink the tools. If what you want to change is what it knows or how it works, a skill or an instruction file is enough.

## For leaders {#for-leaders}

- **The decision:** approve a custom agent only when it changes something that cannot be shared another way: its tools, its model, or a context that must not see the caller's reasoning.
- **The risk:** a role that is only a different tone and some know-how is a costume, one more file to keep in step that the platform does not enforce. In my early setup, three job-title agents cost about 4.5 times the usage of one agent on four small tasks, with no better result, although each task ran only once.
- **The cost of doing it right:** one agent file per real limit, changed through code review like any rule. Mine keeps only a read-only helper and a checker.
- **Ask the team:** "Does this agent file list tools or a model? If not, why isn't it a skill?"

## When you want a different agent, what do you build? {#problem}

[Use subagents sparingly](2-3-subagents.html) asked whether to split work between agents at all. The question here is a smaller one: when you want a different agent, what do you actually have to build?

Many setups answer it by building roles, such as a "SQL expert", a "code reviewer" and a "documentation writer", each in its own agent file. It feels like organizing. To see whether it is, start with what such a file is. A **custom agent** is a file that defines a role for the agent. In VS Code Copilot it is a file ending in `.agent.md`, with a short header (name, description, settings) above a body of instructions. The **default agent**, by contrast, is the plain agent you talk to when you pick nothing.

Look at what such a file holds, though, and you find that most of it could reach the default agent some other way. A role that is only a different tone and some know-how is then a costume: it adds a thing to maintain, but nothing in it is enforced by the platform. So which parts of the file are more than that?

## Which parts of an agent file are more than a costume? {#how-it-works}

### What is in an agent file

The answer starts in the header, where the settings live. Going by the VS Code docs and my own files, only a few of them matter.

The name and the description are written for whoever calls the agent. The description tells the model when this agent is the right one to call, so say in it what the agent is for and what it needs to be told. A subagent starts with an empty context ([Use subagents sparingly](2-3-subagents.html)), and a vague call message gives it nothing to work from.

The other settings decide what the agent works with and who may call it. If the header gives a list of tools, only those tools are available to the agent. The model is optional and can be a list in order of preference, so that when the first cannot be used, the next one is tried. Who may call the agent takes two settings, and they do different things. `user-invocable: false` keeps the agent out of the drop-down list (the VS Code docs call it picker visibility), while a separate setting, `disable-model-invocation`, is for whether the model may call it as a subagent. Each of them still lets some calls through, as "Hidden is not forbidden" below explains.

Below the header, the body is text. It says what the role is for, how it works, what it must not do and what it hands back.

### What only an agent file can do

::: figure 2-4-what-differs

Put the settings next to each other and ask of each one whether the default agent could get it some other way.

For what the agent knows and how it works, the answer is yes. Instruction files and skills reach any agent, so a SQL style guide, a review checklist or the way things are named here can go into a skill or an instruction file ([Instructions and skills](3-3-instructions-and-skills.html)). The default agent then does the job, with no new agent.

The tools are another matter, because they cannot be given another way. An agent has the tools its file lists, and the platform enforces that list, so an agent without the edit tools cannot edit, however it is asked. That is the hard limit an agent file gives you. A rule written in the body of the file, such as "do not edit files", has no such force. It is a request like any other.

The model, too, can only be set in an agent file, whether that is a cheap model for a simple job or a strong one for hard thinking. The person can switch the model in the drop-down for the default agent, but a subagent's model is set in its file.

The tools and the model are both written in the file. A separate context is different, because it is not written in the file at all. When the agent runs as a subagent, it starts with an empty context and only its report comes back, and that comes from running as a subagent, not from anything in the file. It is a reason to build one when you want an independent check, the case that [Use subagents sparingly](2-3-subagents.html) covers.

So the rule I use is short. **Build a custom agent when at least one of these cannot be shared: the tools differ, the model differs, or you need a context that must not see the caller's reasoning.** For everything else, use the default agent and write the know-how down.

The rule is easier to apply with a quick test. If you can say it as "when doing X, do it like this", it is a skill. If you can say it as "this job must not have tool Y" or "this job should run on model Z", it is an agent. And before I add one, I still ask two questions: which failure does it prevent, and why can the default agent not do the same?

The VS Code context engineering guide draws the same line. It offers agents for "workflows that follow a multi-turn process with specific tools", and its example planning agent fits it: the short, read-only tool list is the limit, while the instruction not to implement is a request.

### An example: the reviewer

In my setup there is one custom agent I would keep above all others. It is the reviewer, a checker that sees only the request and the result, and here is the top of its file:

::: code harness .github/agents/reviewer.agent.md L1-L8 "The header of the reviewer: the tools line is the limit, the model line is a fallback list, the description is a request to the model that calls it."

The `tools` line gives it tools for reading, searching and running commands but none for changing files, so it cannot "just fix it". `agents: []` means it cannot start other subagents. The model is a fallback list, so if the first model cannot be used, the next one is. (The reasons for each choice are in [Use subagents sparingly](2-3-subagents.html).) What matters here is that every line of the header that changes behavior is a tool limit, a model or a boundary of context. The description, by contrast, only asks, and the body mostly says what to look at and what to hand back.

Not everything I ran into was this tidy.

### Three facts that bit me

The first is that "hidden" is not "forbidden". The setting that keeps an agent out of the drop-down list does not stop another agent from calling it as a subagent, and neither does the setting that keeps the model from using it. If "who may call whom" matters, a hook has to decide it ([Hooks](2-2-hooks.html)), not these two settings.

A hook has a blind spot of its own, because it cannot see which agent is current. The events it receives carry no name for the main agent ([Hooks](2-2-hooks.html)), so rights cannot be handed to "the admin agent": any agent could pass for it. Rights have to follow the session instead. In my setup, for example, an admin switch is turned on by the person in a terminal ([Guard the files that hold the rules](4-3-guardrails.html)). I once had an admin agent, and I retired it.

The last one is that a check may be silently skipped. When a subagent's model is a class above the main model, the platform does not run it and says nothing. I saw this only once and have not tested it again. So "did the check really happen" has to be confirmed by something that is not the model, such as a hook that saves the reviewer's answer to disk. If a check matters to you, keep a record that it ran.

### Test your own setup

Now go back to the rule and test your own role agents against it. Take one you have, a "SQL expert" or a "documentation writer", and look at whether its file lists tools or a model. If it lists neither, move its body into a skill ([Instructions and skills](3-3-instructions-and-skills.html)), give the same task to the default agent with and without the skill, and compare. If you see no difference, the agent was a costume, though you should run each a few times before you trust what you see.

## What more agents cost, and a limit that is only a request {#costs-and-traps}

Keeping agents costs you in a few ways: files to keep in step, a chat that a switch may lose, limits that are only requests, and usage.

Upkeep is the plainest of these. Each file has a model name, a tool list and a body that can go out of date. Model names change, for one, so a name that no longer matches the drop-down breaks the agent. Because an agent file sets limits, in a team it should be changed through code review like any rule.

Switching agents may also lose the chat. The VS Code docs say a selected agent applies to your requests until you switch. They do not say what happens to the chat history on a plain switch, and I have not tested it, so keep what matters in files ([Long chats get worse](3-2-long-sessions.html)).

Inside a role, a line in the body such as "do not do X" can feel like a limit. As we saw above, it is only a request, and the agent does X anyway. Only the tool list is a limit.

Last comes usage, and here you need fewer roles than you think. In my early setup I had three job-title agents, one to coordinate, one to build and one to check. On four small tasks they cost about 4.5 times the usage of one agent and gave no better result ([Use subagents sparingly](2-3-subagents.html)). I kept only the checker. That is four tasks, run once each, so it is weak evidence, not a result. Anthropic reports the same direction on a different scale: in their research system, agents use about 4 times the tokens of a chat, and multi-agent systems about 15 times ([How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)). My number and theirs measure different things, so compare only the direction.

## When to delete an agent file {#when-to-delete-it}
{status: industry}

So when can an agent file go? It stays as long as it enforces something a skill cannot: a tool list or a model. Some platforms already let a skill carry tool settings. In Claude Code, a skill's `allowed-tools` only pre-approves tools and does not restrict them. Removing tools is the job of a separate setting, `disallowed-tools`, which takes them away while the skill is active ([Skills](https://code.claude.com/docs/en/skills)). Whether such a setting is enforced on your platform is something you have to check. Where it is, many agent files become unnecessary. And any agent whose only content is "act like an expert in X" can be deleted today.

## Try it on your own setup {#try-it}

::: prompt
Find every custom agent file in this project. For each one, report: does its header limit the tools, set a model, or neither; is the description written so a caller knows when to use it and what to say; and which lines of the body are only requests. Mark every agent with no tool limit and no model setting as a likely costume, and say which skill or instruction file could replace it. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- Anthropic: [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Instructions and skills](3-3-instructions-and-skills.html): the other way to change what an agent does

## Explore it in the harness {#explore}

The harness keeps its set of custom agents very small on purpose: a read-only helper and a checker. You can open both files and compare each line with the table above.

::: prompt
/harness-rookie-wondering I have read the chapter "Custom agents". Teach me what is in this harness's agent files: the tool lists, the model lists, and which lines change behavior and which are only requests. Open the real files with me, and show me why there are so few agents.
:::
