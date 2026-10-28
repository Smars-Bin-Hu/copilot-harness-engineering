This chapter assumes you have read [Use subagents sparingly](2-3-subagents.html) and [Manage tasks, not chats](5-1-tasks.html).

## In one sentence {#in-one-sentence}

The three job-title agents cost the most and bought nothing I could measure. Removing them, along with levels and a separate coordinator, made the harness simpler. Only the first removal was measured.

## For leaders {#for-leaders}

- **The decision:** ask of every agent, rule and step what it bought and what would make it safe to remove, and set a time to review the answers.
- **The risk:** setups only grow, so every part keeps costing context, upkeep and learning time. The one cut I measured was three job-title agents against one agent: several times the cost for the same number right, on four tasks run once each.
- **The cost of doing it right:** an hour to list the parts and write one line for each. The harder cost is telling the people already using a part what replaces it.
- **Ask the team:** "For each agent, rule and step: what did it buy, how do you know, and what would make it safe to remove?"

## The problem {#problem}

Every part you add to an agent setup has a price. It takes room in the context, it has to be kept true, and a newcomer has to learn it. Most setups only grow, because adding feels like progress and removing feels like losing something.

I want to ask a different question of each part: **what did it buy, and when can it go?** If I cannot answer the first, the part is a cost with no return. If I cannot answer the second, I will keep it forever.

Version 1.0 of my own setup was a good test of this. It had several parts that sounded right. I shipped it, used it, and after a few days of use, in version 1.1, I took out a large share of it. This chapter lists what I cut and why. It keeps one line clear throughout: **for each cut, what I measured and what I only judged.**

A few words first.

- A **level** was a choice the user made at the start of each job: a light level for a quick answer, a middle one for a medium task, a heavy one for several agents working together. Different levels had different rules.
- A **coordinator** is an agent whose only job is to hand work to others (the word is used as in [Use subagents sparingly](2-3-subagents.html)). In my old heavy level it was a separate agent.
- A **request folder** was a separate folder, apart from the task, where the heavy-level team kept its plan, its handovers and its results.
- A **job-title agent** is an agent given a role like planner, builder or reviewer, as in a team of people.

## How it works {#how-it-works}

### At a glance

The four cuts, with how much evidence each has. The sections below give the reasons.

| Cut | What it was meant to buy | Why it went | Evidence | Reconsider when |
| --- | --- | --- | --- | --- |
| Three job-title agents | A division of labour like a human team | Several times the cost, same result | Measured: 4 tasks, one run each, direction only | A comparison on a larger, messier task shows a gain |
| Levels | Rules matched to the difficulty of a job | Only one was used; hard to choose; rules clashed | My experience of use, no count | How hard a job is can be reliably told before it starts |
| Separate coordinator | Someone to hand out the work | The one that understands is not the one that acts; the worker learns it again | Reasoned; a clue in the test records, not measured alone | The platform can restore the context of a finished subagent |
| Request folder | A separate place for a team's files | Nothing needed it once the team was gone | Follows from the other cuts, untested | A flow comes back that needs its own workspace |

### The test I use for any part

Your setup also only grows, so these questions are for you. Before I keep a part, I ask the same few questions (the ones in [Roll out and govern a harness](7-4-rollout-and-governance.html)): what failure does it prevent, with a real example? What does it cost? What would have to change for it to go? The cuts below are those questions, answered late, after use.

::: figure 7-3-before-after

The picture shows the two versions. The lit box is the one cut I measured. The dashed boxes are the cuts I did not measure.

### Cut 1: the three job-title agents (measured)

In 1.0, the heavy mode ran a team: a coordinator wrote the plan, a builder made the changes, a reviewer checked them. I compared it with one agent working alone on the same four tasks. That test is in [Use subagents sparingly](2-3-subagents.html), so I will not repeat it. Only what limits it matters here.

- **Four tasks, each run once.** Run it again and the numbers move.
- **The two sides were not equal.** The single agent used a top model; the team had a knowledge base to read ([A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)).
- **What I trust is the direction.** The team cost several times more, with the same number right. I do not trust the exact ratio.

So this cut has data, and the data is thin. It is enough to say the team did not pay on those tasks. It does not say a team never pays. I kept one role, the independent reviewer, because an independent check is one of the four things worth a second agent. That is reasoning, not a measurement: I did not test the reviewer alone, to the same standard as the cut that I did measure.

### Cut 2: levels (design history, no data)

I did not measure levels. What I have is what I saw using them.

- Only the middle level got used. The light and the heavy ones sat idle most of the time.
- Choosing a level first was one more step every time.
- Two sets of rules side by side confused the agent. It gave wrong explanations about which applied.
- The deeper reason: how hard a job is cannot be told before it starts. A level asks you to guess.

This is my own experience over a few days, not a count. I did not log how often each level was used. What replaced levels is the task, with care set by what a mistake would cost and the kind of the task ([Manage tasks, not chats](5-1-tasks.html)).

### Cut 3: the separate coordinator (reasoned, partly from the test)

The problem was not whether the coordinator understood the task. It did. The problem was that the one that understood was not the one that acted, so the worker it handed the task to had to learn it again. That matches what I saw in the records of the three-role test: the coordinator read the files and understood the change, and the builder started from nothing and read them again.

The test compared the whole team with one agent, not the team with and without a separate coordinator, so I have no number for the coordinator alone. The double reading in the records is a clue, not a measurement. The rest is an argument: whoever moves a task forward has to understand it, and the agent that holds the task already does.

### Cut 4: the request folder (design history, no data)

The heavy-level team kept its work in a request folder, separate from the task folder. Once the heavy-level flow was gone, a second place to keep a job's files had no use. The task folder is the workspace. One place is easier to find, to back up, and to read for a person or a new session. I did not test this. It follows from the other cuts: nothing needed it any more.

### What the cuts took out, and what it did to the harness

The 1.1 release removed the levels, the whole heavy-level flow with its commands, two agents, a skill, some numbers in the configuration and the request folder. It also shortened the rules that are injected at the top of every prompt to three or four lines, and it dropped the limits on the count of searches and tool calls. The agent now sees fewer rules, and fewer ways to be confused.

This is the benefit I trust most, and it is not a measurement. A smaller harness is easier to explain, to test and to hand to a colleague ([Roll out and govern a harness](7-4-rollout-and-governance.html)). I did not measure the effect on accuracy or cost.

### Things I chose not to build

A cut removes something that existed. There is a second list: things I decided not to build, each with the condition that would make me reconsider. A few examples:

- **Agents sending messages to each other.** A subagent has no state, and messages across sessions were not verified. Reconsider when it is measured to be reliable.
- **Several subagents changing the same files at once.** Merge conflicts, and the code cannot be run to judge who is right. Reconsider when the repository can run its tests locally.
- **My own sandbox, context compression or subagent scheduling.** The platform keeps changing these, and I would rather wait for the platform.
- **Features built on Preview or experimental settings.** They can change or vanish. Reconsider when they are stable.

The habit behind the list: a "no" that comes with a reason and a condition can be reopened. A "no" with neither becomes a taboo.

## Costs and traps {#costs-and-traps}

**Cutting is also a bet.** The three-role team lost on four tasks, one run each, in a made-up repository. A very large, messy repository with a vague request may be different, and I have no data either way. If your tasks look like that, test before you copy my cut.

**Do not read "multi-agent is bad" from this.** I kept an independent reviewer, on reasoning that I did not test. I use read-only helpers for broad reading ([Use subagents sparingly](2-3-subagents.html)). What I cut is splitting one piece of work by job title.

**An unmeasured cut is a judgment.** Levels, the separate coordinator and the request folder went on reasoning and use. A reader could disagree, and I could be wrong. I have written which is which so that you can.

**Do not cut and forget.** Write down why a thing went and when to reconsider, in the same place as the reason you added it. Without that, someone adds it back a year later for the same reason.

**Old setups need an exit.** Taking out the old flow broke a request in progress, and anyone with old settings had to change them by hand. The 1.1 notes say so. Removing a part has a cost to the people already using it. When you remove one, say what replaces it, how to move, which old settings stop working, and what happens to work in progress.

## When to delete it {#when-to-delete-it}

The best time to review a cut is after a model upgrade. The reasons behind my cuts were facts about the models and the platform of that month. Models get better at long tasks, and the platform may one day let a finished subagent be resumed, which would remove the relearning cost behind the coordinator cut. Re-run the same fixed tasks and see ([Fixed tasks, scored by a script](6-3-eval-tasks.html)).

The list of "not built, reconsider when" is itself a thing to prune ([When the model is upgraded, delete](6-5-model-upgrades.html) uses the same habit for the rules you keep). When a condition has been met, build it or strike it out.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
List every custom agent, skill, rule, hook and check this repository defines for AI agents. For each, write two things: what it bought (a failure it prevented, with a real example from git history or issues if one exists), and what would make it safe to remove. Mark each answer "measured", "seen" or "only reasoned". Put the parts with no stated purpose first. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Use subagents sparingly](2-3-subagents.html): the measured cut in full, and the four things a second agent can buy.
- [Manage tasks, not chats](5-1-tasks.html): what replaced the levels.
- [Roll out and govern a harness](7-4-rollout-and-governance.html): the questions to ask before keeping any rule or part.
- [Model upgrades](6-5-model-upgrades.html): reviewing what is still needed after a model change.

## Explore it in the harness {#explore}

The 1.0 design is gone from the current harness, but its release notes and design notes remain, with the reasons. The harness can walk you through them. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "What I cut". Teach me topic 15, the design choices: why there are no Levels, and the list of what the harness deliberately does not do and when each would be reconsidered. Open the release notes of version 1.1.0 with me, and show what was retired.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
