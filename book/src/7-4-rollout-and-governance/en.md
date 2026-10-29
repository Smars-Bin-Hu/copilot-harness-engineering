This chapter assumes you have read [Guard the files that hold the rules](4-3-guardrails.html), [Instructions and skills](3-3-instructions-and-skills.html) and [Record what happened, not what the agent said](6-1-observe.html).

## In one sentence {#in-one-sentence}

Rolling an agent setup out to a team is mostly a question of who owns the rules and who reviews changes to them. Widen the rollout only when the logs show that the rules hold.

## For leaders {#for-leaders}

- **The decision:** name an owner for each layer of rules, require a second reviewer for any change to them, and agree on what has to be true before the setup goes to the next team.
- **The risk:** without owners, the rules drift into one copy per person and stale rules stay. Because I have no team data, I cannot put a number on that, so what this chapter gives is the design I would use, not a measured result.
- **The cost of doing it right:** mostly people's time, both for the owners of the core and of each area and for a reviewer on every rule change. The setup itself adds little.
- **Ask the team:** "Who owns this rule, who reviewed the last change to it, and what would the logs show if it were wrong?"

## What goes wrong when a team shares one person's setup? {#problem}

A setup that suits one person has one owner by accident. That person writes the rules, notices when one is wrong, and knows why each one is there. Hand the same files to ten colleagues, though, and three things go wrong, none of them about the tools.

The first is that copies drift. Everyone fixes the rules for their own task in their own copy, so that after a month there are ten versions and no one can say which of them is "the rules". The second is that no single rule has an owner. A rule that was right last year is wrong now, but everyone has learned to ignore it. Rules go stale like that unless someone is paid in attention to prune them. The third is that a change made for one place breaks another. Tightening a rule for one project blocks another team's normal work, while the person who made the change never sees the damage.

A leader has a fourth worry on top of these: after the rollout, how do you know what the agents did? Answering it needs a record that someone looks at.

I should be honest about where I stand. I built my setup for one person and have not run a team rollout with measurements. What follows is the design I would use, built from what the setup already does (the parts I can point to) and from the questions I ask before adding anything. Where something is only a proposal, I say so.

## Owners, reviews, records, and a rollout in stages {#how-it-works}

### Who owns the rules

Drifting copies and rules nobody owns both lead back to the question of who owns the rules. It has no single answer, because not all rules are alike, so I split them into three layers by who is hurt when one of them is wrong.

::: figure 7-4-rule-layers

**The core** is the short set of rules every task must follow, together with the files that enforce them (the fence from [Guard the files that hold the rules](4-3-guardrails.html)). A mistake here reaches everyone. It has one or two named owners, and nobody else edits it.

Below it sits **the team layer**: domain skills, the team's knowledge base (an index of the code, see [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)), and settings that are the same for everyone, such as which paths no agent may touch. Here each area has one owner, the person who knows that part of the code. A skill about deployment, for example, belongs to whoever deploys.

Last comes **the personal layer**: a user name, a language, the folder where your repositories sit on your machine. It belongs to the individual and is not committed, because it holds paths that exist on one computer only.

Two mechanisms make this workable in my setup, though a team can copy the idea without the tool.

One is the **override**, a small config that sits next to the default instead of copying it and lists only what you change. Someone who wants to add one forbidden path writes one line rather than forking the whole rule file. So the team's customisation stays a few lines that anyone can read, and an upgrade of the core does not collide with it. In my implementation an override cannot remove the core's guardrails: if one drops them, the engine puts them back and reports an error. The setup's health check also lists what every override changes, which gives a reviewer one place to look.

The other is that one rule has one main source. The same rule written in three files is how copies drift ([Instructions and skills](3-3-instructions-and-skills.html)), so when you assign owners, assign them to sources. A rule with two homes has two owners, so in effect it has none.

### Who reviews a change to a rule

Once a layer has an owner, the next question is who checks a change to it. The answer starts from what a rule file is. It is not documentation. It is what the agent obeys, so changing it changes what the team's agents do tomorrow. I treat it like code, with four habits.

The first habit is that the agent does not edit the rules. Because the files are fenced, a person opens the fence for one session, makes the change, closes it, and reads the diff in git afterwards ([Guard the files that hold the rules](4-3-guardrails.html)). What that leaves behind is a diff that someone else can review.

The second is that the author is not the only reviewer. The owner of the layer reads the change, as does someone who was not in the discussion. Treat a rule change like a change to code that an attacker would love to make, because a careless or hostile pull request is a way in, as is a shared skill or knowledge-base file that carries instructions the agent will read as its own ([Text the agent reads can give it orders](4-6-untrusted-input.html)).

Two readers settle this change, but not the ones that come after it. For those, agree on who may approve exceptions and who takes over a layer when its owner leaves. Clarity matters too: a rule that makes sense only to its author is a poor rule for an agent, because the agent reads it cold.

The third habit is a fixed set of questions. The review asks six, the ones I ask before adding anything to my own setup.

- What failure does this prevent? Is there a real example, log or measurement?
- Does the platform already do it? Did anyone read its current docs?
- What does it cost, in context, tokens and time?
- Is it a request in words, or a rule in code ([A rule in a prompt is a request](4-1-requests-and-rules.html))? Is that the right one for the harm?
- When can it be deleted? What would have to change?
- If we moved to another tool, would what we learned still be useful?

One more rule helps the review: **write down only what the model gets wrong**. A line the model would follow anyway costs context and gives the reviewer more to read. If you cannot name an error it prevents, leave it out.

The last habit is that a claim of "this helps" needs the same tasks before and after. If a change is meant to improve results, the review should ask for a before-and-after on fixed tasks ([Fixed tasks, scored by a script](6-3-eval-tasks.html)), not for an opinion.

### Audit: what the setup leaves behind

Review happens before a change goes in, but afterwards a leader who was not there needs to answer "what did the agents do, and who let them?" Answering that is an audit. It works only if the setup writes records that the agent does not control, so here is what mine writes. Five kinds of record are built.

- Each tool call gets one log line: the kind of call, whether it was let through or refused, which rule refused it, and how long it took. The line holds no arguments and no prompt text, except that a refused call keeps its path and command ([Record what happened, not what the agent said](6-1-observe.html)).
- Refusals are also counted. A statistics command sums the prompts, the calls and the refusals, and which part of the setup refused.
- Each task's approvals are kept as records that only a person can create, and the task's report shows the time of both.
- The task report is written by code when a task closes. It says what was asked, what changed, how many checks there were and the verdict of each, and what was refused ([A report a person can read in five minutes](6-2-task-report.html)).
- Changes to the rules leave their own trace. The agent cannot edit the rule files, so a person does it, in a session where every logged call is marked as admin, and the change is a diff in git.

Two more are ideas I have not built. The approval records carry a time, but I have not checked whether they carry a person's name. My setup has one user, so I never needed that. A team does. Nor is there one place for the logs: in my setup they stay on each computer, out of git, and I have not built any way to gather them across a team.

Records still need a reader. So who looks, and how often? In my own setup I read the log when a run fails and when I change a rule, not every day ([Record what happened, not what the agent said](6-1-observe.html)). For a team I would propose a short routine, in which the owner of each layer looks at the refusal counts now and then and reads the diff of every rule change. A log that nobody owns is not an audit trail.

### A rollout in stages

That leaves the order in which to hand all this out. Going wide first and adding review later is how you get the ten copies this chapter started with, so I would widen in stages and write down, for each stage, what has to be true before entering it.

::: figure 7-4-rollout-stages

1. One team, core only. Pick a team that wants the setup and owns its own code, and give the core to one or two owners from day one. *Enter when:* the team asks for it. Nothing needs to be proven yet.
2. Add the team layer. Domain skills, shared settings and the knowledge base come after the team has used the core long enough to know what it needs. *Enter when:* the core has named owners, and the owner can say what happened in a recent task from the records, not from the agent's summary.
3. Open it to the next team. *Enter when:* the review habit works in the first team, meaning that every rule change had a second reviewer, the diff was read, and any change meant to improve results came with a before-and-after on fixed tasks.
4. Everyone, including the colleague who did not ask for it. *Enter when:* the logs show the rules hold. What that looks like is the subject of the next section.

Like the rest of this design, these conditions have not been run on a team, and the thresholds (how long is "long enough") are for you to set.

### How you would know it is working

Stage 4 rests on the phrase "the logs show the rules hold", so it has to mean something you can look at. Without team numbers, I can only say what I would watch, not what I measured.

- Do people open tasks, or go around the setup? Count the tasks opened, against work done in plain chats.
- What do the rules refuse, and is it the same thing every week? A rule that refuses the same normal work is a rule to fix ([Ask or refuse](4-2-ask-vs-refuse.html)).
- How often does work come back after approval? Rework after a yes means the gate was read too fast.
- How many local overrides exist, and do they match? See the trap about overrides, below.

Stage 4 asks that these have stopped moving: the refusals are steady and mostly the ones you meant, rework is low, and the overrides are few. That, and nothing grander, is what "the logs show the rules hold" means.

### How strong the evidence in this book is

If this chapter rests on a design rather than data, so, to a degree, does the whole book. Its limits are worth keeping in mind as you read the rest. Everything was built and tried on one platform, VS Code Copilot. Other tools have counterparts, but I have not tested them. It is also one person's harness: I built it and I use it. Nobody else has tested it, and as its builder I am not a neutral judge of it. I also have no team data or incidents to go on: I have not measured adoption, and I have no record of a rule failing in a team. My one measured comparison is four tasks, one run each ([Use subagents sparingly](2-3-subagents.html)). Where a chapter does give a figure, it gives the run count and the setup next to it, so that you can see how far to trust the number.

So use the book for its questions and its design, not as proof. Take a design from it, state what you expect it to do, and check that on your own tasks ([Fixed tasks, scored by a script](6-3-eval-tasks.html), [One run proves nothing](6-4-variance.html)). Your numbers should replace mine.

## Where governance can go wrong {#costs-and-traps}

Governance has costs of its own, and most of them fall on people. The first is that the owner can become a bottleneck. If every rule change goes through two people, people stop proposing changes and start keeping private copies, which is the problem you were solving. Keep the core small, so that few changes need the strict path, and let the team layer move fast.

Review of rules is also unglamorous, because no one is thanked for a rule that was not added. Put the owner's time in someone's plan, or the review turns into a rubber stamp. And the reviewer has to be able to judge the rule. A rule about a deployment path, reviewed by someone who has never deployed, gets only a spelling check.

Overrides need watching too, since too many local overrides amount to a fork. If most users carry the same override, it belongs in the team layer, so look at the overrides now and then and promote the common ones.

The logs bring a cost of a different kind, because they hold things about people. A log of every call says when someone worked and what they asked the agent to touch. Decide who may read it and how long it is kept before you collect it centrally.

The logs matter in one more way, as the evidence for a stage gate, and a gate is only as good as the record behind it. A hole in the logs ([Record what happened, not what the agent said](6-1-observe.html)) makes "the rules hold" look true when it is not known.

All of this rests on the limit I admitted at the start. The three layers, the review habits, the audit routine and the stages are built on one person's use. I have not measured adoption or tracked who edits what in a team, so treat them as a starting point to check, not as results.

## When to delete the layers, and what stays {#when-to-delete-it}

The three-layer split exists because the platform gives you files but no way to own them. If your platform lets an organisation publish rules centrally, with its own review, audit and roll-out, use that for the core layer and keep only the team layer yourself. I have not checked what Copilot offers here today, so look at its current docs before building your own.

The review questions, though, do not retire. They are how you decide whether any rule, skill or agent deserves to exist.

## Try it on your own setup {#try-it}

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

Overrides, the health check, the fenced rule files and the logs all run in Copilot Harness. The harness can show them to you with the real files.

::: prompt
/harness-rookie-wondering I have read the chapter "Roll out and govern a harness". Teach me how this harness lets a team customise it without forking it (policy overrides, the health check that lists them), how it guards its own rule files, and what its logs and reports record. Open the real files with me, and show where a team's changes go and where they must not go.
:::
