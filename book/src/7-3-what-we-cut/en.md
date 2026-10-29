This chapter assumes you have read [Use subagents sparingly](2-3-subagents.html) and [Manage tasks, not chats](5-1-tasks.html).

## In one sentence {#in-one-sentence}

The three job-title agents cost the most and bought nothing I could measure. Removing them, along with levels and a separate coordinator, made the harness simpler, though only the first removal was measured.

## For leaders {#for-leaders}

- **The decision:** ask of every agent, rule and step what it bought and what would make it safe to remove, then set a time to review the answers.
- **The risk:** setups only grow, so every part keeps costing context, upkeep and learning time. The one cut I measured was three job-title agents against one agent, and the team cost several times as much for the same number right (four tasks, run once each).
- **The cost of doing it right:** an hour to list the parts and write one line for each. The harder cost is telling the people already using a part what replaces it.
- **Ask the team:** "For each agent, rule and step: what did it buy, how do you know, and what would make it safe to remove?"

## What did each part buy, and when can it go? {#problem}

Every part you add to an agent setup has a price. It takes room in the context, someone has to keep it true, and every newcomer has to learn it. Yet most setups only grow, because adding a part feels like progress and removing one feels like losing something.

So I want to ask each part a different question: **what did it buy, and when can it go?** If I cannot answer the first half, the part is a cost with no return. If I cannot answer the second, I will keep it forever.

Version 1.0 of my own setup turned out to be a good test of this, because it had several parts that sounded right. I shipped it and used it, and after a few days of use I took out a large share of it in version 1.1. As I go through what I cut and why, the line I most want to keep clear is **for each cut, what I measured and what I only judged.**

The cuts only make sense against how that version worked. At the start of each job the user chose a **level**: a light one for a quick answer, a middle one for a medium task, or a heavy one for several agents working together, and each level came with its own rules. A **job-title agent** is an agent given a role like planner, builder or reviewer, as in a team of people. The heavy level was built out of them. With several roles, someone has to hand out the work. That is the **coordinator**, an agent whose only job is to hand work to others (the word is used as in [Use subagents sparingly](2-3-subagents.html)), and in the heavy level it was a separate agent of its own. The team kept its plan, its handovers and its results in a **request folder**, a separate folder apart from the task.

Four cuts came out of that design, and they do not all stand on the same kind of evidence.

## Four cuts, and how sure I am of each {#how-it-works}

### At a glance

The table puts the four cuts side by side with the evidence behind each, leaving the reasons to the sections after it.

| Cut | What it was meant to buy | Why it went | Evidence | Reconsider when |
| --- | --- | --- | --- | --- |
| Three job-title agents | A division of labour like a human team | Several times the cost, same result | Measured: 4 tasks, one run each, direction only | A comparison on a larger, messier task shows a gain |
| Levels | Rules matched to the difficulty of a job | Only one was used; hard to choose; rules clashed | My experience of use, no count | How hard a job is can be reliably told before it starts |
| Separate coordinator | Someone to hand out the work | The one that understands is not the one that acts; the worker learns it again | Reasoned; a clue in the test records, not measured alone | The platform can restore the context of a finished subagent |
| Request folder | A separate place for a team's files | Nothing needed it once the team was gone | Follows from the other cuts, untested | A flow comes back that needs its own workspace |

### The test I use for any part

Before the cuts one by one, here is the test behind them. Your setup only grows too, so the questions are as much for you as for me. Whenever I decide whether to keep a part, I ask the same few (the ones in [Roll out and govern a harness](7-4-rollout-and-governance.html)). What failure does it prevent, with a real example? What does it cost? What would have to change for it to go? The cuts below are those questions answered late, after use.

::: figure 7-3-before-after

In the picture of the two versions, the lit box marks the one cut I measured and the dashed boxes are the cuts I did not.

### Cut 1: the three job-title agents (measured)

In 1.0, the heavy level ran a team in which a coordinator wrote the plan, a builder made the changes and a reviewer checked them. I compared it with one agent working alone on the same four tasks. That test is told in [Use subagents sparingly](2-3-subagents.html), so instead of repeating it I will only go through what limits it.

The first limit is size. Each of the four tasks ran only once, and a second run would move the numbers. The second is that the two sides were not equal. The single agent used a top model, while the team had a knowledge base to read ([A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)). With limits like these, why trust the test at all? What I trust is the direction: the team cost several times more and got the same number right. The exact ratio I do not trust.

That is enough to say the team did not pay on those tasks, but not that a team never pays. Not all of the team went, though. I kept one role, the independent reviewer, because an independent check is one of the four things worth a second agent. That is reasoning rather than measurement, since I did not test the reviewer alone to the same standard as the cut I did measure.

### Cut 2: levels (design history, no data)

What I have on levels is what I saw while using them over a few days. I did not log how often each was used, so it is experience, not a count. Only the middle level got used, while the light and the heavy ones sat idle most of the time. Even so, every job began with the extra step of choosing a level. And when two sets of rules sat side by side, the agent got confused and gave wrong explanations of which one applied.

The deeper reason under all of that is that how hard a job is cannot be told before it starts, yet a level asks you to guess it.

What replaced levels is the task, with care set by what a mistake would cost and by the kind of task ([Manage tasks, not chats](5-1-tasks.html)).

### Cut 3: the separate coordinator (reasoned, partly from the test)

The coordinator did understand the task. That was never the trouble. The trouble was that the one that understood was not the one that acted, so the worker it handed the task to had to learn it again. That matches what I saw in the records of the three-role test, where the coordinator read the files and understood the change, after which the builder started from nothing and read them again.

What the test cannot do is single out the coordinator. It compared the whole team with one agent, not the team with and without a separate coordinator. So I have no number for the coordinator alone, and the double reading in the records is a clue, not a measurement. The rest is an argument: whoever moves a task forward has to understand it, and the agent that holds the task already does.

### Cut 4: the request folder (design history, no data)

The last cut followed from the others. The heavy-level team kept its work in a request folder, separate from the task folder, so once the heavy-level flow was gone, a second place to keep a job's files had no use. The task folder is now the workspace. One place is easier to find, to back up, and for a person or a new session to read. I did not test any of this.

### What the cuts took out, and what it did to the harness

In all, the 1.1 release removed the levels, the whole heavy-level flow with its commands, two agents, a skill, some numbers in the configuration and the request folder. It also shortened the rules that are injected at the top of every prompt to three or four lines and dropped the limits on the count of searches and tool calls. The agent now sees fewer rules, and fewer ways to be confused.

That is the benefit I trust most, even though it is not a measurement. A smaller harness is easier to explain, to test and to hand to a colleague ([Roll out and govern a harness](7-4-rollout-and-governance.html)). What the change did to accuracy or cost, I did not measure.

### Things I chose not to build

Cuts deal with things that existed. Beside them I keep a second list, of things I decided not to build, each with the condition that would make me reconsider. A few examples:

- I did not let agents send messages to each other, because a subagent has no state and messages across sessions were not verified. I will reconsider when that is measured to be reliable.
- I did not let several subagents change the same files at once. That would bring merge conflicts, and the code cannot be run to judge who is right, so it waits until the repository can run its tests locally.
- Nor did I build my own sandbox, context compression or subagent scheduling. The platform keeps changing these, so I would rather wait for the platform.
- Features on Preview or experimental settings stay unbuilt too, since they can change or vanish. That waits until they are stable.

The habit behind the list is simple. A "no" that comes with a reason and a condition can be reopened, while a "no" with neither becomes a taboo.

## Where a cut can go wrong {#costs-and-traps}

Even the measured cut is a bet. The three-role team lost in the small comparison above, in a made-up repository. A very large, messy repository with a vague request may be different, though I have no data either way. If your tasks look like that, test before you copy my cut. The other three cuts, levels, the separate coordinator and the request folder, went on reasoning and use rather than data. They are judgments, so a reader could disagree, and I could be wrong. I have marked which cut is which so that you can judge for yourself.

It would be a misreading to take "multi-agent is bad" from any of this. I kept an independent reviewer, on reasoning that I did not test, and I use read-only helpers for broad reading ([Use subagents sparingly](2-3-subagents.html)). What I cut is splitting one piece of work by job title.

Once a thing is cut, write down why it went and when to reconsider it, in the same place as the reason you added it. Without that, someone adds it back a year later for the same reason.

Old setups need an exit. Taking out the old flow broke a request in progress, and anyone with old settings had to change them by hand, as the 1.1 notes say. Removing a part has a cost to the people already using it, so when you remove one, say what replaces it, how to move, which old settings stop working, and what happens to work in progress.

## When to revisit the cuts, and prune the list of what I did not build {#when-to-delete-it}

If cuts are bets, they need a time to be checked again. The best time is after a model upgrade, because the reasons behind my cuts were facts about the models and the platform of that month. Models get better at long tasks, and the platform may one day let a finished subagent be resumed, which would remove the relearning cost behind the coordinator cut. After an upgrade, re-run the same fixed tasks and see ([Fixed tasks, scored by a script](6-3-eval-tasks.html)).

The list of "not built, reconsider when" is itself something to prune ([When the model is upgraded, delete](6-5-model-upgrades.html) uses the same habit for the rules you keep). When a condition has been met, build the thing or strike it out.

## Try it on your own setup {#try-it}

::: prompt
List every custom agent, skill, rule, hook and check this repository defines for AI agents. For each, write two things: what it bought (a failure it prevented, with a real example from git history or issues if one exists), and what would make it safe to remove. Mark each answer "measured", "seen" or "only reasoned". Put the parts with no stated purpose first. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Use subagents sparingly](2-3-subagents.html): the measured cut in full, and the four things a second agent can buy.
- [Manage tasks, not chats](5-1-tasks.html): what replaced the levels.
- [Roll out and govern a harness](7-4-rollout-and-governance.html): the questions to ask before keeping any rule or part.
- [Model upgrades](6-5-model-upgrades.html): reviewing what is still needed after a model change.

## Explore it in the harness {#explore}

The 1.0 design is gone from the current harness, but its release notes and design notes remain, along with the reasons. The harness can walk you through them.

::: prompt
/harness-rookie-wondering I have read the chapter "What I cut". Teach me topic 15, the design choices: why there are no Levels, and the list of what the harness deliberately does not do and when each would be reconsidered. Open the release notes of version 1.1.0 with me, and show what was retired.
:::
