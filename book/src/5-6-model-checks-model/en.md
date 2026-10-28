This chapter assumes you have read the independent check in [Use subagents sparingly](2-3-subagents.html), and how its passes are counted in [Make a pass count](5-5-counted-checks.html).

## In one sentence {#in-one-sentence}

A model checking a model catches some errors, but the two share blind spots. Hiding the author's reasoning, or using another angle or model, helps; it does not remove them, and how much it helps has to be measured.

## For leaders {#for-leaders}

- **The decision:** decide how far to trust a model that reviews another model's work, and pay for a small measurement before relying on it for anything important.
- **The risk:** the checker and the author share blind spots, so a pass means "a second reader found nothing", not "it is correct". A wrong FAIL also costs real work. I have not measured how often my checker fails good work or passes bad work. My one weak signal is that two checkers gave different verdicts on the same work.
- **The cost of doing it right:** the cheap moves cost little: hide the author's reasoning, and ask a narrower question. A different model costs the most. The small measurement in the chapter takes about ten minutes: plant three errors, run the checker three times, and count.
- **Ask the team:** "Have we ever planted known errors and counted how many our reviewing agent finds?"

## The problem {#problem}

An independent check is a model reading another model's work. That should make you a little uneasy. If the author model has a blind spot, why would a second copy of the same model not have it too?

There is research behind the unease. Huang and colleagues tested whether a model can fix its own reasoning when nothing outside tells it what is wrong. Their finding: models "struggle to self-correct their responses without external feedback", and sometimes "their performance even degrades after self-correction" ([Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798), ICLR 2024). That paper is about a model revising its own answer, not about a second model checking. But it warns against the lazy reading of "ask the model to look again".

Two more papers are close to the checking case, though neither tests my checker. Panickssery and colleagues found that a model used as an evaluator can score its own outputs higher than others' ("self-preference"), and that this grows with how well it recognizes its own text ([LLM Evaluators Recognize and Favor Their Own Generations](https://arxiv.org/abs/2404.13076)). Zheng and colleagues, studying models as judges, list position, verbosity and self-enhancement biases ([Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685), NeurIPS 2023). I use them as a reason to doubt a same-family checker, not as a measurement of one.

So the honest question is not "does a model check work?" It is **"which errors does the checker see that the author did not, and which does it miss with the author?"**

## How it works {#how-it-works}

Picture the errors in a piece of work as a set. The author misses some of them. The checker misses some of them. What you want to know is how much the two misses overlap.

::: figure 5-6-blind-spots

Every method below tries to make the circle of the checker different from the circle of the author. None can make them fully apart.

### 1. Hide the author's reasoning

When you proofread your own essay, you read what you meant. An author's context is full of its own reasoning, and that reasoning explains away its own mistakes. A checker that has seen the reasoning is pulled along the same path.

So the first move is to give the checker only the request, the work and the diff (the list of changed lines), and keep the author's notes out on purpose ([Use subagents sparingly](2-3-subagents.html) explains why). This is cheap, and it should reduce the part of the overlap that comes from shared reasoning; I have not tested how much. It does not touch the part that comes from the shared model.

### 2. A different angle

The same model asked a different question looks at different things. "Is this right?" invites a general skim. A checklist tied to the requirement is narrower: for each item of the requirement, find the evidence in the work; for each conclusion in the work, find its source. The checker has to go and look, not to feel.

Two more rules push the angle: every finding names a file and line, and the checker points out but never writes the fix. Both are in [Use subagents sparingly](2-3-subagents.html).

### 3. A different model

A checker from another model family, or at least another size, has different habits and different holes. This should shrink the shared circle the most, and it is also the one with the most cost: another model to set up, to pay for and to keep in step. It is a good candidate for a small trial before you commit to it. In my setup the checker runs on a model chosen separately from the main agent's, but I have not tested whether choosing a different family changes how many errors it finds.

### 4. A different kind of check

Some errors a model reading text will not find, by any means. A test that runs the code finds them. The same goes for the checker itself: if you give it tools to run the code and look at files, it stops guessing from the text and starts verifying. A person who knows the business finds others. A script finds anything that has one right answer. Put these next to the model checker, not behind it. [Let the agent check its own work](5-4-self-checks.html) covers tests; [Who decides](5-9-who-decides.html) covers which kind of judge fits which question.

### Where I would start

My order, which I have not tested: first the two cheap moves (hide the reasoning, ask a narrower question), then a different kind of check that runs things, and only then a different model, because it costs the most.

### How much does it catch?

Here I do not have an answer. I have not measured how often my checker fails good work or passes bad work. What I do have is one weak signal: two checkers gave different verdicts on the same work. That tells me a single verdict is not a fact.

The way to measure it is simple to state. Take work whose right answer you know, with some errors put in on purpose, and some "wrong-looking but fine" cases. Run the checker several times. Count the good work it failed, the bad work it passed, and how often its findings point at the right line. The measuring itself is the subject of [the chapters on evidence](6-3-eval-tasks.html); here the point is only that you should do it before you trust the checker with something important. A small version takes about ten minutes: put three errors into a piece of work you know, run the checker three times, and count how many it finds each time.

## Costs and traps {#costs-and-traps}

**A pass lowers the risk. It does not remove it.** Treat it as "a second reader found nothing", not "it is correct".

**A wrong FAIL costs real money.** Each false FAIL sends the author back to fix a problem that is not there, and may make the work worse. The rule that findings must point to a real file and line cuts this, but only for the form of a finding, not for its truth.

**Agreement is not independence.** If both models are the same one and have seen the same reasoning, two passes may be one opinion twice. That is why the checker is a new one every time, with a clean context.

**A model checker does not replace a person.** It narrows what a person has to read. Approval of the final result stays with a person ([Two approvals](5-3-two-approvals.html)).

## When to delete it {#when-to-delete-it}

If you measure your checker and find that it catches nothing the author's own run of the tests did not, drop it and keep the tests. If the platform later offers a way to see how well a checker does on your own tasks, use that instead of a feeling.

## Go deeper {#go-deeper}

- Huang et al.: [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) (ICLR 2024)
- Claude Code docs: [Best practices](https://code.claude.com/docs/en/best-practices), on giving the agent something to check against

## Explore it in the harness {#explore}

The checker that cannot see the author's reasoning, the format it must follow, and the script that drops findings without a real line all run in Copilot Harness. The harness can teach them to you from the inside, with the real agent file. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Can a model check a model?". Teach me how this harness builds its independent checker (topic 11): what it is and is not allowed to see, how its answer is shaped, and what the honest limits are. Open the checker's agent file with me and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.