This chapter assumes you have used an AI coding agent and that you have seen it do something slightly different when you asked for the same thing twice. Nothing else.

## In one sentence {#in-one-sentence}

An agent never does exactly the same thing twice, so one run proves nothing. Run the task several times, look at the spread, and report numbers together with their conditions.

## For leaders {#for-leaders}

- **The decision:** require that every claim that one setup is better states how many times each side was run and under what conditions. For unattended work, ask for "works every time", not the average.
- **The risk:** one run each proves nothing. In the textbook example in this chapter, 4 passes out of 5 runs is compatible with a true pass rate anywhere from about 38 to 96 percent. To tell 50 from 70 percent reliably takes roughly ninety runs a side. These are rough numbers for a pass/fail task, not measurements of any agent.
- **The cost of doing it right:** runs multiply: tasks times setups times runs. Mostly money and time.
- **Ask the team:** "How many times was each side run, do the ranges overlap, and is everything equal except the thing being tested?"

## The problem {#problem}

Every number in [Use subagents sparingly](2-3-subagents.html) comes from one run per task. The team cost about 4.5 times the usage and about 6 times the time of a single agent. Those two ratios are the most quoted figures in that chapter, and also the weakest. If I ran the same four tasks again, the ratios would move. I do not know by how much.

That is the problem this chapter is about. You ran the old setup once and the new setup once, and the new one scored higher. Is the new one better? Or would the old one have scored higher the next time?

Two words first.

- A **run** is one attempt by the agent at one task, from the start to the end.
- The **spread** is how much the results differ between runs of the same setup on the same task.

## How it works {#how-it-works}

### Why runs differ

If you ask a person to do the same job twice, you get two slightly different results. An agent is the same, for plain reasons.

- **The model picks its words with some chance in it.** It does not always take the single most likely next move. Two runs begin with the same request and may take different first moves.
- **Small differences grow.** An agent works in a loop ([The agent loop, and where you can step in](2-1-agent-loop.html)). If run A reads file X first and run B reads file Y first, everything afterwards is built on a different picture. One early choice can end in a different answer.
- **The world around it changes.** Tools return what they return at that moment. A command takes a different time, or times out, or is slowed by a rate limit. A search lists results in a different order.
- **The model itself can change.** If the platform can change the model behind a name without telling you, two runs a week apart may not be the same model. Note the model and the date next to every run.

I have not measured how much of the spread comes from each of these. For this chapter that does not matter. What matters is that the spread exists, and you have to see it before you decide anything.

### One run against several

::: figure 6-4-spread

Look at the picture. With one run each, setup B looks better than setup A. With several runs each, you see that the two overlap. The one run that made B look better could have come from either setup. This is a picture, not data: it shows the shape of the problem, not how big it is for your agent.

### How many runs?

There is no number that is right for every case. The size of the difference you want to see decides it. A large gap shows up in a few runs. A small gap needs many.

To feel why, count a single setup. Suppose it passed 4 of 5 runs. The usual 95 percent interval for that (the Wilson interval, which I computed by hand) runs from about 38 percent to 96 percent. With 5 of 5 it is still only about 57 percent to 100 percent. Five runs cannot tell a setup that passes 40 percent of the time from one that passes 95 percent. Two setups need more: the standard sample-size formula says that to see 50 against 70 percent reliably you need roughly ninety runs on each side. These are rough, textbook numbers for a pass/fail task, not measurements of any agent.

What I do:

- **Start with a few runs of the setup you already have**, on one task. Five per side is a starting point, not a conclusion. See how much the results differ by themselves. If they differ a lot, you cannot see small effects with a few runs.
- **Add runs until the picture stops changing.** If another run does not move the range much, you have a rough idea of the spread.
- **Compare in pairs.** Run both setups on the same tasks, and look at the difference task by task. A task that is hard for both sides stops adding noise to the comparison, so you need fewer runs than if you compared two averages.
- **Run more for the changes you care about.** You do not need a lot of runs for everything.

This costs money, and it grows fast: tasks times setups times runs. That is a reason to keep the set of tasks small and well chosen ([Fixed tasks, scored by a script](6-3-eval-tasks.html)), and a reason to be honest when you could not afford more.

### "All k succeeded" and "at least one of k succeeded"

When you run a task k times, there are two questions, and they have very different answers.

- **At least one success in k runs.** If a person can try several times and pick the best, this is what matters. It is called **pass@k** (Anthropic: "the likelihood that an agent gets at least one correct solution in k attempts"). It goes up as k grows.
- **All k runs succeed.** If the agent runs alone, nobody is watching, and it must work every time, this is what matters. It is called **pass^k**. It goes down as k grows: "demanding consistency across more trials is a harder bar to clear." ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents))

The tau-bench paper proposed pass^k for this reason. It reported that the agents it tested in 2024 were "quite inconsistent (pass^8 <25% in retail)". Here pass^8 means that all eight tries of the same task succeeded. That figure is for their retail tasks and those models, and it is not a statement about your tasks. ([tau-bench](https://arxiv.org/abs/2406.12045)) What carries over is the question. If the agent runs unattended, an average pass rate of 80 percent is not the number you need. You need to know how often it works every time. The same goes for a pilot: judge it by that, not by the average pass rate.

Pick the question that matches how you use the agent. Your agent with a person watching asks the first. An agent running overnight asks the second ([Unattended: when it must stop](5-7-when-to-stop.html)).

### Direction yes, ratio no

My result in [Use subagents sparingly](2-3-subagents.html) has a limited kind of strength. A gap of four to six times is large, and for that reason I trust the direction: the team cost much more for the same result. I do not trust "4.5" or "6". Each task ran once, and the two sides were not set up the same way. This is the shape of an honest claim from few runs: say which way it points, and do not say how far.

### Common misreadings

- **One run each.** The case above.
- **The average of a few runs, reported as one number.** It hides the spread. Two setups with the same average can behave very differently: one always lands in the middle, the other swings between very good and very bad.
- **Counting only the runs that succeeded.** If you drop the failures to "get clean numbers", you have measured something else.
- **Stopping when the result looks good.** If you run until the new setup wins and then stop, you chose the answer. Three good runs in a row can come from a setup that passes half the time. Decide the number of runs before you start.
- **Comparing sides that are not equal.** A top model against a smaller one, with or without a knowledge base ([A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)), with different rules. Then the gap is the sum of several differences. Keep everything the same except the thing you test.
- **Leaving out the hidden costs.** If the usage you report does not include the subagents, the setup that uses them looks cheap ([Use subagents sparingly](2-3-subagents.html)).

### How to write one honest sentence

Put the conditions next to the number. A number with no conditions cannot be checked and cannot be repeated. The conditions I write down:

1. **How many runs, and of how many tasks.**
2. **Which model and setup, on each side.**
3. **How it was scored,** and by whom or what.
4. **What the usage counts** (main conversation only, or subagents too).
5. **What the spread was,** or "I ran it once" when I did.

Here is my own result, written that way: "Four tasks, one run each; one agent on a top model against a three-role team with a knowledge base; scored by the same script; usage in AI credits from the platform. Both got all four right. The team used about 4.5 times the usage and about 6 times the time. One run each, so I trust the direction and not the ratio."

It is a worse-looking sentence than "the team costs 4.5 times as much". It is the one that is true.

### Test your own setup

**Three questions** for any claim that something is better:

1. How many times was each side run?
2. Do the ranges overlap?
3. Is everything equal except the thing being tested?

**A test you can run today.** Take one task you know the right answer to. Give it to your agent five times, each in a new chat, with the same request. A new chat matters: an old chat carries what it learned, so the later runs would not be fair. Make a small table with one row per run: pass or fail, minutes, usage. Look at the five results next to each other. That is the spread of your own setup on that task, and it is usually bigger than people expect.

## Costs and traps {#costs-and-traps}

**More runs cost real money.** If the budget does not allow enough runs, say that, and use the weaker words: "points toward", "I ran it twice".

**Spread is not a fault to remove.** You can lower it with a tighter setup, but part of it stays. Plan for it: checks, a person at the gates, and a limit on retries ([Make a pass count](5-5-counted-checks.html)).

**A statistic does not replace reading.** Five runs tell you the spread. They do not tell you why one failed. Read the failures ([Fixed tasks, scored by a script](6-3-eval-tasks.html)).

**My own results have no confidence interval.** With one run each there is nothing to compute an interval from, and with a handful of runs it would be very wide, as the example above shows. So I show the runs and say which way they point.

## When to delete it {#when-to-delete-it}
{status: industry}

The hand-made habit of running a task again and again exists because I have no tool that does it and reports the spread. If a platform runs the same task several times and shows the spread, use that. If the models become so steady that the spread is small on my tasks, I can run fewer. I would have to measure that, not assume it.

The reasoning stays as long as the agent chooses its moves with some chance in them: one run cannot say how good a setup is.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Search this repository's README, docs, pull request templates and any decision records for claims about AI agent results: words like faster, better, cheaper, saves, fewer errors. For each claim, list the evidence given: how many runs, how many tasks, which model and setup on each side, how it was scored, and what the usage counted. Mark each claim as "conditions stated", "partly stated" or "no conditions". Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), on multiple trials, pass@k and pass^k
- tau-bench: [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)
- In this book: [Fixed tasks, scored by a script](6-3-eval-tasks.html), [Use subagents sparingly](2-3-subagents.html)

## Explore it in the harness {#explore}

Copilot Harness does not run its scenarios several times; each one runs once, by hand. What the harness has is the material this chapter builds on: the log and the report that tell you what each run did. The harness can show you where a run's time and usage are recorded, so you can build your own repeated runs on top. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "One run proves nothing". Teach me what this harness records for a single run (topic 12): the log, the usage and time of a task, and the fixed scenarios. Help me see what I would need to add to run one scenario five times and compare the results.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.