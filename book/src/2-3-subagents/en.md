This chapter assumes only that you have used an AI coding agent, such as Copilot in agent mode.

## In one sentence {#in-one-sentence}

Dividing the work has no value in itself. Another agent is worth it only when it buys one of four things: an independent check, parallel work, work that runs unattended, or a hard limit on tools.

## For leaders {#for-leaders}

- **The decision:** approve an extra agent only when it buys one of the four things above.
- **The risk:** a team of role agents can cost several times the usage and time for the same result. In my test on four tasks, it took about 4.5 times the usage and 6 times the time.
- **The cost of doing it right:** usually one extra agent per task, a reviewer.
- **Ask the team:** "Which of the four does this agent buy, and did you try the task without it?"

## What did a team of role agents buy? {#problem}

I once gave one AI three job titles. On the same four tasks, the three-agent team cost about 4.5 times as much as one agent alone and took about 6 times as long, yet it got nothing more right. Now one agent does the work, and a second one only checks it.

This whole story turns on what each agent can see. An **agent** is an AI model that runs in a loop: it reads files, runs commands, changes code, and decides the next step by itself. Everything it has seen in one conversation, from your request to the files it read and what it tried, is its **context**, which works as the agent's working memory and has a size limit. A **subagent** is a second agent that the first one starts for a piece of the work, and it does not share that memory. It begins with an empty context.

### The idea that feels right

It seems natural to give the AI job titles: a planner, a developer, a reviewer, each its own agent. Teams of people work that way, and many tools make it a few clicks.

I built exactly that in an early version of my own Copilot setup. A **coordinator** read the request and wrote a plan, a **builder** made the changes, and a **reviewer** checked them. Then I measured it against one agent working alone.

### How I tested it

The repository was made up, a data engineering project with 93 files in 5 areas, so that the tasks and their right answers were known in advance. The four tasks on it ran from small to medium. One added a pipeline, one added a field across several areas, and one renamed a pipeline and deleted its old files. The last fixed a formula, but its request also asked to change a file that must not be touched.

Each task was then done two ways. The three-role team did it once, with a knowledge base to read (notes about the repository, written for agents). A single agent on a top model did it once, with no extra setup and the rules written into the request. The same script checked every result by reading the files, so nobody judged by eye. For each run I counted whether it passed on the first try, how much usage it took (AI credits, what the platform charges you), and how long it took.

::: figure agents-vs-roles

Both ways got all four tasks right, so the team bought nothing in correctness for its extra cost. Each task ran once, though, so another run would move the numbers. The two sides were also not equal, because the single agent used a top model with no extra setup while the team had a knowledge base to read, and each difference could push the numbers either way. So I trust the direction, that the team cost several times more for the same outcome, but not the exact ratio. A gap of four to six times is large enough to take seriously, but being sure of its size would take several runs.

### Where the extra cost went

When I read the records of each run, the biggest waste turned out to be the handover. The coordinator studied the task carefully, reading the request and the files until it understood what had to change. Then it wrote a short plan and handed it over. The builder started with an empty context, so after reading the plan it had to study the same files again.

::: figure handoff-relearn

### Why job titles do not help an AI

What the picture shows is true of any handover, because understanding has to be squeezed into a summary before it can be handed over, yet the next agent needs more than the summary to act.

Why, then, do teams of people split roles at all? Because of human limits. No one learns every specialty, a day has 8 hours, and one person cannot be in two places at once. A model does not have these limits. Its real limit is the size of its context, which is what the four cases in the next section are all about.

And a title on its own carries no knowledge. "You are a designer" changes the tone, not what the agent knows. What does help is a setup fitted to the job. That means the know-how of the field, written in files that any agent can read, and a set of tools fitted to the work. The first needs no second agent. The second can be a reason for one (case 4 below).

The team also handed a model decisions it did not need to make. Questions like "who works next" and "is it finished" often have fixed answers, and a small program answers them right every time, where a model answers them right most of the time. So what a fixed rule can decide should not be left to a model. And when the work has to be redone, rework starts from zero: in my setup, every round of checks starts a new reviewer, which reads the work again from the start.

None of this means a second agent never helps, only that it has to earn its place. So when does it?

## When is a second agent worth it? {#how-it-works}

### What a subagent can and cannot do

Think of a subagent as a contractor you send a written brief to. It sees only the brief, not your conversation or your notes. It cannot call you back either, so if the brief is missing something, it guesses or stops. And what it sends back is a report, not its understanding, because everything it read stays with it.

So before you split off any work, ask one question: **will a short report be enough for the main agent to go on?**

If yes, a split can work. If the main agent needs everything the helper understood, do not split. A designer handing work to a developer fails this test, because the developer needs more than a summary.

Passing the test is not enough, though. The split also has to buy something one agent cannot get alone, and there are four such things.

### 1. An independent check

When you proofread your own essay, you read what you meant, not what you wrote. An agent checking its own work has the same problem. Its context is full of its own reasoning, which leads it past its own mistakes.

A checker who has never seen that reasoning reads only the request and the result, so if the result does not match, it sees it. That checker is a **reviewer**, the one of my three roles that I kept (why, I come back to later). It has to be a separate agent because it needs a separate context.

::: figure independent-check

A separate context is needed, but it is not enough. The reviewer is often the same model, with the same blind spots, and it can be wrong either way, failing good work or passing bad work. So an independent check lowers the risk without removing it.

A good reviewer comes down to a few design choices:

- **Give it a package, not the conversation:** the request, the changed files, and the diff (exactly which lines changed). Leave the author's notes out on purpose.
- **Take away its tools to change files**, so it cannot "just fix it", even when it wants to.
- **Let it point out, not fix.** If it wrote the fix, the next check would be checking its own solution.
- **Every finding names a file and a line.** What it cannot point to is not a finding, which keeps out vague worries.
- **Fix the first line: PASS or FAIL.** Then a small program can read the verdict, without asking another AI what the reviewer meant.
- **Limit the rounds.** After a few checks per task, a person decides. From the second round on, report only what affects correctness, or the checks never end over wording.

### 2. Parallel reading

Some questions need a lot of reading, such as "What does each of these five areas own, and what are its rules?" One agent would read the five areas one after another, which is slow, and by the end its context is full of raw material it no longer needs.

Instead, the work can be split the way big data jobs are split. You **map** each part to a helper that reads it and writes a short summary, then **reduce** the summaries into one answer. The method is called **map-reduce**, and each helper is a **mapper**. Reading the parts at the same time answers the slowness, and since the main agent only ever sees the summaries, the raw material never reaches its context.

::: figure parallel-read

**This is where several agents clearly win.** Anthropic built a research system on this pattern, in which a lead agent plans and subagents search different directions at the same time. On their internal research tests it beat a single agent (Claude Opus 4) by 90.2%, and it shines on broad questions that split into independent directions. The price is that such systems use about 15 times the tokens of a chat. Anthropic also notes that most coding tasks have fewer parts that can run in parallel than research does. ([How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system))

So the test comes down to two questions: does the job split into parts that do not need each other, and is the answer worth several times the cost?

Even then, this only works for reading. If several helpers changed the same files at the same time, someone would have to merge their changes, and conflicts hide in a merge.

Parallel reading, too, needs a few design choices to work well:

- **The person switches it on, not the agent.** It costs several times as much, and that is your decision. A small program counts the helpers (for example, four within an hour), so the agent cannot start more. Only a command the person types counts, and the agent cannot type it for itself.
- **Each mapper can read and search, nothing else.**
- **Every brief has three parts:** the question, the scope (which files or folders to read, and only those), and what to hand in. Anthropic saw what vague briefs do: helpers duplicate work, leave gaps, or misread the task. Early versions even started 50 subagents for a simple question.
- **Every summary has a fixed shape:** conclusions, each with the file and line it comes from; what it could not find; what it is not sure of.

### 3. Work that runs unattended

Normally an agent stops after each step and waits for you. Sometimes, though, you want to hand over a whole to-do list and come back when it is done.

The simplest way to do that needs a **hook**, a small program that the tool runs at fixed moments (Copilot and Claude Code both have them). Here the moment is "the agent has stopped". The hook looks at the to-do list and, if a step is still open, tells the agent to go on. Only the person can switch this on, and only for one task at a time.

A hook that keeps pushing also needs to know when to stop. Each stop rule catches a different way the run can go wrong:

- **A cap on steps and on time** (for example, 20 steps or 2 hours): a runaway run cannot spend all night.
- **Stop after a few refusals** (for example, two): when the agent keeps trying things it is not allowed to do, something is wrong, and a person should look.
- **Stop when nothing moves** (for example, three pushes in a row with no step done): the agent is stuck in a loop.

In this simplest version one agent does every step, which is fine for a short list. On a long one, its context fills up with everything from the earlier steps: files it read for step 2, commands it ran for step 5, a test that failed and was fixed. By step 15 it is carrying fourteen steps of leftovers, and a context that full forgets and mixes things up.

A better version works like a site manager on a building site. The manager does not lay bricks. Instead they keep the plan and the checklist, give each job to a worker on a written job card, and tick the job off when the worker reports back. The manager's head stays clear because the details of each job stay with the worker who did it.

::: figure autorun-manager

1. **You hand over the whole to-do list.** The main agent takes your place as the one in charge.
2. **For each step, the main agent writes a brief** (what to do, which files, what "done" looks like, how to test it) and starts a fresh subagent, a worker.
3. **The worker does the step and its tests**, writes down what it did, and reports back in a few lines: done or not, tests passed or not, which files changed.
4. **The main agent ticks the step off** and starts a new worker for the next step. Its own context only ever holds the plan, the checklist and the short reports.
5. **When every step is done, the reviewer checks the whole result.** If it fails, the main agent starts a worker to fix what the reviewer found.

Why does this split work, when the three-role team did not? The team split one piece of work by phase, so one agent understood it and another had to act on that understanding. Here the split is by piece. Each worker gets a whole small job, both the doing and the testing, so the main agent needs only "done, tests pass" to go on, which passes the summary test.

This split still has a price, and two things cause most of it. The first is that every worker starts from zero, with only its brief. It cannot ask back, so the brief must be complete, with whatever it needs written down. It also has to read its files again, so many small steps cost more than one agent doing them in a row. The second is that the main agent sees only reports, and a report is not proof. A worker that says "tests pass" may be wrong, and the main agent cannot tell. So the independent check at the end matters, and the main agent should open the files of a step now and then.

Steps that depend on each other's details do not fit this split at all. If step 4 needs to know exactly how step 3 was done, either write that down for the next worker or keep both steps with one agent.

So it pays for a long list of steps that each stand on their own. For a short list, one agent is still cheaper. And if you are there to watch, splitting a long task into several smaller tasks gets most of the same benefit.

### 4. A hard limit on tools

Each agent has a list of tools it may use, such as reading files, searching, running commands and changing files. In Copilot it is the `tools` list in an agent file (Claude Code's subagents have one too). Unlike an instruction, that list is enforced by the platform, so an agent without the "change files" tool cannot change a file, however it is asked.

The main agent usually has every tool. So if a job must not change anything, telling the main agent "please do not change files" is only a request, while giving the job to a subagent that has no such tool makes it a rule.

::: figure tool-limit

### Make it a rule, not a request

How do you make sure no other subagent runs? Here, too, it comes back to the difference between a request and a rule. Writing "do not start other subagents" in the instructions is only a request, which the model follows most of the time.

A hook makes it a rule. One that runs just before any subagent starts can read the subagent's name and say yes or no. It runs every time, and the model cannot talk it out of its answer. A good refusal also says what to do instead, so the agent does not try the same thing again.

### Hand over through files

Once more than one agent is involved, the work has to pass between them, but they should not send each other messages to do it. Instead, give each piece of work its own **task folder**, holding the request, the plan, the to-do list and the results of every check. The agents then hand over by writing files there.

Why files rather than messages? Because you can open the same files and see what happened. If you stop for a day, the next session picks the work up from the files. And afterwards, the folder is a record of who did what and what the checks said.

::: figure subagent-map

### Test your own setup

You can run a test today, with no extra setup. Take a task you know the right answer to and do it twice in your own tool. The first time, ask the agent to check its own work. The second time, open a new chat, give it only the request and the result, and ask it to check. Then compare what each one found.

If you want to compare two setups fairly, a few habits matter:

- Run each one several times, not once, because an agent does not do the same thing twice.
- Score both the same way, ideally with a script.
- Write down three numbers: was it right, how much usage, how long.

To repeat my test, the made-up repository, the four tasks and the scoring script are in [`labs/subagents/`](../labs/subagents/README.md). They work with any agent tool.

## What the extra cost bought, and what else it costs {#costs-and-traps}

Even in my test, the extra money was not all wasted. Once, when the builder missed two references across areas, the reviewer caught them and sent the work back, with no person stepping in. So when the rest of the team went, I kept the reviewer.

Splitting also has two costs that are easy to miss. The first is that parallel reading is not free, because every mapper starts from an empty context and reads its part from zero. Use it when the reading is too much for one context, not to save time on a few files.

The other is subagent usage, because a tool often shows the usage of the main conversation only. Check whether yours counts subagents too. And even once you can see it, limiting how many helpers start does not limit what they spend together. The better design gives the main agent and all its subagents one budget, so that a subagent gets what is left of it, not a fresh one of its own.

## Do the platform makers agree? {#industry}
{status: industry}

The platform makers agree on the direction: more agents, many more tokens. Anthropic's research system under parallel reading is one example ([How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)). Claude Code has *agent teams*, several agents that act as a team and message each other. Its docs say they "use approximately 7x more tokens than standard sessions when teammates run in plan mode" (plan mode: each teammate plans before it acts). That is a different setup from my test, so the numbers do not compare directly. Agent teams are also experimental and off by default ([Manage costs](https://code.claude.com/docs/en/costs)). The VS Code guide, for its part, says: "Keep agent chains as shallow as practical and limit tools to what each agent actually needs." ([Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide))

None of them says one agent is always better. Read together with my test, they come down to this: for one task with a clear request, do not orchestrate, but for broad work that splits into independent parts, several agents can be worth their cost.

## When to delete the hooks, and when to rethink the split {#when-to-delete-it}
{status: industry}

The hooks in this chapter (allow only named subagents, count the helpers, push an unattended run) exist because the platform does not do these things yet. When Copilot itself can allow only named subagents and give a whole task one usage budget, drop the hooks.

The hooks can go, but the reasoning stays. What would make me look again at the split itself is one of two things. The first is a platform that can resume a finished subagent. Rework would then stop starting from zero, and a thin coordinator inside one task might pay off. The second would be a comparison showing that a self-check catches everything an independent check catches, in which case even the reviewer could go.

## Try it on your own setup {#try-it}

::: prompt
List every custom agent, subagent or role this project defines (look in the agent and instruction files). For each one, tell me which of these it buys: an independent check, parallel work, work that runs unattended, or a hard limit on tools. Mark any that buys none of them, and say what would break if it were removed. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Claude Code docs: [Manage costs](https://code.claude.com/docs/en/costs)
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)

## Explore it in the harness {#explore}

Most of this chapter runs in Copilot Harness: the reviewer, parallel reading, the simplest unattended run, the tool limits, the hook that refuses other subagents, and the task folder. The harness can teach it to you from the inside, with the real files and code.

::: prompt
/harness-rookie-wondering I have read the chapter "Use subagents sparingly". Teach me how this harness builds what it describes: subagents (topic 10), independent checks (topic 11), and the unattended run (autorun). For each one, open the real files and code with me, and draw how the pieces fit together.
:::
