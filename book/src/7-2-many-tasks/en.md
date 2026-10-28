This chapter assumes you have read [Use subagents sparingly](2-3-subagents.html) and [Manage tasks, not chats](5-1-tasks.html).

## In one sentence {#in-one-sentence}

To run ten things at once, run ten separate tasks with one agent each, and call the person only at the gates. Split by task, not by file. Read-only work inside a task can still go to subagents.

## For leaders {#for-leaders}

- **The decision:** decide whether people may run several tasks at once, how many to start with, and where a person is called.
- **The risk:** the limit is a person's attention, not the number of agents. A gate that is always approved without reading is decoration. I have no evidence of a net speed-up: I have not measured ten tasks in parallel against ten in a row.
- **The cost of doing it right:** usage grows with the number of tasks (ten tasks, ten times the usage), plus a board or a simple list of what waits. Start with two or three.
- **Ask the team:** "Which tasks are waiting for a person right now and since when, and what happens if two of them change the same files?"

## The problem {#problem}

An agent can do a lot while you are away. So the next thought is: if one agent is good, why not run many at once? There are two ways to read that thought, and only one of them works.

**The first way is one big job with many agents.** You hand over a large task, and a coordinator splits it among a team of agents, each with a role (plan, implement, check). This looks like a company org chart. It is the setup that [Use subagents sparingly](2-3-subagents.html) tested: handovers lose understanding, and the same files get read again by every agent. That chapter does not argue against a fresh worker for each step of one task. What it argues against is several agents changing the same files at the same time, because then someone has to merge their work.

**The second way is many jobs, one agent each.** Ten requests from ten people, or ten different problems of your own. Each one is a separate piece of work with its own folder, its own agent, and its own finish line. Nothing is shared between them, so nothing needs to be merged.

This chapter is about the second way. It is not clever, and it is what lets one person keep ten things moving.

The thing in short supply is not agents. It is you. An agent can wait for a person for hours without using any compute. But what it waits with goes stale: the conversation's cache expires, and the repository may have moved on by the time you answer. A person cannot wait for ten agents without losing the thread either. So the design question is: how do you spend one person's attention across ten tasks?

## How it works {#how-it-works}

### Parallel across tasks, not inside one

Each task is a folder, as in [Manage tasks, not chats](5-1-tasks.html): the requirement, the plan, the to-do list and the handover file all live in files. One agent session holds one task at a time. Ten tasks are ten folders and ten sessions.

::: figure 7-2-ten-lanes

Why this splits cleanly where the one-big-job split does not:

- **Nothing is shared.** Each task has its own folder, so two agents never edit the same file at the same moment. There is no merge inside a task, because there is only one writer.
- **Each task is whole.** The agent that does the work also holds the plan and the context. There is no handover from an agent that understood to an agent that must act. That was the cost in the three-role test.
- **The hand-off is a file, not a message.** If a task stops for a day, whoever picks it up reads the folder.

The agents do not talk to each other. The only thing that crosses between tasks is you.

### When a task needs a person

Now the question that matters: when does a task need you? If the answer is "often and unpredictably", ten tasks will eat your day. So the design pushes every need for a person into a few fixed points, the **gates**. A gate is a point where the agent stops and waits for a person's yes (the details are in [Two gates: where a person approves](5-3-two-approvals.html)).

A task waits for you only for reasons like these:

- the first gate: the requirement is written and the plan is ready, and both wait for you to confirm and approve;
- the second gate: the write-back (copying the finished changes into the repository) waits for your approval;
- a write failed halfway;
- it needs the results of a run that only you can do;
- its independent checks are used up and you decide what next;
- the agent stopped, or an unattended run ended.

Between those points, the agent works and you are not needed. That is the whole idea: **call the person only at the gates.** A task that needs you "now and then, when it has a question" is the worst case, since you cannot plan around it. A task that asks only at named points can be scheduled.

This also tells you what to build. Anything that makes the agent stop for a reason that is not a gate is a leak in your attention: a vague request, a missing permission, a confirmation box for a harmless action. Each one is worth removing ([Ask or refuse](4-2-ask-vs-refuse.html)).

### Tasks that touch the same code

This is the common case, so it comes early. Separate task folders do not make separate repositories. Two tasks that change the same files will meet when they are written back. One way to design for it: give each task its own branch or working copy (git worktree is one way), have the write-back check whether the files it touches changed since the task began, and stop and ask a person if they did. Write back one task at a time. I have not tested ten tasks changing one repository at once, so I cannot say how often this bites.

### Attention is the expensive part

Running ten tasks does not make you ten times faster. It moves your time to the gates, and a gate is only worth something if you read it.

- **Keep every gate cheap to read.** A plan you approve should fit on a page, in an editor, not scroll through a terminal. A requirement you confirm should be one page too ([The agent writes the requirement, the person confirms it](5-2-requirements.html)). If reading takes twenty minutes, you will skim, and a skimmed approval is the "click Allow" problem again. A number worth watching is how often you reject or change a plan: if it is never, you may be skimming.
- **Do not hold more than you can read.** The number of tasks you can run is set by how fast you can read plans and diffs, not by how many sessions fit on the screen. Start with two or three. How many you can hold well depends on the tasks, and I have not measured it.
- **Group similar gates.** If three plans wait, read them in one sitting. Switching between a plan, a diff and a requirement costs more than reading three plans.
- **Cost adds up.** Ten tasks are ten times the usage, so put a stop rule on each one ([Unattended: when it must stop](5-7-when-to-stop.html)). A task that waits for you for longer than the prompt cache lives (five minutes or an hour on Anthropic's API, see [Models and cost](1-1-models-and-cost.html)) pays full price to read its context again when you return. I have not checked how Copilot behaves here.

### One list of what waits for you

With ten sessions open, how do you know which one is waiting? Going through the windows one by one is the exact cost you want to avoid.

The answer is a **board**: one page that lists every open task, what it is waiting for, and for how long. Two design points make it trustworthy.

::: figure 7-2-board

- **The state is written by code, not by the agent.** A hook runs when the agent stops and notes "waiting for you". The board reads that state from a file made for machines. It does not read progress notes that the agent wrote in prose, because an agent forgets to tick things or ticks too many.
- **Waiting is a number.** The time since a task started waiting tells you which one to open first.

The same page has a switch that I use at the end of the day. It pauses every open task the agent is not working on and takes them back in the morning. The waiting time while paused is not counted, so the numbers stay honest.

**No board? Use a list.** The idea works by hand: one terminal tab per task, titled with the task, and a short list you keep of which tab is waiting and since when.

### Read-only helpers inside a task

The one-agent-per-task rule is about work that writes. Inside one task, helpers that only read can still run in parallel and hand in short summaries, because no helper changes a file ([Use subagents sparingly](2-3-subagents.html)). A writer per task, and as many readers as the reading is worth.

## Costs and traps {#costs-and-traps}

**Context switching is yours.** The agents do not mind switching. You do. Ten tasks in ten different domains cost more attention than ten in the same domain, because each gate needs different knowledge.

**A gate that is always yes is a gate you do not read.** If you approve ten plans in a row without opening one, the gates are decoration. The remedy is fewer, smaller gates, not more.

**A board is only as good as its state.** If the state came from the agent's own words, the board would lie. That is why the state comes from hooks and files.

**I have not compared this with other ways.** I have no evidence of a net speed-up: I have not measured ten parallel tasks against ten in a row, or against a team. The argument is the structure: nothing is shared, and a person's attention is the limit. The number ten in the title is an illustration, not a result.

## When to delete it {#when-to-delete-it}

The board exists because a session does not tell you that it is waiting. When the platform shows, in one place, every running agent session and what each is waiting for, the board can go. I have not checked how far Copilot has got with that.

The idea does not go. Even when the platform does the listing, the split stays: one writer per task, and the person called at the gates.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

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

The task folders, the board and the "waiting for you" state run in Copilot Harness. The harness can show you a board with real tasks on it. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Ten things at once". Teach me how this harness lets one person run several tasks: the task folder, the states a task can wait in, and how the board knows a task is waiting. Open the real files with me, and show me what the board reads and who writes it.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
