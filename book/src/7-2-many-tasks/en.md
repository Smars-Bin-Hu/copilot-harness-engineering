This chapter assumes you have read [Use subagents sparingly](2-3-subagents.html) and [Manage tasks, not chats](5-1-tasks.html).

## In one sentence {#in-one-sentence}

To run ten things at once, run ten separate tasks with one agent each, and call the person only at the gates. Split by task, not by file, although read-only work inside a task can still go to subagents.

## For leaders {#for-leaders}

- **The decision:** decide whether people may run several tasks at once, how many they start with, and where a person is called.
- **The risk:** the limit is a person's attention, not the number of agents, and a gate that is always approved without reading is decoration. I have no evidence of a net speed-up, because I have not measured ten tasks in parallel against ten in a row.
- **The cost of doing it right:** usage grows with the number of tasks (ten tasks, ten times the usage), and you need a board or a simple list of what waits. Start with two or three.
- **Ask the team:** "Which tasks are waiting for a person right now and since when, and what happens if two of them change the same files?"

## If one agent is good, why not run ten? {#problem}

An agent can get a lot done while you are away, so the next thought comes naturally: if one agent is good, why not run many at once? There are two ways to read that thought, and only one of them works.

The first reading is one big job with many agents. When you hand over a large task, a coordinator splits it among a team of agents, each with a role such as plan, implement or check. The whole thing looks like a company org chart. That is the setup [Use subagents sparingly](2-3-subagents.html) tested, and what it found was that handovers lose understanding and that every agent reads the same files again. That chapter does not argue against a fresh worker for each step of one task. What it argues against is several agents changing the same files at the same time, because then someone has to merge their work.

The second reading is many jobs with one agent each: ten requests from ten people, say, or ten different problems of your own. Each one is a separate piece of work with its own folder, its own agent and its own finish line. Since nothing is shared between them, nothing needs to be merged. This is the reading the rest of the chapter follows. It is not clever, but it is what lets one person keep ten things moving.

Run work that way and the thing in short supply is not agents. It is you. An agent can wait for a person for hours without using any compute, but what it waits with goes stale: the conversation's cache expires, and by the time you answer, the repository may have moved on. The waiting is costly on your side too, because a person who keeps ten agents in mind soon loses the thread. So the design question becomes how to spend one person's attention across ten tasks.

## Split by task, and call the person only at the gates {#how-it-works}

### Parallel across tasks, not inside one

The first half of the answer is in how the work is split. Each task is a folder, as in [Manage tasks, not chats](5-1-tasks.html), so the requirement, the plan, the to-do list and the handover file all live in files. Since one agent session holds one task at a time, ten tasks are ten folders and ten sessions.

::: figure 7-2-ten-lanes

Why does this split cleanly when splitting one big job does not? The first reason is that nothing is shared. Each task has its own folder and only one writer, so two agents never edit the same file at the same moment, and there is nothing to merge inside a task. The second is that each task is whole. The agent that does the work holds the plan and the context as well, so nothing has to pass from an agent that understood to an agent that must act. That handover was the cost of the three-role setup described above. When a task does change hands, the hand-off is a file rather than a message: if it stops for a day, whoever picks it up reads the folder.

The agents do not talk to each other. The only thing that crosses between tasks is you.

### When does a task need you?

You are what crosses between tasks, so the other half of the answer is when a task needs you. Were the answer "often and unpredictably", ten tasks would eat your day. So the design pushes every need for a person into a few fixed points, the **gates**, where the agent stops and waits for a person's yes (the details are in [Two gates: where a person approves](5-3-two-approvals.html)).

A task waits for you only for reasons like these:

- the first gate: the requirement is written and the plan is ready, and both wait for you to confirm and approve;
- the second gate: the write-back (copying the finished changes into the repository) waits for your approval;
- a write failed halfway;
- it needs the results of a run that only you can do;
- its independent checks are used up and you decide what next;
- the agent stopped, or an unattended run ended.

Between those points the agent works and you are not needed. That is the whole idea: **call the person only at the gates.** The worst case is a task that needs you "now and then, when it has a question", because you cannot plan around it. A task that asks only at named points, by contrast, can be scheduled.

This also tells you what to build. Anything that makes the agent stop for a reason that is not a gate, such as a vague request, a missing permission or a confirmation box for a harmless action, is a leak in your attention and worth removing ([Ask or refuse](4-2-ask-vs-refuse.html)).

### Tasks that touch the same code

The agents never talk, but their work can still collide, and that is the common case. Separate task folders do not make separate repositories, so two tasks that change the same files will meet when they are written back. Start by giving each task its own branch or working copy (git worktree is one way). Then, when a task is written back, check whether the files it touches changed since it began. If they did, stop and ask a person. Either way, write back one task at a time.

### Attention is the expensive part

Even when the write-backs are in order, running ten tasks does not make you ten times faster. What it does is move your time to the gates, and a gate is only worth something if you read it.

That raises the question of what makes reading cheap. A plan you approve should fit on a page and sit in an editor, not scroll through a terminal. A requirement you confirm should be one page too ([The agent writes the requirement, the person confirms it](5-2-requirements.html)). If reading takes twenty minutes, you will skim, and a skimmed approval is the "click Allow" problem again. One number worth watching is how often you reject or change a plan. If it is never, you may be skimming.

How fast you can read plans and diffs, not how many sessions fit on the screen, is also what sets how many tasks you should hold. Start with two or three. How many you can hold well depends on the tasks.

The same reasoning says to group similar gates. If three plans are waiting, read them in one sitting, because switching between a plan, a diff and a requirement costs more than reading three plans.

Attention is not the only thing ten tasks multiply. Ten tasks are also ten times the usage, so put a stop rule on each one ([Unattended: when it must stop](5-7-when-to-stop.html)). A task that waits for you for longer than the prompt cache lives (five minutes or an hour on Anthropic's API, see [Models and cost](1-1-models-and-cost.html)) pays full price to read its context again when you return. I have not checked how Copilot behaves here.

### One list of what waits for you

With ten sessions open, how do you know which one is waiting? Going through the windows one by one is exactly the cost you want to avoid.

The answer is a **board**: one page that lists every open task, what it is waiting for and for how long. Two design points make it worth looking at.

::: figure 7-2-board

One is that the state is written by code, not by the agent. A hook runs when the agent stops and notes "waiting for you". The board reads that state from a file made for machines. It does not read the progress notes the agent wrote in prose, because an agent forgets to tick things or ticks too many. The other is that waiting is a number, the time since a task started waiting, so the board can also tell you which one to open first.

The same page has a switch that I use at the end of the day. It pauses every open task the agent is not working on and takes them back in the morning. Because the waiting time while paused is not counted, the numbers stay honest.

If you have no board, a list will do. The idea works just as well by hand: one terminal tab per task, titled with the task, and a short list you keep of which tab is waiting and since when.

### Read-only helpers inside a task

The one-agent-per-task rule is about work that writes. Inside one task, helpers that only read can still run in parallel and hand in short summaries, because no helper changes a file ([Use subagents sparingly](2-3-subagents.html)). The shape, then, is one writer per task, and as many readers as the reading is worth.

## What still lands on you, and what I have not measured {#costs-and-traps}

Context switching costs the agents nothing. It lands on you. Each gate needs different knowledge, so ten tasks in ten different domains cost more attention than ten in the same domain.

Skimming has an extreme form, too: a gate that is always yes is a gate you do not read. Approve ten plans in a row without opening one, and the gates are decoration. The remedy is fewer, smaller gates, not more.

The board, for its part, is only as good as its state. If the state came from the agent's own words, the board would lie. That is why, as described above, it comes from hooks and files.

Beyond these costs, I have not compared this with other ways of working. I have no evidence of a net speed-up, because I have not measured ten parallel tasks against ten in a row, or against a team. Nor have I measured how many tasks one person can hold well, or tested ten tasks changing one repository at once to see how often they collide. The argument rests on the structure: nothing is shared, and a person's attention is the limit. The number ten in the title is an illustration, not a result.

## When to delete the board {#when-to-delete-it}

The board exists because a session does not tell you that it is waiting. Once the platform shows, in one place, every running agent session and what each is waiting for, the board can go. I have not checked how far Copilot has got with that.

The idea does not go with it. Even when the platform does the listing, the split stays: one writer per task, and the person called at the gates.

## Try it on your own setup {#try-it}

::: prompt
Using read-only git commands, list the branches, worktrees and open pull requests in this repository that have recent commits. For each, list the files it changes relative to the main branch. Then find pairs that change the same files, and say which would conflict if written back together. For each piece of work, say what it is probably waiting for (review, a decision, a test run). Do not change any files.
:::

## Go deeper {#go-deeper}

- [Use subagents sparingly](2-3-subagents.html): why a team of agents on one task did not pay, and where parallel reading does.
- [Manage tasks, not chats](5-1-tasks.html): the task folder that makes each lane independent.
- [Two gates: where a person approves](5-3-two-approvals.html): what a gate is and how to make the yes real.
- [Unattended: when it must stop](5-7-when-to-stop.html): the stop rules for a task that runs while you are away.
- [Roll out and govern a harness](7-4-rollout-and-governance.html): who owns the rules when more than one person runs tasks.

## Explore it in the harness {#explore}

The task folders, the board and the "waiting for you" state all run in Copilot Harness, and the harness can show you a board with real tasks on it.

::: prompt
/harness-rookie-wondering I have read the chapter "Ten things at once". Teach me how this harness lets one person run several tasks: the task folder, the states a task can wait in, and how the board knows a task is waiting. Open the real files with me, and show me what the board reads and who writes it.
:::
