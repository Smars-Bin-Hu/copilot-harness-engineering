This chapter assumes you have read [Use subagents sparingly](2-3-subagents.html), or at least know what a subagent is.

## In one sentence {#in-one-sentence}

Build a custom agent only when you must change the model or shrink the tools. To change what it knows or how it works, a skill or an instruction file is enough.

## For leaders {#for-leaders}

- **The decision:** approve a custom agent only when it changes something that cannot be shared another way: its tools, its model, or a context that must not see the caller's reasoning.
- **The risk:** a role that is only a different tone and some know-how is a costume: one more file to keep in step that the platform does not enforce. In my early setup, three job-title agents cost about 4.5 times the usage of one agent on four small tasks, run once each, with no better result.
- **The cost of doing it right:** one agent file per real limit, changed through code review like any rule. Mine keeps only a read-only helper and a checker.
- **Ask the team:** "Does this agent file list tools or a model? If not, why isn't it a skill?"

## The problem {#problem}

[Use subagents sparingly](2-3-subagents.html) asked whether to split work between agents. This chapter asks a smaller question: when you want a different agent, what do you actually have to build?

Many setups start by building roles: a "SQL expert", a "code reviewer", a "documentation writer", each as its own agent file. It feels like organizing. But look at what an agent file holds, and you find that most of it is something you could give to the default agent in another way. A role that is only a different tone and some know-how is a costume. It adds a thing to maintain and nothing the platform enforces.

Two words first.

- A **custom agent** is a file that defines a role for the agent. In VS Code Copilot it is a file ending in `.agent.md`. It has a short header (name, description, settings) and a body of instructions.
- The **default agent** is the plain agent you talk to when you pick nothing.

## How it works {#how-it-works}

### What is in an agent file

The header holds a few settings. These are the ones that matter, from the VS Code docs and from my own files:

- **A name and a description.** The description tells the model when this agent is the right one to call. Write it for the caller: say what the agent is for and what it needs to be told. A subagent starts with an empty context ([Use subagents sparingly](2-3-subagents.html)), so a vague call message gives it nothing to work from.
- **A list of tools.** If the file gives a list, only those tools are available to the agent.
- **A model**, optional. It can be a list in order of preference: when the first cannot be used, the next one is tried.
- **Who may call it.** Two settings, and they do different things. `user-invocable: false` keeps the agent out of the drop-down list (the VS Code docs call it picker visibility). A separate setting, `disable-model-invocation`, is for whether the model may call it as a subagent. See "Hidden is not forbidden" below.

The body is text: what the role is for, how it works, what it must not do, what it hands back.

### What only an agent file can do

::: figure 2-4-what-differs

Put the settings next to each other and ask: what can I give to the default agent some other way?

- **How it works, what it knows.** Instruction files and skills reach any agent. A SQL style guide, a review checklist, the way things are named here: put them in a skill or an instruction file ([Instructions and skills](3-3-instructions-and-skills.html)). The default agent then does the job, with no new agent.
- **Which tools it has.** This cannot be given another way. An agent has the tools its file lists, and the platform enforces that list. An agent without the edit tools cannot edit, however it is asked. It is the hard limit an agent file gives you. (A rule written in the body of the file, "do not edit files", is a request like any other.)
- **Which model it uses.** Also only an agent file. A cheap model for a simple job, or a strong one for hard thinking. The person can switch the model in the drop-down for the default agent, but a subagent's model is set in its file.
- **A separate context.** When it runs as a subagent, it starts with an empty context, and only its report comes back. This is not a property of the file but of being a subagent. It is a reason to build one when you want an independent check, and [Use subagents sparingly](2-3-subagents.html) covers it.

So the rule I use is short. **Build a custom agent when at least one of these cannot be shared: the tools differ, the model differs, or you need a context that must not see the caller's reasoning.** For everything else, use the default agent and write the know-how down. A quick test: if you can say it as "when doing X, do it like this", it is a skill. If you can say it as "this job must not have tool Y" or "this job should run on model Z", it is an agent.

Before I add one, I ask two questions: which failure does it prevent, and why can the default agent not do the same?

The VS Code context engineering guide offers agents for "workflows that follow a multi-turn process with specific tools", and its example planning agent has a short, read-only tool list and an instruction not to implement. That is the same shape: the tool list is the limit, the instruction is a request.

### An example: the reviewer

In my setup there is one custom agent I would keep above all others: the reviewer. It is a checker that sees only the request and the result. Here is the top of its file:

::: code harness .github/agents/reviewer.agent.md L1-L8 "The header of the reviewer: the tools line is the limit, the model line is a fallback list, the description is a request to the model that calls it."

The `tools` line gives it tools for reading, searching and running commands, and none for changing files. So it cannot "just fix it". `agents: []` means it cannot start other subagents. The model is a fallback list, so if the first model cannot be used, the next one is. The reasons for each choice are in [Use subagents sparingly](2-3-subagents.html). What matters here: every line of the header that changes behavior is a tool limit, a model, or a boundary of context. The description only asks. The body mostly says what to look at and what to hand back.

### Three facts that bit me

**"Hidden" is not "forbidden".** A setting that keeps an agent out of the drop-down list does not stop another agent from calling it as a subagent. Neither does the setting that keeps the model from using it. If "who may call whom" matters, a hook has to decide it ([Hooks](2-2-hooks.html)), not these two settings.

**A hook cannot see which agent is current.** The events a hook receives carry no name for the main agent ([Hooks](2-2-hooks.html)), so rights cannot be handed to "the admin agent": any agent could pass for it. Rights have to follow the session instead, as in my setup, where an admin switch is turned on by the person in a terminal ([Guard the files that hold the rules](4-3-guardrails.html)). I once had an admin agent and retired it.

**A model above the caller may be silently skipped.** I saw this once and have not tested it again: when a subagent's model is a class above the main model, the platform does not run it and says nothing. So "did the check really happen" has to be confirmed by something that is not the model, such as a hook that saves the reviewer's answer to disk. If a check matters to you, keep a record that it ran.

### Test your own setup

Take one role agent you have (a "SQL expert", a "documentation writer"). Does its file list tools, or a model? If neither, move its body into a skill ([Instructions and skills](3-3-instructions-and-skills.html)), give the same task to the default agent with and without the skill, and compare. If you see no difference, the agent was a costume. Run each a few times before you trust what you see.

## Costs and traps {#costs-and-traps}

**More agents are more to keep in step.** Each file has a model name, a tool list and a body that can go out of date. Model names change. A name that no longer matches the drop-down breaks the agent. An agent file sets limits, so in a team change it through code review like any rule.

**A switch may lose the chat.** The VS Code docs say a selected agent applies to your requests until you switch. They do not say what happens to the chat history on a plain switch, and I have not tested it. Keep what matters in files ([Long chats get worse](3-2-long-sessions.html)).

**A role can feel like a limit when it is only a request.** The body says "do not do X" and the agent does X anyway. Only the tool list is a limit.

**Fewer roles than you think.** In my early setup I had three job-title agents (one to coordinate, one to build, one to check). On four small tasks they cost about 4.5 times the usage of one agent and gave no better result ([Use subagents sparingly](2-3-subagents.html)). I kept only the checker. That is four tasks, once each: weak evidence, not a result. Anthropic reports the same direction on a different scale: in their research system, agents use about 4 times the tokens of a chat, and multi-agent systems about 15 times ([How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)). My number and theirs measure different things, so compare only the direction.

## When to delete it {#when-to-delete-it}
{status: industry}

An agent file stays as long as it enforces something a skill cannot: a tool list or a model. Some platforms already let a skill carry tool settings. In Claude Code, a skill's `allowed-tools` only pre-approves tools and does not restrict them, and a separate `disallowed-tools` removes tools while the skill is active ([Skills](https://code.claude.com/docs/en/skills)). Whether such a setting is enforced on your platform is something to check. Where it is, many agent files become unnecessary. And any agent whose only content is "act like an expert in X" can be deleted today.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Find every custom agent file in this project. For each one, report: does its header limit the tools, set a model, or neither; is the description written so a caller knows when to use it and what to say; and which lines of the body are only requests. Mark every agent with no tool limit and no model setting as a likely costume, and say which skill or instruction file could replace it. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- Anthropic: [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Instructions and skills](3-3-instructions-and-skills.html): the other way to change what an agent does

## Explore it in the harness {#explore}

The harness has a very small set of custom agents on purpose: a read-only helper and a checker. You can open both files and compare each line with the table above. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Custom agents". Teach me what is in this harness's agent files: the tool lists, the model lists, and which lines change behavior and which are only requests. Open the real files with me, and show me why there are so few agents.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
