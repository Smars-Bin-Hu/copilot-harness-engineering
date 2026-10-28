This chapter assumes you have used an AI coding agent, such as Copilot in agent mode. Nothing else.

## In one sentence {#in-one-sentence}

Dividing the work has no value in itself. Another agent is worth it only when it buys one of four things: an independent check, parallel work, work that runs unattended, or a hard limit on tools.

## For leaders {#for-leaders}

- **The decision:** approve an extra agent only when it buys one of the four: an independent check, parallel work, work that runs unattended, or a hard limit on tools.
- **The risk:** a team of role agents can cost several times the usage and time for the same result. In my test it was about 4.5 times the usage and 6 times the time, on four tasks run once each.
- **The cost of doing it right:** usually one extra agent, a reviewer, per task.
- **Ask the team:** "Which of the four does this agent buy, and did you try the task without it?"

## The problem {#problem}

I once gave one AI three job titles. On the same four tasks it cost about 4.5 times as much, took about 6 times as long, and got nothing more right. Now one agent does the work, and a second one only checks.

First, three words this chapter uses all the time.

- An **agent** is an AI model that runs in a loop: it reads files, runs commands, changes code, and decides the next step by itself.
- Its **context** is everything it has seen in one conversation: your request, the files it read, what it tried. It is the agent's working memory, and it has a size limit.
- A **subagent** is a second agent that the first one starts for a piece of the work. It begins with an empty context.

### The idea that feels right

Give the AI job titles: a planner, a developer, a reviewer, each its own agent. Teams of people work that way, and many tools make it a few clicks.

I built exactly that in an early version of my own Copilot setup. A **coordinator** read the request and wrote a plan. A **builder** made the changes. A **reviewer** checked them. Then I measured it against one agent working alone.

### How I tested it

- **The repository:** a made-up data engineering project, 93 files in 5 areas. Made up, so the tasks and the right answers were known in advance.
- **Four tasks, small to medium:** add a pipeline; add a field across several areas; rename a pipeline and delete its old files; fix a formula, where the request also asked to change a file that must not be touched.
- **Two ways:** each task was done once by the three-role team, which also had a knowledge base to read (notes about the repository, written for agents). And once by a single agent on a top model, with no extra setup and the rules written into the request.
- **Scoring:** the same script checked every result by reading the files. Nobody judged by eye.
- **What I counted:** did it pass on the first try, how much usage it took (AI credits, what the platform charges you), and how long.

::: figure agents-vs-roles

Both ways got all four right. So the team bought nothing in correctness, and paid about 4.5 times the usage and about 6 times the time.

Before you quote these numbers: four tasks, each run once, and the two sides were not set up the same way. Trust the direction (the team cost several times more for the same result), not the exact ratio. [Costs and traps](#costs-and-traps) says more.

### Where the extra cost went

I read the records of each run. The biggest waste was the handover. The coordinator studied the task carefully: it read the request and the files, and understood what had to change. Then it wrote a short plan and handed it over. The builder started with an empty context, read the plan, and had to study the same files again. The same understanding was paid for twice.

::: figure handoff-relearn

### Why job titles do not help an AI

1. **People split roles because of human limits.** No one learns every specialty, a day has 8 hours, and one person cannot be in two places at once. A model does not have these limits. Its real limit is the size of its context, and the four cases in the next section are all about that.
2. **A title carries no knowledge; a fitted setup does.** "You are a designer" changes the tone, not what the agent knows. Two things do help: the know-how of the field written in files that any agent can read, and a set of tools fitted to the job. The first needs no second agent. The second can be a reason for one (case 4 below).
3. **Handoffs lose understanding.** That is the picture above. Understanding has to be squeezed into a summary to be handed over, and the next agent needs more than the summary to act.
4. **What a fixed rule can decide, do not leave to a model.** "Who works next" and "is it finished" often have fixed answers. A small program answers them right every time; a model answers them right most of the time.
5. **Rework starts from zero.** In my setup, every round of checks starts a new reviewer, which reads the work again from the start.

## How it works {#how-it-works}

### What a subagent can and cannot do

Think of a subagent as a contractor you send a written brief to:

- **It sees only the brief.** It cannot read your conversation or your notes.
- **It cannot call you back.** If the brief is missing something, it guesses or stops.
- **It sends back a report, not its understanding.** Everything it read stays with it.

So before you split off any work, ask one question: **will a short report be enough for the main agent to go on?**

If yes, a split can work. If the main agent needs everything the helper understood, do not split. A designer handing work to a developer fails this test: the developer needs everything the designer understood, not a summary of it.

Passing the test is not enough. The split also has to buy something one agent cannot get alone. There are four such things.

### 1. An independent check

When you proofread your own essay, you read what you meant, not what you wrote. An agent checking its own work has the same problem: its context is full of its own reasoning, and that reasoning leads it past its own mistakes.

A checker who has never seen that reasoning reads only the request and the result. If the result does not match, it sees it. That checker is a **reviewer**. It has to be a separate agent, because it needs a separate context.

::: figure independent-check

A separate context is needed, but it is not enough. The reviewer is often the same model, with the same blind spots, and it can be wrong: fail good work, or pass bad work. So an independent check lowers the risk; it does not remove it.

**How to build a good one:**

- **Give it a package, not the conversation:** the request, the changed files, and the diff (exactly which lines changed). Leave the author's notes out on purpose.
- **Take away its tools to change files.** It cannot "just fix it", even when it wants to.
- **Let it point out, not fix.** If it wrote the fix, the next check would be checking its own solution.
- **Every finding names a file and a line.** What it cannot point to is not a finding. This keeps out vague worries.
- **Fix the first line: PASS or FAIL.** Then a small program can read the verdict, without asking another AI what the reviewer meant.
- **Limit the rounds.** A few checks per task; after that, a person decides. From the second round on, report only what affects correctness, or the checks never end over wording.

### 2. Parallel reading

Some questions need a lot of reading. "What does each of these five areas own, and what are its rules?" One agent would read the five areas one after another. That is slow, and by the end its context is full of raw material it no longer needs.

Instead, the work can be split the way big data jobs are split: **map** each part to a helper that reads it and writes a short summary, then **reduce** the summaries into one answer. The method is called **map-reduce**, and each helper is a **mapper**. The parts are read at the same time, and the main agent only ever sees the summaries.

::: figure parallel-read

**This is where several agents clearly win.** Anthropic built a research system on this pattern: a lead agent plans, and subagents search different directions at the same time. On their internal research tests it beat a single agent (Claude Opus 4) by 90.2%, and it shines on broad questions that split into independent directions. The price: such systems use about 15 times the tokens of a chat. They also note that most coding tasks have fewer truly parallel parts than research. ([How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system))

So the test is two questions: does the job split into parts that do not need each other, and is the answer worth several times the cost?

This only works for reading. If several helpers changed the same files at the same time, someone would have to merge their changes, and conflicts hide in a merge.

**How to build it:**

- **The person switches it on, not the agent.** It costs several times as much, and that is your decision. A small program counts the helpers (for example, four within an hour), so the agent cannot start more. Only a command the person types counts; the agent cannot type it for itself.
- **Each mapper can read and search, nothing else.**
- **Every brief has three parts:** the question, the scope (which files or folders to read, and only those), and what to hand in. Anthropic saw what vague briefs do: helpers duplicate work, leave gaps, or misread the task. Early versions even started 50 subagents for a simple question.
- **Every summary has a fixed shape:** conclusions, each with the file and line it comes from; what it could not find; what it is not sure of.

### 3. Work that runs unattended

Normally an agent stops after each step and waits for you. Sometimes you want to hand over a whole to-do list and come back when it is done.

**The simplest version** needs a **hook**: a small program that the tool runs at fixed moments. Copilot and Claude Code both have them. Here the moment is "the agent has stopped". The hook looks at the to-do list. If a step is still open, it tells the agent to go on. Only the person can switch this on, for one task at a time.

It also needs to know when to stop pushing. Each stop rule catches a different way it can go wrong:

- **A cap on steps and on time** (for example, 20 steps or 2 hours): a runaway run cannot spend all night.
- **Stop after a few refusals** (for example, two): when the agent keeps trying things it is not allowed to do, something is wrong, and a person should look.
- **Stop when nothing moves** (for example, three pushes in a row with no step done): the agent is stuck in a loop.

In this simplest version, one agent does every step. That is fine for a short list. On a long one, its context fills up with everything from the earlier steps: files it read for step 2, commands it ran for step 5, a test that failed and was fixed. By step 15 it is carrying fourteen steps of leftovers, and an overfull context forgets and mixes things up.

**The better version** works like a site manager on a building site. The manager does not lay bricks. They keep the plan and the checklist, give each job to a worker on a written job card, and tick the job off when the worker reports back. The manager's head stays clear, because the details of each job stay with the worker who did it.

::: figure autorun-manager

1. **You hand over the whole to-do list.** The main agent takes your place as the one in charge.
2. **For each step, the main agent writes a brief** (what to do, which files, what "done" looks like, how to test it) and starts a fresh subagent: a worker.
3. **The worker does the step and its tests**, writes down what it did, and reports back in a few lines: done or not, tests passed or not, which files changed.
4. **The main agent ticks the step off** and starts a new worker for the next step. Its own context only ever holds the plan, the checklist and the short reports.
5. **When every step is done, the reviewer checks the whole result.** If it fails, the main agent starts a worker to fix what the reviewer found.

Why does this split work, when the three-role team did not? The team split one piece of work by phase: one agent understood it, and another had to act on that understanding. Here the split is by piece. Each worker gets a whole small job, both the doing and the testing, and the main agent needs only "done, tests pass" to go on. That passes the summary test.

The price:

- **Every brief must be complete.** The worker cannot ask back, so whatever it needs has to be written down.
- **Every worker starts from zero.** It reads its files again, so many small steps cost more than one agent doing them in a row.
- **A report is not proof.** A worker that says "tests pass" may be wrong, and the main agent, seeing only reports, cannot tell. That is why the independent check at the end matters, and why the main agent should open the files of a step now and then.
- **Steps that depend on each other's details do not fit.** If step 4 needs to know exactly how step 3 was done, either write that down for the next worker or keep both steps with one agent.

So it pays for a long list of steps that each stand on their own. For a short list, one agent is still cheaper. And if you are there to watch, splitting a long task into several smaller tasks gets most of the same benefit.

### 4. A hard limit on tools

Each agent has a list of tools it may use: read files, search, run commands, change files. In Copilot it is the `tools` list in an agent file; Claude Code's subagents have one too. The platform enforces that list. An agent without the "change files" tool cannot change a file, however it is asked.

The main agent usually has every tool. If a job must not change anything, telling the main agent "please do not change files" is only a request. Giving the job to a subagent that has no such tool makes it a rule.

::: figure tool-limit

### Make it a rule, not a request

How do you make sure no other subagent runs? Writing "do not start other subagents" in the instructions is only a request: the model follows it most of the time.

A hook makes it a rule. One that runs just before any subagent starts can read the subagent's name and say yes or no. It runs every time, and the model cannot talk it out of its answer. A good refusal also says what to do instead, so the agent does not try the same thing again.

### Hand over through files

Agents should not send each other messages. Give each piece of work its own **task folder**, holding the request, the plan, the to-do list and the results of every check. Agents hand over by writing files there.

This buys three things at once. You can open the same files and see what happened. If you stop for a day, the next session picks the work up from the files. And afterwards, the folder is a record of who did what and what the checks said.

::: figure subagent-map

### Test your own setup

**Three questions** for any extra agent, in your own setup or in a proposal you are asked to approve:

1. Which of the four does it buy?
2. Will a short report be enough for the main agent to go on?
3. Did you try the same task without it?

**A test you can run today, with no extra setup.** Take a task you know the right answer to. Do it twice in your own tool. Once, ask the agent to check its own work. Once, open a new chat, give it only the request and the result, and ask it to check. Compare what each one found.

**To compare two setups fairly:**

- Run each one several times, not once. An agent does not do the same thing twice.
- Score both the same way, ideally with a script.
- Write down three numbers: was it right, how much usage, how long.
- Do not decide from a single run.

**To repeat my test.** The made-up repository, the four tasks and the scoring script are in [`labs/subagents/`](../labs/subagents/README.md). They work with any agent tool.

## Costs and traps {#costs-and-traps}

**How sure I am.** Sure of the direction, not of the exact ratio. Two reasons:

- **Each task ran once.** Run it again and the numbers move.
- **The two sides were not equal.** The single agent used a top model and had no extra setup. The team had a knowledge base to read. Each difference could push the numbers either way.

A gap of four to six times is large enough to take seriously. To be sure of it, the test has to be run several times.

**What I did not measure.** A vague request in a very large, messy repository. That is where splitting might pay off. I have no data either way.

**What the extra money did buy.** Once, the builder missed two references across areas. The reviewer caught them and sent the work back, with no person stepping in. That is why I kept the reviewer when the rest of the team went.

**Parallel reading is not free.** Every mapper starts from an empty context and reads its part from zero. Four mappers cost several times one agent. Use it when the reading is too much for one context, not to save time on a few files.

**Subagent usage is easy to miss.** A tool often shows the usage of the main conversation only. Check whether yours counts subagents too.

**A count is not a budget.** Limiting how many helpers start does not limit what they spend together. The better design gives the main agent and all its subagents one budget, and a subagent gets what is left of it, not a fresh one of its own.

## What the industry says {#industry}
{status: industry}

The platform makers agree on the direction: more agents, many more tokens.

- **Anthropic's research system** (above): about 15 times the tokens of a chat, worth it for broad research, less so for most coding. ([How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system))
- **Claude Code** has *agent teams*: several agents that act as a team and message each other. Its docs say they "use approximately 7x more tokens than standard sessions when teammates run in plan mode" (plan mode: each teammate plans before it acts). That is a different setup from my test, so the numbers do not compare directly. Agent teams are experimental and off by default. ([Manage costs](https://code.claude.com/docs/en/costs))
- **VS Code**: "Keep agent chains as shallow as practical and limit tools to what each agent actually needs." ([Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide))

None of them says one agent is always better. Together with my test: for one task with a clear request, do not orchestrate; for broad work that splits into independent parts, several agents can be worth their cost.

## When to delete it {#when-to-delete-it}
{status: industry}

The hooks in this chapter (allow only named subagents, count the helpers, push an unattended run) exist because the platform does not do these things yet. When Copilot itself can allow only named subagents and cap the usage of the main agent and all its subagents together, drop the hooks.

The reasoning does not retire with them. Two things would make me look again at the split itself:

- **The platform can resume a finished subagent.** Rework would stop starting from zero, and a thin coordinator inside one task might pay off. I have not tested whether Copilot can do this today.
- **A comparison shows a self-check catches everything an independent check catches.** Then even the reviewer can go.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
List every custom agent, subagent or role this project defines (look in the agent and instruction files). For each one, tell me which of these it buys: an independent check, parallel work, work that runs unattended, or a hard limit on tools. Mark any that buys none of them, and say what would break if it were removed. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Claude Code docs: [Manage costs](https://code.claude.com/docs/en/costs)
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)

## Explore it in the harness {#explore}

Most of this chapter runs in Copilot Harness: the reviewer, parallel reading, the simplest unattended run, the tool limits, the hook that refuses other subagents, and the task folder. The harness can teach it to you from the inside, with the real files and code. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Use subagents sparingly". Teach me how this harness builds what it describes: subagents (topic 10), independent checks (topic 11), and the unattended run (autorun). For each one, open the real files and code with me, and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
