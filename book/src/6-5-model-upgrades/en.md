This chapter assumes you have used an AI coding agent and that you have written rules or steps for it. Nothing else.

## In one sentence {#in-one-sentence}

When the model is upgraded, rerun your evals first. Then delete the rules, checks and steps that the new model no longer needs, because scaffolding built for an old model may slow the new one.

## For leaders {#for-leaders}

- **The decision:** after each model change, schedule a review of the setup, and decide who reruns the evals and who may delete a rule.
- **The risk:** rules and steps built for an old model may slow the new one. I have not measured this on an upgrade, so it is a worry rather than a result. Hard limits against damage, the record and the evals are not on the list to cut.
- **The cost of doing it right:** a rerun of your fixed tasks, more than once, plus one person's time to remove one piece at a time. That is mostly money and time, and I have no numbers for it.
- **Ask the team:** "If the model changed tomorrow, which rules would we test removing first, and which evals would tell us?"

## What happens to the scaffolding when the model gets better? {#problem}

Think of the setup around an agent as **scaffolding**, the frame builders put up around a building while they work. Every rule, check and written-out step in it was put there for a reason, to cover something that the model of that day got wrong, did badly or forgot.

Then the model is upgraded. The reasons were about the old model, and with a new one some of them are gone. Nobody told your setup.

This is a real worry, though I have not measured it on an upgrade. What I do have is the history of my own harness, whose first version had levels and three job-title agents. The three agents came out after a few days of use, on the evidence in [Use subagents sparingly](2-3-subagents.html) (that chapter has the cost numbers and their limits), while the levels went for a different reason ([What I cut, and what the data says](7-3-what-we-cut.html)). Both had seemed reasonable at the time they went in. What I take from this is a question rather than a result: might structure built when the model was weaker stop earning its cost once the model improves? If it does, it keeps costing until someone tests it and removes it.

While it stays, scaffolding that no longer earns its place costs in three ways. There is time and money, since every extra step is paid for at every task. There is room, since a long rule file uses part of the context window on every turn ([Context is a budget](3-1-context-budget.html)). And there is confusion, because a rule written for an old model's habit can pull a new model the wrong way, a risk I have not measured.

So which pieces are dead, and how would you know?

## How to find out what the new model no longer needs {#how-it-works}

The rule is simple: **do not delete by feeling, and do not keep by habit. Run the evals.** The picture shows the order in which that happens.

::: figure 6-5-thinner

### 1. Before you upgrade, have something to rerun

Running the evals assumes there is something to run, which is why [fixed tasks](6-3-eval-tasks.html) come first. Without a set of fixed tasks and a script to score them, an upgrade is a change you cannot judge. So keep the set and its old results as your baseline.

### 2. Rerun with only the model changed

If the provider publishes notes on moving from the old model to the new one, read them before the rerun, so that you know what to watch. Then run the same tasks on the new model with the same setup, making sure the model is the only thing you changed, and compare the results with the baseline. Even so, more than quality can move: a new model can tokenize text differently, change the default amount of thinking and miss the prompt cache at first. Each of these changes cost without changing quality, so record them next to the numbers.

The rerun then tells you one of two things. Either something got worse (a rule that held with the old model may not hold with the new one), and you want to know that before you remove anything. Or the results got better or held, in which case the gap to look at is the cost: time, usage, turns. Either way, runs differ ([One run proves nothing](6-4-variance.html)), so run each more than once, or you will read noise as a result.

### 3. What does not go, whatever the evals say

Before you start removing, it is better to know that some things should not be on the list at all. They start with hard limits against damage: a refusal to touch production, a guard on the rule files, a person approving what cannot be undone. None of these depends on how clever the model is, because they protect against what happens if it is wrong or fooled. **A better model is not a reason to remove them** ([Some things you never hand over](4-5-least-privilege.html)). The record stays too, because a better model still needs a log, a report and a person to read them ([Record what happened](6-1-observe.html)). And the evals stay, because they are how you decide everything else.

The pieces you may cut do not all age at the same speed. Text (rules and steps) changes first and is the easiest to cut. Enforcement in code changes more slowly, and on the evidence of the evals. A platform change sits underneath all of it.

### 4. Take out one piece at a time

Now you can ask of each piece of scaffolding: does the new model still need it? You find out by removing it and running the tasks again. Take out one piece per round, because if you take out two, you will not know which one mattered.

For a piece like an independent check, the experiment is direct: run the tasks with the check on and with it off, and compare. If the evals show no difference, the check is not earning its cost for those tasks ([Use subagents sparingly](2-3-subagents.html) has the same reasoning for the second agent). But if it still catches things, keep it.

### 5. What I would look at first

Which pieces would I try first? The table lists the parts that I expect to be the first candidates in my own setup. They are things to test, not results, because I have not rerun them after a model upgrade.

| Part | Why it may change | What I would do |
| --- | --- | --- |
| Written-out playbooks for kinds of work | A newer model may need steps spelled out less | Shorten them. Keep the lists of what counts as done: they say what you want, not how to get it ([Manage tasks, not chats](5-1-tasks.html)) |
| Independent checks | A model may check itself more reliably | Compare no check and one check. Only if the evals show no difference between them does the default become no check |
| Reminders and workarounds | They cover a habit the old model had | Test with them off ([Turn your way of working into skills](3-4-skills-and-workflows.html) says the same of "gotchas") |
| Rules moved into code because the model ignored them | The new model may follow them | Switch the code rule off where a breach can be undone, and count ([A rule in a prompt is a request](4-1-requests-and-rules.html)) |
| Which model each role uses | New models come out | Change the one setting, and run the tasks |
| Wording tuned for the old model | Emphasis written to be heard by one model may be too strong for another | Rewrite it plainly and run the tasks |

The table is only my guess. The fuller list is already in the book. Almost every chapter ends with a section on when to delete what it describes. After an upgrade I go through those sections in order, asking of each one whether its condition now holds.

### 6. Write down what you deleted, and when you would put it back

When I take something out, I write one line: what, why, and what evidence would bring it back. That line is what keeps the setup from becoming a guess, because when the next model is worse at something, you know which line to look at. (The same habit runs through [What I cut, and what the data says](7-3-what-we-cut.html).)

### Test your own setup

Three questions are worth asking about your own setup:

1. If the model were upgraded tomorrow, what would you rerun to find out whether your setup still works?
2. Which rule or step do you keep only because you added it once?
3. Which one would hurt if it were removed, and how do you know?

There is also a test you can run today. Pick one rule or step in your setup that you suspect is dead weight, then choose three tasks where it should matter. Copy the rule file first, so that you can put the rule back. Then run the tasks with and without it, more than once, and compare pass and usage. If you cannot tell the two apart, you have learned something. If it does matter, you have learned what the rule is worth.

## The risks of removing, and the price of rerunning {#costs-and-traps}

The procedure itself has risks and a price. Removing a piece is a change like any other and can break things, which is why you remove one piece at a time and run the evals after each.

Even then, your claim stops at the edge of the evals: you can only say that a piece is not needed for the tasks you tested. If the tasks are few, say so and be careful with anything that guards against damage, because a new model can be worse than the old one at some tasks.

Each rerun also costs money, so a full rerun after every model release is not always affordable. Rerun when you change model family, when the version number changes, or when you notice a change in behaviour. The cache can skew the sum as well. On Anthropic's API, cached reads cost about a tenth of the base input price ([Models and cost](1-1-models-and-cost.html)), but the first runs on a new model start cold. How Copilot bills any of this, I have not checked.

There is a subtler risk, too: scaffolding can hide a weak spot. A check that always caught the same mistake may be the thing that kept you from noticing it, so when you remove it, look at the failed runs.

## When to delete this procedure {#when-to-delete-it}
{status: industry}

This chapter is itself a procedure for deleting, so what is there to delete? The step-by-step rerun. If a platform tells you, on your own tasks, what an upgrade changed, or runs your evals on each release, I would use that. What stays is the habit: nothing in the setup is permanent, and every piece has to earn its place against the model you have now.

## Try it on your own setup {#try-it}

::: prompt
List every rule, step and check in this repository's agent instruction, skill and hook files. Sort each into one of: hard limit against damage, record or log, workaround for a habit of an older model, written-out playbook, or emphasis in the wording. For each workaround, playbook or emphasis, say from git history what failure it was added for, or "no reason found". Then name the five I should test removing first after a model upgrade, and which of my tasks should be rerun to check. Do not change any files.
:::

## Go deeper {#go-deeper}

- In this book: [Fixed tasks, scored by a script](6-3-eval-tasks.html), [One run proves nothing](6-4-variance.html), [What I cut, and what the data says](7-3-what-we-cut.html)

## Explore it in the harness {#explore}

Copilot Harness keeps two lists that go with this chapter, one of what it expects to change first after a model upgrade and one of what it chose not to build, with when it would reconsider. The harness can walk you through both.

::: prompt
/harness-rookie-wondering I have read the chapter "When the model is upgraded, delete". Teach me what this harness expects to change after a model upgrade (topic 15) and what it will never remove. For each part, open the real files with me and show how I would test whether it is still needed.
:::
