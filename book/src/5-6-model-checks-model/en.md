This chapter assumes you have read the independent check in [Use subagents sparingly](2-3-subagents.html), and how its passes are counted in [Make a pass count](5-5-counted-checks.html).

## In one sentence {#in-one-sentence}

A model checking a model catches some errors, but the two share blind spots. Hiding the author's reasoning, or bringing in another angle or another model, helps without removing them, and how much it helps is something you have to measure.

## For leaders {#for-leaders}

- **The decision:** decide how far to trust a model that reviews another model's work, and before you rely on it for anything important, pay for a small measurement.
- **The risk:** the checker and the author share blind spots, so a pass means "a second reader found nothing", not "it is correct". A wrong FAIL costs real work too. I have not measured how often my checker fails good work or passes bad work. All I have is one weak signal: two checkers gave different verdicts on the same work.
- **The cost of doing it right:** the two cheap moves, hiding the author's reasoning and asking a narrower question, cost little, while a different model costs the most. The small measurement in this chapter takes about ten minutes: plant three errors, run the checker three times, and count.
- **Ask the team:** "Have we ever planted known errors and counted how many our reviewing agent finds?"

## If the author has a blind spot, why wouldn't the checker? {#problem}

An independent check is a model reading another model's work, and that should make you a little uneasy. If the author model has a blind spot, why would a second copy of the same model not have it too?

The unease has research behind it. Huang and colleagues tested whether a model can fix its own reasoning when nothing outside it says what is wrong. They found that models "struggle to self-correct their responses without external feedback", and that sometimes "their performance even degrades after self-correction" ([Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798), ICLR 2024). Their paper is about a model revising its own answer rather than a second model checking it. Even so, it warns against the lazy reading of "ask the model to look again".

Two more papers come closer to the checking case, though neither tests my checker. Panickssery and colleagues found that a model used as an evaluator can score its own outputs higher than others' ("self-preference"), and that this grows with how well it recognizes its own text ([LLM Evaluators Recognize and Favor Their Own Generations](https://arxiv.org/abs/2404.13076)). Zheng and colleagues, studying models as judges, list position, verbosity and self-enhancement biases ([Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685), NeurIPS 2023). I take them as a reason to doubt a same-family checker, not as a measurement of one.

So the honest question is not "does a model check work?" It is **"which errors does the checker see that the author did not, and which does it miss along with the author?"**

## Pulling the two blind spots apart {#how-it-works}

To see what that question asks, picture the errors in a piece of work as a set. The author misses some of them, and the checker misses some of them too. What you want to know is how much those two misses overlap.

::: figure 5-6-blind-spots

Every method below tries to make the checker's circle different from the author's. None can pull the two fully apart.

### 1. Hide the author's reasoning

When you proofread your own essay, you read what you meant, and an author model does the same: its context is full of its own reasoning, which explains away its own mistakes. A checker that has seen that reasoning gets pulled along the same path.

So the first move is to give the checker only the request, the work and the diff (the list of changed lines), and to keep the author's notes out on purpose (why is explained in [Use subagents sparingly](2-3-subagents.html)). The move is cheap, and it should shrink the part of the overlap that comes from shared reasoning. What it cannot touch is the part that comes from a shared model. That part is for the third move.

### 2. A different angle

Even when the checker is the same model, the question you put to it changes what it looks at. "Is this right?" invites a general skim. A checklist tied to the requirement is narrower: for each item of the requirement, find the evidence in the work, and for each conclusion in the work, find its source. The checker has to go and look instead of going on a feeling.

Two more rules from [Use subagents sparingly](2-3-subagents.html) push the angle further. Every finding names a file and line, and the checker points out problems but never writes the fix.

### 3. A different model

A checker from another model family, or at least another size, brings different habits and different holes. That should shrink the shared circle the most, but it is also the move with the most cost, since it means another model to set up, to pay for and to keep in step. It is a good candidate for a small trial before you commit to it. In my setup the checker runs on a model chosen separately from the main agent's.

### 4. A different kind of check

Some errors a model reading text will not find by any means, but a test that runs the code will. The model checker can do this too. Once you give it tools to run the code and look at files, it stops guessing from the text and starts verifying. Other kinds of check find other errors. A person who knows the business finds some of them, and a script finds anything that has one right answer. Put these next to the model checker, not behind it. Tests are the subject of [Let the agent check its own work](5-4-self-checks.html). [Who decides](5-9-who-decides.html) covers which kind of judge fits which question.

### Where I would start

With four moves on the table, which comes first? My order starts with the two cheap moves (hide the reasoning, ask a narrower question). After them comes a different kind of check that runs things, and only then a different model, because it costs the most.

### How much does it catch?

That order rests on a guess that each move helps. How much, though? Here I do not have an answer, because none of it has been measured in my setup: not the order, not how much hiding the reasoning shrinks the overlap, not whether choosing a different model family changes how many errors the checker finds. Nor have I measured how often my checker fails good work or passes bad work. What I do have is one weak signal: two checkers gave different verdicts on the same work. That tells me a single verdict is not a fact.

The way to measure it is simple to state. Take work whose right answer you know, with some errors put in on purpose and some cases that look wrong but are fine. Run the checker several times, then count the good work it failed, the bad work it passed, and how often its findings point at the right line. The measuring itself is the subject of [the chapters on evidence](6-3-eval-tasks.html). Here the point is only that you should do it before you trust the checker with something important. A small version takes about ten minutes: put three errors into a piece of work you know, run the checker three times, and count how many it finds each time.

## What a verdict is worth, and what it costs {#costs-and-traps}

Until you have measured, read a pass for what it is. It lowers the risk but does not remove it, so treat it as "a second reader found nothing", not as "it is correct".

A FAIL deserves the same caution, because a wrong one costs real money. Each false FAIL sends the author back to fix a problem that is not there. That fix may make the work worse. The rule that findings must point to a real file and line cuts this down. A finding then has to point at something real, but the rule cannot tell whether what it points at is actually wrong.

You might also feel safer when two passes agree. Agreement is not independence, though. If both models are the same one and have seen the same reasoning, two passes may be one opinion given twice. That is why the checker is a new one every time, with a clean context.

None of this makes a person unnecessary. What the checker does is narrow what a person has to read. Approval of the final result still stays with that person ([Two approvals](5-3-two-approvals.html)).

## When to delete the model checker {#when-to-delete-it}

Measuring also tells you when the checker can go. If you measure it and find that it catches nothing the author's own run of the tests did not, drop it and keep the tests. And if the platform later offers a way to see how well a checker does on your own tasks, use that instead of a feeling.

## Go deeper {#go-deeper}

- Huang et al.: [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) (ICLR 2024)
- Claude Code docs: [Best practices](https://code.claude.com/docs/en/best-practices), on giving the agent something to check against

## Explore it in the harness {#explore}

The checker that cannot see the author's reasoning, the format it must follow, and the script that drops findings without a real line all run in Copilot Harness. The harness can teach them to you from the inside, with the real agent file open.

::: prompt
/harness-rookie-wondering I have read the chapter "Can a model check a model?". Teach me how this harness builds its independent checker (topic 11): what it is and is not allowed to see, how its answer is shaped, and what the honest limits are. Open the checker's agent file with me and draw how the pieces fit together.
:::
