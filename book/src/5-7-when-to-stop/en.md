This chapter picks up the unattended run from [Use subagents sparingly](2-3-subagents.html), where a hook keeps the agent working down a to-do list while nobody watches. That chapter showed how such a run keeps going. This one is about how it ends.

## In one sentence {#in-one-sentence}

An unattended agent goes only as far as its stop rules reach. Set them in advance, as a total budget and not only a step count, and guard against the agent declaring the job done too early.

## For leaders {#for-leaders}

- **The decision:** before approving an unattended run, set its stop rules in advance, as a total budget and not only a step count, and require a stop to hand back a reason.
- **The risk:** once you leave, you are no longer the stop rule. The run could loop for hours, spend a night's usage on a step that cannot succeed, or stop early and say it is finished. My setup has step and time limits but no total budget yet, and I call unattended runs beta. I have not measured whether an unattended run beats a person watching to the end.
- **The cost of doing it right:** a few rules and one budget number per task. The price of tight rules is more stops, and a person on call in the morning. A vague hand-back, on the other hand, costs more time than watching would have.
- **Ask the team:** "If this runs overnight and goes wrong, what stops it, and what will I find in the morning?"

## When you leave, who stops the run? {#problem}

When you watch an agent, you are its stop rule. You see it go wrong, and you press stop. When you leave, that rule leaves with you. What remains is whatever you wrote down before going.

So the question to ask of an unattended run is not "will it work?" but "what happens when it does not?" It could loop for hours, or spend a night's worth of usage on a step that cannot succeed. It could reach a choice that only you can make and make it anyway. Or it could do the opposite and stop early, saying it is finished.

Each of these needs a different rule, set before you leave. Together they come down to three questions. When must the run stop, what does it hand back when it does, and how do we know it is really done?

## When it stops, what it hands back, and when it is really done {#how-it-works}

::: figure 5-7-stop-points

### Each stop rule catches one way to go wrong

The first question, when the run must stop, has several answers, because each stop rule catches a different way a run goes wrong. What the rules share is one principle: **code judges them from facts, not the agent.** An agent that is stuck is the worst judge of whether it is stuck.

Three of the rules you have already met in [Use subagents sparingly](2-3-subagents.html): a cap on steps and time, a stop after the guardrails refuse the agent twice in a run, and a stop when no step gets ticked. (A **step** is one item on the to-do list. This stop rule is not the breaker of [Guard the files that hold the rules](4-3-guardrails.html), which reacts to one refusal repeating inside a session.) Their numbers are there too. Those are the numbers in my setup, and they are examples, not wisdom: I chose them, and I have not measured whether they are the right ones.

Two more can be judged from facts in the same way. One is a change of plan: the run is allowed to carry out the plan the person approved, so if the plan changes, the permission ends at once. The other is running out of checks: the independent check keeps failing until its limit is reached ([Make a pass count](5-5-counted-checks.html)).

The last kind is different, because some stops cannot be seen in the facts. Say two tables define a field differently and the plan does not say which to use. Only the agent can see that, so it may stop itself, but only with a reason and only for the cases that need a person, not for small choices.

### A budget is a total, not a count

All the rules above count things, whether steps or refusals. But what you are afraid of is **spending**, which a count does not limit. Twenty small steps and twenty steps that each launch helpers are not the same bill.

What limits spending is a **budget**, a total over usage and time that covers the main agent and all its helpers together. A helper gets what is left rather than a new allowance of its own. As soon as either line, usage or time, is crossed, the run stops.

My own setup does not have this yet (it has the counts above and a time limit), but here is a way to build it. The person sets one task-level budget, in usage and minutes. Before each step, a hook adds up the usage of the main session and every helper session from the platform's own session record. At the line, it stops the run and writes "budget" as the reason. Whether the helpers' usage shows up in that record in time to stop on, I have not checked.

And a budget in usage is not quite a budget in money: input the provider has cached is read at about a tenth of the base price ([Models and cost](1-1-models-and-cost.html); how Copilot bills it, I have not checked).

Some tools already offer a simple version for non-interactive runs, though I have not tried them. Claude Code has `--max-turns` and `--max-budget-usd`, both for print mode (`claude -p`) only. The money cap is checked against a client-side estimate rather than your bill and can be passed. Spend from subagents counts toward it, and once it is reached no new subagent can start ([CLI reference](https://code.claude.com/docs/en/cli-reference)).

### What the person coming back should find

Whichever rule fires, a person will come back to a run that has stopped. If it stopped without saying why, what they find is a puzzle. So a stop has to hand back three things:

1. **Why it stopped**, in a word the person can act on: budget, refused, no progress, needs a decision.
2. **Where it is**: the steps done, the step it was on, and the state of the work.
3. **What a person has to decide**, in one sentence.

In my setup, the code writes the reason when it stops on facts, while the agent writes one sentence when it stops itself. The instruction for that sentence asks which step is stuck, why, and what you must decide. "Ran into a problem" is not enough.

The decisions the agent made along the way matter too. For anything the plan left open and the agent chose, it writes a line saying what it chose and why. That log, read when the person returns, is what makes unattended work reviewable.

### When "done" comes too early

So far the worry has been a run that does not stop when it should. The opposite failure is just as real: a run that stops too soon and calls itself finished. Anthropic described it in a long-running coding agent, where "a later agent instance would look around, see that progress had been made, and declare the job done" ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).

After all, stopping is what the agent was asked to do, so it has a reason to say it is done. That is why the end of a run goes by facts that code can check, not by the agent's word:

- **Every step on the list is ticked.**
- **The independent check passed**, counted by code, on the version of the work as it is now.
- **The plan is the one that was approved.**
- **The write-back plan is made**, for a person to read ([Two gates](5-3-two-approvals.html)).

Only then is "done" a state, not a claim.

Even this is not airtight, because an agent can tick a step without finishing it. The checker reads the whole result at the end and the person reads the whole diff, but nothing in code proves that step 7 was really done. That is why I treat ticks as claims and the end-of-run check as the thing that counts.

## What safety costs, and what stop rules cannot do {#costs-and-traps}

All of this makes a run safer, but it is not free. The more rules a run has, the fewer wins it brings home. A run with tight stop rules will stop on many nights and hand back little, so the price of safe is a person on call in the morning. I have not measured whether an unattended run is better than a person watching to the end. That is why my setup still calls it beta.

And a stop is not an answer: each one leaves the work half done. The snapshots taken at the gates ([Two gates](5-3-two-approvals.html)) let a person look at the state the run stopped in. Even so, a vague hand-back costs the person more time than watching would have.

Some work, though, should not run unattended at all, however good the stop rules are. The three points of [Two gates](5-3-two-approvals.html) apply here: work that spends real money, grants power such as writing to a shared repository, or cannot be undone needs a person.

The last trap is for the agent rather than for you: taking a detour to avoid a refusal. A refusal is the system telling you that a step is out of scope, so the rule I give the agent is to change the step once as the reason says, then stop if that does not work.

## When to delete these rules, and what stays {#when-to-delete-it}

The stop rules exist because the platform does not provide them. If the platform gives you a total budget over the whole run, helpers included, use it. The idea of stopping on facts stays either way: the agent's "I'm done" is not a finish line.

## Try it on your own setup {#try-it}

::: prompt
Find every place in this project where an agent can run without a person watching: scheduled jobs, CI steps that call an agent, auto-approve or autopilot settings, loops, background tasks. For each, tell me what stops it (a step or time limit, a spend limit, a refusal count, a check), whether the limit covers helper agents too, and what it leaves behind when it stops: reason, state, and the decision a person must make. Flag any run with no stop rule at all. Do not change any files and do not start any run.
:::

## Go deeper {#go-deeper}

- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Claude Code docs: [CLI reference](https://code.claude.com/docs/en/cli-reference) (`--max-turns`, `--max-budget-usd`)

## Explore it in the harness {#explore}

The stop rules, the facts that decide each stop, and what the agent writes when it stops itself all run in Copilot Harness, where the unattended run is in beta. The budget over helpers is not built yet, but the harness can teach the rest from the inside, with the real files.

::: prompt
/harness-rookie-wondering I have read the chapter "Unattended: when it must stop". Teach me how this harness's unattended run (autorun) decides when to stop (topics 11 and 15): the stop reasons, who judges each one, and what is handed back. Open the real files with me and draw how the pieces fit together.
:::
