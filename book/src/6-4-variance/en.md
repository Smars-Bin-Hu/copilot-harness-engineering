This chapter assumes you have used an AI coding agent and that you have seen it do something slightly different when you asked for the same thing twice. Nothing else.

## In one sentence {#in-one-sentence}

An agent never does exactly the same thing twice, so one run proves nothing. Run the task several times, look at the spread, and report numbers together with their conditions.

## For leaders {#for-leaders}

- **The decision:** require that every claim that one setup is better states how many times each side was run and under what conditions. For unattended work, ask for "works every time", not for the average.
- **The risk:** one run each proves nothing. In the textbook example in this chapter, 4 passes out of 5 runs is compatible with a true pass rate anywhere from about 38 to 96 percent, and telling 50 from 70 percent reliably takes roughly ninety runs a side. These are rough numbers for a pass/fail task, not measurements of any agent.
- **The cost of doing it right:** the runs multiply, because you pay for tasks times setups times runs. Most of that is money and time.
- **Ask the team:** "How many times was each side run, do the ranges overlap, and is everything equal except the thing being tested?"

## Is the new setup really better? {#problem}

Every number in [Use subagents sparingly](2-3-subagents.html) comes from one run per task. That includes the two figures the chapter is quoted for most often: the team cost about 4.5 times the usage and about 6 times the time of a single agent. Those two ratios are also its weakest. If I ran the same four tasks again, the ratios would move. I do not know by how much.

The same problem comes up whenever you compare two setups. You ran the old setup once and the new setup once, and the new one scored higher. Is the new one better, or would the old one have scored higher the next time?

To answer it, we need names for two things. One attempt by the agent at one task, from the start to the end, is a **run**. How much the results differ between runs of the same setup on the same task is the **spread**. Before asking how big the spread is, it is worth asking why there is any spread at all.

## Seeing the spread, and saying what it means {#how-it-works}

### Why runs differ

If you ask a person to do the same job twice, you get two slightly different results. An agent is the same, for plain reasons.

The first is that the model picks its words with some chance in it. It does not always take the single most likely next move, so two runs that begin with the same request may take different first moves. Those small differences then grow, because an agent works in a loop ([The agent loop, and where you can step in](2-1-agent-loop.html)). If run A reads file X first and run B reads file Y first, everything afterwards is built on a different picture. One early choice can end in a different answer.

The world around the agent changes as well. Tools return what they return at that moment, so a command takes a different time, times out or is slowed by a rate limit, and a search lists its results in a different order. Even the model itself can change. If the platform can change the model behind a name without telling you, two runs a week apart may not be the same model, so note the model and the date next to every run.

I have not measured how much of the spread comes from each of these, but for this chapter that does not matter. What matters is that the spread exists and that you see it before you decide anything.

### One run against several

::: figure 6-4-spread

In the picture, setup B looks better than setup A when each side runs once. Run each side several times and you see that the two overlap. The one run that made B look better could have come from either setup. The picture is a sketch, not data. It shows the shape of the problem, not how big it is for your agent.

### How many runs?

There is no number that is right for every case, because the size of the difference you want to see decides it. A large gap shows up in a few runs, while a small gap needs many.

To feel why, start with a single setup that passed 4 of 5 runs. The usual 95 percent interval for that (the Wilson interval, which I computed by hand) runs from about 38 percent to 96 percent. Even with 5 of 5 it is still only about 57 percent to 100 percent. Five runs, in other words, cannot tell a setup that passes 40 percent of the time from one that passes 95 percent. Comparing two setups needs more: the standard sample-size formula says that to see 50 against 70 percent reliably, you need roughly ninety runs on each side. These are rough, textbook numbers for a pass/fail task, not measurements of any agent.

In practice I start small, with a few runs of the setup I already have on one task, to see how much the results differ by themselves. If the results differ a lot, a few runs cannot show small effects, so the next step is to add runs until the picture stops changing. Once another run no longer moves the range much, I have a rough idea of the spread.

Five per side is a starting point, not a conclusion. For the comparison itself, I work in pairs, running both setups on the same tasks and looking at the difference task by task. A task that is hard for both sides then stops adding noise to the comparison, so this takes fewer runs than comparing two averages would.

Runs cost money, and the bill grows fast because it is tasks times setups times runs. The bill is also a reason to keep the set of tasks small and well chosen ([Fixed tasks, scored by a script](6-3-eval-tasks.html)), and to be honest when you could not afford more. Not everything needs that many, so I save the extra runs for the changes I care about.

### "All k succeeded" and "at least one of k succeeded"

Once you run a task k times, there are two questions you can ask of the results, with very different answers. The first is whether at least one of the k runs succeeded. That is what matters if a person can try several times and pick the best. This measure is called **pass@k**. Anthropic defines it as "the likelihood that an agent gets at least one correct solution in k attempts". It goes up as k grows.

The second question is whether all k runs succeeded. That is what matters if the agent runs alone, nobody is watching and it must work every time. This one is called **pass^k**. It goes down as k grows, because "demanding consistency across more trials is a harder bar to clear." ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents))

The tau-bench paper proposed pass^k for this reason. It reported that the agents it tested in 2024 were "quite inconsistent (pass^8 <25% in retail)", where pass^8 means that all eight tries of the same task succeeded. That figure is for their retail tasks and those models, not a statement about your tasks ([tau-bench](https://arxiv.org/abs/2406.12045)). What carries over is the question. If the agent runs unattended, an average pass rate of 80 percent is not the number you need. What you need to know is how often it works every time. Judge a pilot by that too.

So pick the question that matches how you use the agent. With a person watching, ask the first. For an agent running overnight, ask the second ([Unattended: when it must stop](5-7-when-to-stop.html)).

### Direction yes, ratio no

That brings us back to the two ratios this chapter started with. My result in [Use subagents sparingly](2-3-subagents.html) has a limited kind of strength. Because a gap of four to six times is large, I trust its direction: the team cost much more for the same result. What I do not trust is "4.5" or "6", because each task ran once and the two sides were not set up the same way. This is the shape of an honest claim from few runs. It says which way the result points but not how far.

### Common misreadings

Running each side once is the misreading this chapter started with, but it is not the only one.

- Reporting the average of a few runs as one number. It hides the spread, and two setups with the same average can behave very differently: one always lands in the middle, while the other swings between very good and very bad.
- Counting only the runs that succeeded. If you drop the failures to "get clean numbers", you have measured something else.
- Stopping when the result looks good. If you run until the new setup wins and then stop, you chose the answer, since three good runs in a row can come from a setup that passes half the time. Decide the number of runs before you start.
- Comparing sides that are not equal, such as a top model against a smaller one, with or without a knowledge base ([A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)), with different rules. The gap is then the sum of several differences, so keep everything the same except the thing you test.
- Leaving out the hidden costs. If the usage you report does not include the subagents, the setup that uses them looks cheap ([Use subagents sparingly](2-3-subagents.html)).

### How to write one honest sentence

What an honest sentence needs is its conditions, written next to the number. A number with no conditions can be neither checked nor repeated. These are the conditions I write down:

1. How many runs, and of how many tasks.
2. Which model and setup, on each side.
3. How it was scored, and by whom or what.
4. What the usage counts (main conversation only, or subagents too).
5. What the spread was, or "I ran it once" when I did.

Here is my own result, written that way: "Four tasks, one run each; one agent on a top model against a three-role team with a knowledge base; scored by the same script; usage in AI credits from the platform. Both got all four right. The team used about 4.5 times the usage and about 6 times the time. One run each, so I trust the direction and not the ratio."

It is a worse-looking sentence than "the team costs 4.5 times as much", but it is the one that is true.

### Test your own setup

For any claim that something is better, ask three questions:

1. How many times was each side run?
2. Do the ranges overlap?
3. Is everything equal except the thing being tested?

You can also see the spread of your own setup today. Take one task you know the right answer to and give it to your agent five times with the same request, each time in a new chat. The new chat matters, because an old chat carries what it learned and the later runs would not be fair. Make a small table with one row per run (pass or fail, minutes, usage), then look at the five results next to each other. That is the spread of your own setup on that task. It is usually bigger than people expect.

## What more runs cost, and what they cannot tell you {#costs-and-traps}

When the spread turns out bigger than you expected, the natural answer is more runs, and more runs cost real money. If the budget does not allow enough of them, say so and use the weaker words: "points toward", "I ran it twice".

And even when you can afford them, the spread itself is not a fault to remove. A tighter setup can lower it, but part of it stays, so plan for it with checks, a person at the gates and a limit on retries ([Make a pass count](5-5-counted-checks.html)).

A statistic does not replace reading, however many runs are behind it. Five runs tell you the spread, but they do not tell you why one of them failed. For that you have to read the failures ([Fixed tasks, scored by a script](6-3-eval-tasks.html)).

My own results have no confidence interval, because with one run each there is nothing to compute one from, and with a handful of runs it would be very wide, as the example above shows. So I show the runs and say which way they point.

## When to delete the habit of rerunning by hand {#when-to-delete-it}
{status: industry}

Running a task again and again by hand is a habit that exists only because I have no tool that does it and reports the spread. If a platform runs the same task several times and shows the spread, use that. And if the models become so steady that the spread is small on my tasks, I can run fewer, though I would have to measure that rather than assume it.

The reasoning stays for as long as the agent chooses its moves with some chance in them: one run cannot say how good a setup is.

## Try it on your own setup {#try-it}

::: prompt
Search this repository's README, docs, pull request templates and any decision records for claims about AI agent results: words like faster, better, cheaper, saves, fewer errors. For each claim, list the evidence given: how many runs, how many tasks, which model and setup on each side, how it was scored, and what the usage counted. Mark each claim as "conditions stated", "partly stated" or "no conditions". Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), on multiple trials, pass@k and pass^k
- tau-bench: [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)
- In this book: [Fixed tasks, scored by a script](6-3-eval-tasks.html), [Use subagents sparingly](2-3-subagents.html)

## Explore it in the harness {#explore}

Copilot Harness runs each of its scenarios once, by hand, not several times. What the harness does have is the material this chapter builds on, the log and the report that tell you what each run did. It can also show you where a run's time and usage are recorded, so that you can build your own repeated runs on top.

::: prompt
/harness-rookie-wondering I have read the chapter "One run proves nothing". Teach me what this harness records for a single run (topic 12): the log, the usage and time of a task, and the fixed scenarios. Help me see what I would need to add to run one scenario five times and compare the results.
:::
