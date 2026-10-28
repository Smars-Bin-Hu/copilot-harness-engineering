This chapter assumes you have read [Instructions and skills](3-3-instructions-and-skills.html). The rules, their owners and their review are in [Roll out and govern a harness](7-4-rollout-and-governance.html).

## In one sentence {#in-one-sentence}

With an agent doing more, a person's work moves up to four judgments: what to do, what is allowed, where to say yes, and whether the result is good. A new teammate needs one habit and one real task, not the full tour.

## For leaders {#for-leaders}

- **The decision:** decide who in the team makes each of the four judgments, and decide that a newcomer starts with one habit and one real task.
- **The risk:** I have no numbers. The risk I can name is this: if the first hour is the full tour, a newcomer decides the setup is heavy and goes back to what they did before. And a setup that holds only if every person reads the rules is weaker than one that refuses the dangerous thing by itself.
- **The cost of doing it right:** a first hour per newcomer, plus the time to pick one small task from the team's own work.
- **Ask the team:** "Who decides what is allowed, where a person must say yes, and whether the result is good, and what does a new person do in their first hour?"

## The problem {#problem}

When one person uses an agent, the person does all four jobs without noticing. They know what they want, they know what the agent may touch, they decide when to stop and look, and they judge the result. Hand the setup to a team and these jobs have to be assigned, or nobody does them.

There is a second problem, and it is about people, not rules. **Some colleagues will not read anything.** They did not ask for an agent. If their first hour is a lecture, they go back to what they did before.

I should be honest about my own position. I built my setup for one person and I have not run a team rollout with measurements. What follows is a design built from what the setup already does and from my own use. Where something is only a proposal, I say so.

## How it works {#how-it-works}

### What stays with a person

First, what the people are for. The more the agent does, the more a person's work moves up, away from typing and toward four judgments the agent cannot make for you.

::: figure 7-1-person-moves-up

1. **What to do.** A request is vague and it shifts. A person confirms the one page that says what "done" means ([The agent writes the requirement, the person confirms it](5-2-requirements.html)).
2. **What is allowed.** The rules, and who may pass them. Who owns them and who reviews a change is the subject of [Roll out and govern a harness](7-4-rollout-and-governance.html).
3. **Where to say yes.** The points that cost money, grant power or cannot be undone ([Two gates: where a person approves](5-3-two-approvals.html)).
4. **Whether the result is good.** An agent's report can be wrong. A person, or a check the person trusts, decides ([Can a model check a model?](5-6-model-checks-model.html)).

A team needs all four, and the second is the one that no tool will do for you.

### Getting a new person started

The failure to avoid is the full tour. Two gates ([Two gates: where a person approves](5-3-two-approvals.html)), a board ([Ten things at once: parallel tasks](7-2-many-tasks.html)), a knowledge base and reports on the first day tell a newcomer that this is heavy ([A minimal harness in 30 minutes](0-2-minimal-harness.html)). A better first hour has three parts.

1. **A guided setup that checks itself.** A skill walks them through the steps one by one (the install, their name and language, the repositories, the knowledge base) and runs a check after each. The newcomer is never left wondering whether it worked.
2. **One small real task, from the team's own work.** In my setup the first lesson ends in a practice task, and its scenario is a file that a team can replace with its own. Practice on the code they will really touch, not on a toy.
3. **A way to ask why.** A newcomer who can ask the harness to explain itself, with the real files open, needs no one to sit beside them.

### The colleague who does not care

For the colleague who does not care, I would ask for one habit, not a mindset: say what you want done and open a task for it. The rest is carried by the setup. Dangerous commands are refused whether or not the person has read a rule, and a write needs approval whether or not they remember why. A harness that depends on every person reading the rules is a worse harness. I have not measured how this lands with a team that did not choose it.

### What to learn, and what to skip

How much should people study? **Learn the problems that stay the same**: whom to trust, how to know it is right, what the agent should know, how to split work, what it costs. **Skip what changes monthly**: the setting names of one tool, the details of each new plugin system, which model is best this week. An hour on what a new thing is, and which old problem it answers, is enough. Look up the exact format when you need it.

## Costs and traps {#costs-and-traps}

**A guided first hour needs maintenance.** The practice task and the checks go stale when the code changes. Someone has to own them.

**A small real task can still be the wrong one.** Pick one that is real but forgiving: a mistake should cost the newcomer a retry, not a bad day.

**One habit is not enough forever.** It gets the person started. Over time they will meet the gates and the reports, and the first hour should not hide them.

**I have no team data.** The first hour and the one habit are a design built on one person's use. I have not measured how newcomers take to them. Treat them as a starting point to check, not as results.

## When to delete it {#when-to-delete-it}

The guided setup exists because installing and configuring the harness takes many steps. If the setup shrinks to one command, or the platform does it, the guide can go. The four judgments do not go. They are what remains for a person however much the agent does.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Pretend you are a new teammate who has never used an AI agent here. Read this repository's README and its agent instruction files, and write down your first hour: what you would have to install, read and learn before you could finish one small real task. Then, for each of these four judgments (what to do, what is allowed, where a person must say yes, whether the result is good), say where in this repository it is written down, or that it is not. Mark anything that would make a newcomer think the setup is heavy. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Roll out and govern a harness](7-4-rollout-and-governance.html): who owns the rules, who reviews a change, and in what order to widen.
- [A minimal harness in 30 minutes](0-2-minimal-harness.html): what a newcomer should have on day one.
- [Two gates: where a person approves](5-3-two-approvals.html): where the "yes" belongs.

## Explore it in the harness {#explore}

The guided first setup and the first lesson run in Copilot Harness. The harness can show them to you with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "People and teams". Teach me how this harness gets a newcomer started: the guided first setup, the first lesson and its practice task that a team can replace with its own. Open the real files with me, and show what a new person sees in the first hour.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.