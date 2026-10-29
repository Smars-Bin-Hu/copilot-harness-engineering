This chapter assumes you have used an AI coding agent, and that you have changed its rules or setup at least once. Nothing else.

## In one sentence {#in-one-sentence}

To know whether a change helped, run the same fixed tasks before and after the change and score them with a script. Then read the runs that failed.

## For leaders {#for-leaders}

- **The decision:** require that any change to the agent's rules or setup comes with a before-and-after run on the same fixed tasks, scored by a script.
- **The risk:** one good result cannot tell you whether a change helped. My own set has four tasks, which is enough to show a gap of four to six times but not a gap of ten percent.
- **The cost of doing it right:** an afternoon to build the scorer and test it on a good answer and a broken one, and after that the cost of every run. In my lab, the three-role team took about 16 minutes and about 456 AI credits to do the four tasks once.
- **Ask the team:** "Which fixed tasks did you run before and after this change, and how do you know the script that scores them catches a wrong answer?"

## How do you know a change helped? {#problem}

After you add a rule, change a prompt or switch on a check, the next task goes well. Did the change help?

You cannot tell from that. The next task may simply have been easy, or the agent may have done well by luck ([the next chapter](6-4-variance.html) is about that). Nor are you a neutral judge, because you made the change and you want it to work. Looking at a result and feeling that it is better is not evidence.

When I wrote [Use subagents sparingly](2-3-subagents.html), I wanted to know whether three job-title agents did better than one agent. Rather than take one task and look, I took four fixed tasks, ran both setups on each of them (once each) and let the same script score all of the results. What came out changed my design: the team cost far more and got nothing more right (the numbers are in that chapter, with their limits). Looking at a few results, I would not have believed it.

What I did there is called an **eval** (short for evaluation), a test for an agent setup. It has three parts: a set of tasks, a way to run them and a way to score the results. My tasks were **fixed tasks**: their request, starting files and right answer did not change between runs. Whatever scored them, here mostly a script, is the **grader**. How, then, do you build an eval whose answer you can believe?

## Building an eval you can believe {#how-it-works}

The picture shows the method: fixed tasks, a run before and after the change, a script that scores both, and a person who reads what failed.

::: figure 6-3-eval-loop

### What a good task looks like

The method starts with the tasks, but not every task makes a good eval. I look for three things.

1. It is real. It should look like the work the agent does for you, not like an exam question, so if you only ever add pipelines and fix formulas, do not test poetry. A change that helps on made-up work but not on yours teaches you nothing.
2. It has one right answer you can check. "Add a pipeline" is checkable: five files exist, in the right places, and agree with each other. "Make the code nicer" is not. If two reasonable people would disagree on whether the result is right, a script cannot score it.
3. It covers the mistakes people actually make. A good set has an easy case, but it also has the traps. In my lab, one task asks the agent to change a file that the rules forbid it to change, and the good result is to refuse. That task is there because a real request can ask for exactly that, and an agent that obeys it has done wrong.

The four tasks of my lab run from small to medium. They add a pipeline, pass a column downstream through three pipelines (one column is renamed on the way), rename a pipeline across areas and delete its old files, and fix a formula that lives in two places, where the request also asks to change a protected file. Four is few, and I come back below to what that means for the results.

These tasks also come in two sorts, and a failure means something different in each. A **capability** task checks something the setup cannot do yet, so you expect it to fail often at first. A **regression** task checks something that already works, so you expect it to pass every time, and a failure means a change broke it. Mix the two on purpose, but read a pass rate differently for each.

The repository under all of this is made up (93 files, 5 areas) and cannot be run. That is a choice. Because the right answers are known in advance, the script can say which result is right without anyone running code to find out.

### Outcome or process?

With the tasks in place, what should the grader look at? It can look at the outcome, meaning the files the agent left behind, such as whether it added the five files, whether the registry lists the new pipeline and whether the protected file is untouched. Or it can look at the process, meaning what the agent did to get there, such as whether it got refused or wrote to a place before the plan was approved.

For most tasks, grade the outcome. Because there are usually many valid ways to reach a right answer, a grader that insists on one path marks good work as wrong. Grade the process only when the process is the thing you care about, such as "the rules refuse a write before the plan is approved". In my harness, such a scenario looks at two things, and it passes only if the log shows the refusal and the file is unchanged. Without a log there is nothing to check, which is why [recording every call](6-1-observe.html) comes first.

In my lab's scoring, the outcome is a checklist. Some items are the same for every task and check that the repository is still consistent (valid files, every pipeline has its five files, columns agree, the protected area is untouched). Others belong to one task and check that the request itself is done. One more checks the scope: only the files that should change were changed. A task passes only when every item passes.

That makes the score all-or-nothing. If you want to see progress on a long task, score it in parts (partial credit) and report the parts. I do not split, because for a short task like these, one wrong item usually means a wrong result.

### A script or a model as the grader

Then there is the question of who, or what, does the scoring. A script reads the files and answers pass or fail. A model can read the result and give a judgment. Each has a weak side.

A script is cheap and quick and gives the same answer every time. Its weakness is brittleness. Because it looks for one particular form, it can mark a valid result wrong, and you only find those cases by reading the failures. A model grader can accept valid variations and judge things a script cannot, such as whether an explanation is clear. But its answer can change from run to run. It can also share blind spots with the agent it grades ([Can a model check a model?](5-6-model-checks-model.html)).

Anthropic's advice agrees: "We recommend choosing deterministic graders where possible, LLM graders where necessary or for additional flexibility." ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) That is also how I work. I use a script wherever the answer can be checked in files and keep a model grader for the few things a script cannot see. The lab here has no model grader.

### Prove the grader first

Either way, a grader is a program, and programs have bugs. A grader that passes everything makes every change look harmless. A grader that fails everything makes every change look harmful. So before I trust any score, I test the grader. My lab has a self-test with three parts:

- The **untouched** repository must fail every task, since nothing was done.
- The **right answers**, written by hand, must pass every task.
- **Broken versions** of the right answers must all be caught. There are 23, each with one mistake such as a missing registry line or a wrong column. If the grader lets one pass, the grader is wrong.

The smallest version is one good answer and one answer you broke by hand: the grader must pass the first and catch the second. For my lab it took an afternoon. It is the part people skip, and also the reason I can say that a failed item means something.

### Read the failed runs

Even a grader you have tested only tells you that something failed, not why. So I keep one habit even with a script: **when a run fails, I open it and read what happened**. The reason can be one of three very different things. The agent may have made a real mistake, which is what the eval is for. The grader may be wrong, because the result was right but came in a form the script did not expect. Or the task may be unclear, with two reasonable answers and a request that did not say which.

Only the first of these tells you about the agent. If you take every failure for that kind, you will throw away good changes and keep bad ones. Anthropic puts it this way: "Reading transcripts is how you verify that your eval is measuring what actually matters." (the same article)

So the script does not replace looking. What it replaces is reading every run. The script picks the runs that failed, as its guess at where to look, and a person then reads those.

### Your tasks and public benchmarks

You might ask why I build my own tasks at all, when public ones exist. A **benchmark** is a public set of tasks, scored the same way for everyone, so that models can be compared. It is useful for one question: how does this model do on someone else's tasks? It cannot answer a different one: did my change to my setup help on my work? For that you need tasks from your repository, with your rules in them, such as the protected file in my lab. That is why I build my own.

That choice has a price. A set I build is small, and it is mine alone. It also goes stale: whenever the repository changes, the tasks must change with it.

### What my harness does today

Everything so far has been about the lab. My harness itself does less. In my setup there are a few fixed scenarios, each one a prompt plus what is expected: a few calls that must appear in the log (such as a refusal) and a few files that must or must not change. I run a scenario by hand once, in Copilot, after which a check reads the log and the files and says whether it went right.

What it cannot do yet is run them in a batch. At the time of writing (October 2026), I see in my own setup that the non-interactive mode of Copilot does not run hooks, so I cannot run the scenarios in a batch. A before-and-after comparison on real tasks is not done yet either. In daily use, then, I have one scenario run by hand and a look at the log it leaves. What I have done with numbers, the scored and repeated comparison of this chapter, is the lab in this repository.

### Run it yourself

If you want to see all of this working before you build your own, start with the lab. It is the test behind the numbers in [Use subagents sparingly](2-3-subagents.html): the made-up repository, the four tasks and the scoring script. All of them work with any agent tool. [`labs/subagents/`](../labs/subagents/README.md) says how to run the self-test first and then your own comparison. Once you see how it works, replace the tasks with tasks of your own.

### Test your own setup

Whether or not you run the lab, three questions are worth asking before any change you are about to make to an agent setup:

1. What would I see if this change helped, and what if it did not?
2. Can a script tell the two apart?
3. Does the script itself pass the untouched, right and broken test?

You can also make a small start with no tools at all. Pick three tasks you have done with your agent. For each one, write down the files you would expect in the end and one mistake you have seen, then write a short script that checks the files. (If your work is not code, check the output instead: the columns of a table, the row count, a total.) Run it on a good result and on a result you break by hand. If it catches the broken one and passes the good one, you have an eval. It is small. Use it the next time you change a rule.

## What a small eval cannot tell you, and what it costs {#costs-and-traps}

How far can an eval this small take you? Most of its limits come from the tasks. Four tasks are a thin base. Mine suggested a gap of four to six times, but they would not show a gap of ten percent. Nor can they cover what you did not think of, so add a task each time a real failure surprises you. The tasks can also mislead you in two quieter ways. If you tune the setup until they pass, you have measured how well you fit those four tasks, so keep some tasks aside that you do not tune against. And once every setup passes every task, the tasks have saturated. In Anthropic's words, "Eval saturation occurs when an agent passes all of the solvable tasks, leaving no room for improvement." An eval in that state can no longer tell the setups apart, so add harder tasks.

Other limits sit in the score. The first is that a static score does not run the code. My grader reads files, so it cannot say that the code works. For work where running matters, the grader has to run the tests ([Let the agent check its own work](5-4-self-checks.html)). The second is that a score is only as fair as the runs behind it, so tasks must not share state. Start every run from the same clean copy. If one run leaves files, caches or a changed setting behind, the next run is not a fair test, because the score measures the leftovers.

Then there is the bill: running costs money and time. In my lab, the team took about 16 minutes and about 456 AI credits to do the four tasks once. Prompt caching changes the sum, since on Anthropic's API a cached read costs about a tenth of the base price ([Models and cost](1-1-models-and-cost.html)), but I have not checked how Copilot bills it. A set of ten tasks, run several times on two setups, is a real bill. Decide before you start what you will do with the answer. (As "What my harness does today" explains, in my setup real work cannot be run in a batch for this.)

Last, one run is thin. My results are one run per task, and [the next chapter](6-4-variance.html) says how to run more and how to report what you find.

## When to delete the scripts, and why the tasks stay {#when-to-delete-it}
{status: industry}

The scripts and the habit of running by hand exist because I have no built-in way to run a setup through a fixed set of tasks and compare. If a platform adds that, with logs and scoring, I would use it and drop my glue.

The fixed tasks do not retire with the scripts. Whenever a model is upgraded, a rule is added or a prompt is rewritten, that is a change, and it raises the same question again: did the change help? The fixed tasks are there to answer it ([When the model is upgraded](6-5-model-upgrades.html)). A task retires when every setup passes it. I would look again at the lab's four tasks if they stopped telling the setups apart.

## Try it on your own setup {#try-it}

::: prompt
Look at the last ten commits that changed instruction, skill, agent or hook files in this repository. For each, say what evidence (if any) was given that the change helped. Then propose three fixed tasks taken from this repository's real history: for each, the request, the starting commit, and an end state that a script could check from the files alone. Include one task where the right result is a refusal. Do not create or change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- In this repository: [`labs/subagents/`](../labs/subagents/README.md), with the scorer and its self-test
- In this book: [Record what happened, not what the agent said](6-1-observe.html), [One run proves nothing](6-4-variance.html)

## Explore it in the harness {#explore}

Copilot Harness has a few fixed scenarios that are judged from the log and from the files left behind. The harness can show you how one is written and how it is checked.

::: prompt
/harness-rookie-wondering I have read the chapter "Fixed tasks, scored by a script". Teach me how this harness's fixed scenarios work (topic 12): what a scenario holds, how a check reads the log and the files, and what the scenarios cannot do yet. Open one real scenario with me and draw how the pieces fit together.
:::
