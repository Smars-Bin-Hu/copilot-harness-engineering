This chapter assumes you have read [Guard the files that hold the rules](4-3-guardrails.html), [Instructions and skills](3-3-instructions-and-skills.html) and [Record what happened, not what the agent said](6-1-observe.html).

## In one sentence {#in-one-sentence}

Rolling an agent setup out to a team is mostly a question of who owns the rules and who reviews changes to them. Widen it only when the logs show the rules hold.

## For leaders {#for-leaders}

- **The decision:** name an owner for each layer of rules, require a second reviewer for any change to them, and agree what has to be true before the setup goes to the next team.
- **The risk:** without owners, the rules drift into one copy per person and stale rules stay. I have no team data, so I cannot put a number on it. The chapter gives the design I would use, not a measured result.
- **The cost of doing it right:** mostly people's time: owners for the core and each area, and a reviewer's time on every rule change. The setup itself adds little.
- **Ask the team:** "Who owns this rule, who reviewed the last change to it, and what would the logs show if it were wrong?"

## The problem {#problem}

A setup that suits one person has one owner by accident: that person. They write the rules, they notice when a rule is wrong, and they know why each one is there. Hand the same files to ten colleagues and three things go wrong, none of them about the tools.

- **Copies drift.** Everyone fixes the rules for their own task, in their own copy. After a month there are ten versions, and no one can say which one is "the rules".
- **Nobody owns a rule.** A rule that was right last year is now wrong, and everyone has learned to ignore it. Rules go stale unless someone is paid in attention to prune them.
- **A change breaks someone else.** Tightening a rule for one project blocks another team's normal work. The person who made the change never sees the damage.

A fourth worry is a leader's: after the rollout, how do you know what the agents did? That needs a record that someone looks at.

I should be honest about my own position. I built my setup for one person and I have not run a team rollout with measurements. What follows is the design I would use, built from what the setup already does (the parts I can point to), and from the questions I ask before adding anything. Where something is only a proposal, I say so.

## How it works {#how-it-works}

### Who owns the rules

The question "who owns the rules" has no single answer, because not all rules are alike. I split them into three layers, by who is hurt when one is wrong.

::: figure 7-4-rule-layers

- **The core.** The short rules every task must follow, and the files that enforce them (the fence from [Guard the files that hold the rules](4-3-guardrails.html)). A mistake here reaches everyone. It has one or two named owners, and nobody else edits it.
- **The team layer.** Domain skills, the team's knowledge base (an index of the code, see [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)), and settings that are the same for everyone, such as which paths no agent may touch. Each area has one owner: the person who knows that part of the code. A skill about deployment belongs to whoever deploys.
- **The personal layer.** A user name, a language, the folder where your repositories sit on your machine. It belongs to the individual. It is not committed, because it holds paths that exist on one computer only.

Two mechanisms make this workable in my setup, and a team can copy the idea without the tool.

**An override is a small config next to the default, not a copy of it.** It lists only what you change. A person who wants to add one forbidden path writes one line; they do not fork the whole rule file. So the team's customisation stays a few lines that anyone can read, and an upgrade of the core does not collide with it. In my implementation the core's guardrails cannot be removed by an override: if an override drops them, the engine puts them back and reports an error. The setup's health check also lists what every override changes, which gives a reviewer one place to look.

**One rule has one main source.** The same rule written in three files is how copies drift ([Instructions and skills](3-3-instructions-and-skills.html)). When you assign owners, assign them to sources. A rule with two homes has two owners, which means none.

### Who reviews a change to a rule

A rule file is not documentation. It is what the agent obeys, so changing it changes what the team's agents do tomorrow. I treat it like code, with four habits.

1. **The agent does not edit the rules.** The files are fenced. A person opens the fence for one session, makes the change, closes it, and reads the diff in git afterwards ([Guard the files that hold the rules](4-3-guardrails.html)). That leaves a diff that someone else can review.
2. **The author is not the only reviewer.** The owner of the layer reads the change, and so does someone who was not in the discussion. Treat a rule change like a change to code that an attacker would love to make: a careless or hostile pull request, or a shared skill or knowledge-base file that carries instructions the agent will read as its own, is a way in ([Text the agent reads can give it orders](4-6-untrusted-input.html)). Agree who may approve exceptions, and who takes over a layer when its owner leaves. A rule that makes sense only to its author is a poor rule for an agent too: it will read it cold.
3. **The review asks six questions.** They are the ones I ask before adding anything to my own setup.
   - What failure does this prevent? Is there a real example, log or measurement?
   - Does the platform already do it? Did anyone read its current docs?
   - What does it cost, in context, tokens and time?
   - Is it a request in words, or a rule in code ([A rule in a prompt is a request](4-1-requests-and-rules.html))? Is that the right one for the harm?
   - When can it be deleted? What would have to change?
   - If we moved to another tool, would what we learned still be useful?
4. **A claim of "this helps" needs the same tasks before and after.** If the change is meant to improve results, the review should ask for a before-and-after on fixed tasks ([Fixed tasks, scored by a script](6-3-eval-tasks.html)), not an opinion.

One more rule helps the review. **Write down only what the model gets wrong.** A line the model would follow anyway costs context and gives a reviewer more to read. If you cannot name an error it prevents, leave it out.

### Audit: what the setup leaves behind

A leader who was not there needs to answer "what did the agents do, and who let them?". That is an audit. It works only if the setup writes records that the agent does not control, so here is what mine writes. The first five are built; the last two are ideas.

- **One log line per tool call.** The kind of call, whether it was let through or refused, which rule refused it, and how long it took. No arguments and no prompt text, except that a refused call keeps its path and command ([Record what happened, not what the agent said](6-1-observe.html)).
- **Refusals, and a count of them.** A statistics command sums the prompts, the calls and the refusals, and which part of the setup refused.
- **Approvals.** Each task's approvals are kept as records that only a person can create, and the task's report shows the time of both.
- **The task report.** Written by code when a task closes: what was asked, what changed, how many checks and the verdict of each, and what was refused ([A report a person can read in five minutes](6-2-task-report.html)).
- **Changes to the rules.** The agent cannot edit the rule files. A person does it in a session where every logged call is marked as admin, and the change is a diff in git.
- **Idea, not built: who approved.** The approval records carry a time. I have not checked whether they carry a person's name, and my setup has one user, so I never needed it. A team does.
- **Idea, not built: one place for the logs.** In my setup the logs stay on each computer and are not put into git. I have not built any way to gather them across a team.

Who looks, and how often? In my own setup I read the log when a run fails and when I change a rule, not every day ([Record what happened, not what the agent said](6-1-observe.html)). For a team I would add a short routine, as a proposal: the owner of each layer looks at the refusal counts now and then, and reads the diff of every rule change. A log that nobody owns is not an audit trail.

### A rollout in stages

Going wide first and adding review later is how you get ten copies. So I would widen in stages, and I would write down, for each stage, what has to be true before entering it.

::: figure 7-4-rollout-stages

1. **One team, core only.** Pick a team that wants the setup and owns its own code. Give the core to one or two owners from day one. *Enter when:* the team asks for it. Nothing needs to be proven yet.
2. **Add the team layer.** Domain skills, shared settings and the knowledge base come after the team has used the core long enough to know what it needs. *Enter when:* the core has named owners, and the owner can say what happened in a recent task from the records, not from the agent's summary.
3. **Open it to the next team.** *Enter when:* the review habit works in the first team. Every rule change had a second reviewer, the diff was read, and any change meant to improve results came with a before-and-after on fixed tasks.
4. **Everyone, including the colleague who did not ask for it.** *Enter when:* the logs show the rules hold. The signals are in the next section.

These conditions are my proposal. I have not run them on a team, and the thresholds (how long is "long enough") are for you to set.

### How you would know it is working

I have no numbers from a team, so this is what I would watch, not what I measured:

- **Do people open tasks, or go around the setup?** Counts of tasks opened, against work done in plain chats.
- **What do the rules refuse, and is it the same thing every week?** A rule that refuses the same normal work is a rule to fix ([Ask or refuse](4-2-ask-vs-refuse.html)).
- **How often does work come back after approval?** Rework after a yes means the gate was read too fast.
- **How many local overrides exist, and do they match?** See the fork trap below.

Stage 4 asks that these have stopped moving: the refusals are steady and mostly the ones you meant, rework is low, and the overrides are few. "The logs show the rules hold" means that, and nothing grander.

### How strong the evidence in this book is

Read the rest of the book with these limits in mind.

- **One platform.** Everything was built and tried on VS Code Copilot. Other tools have counterparts, but I have not tested them.
- **One person's harness.** I built it and I use it. Nobody else has tested it, and I am not a neutral judge of it.
- **No team data and no incidents.** I have not measured adoption, and I have no record of a rule failing in a team. My one measured comparison is four tasks, one run each ([Use subagents sparingly](2-3-subagents.html)).
- **Numbers carry their conditions.** Where a chapter gives a figure, it gives the run count and the setup next to it, so you can see how far to trust it.

So use the book for its questions and its design, and not as proof. Take a design from it, state what you expect it to do, and check that on your own tasks ([Fixed tasks, scored by a script](6-3-eval-tasks.html), [One run proves nothing](6-4-variance.html)). Your numbers should replace mine.

## Costs and traps {#costs-and-traps}

**The owner becomes a bottleneck.** If every rule change goes through two people, people stop proposing changes and start keeping private copies, which is the problem you were solving. Keep the core small, so that few changes need the strict path, and let the team layer move fast.

**Review of rules is unglamorous.** No one is thanked for a rule that was not added. Put the owner's time in someone's plan, or the review turns into a rubber stamp.

**A reviewer must be able to judge the rule.** A rule about a deployment path reviewed by someone who has never deployed is only a spelling check.

**Too many local overrides is a fork.** If most users carry the same override, it belongs in the team layer. Look at the overrides now and then, and promote the common ones.

**Logs hold things about people.** A log of every call says when someone worked and what they asked the agent to touch. Decide who may read it and how long it is kept before you collect it centrally.

**A stage gate is only as good as the record.** A hole in the logs ([Record what happened, not what the agent said](6-1-observe.html)) makes "the rules hold" look true when it is not known.

**I have no team data.** The three layers, the review habits, the audit routine and the stages are a design built on one person's use. I have not measured adoption or tracked who edits what in a team. Treat them as a starting point to check, not as results.

## When to delete it {#when-to-delete-it}

The three-layer split exists because the platform gives you files and no way to own them. If your platform lets an organisation publish rules centrally, with its own review, audit and roll-out, use that for the core layer and keep only the team layer yourself. I have not checked what Copilot offers here today, so look at its current docs before building your own.

The review questions do not retire. They are how you decide whether any rule, skill or agent deserves to exist.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Look at the files in this repository that tell an AI agent what to do or what it may not do (instruction files, skills, agent definitions, hook and permission settings). For each one, tell me from git history who last changed it, when, and whether the commit had a reviewer other than the author. List any rule that is written in more than one file. Then list what records exist of what the agent did here (logs, transcripts, reports) and who could read them. Mark every gap. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Guard the files that hold the rules](4-3-guardrails.html): how the fence is held and when a person opens it.
- [Instructions and skills](3-3-instructions-and-skills.html): where rules live and why one rule has one source.
- [Record what happened, not what the agent said](6-1-observe.html): what to record and how to read it.
- [People and teams](7-1-people-and-teams.html): what stays with a person, and how to start a newcomer.
- [What we cut](7-3-what-we-cut.html): the same admission questions, applied to my own setup.

## Explore it in the harness {#explore}

Overrides, the health check, the fenced rule files and the logs all run in Copilot Harness. The harness can show them to you with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Roll out and govern a harness". Teach me how this harness lets a team customise it without forking it (policy overrides, the health check that lists them), how it guards its own rule files, and what its logs and reports record. Open the real files with me, and show where a team's changes go and where they must not go.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.