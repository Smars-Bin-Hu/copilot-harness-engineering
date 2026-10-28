This chapter assumes you have used an AI coding agent, and that you have changed its rules or setup at least once. Nothing else.

## In one sentence {#in-one-sentence}

To know whether a change helped, run the same fixed tasks before and after the change and score them with a script. Then read the runs that failed.

## For leaders {#for-leaders}

- **The decision:** require that a change to the agent's rules or setup comes with a before-and-after run on the same fixed tasks, scored by a script.
- **The risk:** you cannot tell from one good result whether a change helped. My own set is four tasks: enough to show a gap of four to six times, not a gap of ten percent.
- **The cost of doing it right:** an afternoon to build the scorer and test it on a good answer and a broken one, then the cost of every run. In my lab the three-role team took about 16 minutes and about 456 AI credits for four tasks, once.
- **Ask the team:** "Which fixed tasks did you run before and after this change, and how do you know the script that scores them catches a wrong answer?"

## The problem {#problem}

You add a rule. You change a prompt. You switch on a check. The next task goes well. Did the change help?

You cannot tell. The next task may have been easy. The agent may have done well by luck ([the next chapter](6-4-variance.html) is about that). And you are not a neutral judge: you made the change and you want it to work. Looking at a result and feeling that it is better is not evidence.

Here is what I did instead for [Use subagents sparingly](2-3-subagents.html). I wanted to know whether three job-title agents were better than one agent. I did not take one task and look. I took four fixed tasks, ran both setups on each (once each), and let the same script score all of the results. The result changed my design: the team cost far more and got nothing more right (the numbers are in that chapter, with their limits). I would not have believed it from looking at a few results.

Three words first.

- An **eval** (short for evaluation) is a test for an agent setup: a set of tasks, a way to run them, and a way to score the results.
- A **fixed task** is a task whose request, starting files and right answer do not change between runs.
- A **grader** is whatever scores a result: here, mostly a script.

## How it works {#how-it-works}

The method has four steps. The picture shows them; the sections below say how to do each well.

::: figure 6-3-eval-loop

### What a good task looks like

Not every task makes a good eval. I look for three things.

1. **It is real.** It should look like the work the agent does for you, not like an exam question. If you only ever add pipelines and fix formulas, do not test poetry. A change that helps on made-up work and not on yours teaches you nothing.
2. **It has one right answer you can check.** "Add a pipeline" is checkable: five files exist, in the right places, and agree with each other. "Make the code nicer" is not. If two reasonable people would disagree on whether the result is right, a script cannot score it.
3. **It covers the mistakes people actually make.** A good set has an easy case, and also the traps. In my lab, one task asks the agent to change a file that the rules forbid it to change. A good result is to refuse. That task is there because a real request can ask for exactly that, and an agent that obeys it has done wrong.

The four tasks of my lab are small to medium: add a pipeline; pass a column downstream through three pipelines (one column is renamed on the way); rename a pipeline across areas and delete its old files; fix a formula that lives in two places, where the request also asks to change a protected file. Four is few. It suggested a gap of four to six times, and it would not show a gap of ten percent.

Tasks of this kind come in two sorts. A **capability** task checks something the setup cannot do yet, so you expect it to fail often at first. A **regression** task checks something that already works, so you expect it to pass every time, and a failure means a change broke it. Mix the two on purpose, and read a pass rate differently for each.

The repository is made up (93 files, 5 areas) and cannot be run. That is a choice. The right answers are known in advance, so the script can say which result is right, and nobody needs to run code to find out.

### Outcome or process?

There are two things a grader can look at.

- **The outcome:** the files the agent left behind. Did it add the five files? Does the registry list the new pipeline? Is the protected file untouched?
- **The process:** what the agent did to get there. Did it get refused? Did it write to a place before the plan was approved?

For most tasks, grade the outcome. There are usually many valid ways to reach a right answer, and a grader that insists on one path marks good work as wrong. Grade the process only when the process is the thing you care about, such as "the rules refuse a write before the plan is approved". In my harness, those scenarios look at two things: the log must show the refusal, and the file must be unchanged. The log is why [recording every call](6-1-observe.html) comes first.

In my lab's scoring, the outcome is a checklist. Some items are the same for every task: the repository is still consistent (valid files, every pipeline has its five files, columns agree, the protected area is untouched). Some are for one task: the request itself is done. One more checks the scope: only the files that should change were changed. A task passes only when every item passes. That is all-or-nothing; if you want to see progress on a long task, score it in parts (partial credit), and report the parts. For a short task like these, one wrong item usually means a wrong result, so I do not split.

### A script or a model as the grader

A script reads the files and answers pass or fail. A model can read the result and give a judgment. Each has a weak side.

- **A script** is cheap, quick and gives the same answer every time. Its weakness is that it is brittle: it can mark a valid result wrong because it looks for one particular form. You find those by reading failures.
- **A model grader** can accept valid variations and judge things a script cannot, such as whether an explanation is clear. But its answer can change from run to run, and it can share blind spots with the agent it grades ([Can a model check a model?](5-6-model-checks-model.html)).

Anthropic's advice agrees: "We recommend choosing deterministic graders where possible, LLM graders where necessary or for additional flexibility." ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) I use a script wherever the answer can be checked in files, and I keep a model grader for the few things a script cannot see. The lab here has no model grader.

### Prove the grader first

A grader is a program, and programs have bugs. A grader that passes everything makes every change look harmless. A grader that fails everything makes every change look harmful. So before I trust any score, I test the grader. My lab has a self-test with three parts:

- The **untouched** repository must fail every task (nothing was done).
- The **right answers**, written by hand, must pass every task.
- **Broken versions** of the right answers must all be caught. There are 23, each with one mistake such as a missing registry line or a wrong column. If the grader lets one pass, the grader is wrong.

The smallest version is one good answer and one answer you broke by hand: the grader must pass the first and catch the second. For my lab it took an afternoon, and it is the part people skip. It is also the reason I can say that a failed item means something.

### Read the failed runs

Here is a habit I do not give up, even with a script. **When a run fails, I open it and read what happened.** The score says that something failed. It does not say why, and the why can be one of three very different things:

1. **The agent made a real mistake.** That is what the eval is for.
2. **The grader is wrong.** The result was right, but in a form the script did not expect.
3. **The task is unclear.** Two answers were reasonable, and the request did not say which.

Only the first one tells you about the agent. If you take every failure as the first kind, you will throw away good changes and keep bad ones. Anthropic puts it this way: "Reading transcripts is how you verify that your eval is measuring what actually matters." (the same article)

So the script does not replace looking. It replaces looking at everything, with a guess about what to look at. The script picks the runs that failed. A person then reads those.

### Your tasks and public benchmarks

A **benchmark** is a public set of tasks, scored the same way for everyone, so models can be compared. Benchmarks are useful for one question: how does this model do on someone else's tasks? They cannot answer a different one: did my change to my setup help on my work? For that you need tasks from your repository, and your rules, such as the protected file in my lab. That is why I build my own.

The cost of my own is that it is small, it is mine, and it goes stale. When the repository changes, the tasks must change.

### What my harness does today

In my setup there are a few fixed scenarios. Each one is a prompt plus what is expected: a few calls that must appear in the log (such as a refusal) and a few files that must or must not change. I run a scenario by hand once, in Copilot, and a check reads the log and the files and says whether it went right. At the time of writing (October 2026), in my own setup I see that the non-interactive mode of Copilot does not run hooks, so I cannot run the scenarios in a batch, and a before-and-after comparison on real tasks is not done yet. What I have done with numbers is the lab in this repository. In daily use that is one scenario run by hand and a look at the log it leaves. The scored, repeated comparison of this chapter is the lab.

### Run it yourself

The lab is the test behind the numbers in [Use subagents sparingly](2-3-subagents.html): the made-up repository, the four tasks and the scoring script. It works with any agent tool. [`labs/subagents/`](../labs/subagents/README.md) says how to run the self-test first and then your own comparison. Replace the tasks with tasks of your own once you see how it works.

### Test your own setup

**Three questions** for any change you are about to make to an agent setup:

1. What would I see if this change helped, and what if it did not?
2. Can a script tell the two apart?
3. Does the script itself pass the untouched, right and broken test?

**A small start, with no tools.** Pick three tasks you have done with your agent. For each, write down the files you would expect in the end, and one mistake you have seen. Write a short script that checks the files. (If your work is not code, check the output instead: the columns of a table, the row count, a total.) Run it on a good result and on a result you break by hand. If it catches the broken one and passes the good one, you have an eval. It is small. Use it the next time you change a rule.

## Costs and traps {#costs-and-traps}

**Four tasks are a thin base.** They can show a large gap. They cannot show a small one, and they do not cover what you did not think of. Add a task each time a real failure surprises you.

**You can fit the setup to the test.** If you change the setup until the tasks pass, you have measured how well you fit those four tasks. Keep some tasks aside that you do not tune against.

**A static score does not run the code.** My grader reads files. It cannot say that the code works. For work where running matters, the grader has to run the tests ([Let the agent check its own work](5-4-self-checks.html)).

**Tasks saturate.** Anthropic's word is "Eval saturation occurs when an agent passes all of the solvable tasks, leaving no room for improvement." When every setup passes every task, the eval can no longer tell them apart. Add harder tasks.

**Tasks must not share state.** Start every run from the same clean copy. If one run leaves files, caches or a changed setting behind, the next run is not a fair test, and the score measures the leftovers.

**Running costs money and time.** In my lab, the team took about 16 minutes and about 456 AI credits for four tasks, once. Prompt caching changes the sum: on Anthropic's API a cached read costs about a tenth of the base price ([Models and cost](1-1-models-and-cost.html)), but I have not checked how Copilot bills it. A set of ten tasks, run several times on two setups, is a real bill. Decide before you start what you will do with the answer. And in my setup the non-interactive mode of Copilot does not run hooks, so real work cannot be run in a batch for this (see "What my harness does today").

**One run is thin.** My results are one run per task. [The next chapter](6-4-variance.html) says how to run more and how to report what you find.

## When to delete it {#when-to-delete-it}
{status: industry}

The scripts and the habit of running by hand exist because I have no built-in way to run a setup through a fixed set of tasks and compare. If a platform adds that, with logs and scoring, I would use it and drop my glue.

The fixed tasks do not retire. A model is upgraded, a rule is added, a prompt is rewritten: each is a change, and each needs the same answer to the same question ([When the model is upgraded](6-5-model-upgrades.html)). A task retires when every setup passes it. I would look again at the lab's four tasks if they stopped telling the setups apart.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Look at the last ten commits that changed instruction, skill, agent or hook files in this repository. For each, say what evidence (if any) was given that the change helped. Then propose three fixed tasks taken from this repository's real history: for each, the request, the starting commit, and an end state that a script could check from the files alone. Include one task where the right result is a refusal. Do not create or change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- In this repository: [`labs/subagents/`](../labs/subagents/README.md), with the scorer and its self-test
- In this book: [Record what happened, not what the agent said](6-1-observe.html), [One run proves nothing](6-4-variance.html)

## Explore it in the harness {#explore}

Copilot Harness has a few fixed scenarios that are judged from the log and from the files left behind. The harness can show you how one is written and how it is checked. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Fixed tasks, scored by a script". Teach me how this harness's fixed scenarios work (topic 12): what a scenario holds, how a check reads the log and the files, and what the scenarios cannot do yet. Open one real scenario with me and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
