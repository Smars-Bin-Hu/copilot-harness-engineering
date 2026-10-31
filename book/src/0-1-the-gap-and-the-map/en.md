This chapter assumes only that you have typed a request into an AI chat box.

## In one sentence {#in-one-sentence}

**Harness engineering** is building the rules, checks and limits around a model so that an agent can be trusted with real work. Put the same model in a good harness and it can do far more than it can in a chat box, because most of the gap lies outside the model.

## For leaders {#for-leaders}

- **The decision:** where the team's effort goes: a better model, or the rules, checks and limits around the model.
- **The risk:** if the problem sits outside the model, switching models or turning reasoning effort to the maximum leaves the results just as disappointing, and costs more.
- **The cost of doing it right:** the next chapter starts from the smallest setup that is still useful; after that, the cost is mostly the time to build the setup.
- **Ask the team:** "The last time an agent let us down, was it the model, or was something missing around it, such as a check, a rule, or a file it never got to see?"

## Same model, and the gap is outside it {#problem}

A user reports that the export button sometimes produces an empty file. You paste the report into a chat box, and the model gives you a confident explanation and a code change. But it has never seen your code and cannot run your tests, so whether the change is right is yours to find out. Put the same model in Copilot's agent mode and it searches the code, opens the relevant files and runs the tests. It reads the project's written rules before it touches anything, and when it is done, a check outside the model runs the tests again.

The model did not change, yet the results are far apart, because the difference is outside the model: what it can see, what it can do, which rules it must follow, and who checks the result. The whole set of programs and configuration around the model is called the **harness**.

LangChain measured how much changing only the harness can buy. They kept the model fixed at gpt-5.2-codex and went from 52.8% to 66.5% on Terminal Bench 2.0, a benchmark of 89 terminal tasks. The changes came from the traces of failed tasks. The agent wrote its code, read it over and stopped, so they reminded it to verify against the task spec before it exited. It made mistakes finding files and tools, so at the start they told it what the working directory held and which tools were available. It kept making small edits to the same broken approach, more than ten times in some traces, so after a set number of edits to one file they told it to rethink. ([Improving deep agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering))

The result on reasoning effort is the least intuitive. gpt-5.2-codex has four levels: low, medium, high and xhigh. Running at xhigh throughout scored only 53.9%, while running at high throughout scored 63.6%, because the agent thought for so long that many tasks timed out. In the end they used xhigh for planning and verification and high for writing code, though the different splits scored about the same in trial runs. How much reasoning effort to use is itself a harness setting.

This is one team's own result on one benchmark, but it points the same way as the export-button example: what widens the gap is work the model cannot do for itself, such as checking from outside, getting the environment laid out in advance, and breaking out of a loop.

## Seven layers around the model {#how-it-works}

### From model to agent

Start by taking an agent apart. The **model** (the LLM) is the agent's brain: Sonnet, Opus, GPT-5. It reads text and writes text, and on its own it can only answer questions. To act, it needs **tools**, its hands: reading a file, searching code, editing a file, running a terminal command are each one tool. The model uses a tool by writing a request that names the tool and its arguments ("read src/export.ts"). That request is a **tool call** (details in [When an Agent misuses a tool, check its description and errors first](1-2-tool-calling.html)).

The model can only write the request; it cannot carry it out. So a program has to connect the two. It hands the task to the model, runs the tool the model asks for, passes the result back, and asks for the next step, over and over until the model says it is done. The model, the tools and this loop together make an **agent** (how the loop runs is in [The agent loop, and where you can step in](2-1-agent-loop.html)). The program that runs the loop is the first meaning of harness.

### Two meanings of "harness"

The word has two uses, and mixing them causes confusion. The first is the **general harness**, the program that runs the loop: Claude Code, Codex and Copilot's agent mode are all general harnesses that you download or buy and use as they are. The second is the **team harness**: the layer you build on top of a general harness for your own team, made of rules, skills, checks, limits and reports, plugged into the extension points the general harness leaves open.

This book is about the second kind, with every example built on VS Code Copilot. When I say harness engineering, I mean the work of building that layer.

### Seven layers

A team harness has many small pieces. I sort everything around the model into seven layers, each with a question that stays the same however the tools and models change.

::: figure 0-1-seven-layers

| Layer | Analogy | Examples | Question |
| --- | --- | --- | --- |
| Model | Brain | Sonnet, Opus, GPT-5; reasoning effort | How deeply can it think, and what does it cost? |
| Tools | Hands | Reading and writing files, terminal commands, MCP servers | What can it reach? |
| Runtime | Nerves that connect brain and hands | Copilot's agent mode, Claude Code; hooks, subagents | Who runs the loop, and where does it leave me a way in? |
| Context | Onboarding | Instruction files (AGENTS.md), skills, memory | What should it know, and what should it not read? |
| Control | Computer permissions | Permissions, a hook that blocks dangerous commands | Why should I trust it? |
| Flow | Project process, team rules | Task lists, approvals, when to stop | How is the work split, who decides, when does it stop, when does it call a person? |
| Evidence | Work log, expense report | Logs, task reports, evals | What did it do, was it right, what did it cost? |

The lower three layers are the agent itself: a brain, hands, and the nerves that connect them. They are mostly bought, built by model and platform vendors, and they change fast. The upper four layers are how a company manages a new hire: onboarding, computer permissions, project process, a record of the work. You can hire the person, but how you manage them is up to your company, so these four layers are yours to build, and they depend on your code, your colleagues and the risks you carry. They also last longer: a platform upgrade rarely wipes out your rules, though it may make the workarounds you built for a weaker model unnecessary.

### Where hooks and skills belong

The seven layers cover most of harness engineering. The two pieces most often argued over are hooks and skills. Both are mechanisms the platform provides, yet what you build with them belongs to the upper layers. The test is what a piece is used for, not who provides it.

- A **hook** is a gap the platform (Claude Code, Copilot and others) leaves at fixed events: when an event fires, it runs a command you choose. Common events are PreToolUse (before a tool call), PostToolUse (after a tool call), UserPromptSubmit (when the user sends a prompt) and Stop (when the agent is about to finish). When the event fires, the platform hands the details to your command, such as the tool's name and arguments, and the command can let the call through or block it. The hook mechanism belongs to the runtime; what you attach to it belongs where its purpose puts it. A Python script on PreToolUse that blocks any terminal command containing `rm -rf` is control. A script on PostToolUse that writes every call to a log is evidence. (Details in [Hooks, the point every call passes through](2-2-hooks.html).)
- A **skill** is a folder. Its main file, `SKILL.md`, holds a name, a description and a manual, and scripts and templates can sit beside it. The agent normally sees only each skill's name and description, and reads the full manual only when a task calls for it. The mechanism that loads skills on demand belongs to the runtime; the manual is written for the agent to read, so it is context; the scripts in the folder are run as commands, so they are tools. (Details in [Instructions and skills, load only what you need](3-3-instructions-and-skills.html).)

### Three ways to fail

Control, flow and evidence are separate layers because they fail in different ways.

When control fails, the agent does damage: it deletes the wrong thing or edits a file it should not touch.

When flow fails, the work comes back: the agent takes on too much at once or says it is done too early. Anthropic saw both when Opus 4.5 built a clone of claude.ai across many sessions. "The agent tended to try to do too much at once—essentially to attempt to one-shot the app," and "a later agent instance would look around, see that progress had been made, and declare the job done." Their fixes were all outside the model. The first session wrote a list of more than 200 features, each marked as failing. Every later session worked on one feature at a time, could change only whether that feature passed, and was not allowed to remove or edit tests; when it finished, it committed to git and logged what it had done in a progress file. For testing, the agent was told to use browser automation and act as a real user would, which caught bugs that were not obvious from the code alone. ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents))

When evidence fails, it looks different again: the work may be fine, but nobody can say what happened. You cannot show the result is right, you cannot find the cause of an error, and you cannot tell whether a change helped. When the bill goes up, you cannot tell which task spent it.

When something goes wrong, asking "which kind of failure is this?" usually leads to a fix faster than asking "which model should we switch to?"

## You don't need all seven {#costs-and-traps}

Seven layers side by side can make it look as if a good harness needs something in each. It does not. Every layer you add is one more thing to maintain and one more place to fail, which is why the next chapter ([A minimal harness in 30 minutes](0-2-minimal-harness.html)) starts from the smallest useful set.

A stronger model does help. But the model is bought, and for the same model, most of the difference you can influence comes from the layers around it.

## What LangChain and Anthropic found {#industry}
{status: industry}

The two sources point the same way but show different things. LangChain fixed the model, changed only the harness and saw the score rise, which shows how wide a gap the harness can open. Anthropic describes where failures happen on long tasks (doing too much at once, declaring the job done too early) and the fixes it made with a feature list, a progress file and git. It does not compare against a stronger model, so it cannot say how much switching models would help.

## When to redraw the map, or delete it {#when-to-delete-it}
{status: industry}

If a layer does not help you sort a problem, redraw it. What I would keep is the idea behind the picture: when an agent disappoints you, look at what surrounds the model before you blame the model.

## How to read this book {#how-to-read}

The book spends little time on the lower three layers and most of its pages on the upper four: Parts 1 and 2 cover what you need to know about the lower three, and Parts 3 to 6 each take one of the upper layers.

Every chapter has two parts. **The Knowledge** explains the idea and stands on its own; **In my practice** points to the real files in my own setup, so you can look inside.

If you have little time, read the chapters marked as core; they carry the main line of the book, and the others are there for when a problem sends you to them. If you decide where the team's time and budget go, start with [0.2](0-2-minimal-harness.html), [1.1](1-1-models-and-cost.html) and [7.4](7-4-rollout-and-governance.html).

## Try it on your own setup {#try-it}

::: prompt
Look at how you are set up in this repository: the instruction files, tools, hooks, checks and any written rules. Sort what you find into seven layers: model, tools, runtime, context, control, flow, evidence. For each layer, say what exists, and mark the layers where nothing exists. Then name the one missing piece that would most likely cause a bad result here. Do not change any files.
:::

## Go deeper {#go-deeper}

- LangChain: [Improving deep agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Explore it in the harness {#explore}

Copilot Harness is a team harness in the second sense above. It has a part for each of the four upper layers, and it can walk you through them from the inside, with the real files.

::: prompt
/harness-rookie-wondering I have read the chapter "What is Harness Engineering?". Teach me how a coding agent works in this harness: the loop, the tools, and where the harness steps in. Open the real files with me and draw how the pieces fit together.
:::
