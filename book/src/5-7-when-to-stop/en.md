This chapter picks up the unattended run from [Use subagents sparingly](2-3-subagents.html): a hook keeps the agent working down a to-do list while nobody watches. That chapter showed how it runs. This one is about how it ends.

## In one sentence {#in-one-sentence}

An unattended agent goes only as far as its stop rules reach. Set them in advance as a total budget, not only a step count, and guard against it declaring the job done too early.

## For leaders {#for-leaders}

- **The decision:** before approving an unattended run, set its stop rules in advance, as a total budget and not only a step count, and require a stop to hand back a reason.
- **The risk:** when you leave, you stop being the stop rule. The run could loop for hours, spend a night's usage on a step that cannot succeed, or stop early and say it is finished. My setup has step and time limits but not a total budget yet, and I call unattended runs beta. I have not measured whether an unattended run beats a person watching to the end.
- **The cost of doing it right:** a few rules and one budget number per task. The price of tight rules is more stops, and a person on call in the morning. A vague hand-back costs more time than watching would.
- **Ask the team:** "If this runs overnight and goes wrong, what stops it, and what will I find in the morning?"

## The problem {#problem}

When you watch an agent, you are the stop rule. You see it go wrong and you press stop. When you leave, that rule leaves with you. What remains is whatever you wrote down before going.

So the question for an unattended run is not "will it work?" It is "what happens when it does not?" It could loop for hours. It could spend a night's worth of usage on a step that cannot succeed. It could hit a choice that only you can make, and make it anyway. Or it could do the opposite: stop early and say it is finished.

Each of these needs a different rule, set before you leave. There are three questions: when must it stop, what does it hand back, and how do we know it is really done.

## How it works {#how-it-works}

::: figure 5-7-stop-points

### 1. Kinds of stop rule

Each rule catches a different way a run goes wrong. What is common to them: **code judges them from facts, not the agent.** An agent that is stuck is the worst judge of whether it is stuck.

- **The three basic rules.** A cap on steps and time, a stop after the guardrails refuse the agent twice in a run, and a stop when no step gets ticked. They are in [Use subagents sparingly](2-3-subagents.html), with their numbers. (A **step** is one item on the to-do list. This stop rule is not the breaker of [Guard the files that hold the rules](4-3-guardrails.html), which reacts to one refusal repeating inside a session.)
- **The plan changed.** The person approved a plan; the run is allowed to carry out that plan. If the plan changes, the permission ends at once.
- **The checks are used up.** The independent check keeps failing and its limit is reached ([Make a pass count](5-5-counted-checks.html)).
- **The agent says it cannot go on.** Some stops the facts cannot show: two tables define a field differently and the plan does not say which to use. Only the agent can see that. So it may stop itself, but only with a reason, and only for the cases that need a person, not for small choices.

These are the numbers in my setup. They are examples, not wisdom: I chose them, and I have not measured whether they are the right ones.

### 2. A budget is a total, not a count

The rules above count things: steps and refusals. But what you are afraid of is **spending**. A count does not limit spending. Twenty small steps and twenty steps that each launch helpers are not the same bill.

A **budget** is a total over usage and time, covering the main agent and all its helpers together. A helper gets what is left, not a new allowance of its own. When the first line is crossed, the run stops.

Here is a way to build it; my own setup does not have it yet (it has the counts above and a time limit). The person sets one task-level budget, in usage and minutes. Before each step, a hook adds up the usage of the main session and every helper session from the platform's own session record. At the line it stops the run and writes "budget" as the reason. Whether helpers' usage shows up in the record in time to stop on, I have not checked.

Usage is also not the same as money: input the provider has cached is read at about a tenth of the base price ([Models and cost](1-1-models-and-cost.html)). I have not checked how Copilot bills it.

Some tools already offer a simple version for non-interactive runs. Claude Code has `--max-turns` and `--max-budget-usd`, both for print mode (`claude -p`) only. The money cap is checked against a client-side estimate, not your bill, and can be passed; spend from subagents counts toward it, and once it is reached no new subagent can start ([CLI reference](https://code.claude.com/docs/en/cli-reference)). I have not tried them.

### 3. What a stop hands back

A run that stops without saying why is a puzzle for the person who comes back. So a stop has to hand back three things:

1. **Why it stopped**, in a word the person can act on: budget, refused, no progress, needs a decision.
2. **Where it is**: the steps done, the step it was on, and the state of the work.
3. **What a person has to decide**, in one sentence.

In my setup, the code writes the reason when it stops on facts, and the agent writes one sentence when it stops itself. The instruction for that sentence is: which step is stuck, why, and what you must decide. "Ran into a problem" is not enough.

The decisions the agent made along the way matter too. For anything the plan left open and the agent chose, it writes a line: what it chose and why. That is the log a person reads on return, and it is what makes unattended work reviewable.

### 4. Guarding against "done" said too early

The failure on the other side is just as real. Anthropic described it in a long-running coding agent: "a later agent instance would look around, see that progress had been made, and declare the job done" ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).

The agent has a reason to say it is done: the stop is what it was asked for. So a run should not end when the agent says "done". A tick on the list is itself only a claim, as the next paragraphs explain, so the end of a run goes by the facts:

- **Every step on the list is ticked.**
- **The independent check passed**, counted by code, on the version of the work as it is now.
- **The plan is the one that was approved.**
- **The write-back plan is made**, for a person to read ([Two gates](5-3-two-approvals.html)).

Only then is "done" a state, not a claim.

This is not airtight. An agent can tick a step without finishing it. The checker reads the whole result at the end, and the person reads the whole diff, but nothing in code proves that step 7 was really done. I treat ticks as claims and the end-of-run check as the thing that counts.

## Costs and traps {#costs-and-traps}

**More rules, fewer wins.** A run with tight stop rules will stop on many nights and hand back little. The price of safe is a person on call in the morning. I have not measured whether an unattended run is better than a person watching to the end. In my setup it is still called beta for this reason.

**A stop is not an answer.** The run stops, and the work is half done. The snapshots taken at the gates ([Two gates](5-3-two-approvals.html)) are where a person can look at the state it stopped in. If the hand-back is vague, it costs the person more time than watching would.

**Some work should not run unattended at all.** The three points of [Two gates](5-3-two-approvals.html) apply: work that spends real money, grants power such as writing to a shared repository, or cannot be undone needs a person, however good the stop rules are.

**Do not take a detour to avoid a refusal.** A refusal is the system telling you a step is out of scope. The rule I give the agent is: change it once as the reason says; if that does not work, stop.

## When to delete it {#when-to-delete-it}

The stop rules exist because the platform does not provide them. If the platform gives you a total budget over the whole run, helpers included, use it. The stop-on-fact idea stays: the agent's "I'm done" is not a finish line.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Find every place in this project where an agent can run without a person watching: scheduled jobs, CI steps that call an agent, auto-approve or autopilot settings, loops, background tasks. For each, tell me what stops it (a step or time limit, a spend limit, a refusal count, a check), whether the limit covers helper agents too, and what it leaves behind when it stops: reason, state, and the decision a person must make. Flag any run with no stop rule at all. Do not change any files and do not start any run.
:::

## Go deeper {#go-deeper}

- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Claude Code docs: [CLI reference](https://code.claude.com/docs/en/cli-reference) (`--max-turns`, `--max-budget-usd`)

## Explore it in the harness {#explore}

The stop rules, the facts that decide each stop, and what the agent writes when it stops itself all run in Copilot Harness (the unattended run is in beta there). The budget over helpers is not built yet. The harness can teach the rest from the inside, with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Unattended: when it must stop". Teach me how this harness's unattended run (autorun) decides when to stop (topics 11 and 15): the stop reasons, who judges each one, and what is handed back. Open the real files with me and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.