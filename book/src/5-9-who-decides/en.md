This chapter is about cost, not about safety. [Requests and rules](4-1-requests-and-rules.html) asks how hard a rule is enforced: a request, a command, a hook. This chapter asks something else: for each judgment in your workflow, who is the cheapest one that can make it?

## In one sentence {#in-one-sentence}

Give each judgment to the cheapest level that can make it: code first, then a cheap model, the main model, a person. Cheap models tend to be weakest at the vague calls (my rule of thumb, not measured).

## For leaders {#for-leaders}

- **The decision:** assign each judgment in the workflow to the cheapest level that can make it well: code first, then a cheap model, then the main model, then a person.
- **The risk:** giving everything to the main model wastes usage, gives different answers on different days and is slow. Pushing everything into code is brittle and fails with full confidence on the first case it did not foresee. A cheap model on a vague question is the worst case; this is my rule of thumb, which I have not measured.
- **The cost of doing it right:** mostly setup time. Every level you add is one more thing to configure and to fail, so do not add a cheap judge for a call that happens twice a week. Levels are guesses until tested on cases where you know the answer.
- **Ask the team:** "Which judgments in our workflow does a model make that a script could settle, and which does a script make that needs judgment?"

## The problem {#problem}

An agent workflow is full of small judgments. Is this path inside the allowed folder? Has the check passed three times? Is this Excel sheet a mapping table? Does this step go beyond the approved plan? Is this design good?

The easy habit is to give all of them to the main model, because it can answer anything. It gets answers, and it is wasteful in three ways. It costs tokens for questions code answers for free. It answers the same question differently on different days. And it is slow: a model call takes seconds, a check in code takes milliseconds.

The opposite habit is just as bad. Code is the cheapest and most reliable judge, so people push everything into code: a pattern list for "dangerous commands", a keyword match for "is this a bug report". It works until the first case the pattern did not foresee, and then it is wrong with full confidence.

So the real question is: **what is the cheapest level that is still good enough for this judgment?**

## How it works {#how-it-works}

### Four levels

| Level | Good at | Cost | Weak at | Example |
| --- | --- | --- | --- | --- |
| **1. Code** | Anything with one right answer that can be computed | Nearly none, same answer every time | Anything that needs meaning | Count passes in a row; is the path inside the allowed folder; does the data have the required fields; has a file changed since it was read |
| **2. A cheap model** | Narrow, frequent judgments with clear options | Low | Vague calls; long context; cases with no clear options | Sort a request into one of four kinds; does this step name a file outside the plan |
| **3. The main model** | Reasoning, design, reading a lot, judgments that need context | High | Being the same every time; being cheap | What does this change mean; write the plan; decide which of two designs fits |
| **4. A person** | What costs money, grants power, cannot be undone, or needs the business to decide | Their time, which is the most expensive | Speed; being there at night | Approve the plan; decide between two readings of a requirement; accept the result |

Everyday cases for level 1, where a model is often asked by habit: does this file exist, how many rows does this table have, do these two files differ. A script answers each exactly and for free.

Read the table from the top. For each judgment, ask: can code do this? If yes, stop. If not, can a narrow cheap judge? If not, the main model. If the answer has consequences nobody should delegate, a person.

Each level also has a clear failure.

- **Code used for a vague question** is brittle. It passes what it has seen and misses the rest.
- **A cheap model used for a vague question** is the worst case. It answers fast, in the same confident tone as for an easy question, and is wrong more often. That is why cheap models are weakest at the vague calls, and why the example for level 2 is a question with clear options. I hold this as a rule of thumb from how these models behave; I have not measured the gap on my own tasks.
- **The main model used for a code question** is just a waste.
- **A person used for what code could settle** wears out the person, until they approve without reading ([Two approvals](5-3-two-approvals.html)).

### Prepare the input in code too

The same idea reaches before the model. Turning a Word file or an Excel sheet into plain text is a fixed job, so a program does it, not a model: the model should not pay for cover pages, hidden sheets and comments, or take that noise for a requirement ([The agent writes the requirement](5-2-requirements.html) has the details). The model then reads the small, clean result and never sees the originals.

::: figure 5-9-convert-first

The split is the point. Converting is level 1. Deciding what the requirement means is level 3 or 4. Mixing the two makes the model do both, badly.

### Make questions computable

You can move more work down to level 1 by changing the data, not the judge. If "is this knowledge still right?" is asked of a model, it reads everything, guesses, and guesses differently next time. If each card of knowledge records the version of the code it was read from, then "which cards are stale?" is a comparison a script does exactly. The rule is: **where a question has one right answer that a program can compute, put the data in a fixed form and let a program compute it.** The model keeps what needs judgment.

### When to go up

Move a judgment up a level when:

- The lower level is unsure, and says so. Code can be built to say "I cannot tell" and hand on. A model's own statement of confidence is a weak signal, so for a model the safer trigger is the sample you check by hand (next bullet).
- Its answers disagree with a sample you checked by hand.
- The cost of a wrong answer is higher than the cost of the next level. Wrong on a write-back (copying finished work into the real repository, [Two gates](5-3-two-approvals.html)) costs more than a call to the main model.
- The judgment turned out to need context it does not have.

And move one down when you notice you are using a big judge on a question with a stable answer. Most judgments start at level 3 because that is the quickest way to get something working; the work is in noticing which ones can sink.

### What my setup does

My harness's decisions in code include: path and command checks, counting passes, working out fingerprints, the board of task states ([Ten things at once: parallel tasks](7-2-many-tasks.html)), the staleness of knowledge cards ([A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)), scoring of fixed test tasks, and the conversion of business documents. The main model does the thinking and the writing. The independent checker is a model, because reading a result against a requirement is not a narrow call. People hold the approvals.

I have designed a place for a level 2 judge: a cheap model for judgments that are frequent and too varied for rules, such as "has this step gone beyond the approved scope?" It is not built. The first step would be to check whether code can do it, and only then add the cheap judge, with code deciding what to do with its answer, and a fallback to rules when it fails. I have not tested whether a cheap model is good enough for that call.

## Costs and traps {#costs-and-traps}

**Levels are guesses until you test.** Whether a judgment fits level 2 depends on the model you use this month. Measure it on cases where you know the answer ([Eval tasks](6-3-eval-tasks.html)).

**More levels, more parts.** Each level you add is something to configure and to fail. Do not add a cheap judge for a call that happens twice a week.

**Code can be confidently wrong.** A pattern that blocks "dangerous commands" will not see a dangerous command in a form it has not met. For safety, how hard the rule is enforced is the question, and [Requests and rules](4-1-requests-and-rules.html) is the chapter.

**Cost per call is not the whole bill.** Input the provider has cached is read at about a tenth of the base price, so a repeated long prefix is cheaper than it looks ([Models and cost](1-1-models-and-cost.html)). I have not checked how Copilot applies this, so measure on your own setup before you decide that moving a judgment saves money.

**Moving down saves money but can hide errors.** Cheaper judgments are less often looked at. Keep a sample you read by eye.

## When to delete it {#when-to-delete-it}

The levels stay; the line between them moves. As cheap models get better at vague calls, level 2 will take more. As the main model gets cheaper, level 3 will matter less as a cost and more as a reliability question. Re-run your own test of each judgment when the model changes ([After a model upgrade](6-5-model-upgrades.html)).

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
List the judgments in this project's agent workflow: what the instruction files, skills, hooks, scripts and review steps each decide (for example, is this path allowed, did the check pass, is this change in scope, is this design good). For each, name who decides today: code, a cheap model, the main model, or a person. Then mark the ones where a model decides something a script could settle, and the ones where a script or pattern decides something that needs meaning. Do not change any files.
:::

## Go deeper {#go-deeper}

- Claude Code docs: [Manage costs](https://code.claude.com/docs/en/costs)

## Explore it in the harness {#explore}

The code-first judgments, the conversion of business files, and the places where a person decides all run in Copilot Harness. The cheap-model level is not built. The harness can teach what exists from the inside, with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Who decides". Teach me which judgments this harness gives to code, which to the model and which to a person (topic 15), and how it converts business documents before the model reads them. Open the real files with me and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.