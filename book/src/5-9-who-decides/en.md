[Requests and rules](4-1-requests-and-rules.html) asks how hard a rule is enforced: as a request, a command or a hook. That is a question about safety. This chapter asks one about cost instead: for each judgment in your workflow, who is the cheapest one that can make it?

## In one sentence {#in-one-sentence}

Give each judgment to the cheapest level that can make it: code first, then a cheap model, then the main model, then a person. Cheap models tend to be weakest at the vague calls (my rule of thumb, not measured).

## For leaders {#for-leaders}

- **The decision:** assign each judgment in the workflow to the cheapest level that can make it well: code first, then a cheap model, then the main model, then a person.
- **The risk:** giving everything to the main model wastes usage, gives different answers on different days and is slow. Pushing everything into code goes wrong the other way, because code is brittle and fails with full confidence on the first case it did not foresee. The worst case is a cheap model on a vague question, though that is my rule of thumb and I have not measured it.
- **The cost of doing it right:** mostly setup time. Every level you add is one more thing to configure and one more thing that can fail, so do not add a cheap judge for a call that happens twice a week. Until you have tested the levels on cases where you know the answer, they are only guesses.
- **Ask the team:** "Which judgments in our workflow does a model make that a script could settle, and which does a script make that needs judgment?"

## Who should make all the small judgments? {#problem}

An agent workflow is full of small judgments. Is this path inside the allowed folder, and has the check passed three times? Is this Excel sheet a mapping table? Does this step go beyond the approved plan? Is this design good? Each of these has to be answered by something, and the question is what.

You might think the safest choice is the smartest judge. That is the easy habit: give all of them to the main model, because it can answer anything. It does get answers, but it is wasteful in three ways. It spends tokens on questions that code would answer for free. It answers the same question differently on different days. And it is slow, since a model call takes seconds while a check in code takes milliseconds.

The opposite habit is just as bad. Because code is the cheapest and most reliable judge, people push everything into it, such as a pattern list for "dangerous commands" or a keyword match for "is this a bug report". It holds up until the first case the pattern did not foresee, and on that case it is wrong with full confidence.

Both habits hand every judgment to one judge. The real question has to be asked one judgment at a time: **what is the cheapest level that is still good enough for this judgment?**

## Four levels, and how to choose between them {#how-it-works}

### Four levels

To answer it, it helps to have a short ladder of judges, from the cheapest to the most expensive.

| Level | Good at | Cost | Weak at | Example |
| --- | --- | --- | --- | --- |
| **1. Code** | Anything with one right answer that can be computed | Nearly none, same answer every time | Anything that needs meaning | Count passes in a row; is the path inside the allowed folder; does the data have the required fields; has a file changed since it was read |
| **2. A cheap model** | Narrow, frequent judgments with clear options | Low | Vague calls; long context; cases with no clear options | Sort a request into one of four kinds; does this step name a file outside the plan |
| **3. The main model** | Reasoning, design, reading a lot, judgments that need context | High | Being the same every time; being cheap | What does this change mean; write the plan; decide which of two designs fits |
| **4. A person** | What costs money, grants power, cannot be undone, or needs the business to decide | Their time, which is the most expensive | Speed; being there at night | Approve the plan; decide between two readings of a requirement; accept the result |

To use the table, read it from the top. For each judgment, first ask whether code can do it, and if it can, stop there. If it cannot, ask whether a narrow cheap judge can. If that fails too, the judgment goes to the main model, unless the answer has consequences nobody should delegate, in which case it goes to a person.

The first question applies to everyday cases too. Does this file exist, how many rows does this table have, do these two files differ? Questions like these are often put to a model by habit, yet they belong at level 1, because a script answers each one exactly and for free.

Each level also fails in a clear way when it gets the wrong kind of question. Code given a vague question is brittle, passing what it has seen and missing the rest. A cheap model given a vague question is the worst case, because it answers fast, in the same confident tone it uses for an easy question, and is wrong more often. That is why cheap models are weakest at the vague calls, and why the example for level 2 has clear options. It is a rule of thumb from how these models behave, not something I have measured on my own tasks.

The other two failures run the opposite way, with a judge that costs more than the question needs. The main model given a code question is just a waste. A person asked to settle what code could settle is worn out by it, until they approve without reading ([Two gates](5-3-two-approvals.html)).

### Prepare the input in code too

The same idea reaches back to before the model starts. Turning a Word file or an Excel sheet into plain text is a fixed job, so a program does it, not a model. The model should not pay for cover pages, hidden sheets and comments, or take that noise for a requirement ([The agent writes the requirement](5-2-requirements.html) has the details). What it reads is the small, clean result, and it never sees the originals.

::: figure 5-9-convert-first

The point is the split: converting is level 1, while deciding what the requirement means is level 3 or 4. If you mix the two, the model ends up doing both, and doing both badly.

### Make questions computable

You can also move work down to level 1 by changing the data rather than the judge. Take the question "is this knowledge still right?". Put to a model, it means reading everything and guessing, and the guess may be different next time. But if each card of knowledge records the version of the code it was read from, "which cards are stale?" becomes a comparison that a script does exactly. The rule is: **where a question has one right answer that a program can compute, put the data in a fixed form and let a program compute it.** The model keeps what needs judgment.

### When to move a judgment up or down

How do you notice that a judgment sits at the wrong level? Move it up a level when one of these happens:

- The lower level is unsure, and says so. Code can be built to say "I cannot tell" and hand the case on. A model's own statement of confidence is a weak signal, though, so for a model the safer trigger is the sample you check by hand (the next item).
- Its answers disagree with a sample you checked by hand.
- A wrong answer would cost more than the next level does. Being wrong on a write-back (copying finished work into the real repository, [Two gates](5-3-two-approvals.html)) costs more than a call to the main model.
- The judgment turns out to need context it does not have.

And move one down when you notice you are using a big judge on a question with a stable answer. Most judgments start at level 3, because that is the quickest way to get something working, so the work is in noticing which ones can sink.

### What my setup does

In my harness, the decisions made in code fall into a few kinds. Some guard the work, such as path and command checks. Some keep track, such as counting passes, working out fingerprints and the board of task states ([Ten things at once: parallel tasks](7-2-many-tasks.html)). And some check or prepare things, such as the staleness of knowledge cards ([A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)), the scoring of fixed test tasks and the conversion of business documents. The main model does the thinking and the writing. The independent checker is a model too, because reading a result against a requirement is not a narrow call. The approvals stay with people.

That leaves level 2 empty. I have designed a place for a judge there, a cheap model for judgments that are frequent but too varied for rules, such as "has this step gone beyond the approved scope?", but it is not built. If I built it, I would first check whether code can make the call, and only if it cannot would the cheap judge come in. Code would decide what to do with its answer, and when the judge fails, it would fall back to rules. Whether a cheap model is good enough for that call, I have not tested.

## What the levels cost, and where they mislead {#costs-and-traps}

Setting the levels up has two costs. That untested judge points to the first: the levels are guesses until you test them. Whether a judgment fits level 2 depends on the model you use this month, so measure it on cases where you know the answer ([Eval tasks](6-3-eval-tasks.html)).

The other is that every level is one more part. Each one you add is something to configure and something that can fail, so do not add a cheap judge for a call that happens twice a week.

Code adds a trap of its own: as the brittle pattern at the start of the chapter showed, it can be confidently wrong. A pattern that blocks "dangerous commands" will not see a dangerous command in a form it has not met. If the worry is safety rather than cost, though, the question is how hard the rule is enforced, and that is what [Requests and rules](4-1-requests-and-rules.html) is about.

Before you move a judgment down to save money, two more things are worth checking. One is that the cost per call is not the whole bill. Input the provider has cached is read at about a tenth of the base price, so a long prefix that repeats is cheaper than it looks ([Models and cost](1-1-models-and-cost.html)). I have not checked how Copilot applies this, so measure on your own setup before you decide that moving a judgment saves money.

The other is that moving a judgment down saves money but can also hide errors, because cheaper judgments are less often looked at. Keep a sample that you read by eye.

## What stays, and how the line moves {#when-to-delete-it}

The levels themselves stay, but the line between them moves. As cheap models get better at vague calls, level 2 will take on more, and as the main model gets cheaper, level 3 will matter less as a cost and more as a question of reliability. So when the model changes, re-run your own test of each judgment ([After a model upgrade](6-5-model-upgrades.html)).

## Try it on your own setup {#try-it}

::: prompt
List the judgments in this project's agent workflow: what the instruction files, skills, hooks, scripts and review steps each decide (for example, is this path allowed, did the check pass, is this change in scope, is this design good). For each, name who decides today: code, a cheap model, the main model, or a person. Then mark the ones where a model decides something a script could settle, and the ones where a script or pattern decides something that needs meaning. Do not change any files.
:::

## Go deeper {#go-deeper}

- Claude Code docs: [Manage costs](https://code.claude.com/docs/en/costs)

## Explore it in the harness {#explore}

The code-first judgments, the conversion of business files and the places where a person decides all run in Copilot Harness, while the cheap-model level is not built. For what does exist, the harness can teach you from the inside, with the real files.

::: prompt
/harness-rookie-wondering I have read the chapter "Who decides". Teach me which judgments this harness gives to code, which to the model and which to a person (topic 15), and how it converts business documents before the model reads them. Open the real files with me and draw how the pieces fit together.
:::
