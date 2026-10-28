This chapter assumes you have used an AI coding agent and have seen a usage or billing page for it. Nothing else.

## In one sentence {#in-one-sentence}

Judge a model by what it costs to get one task done, not by its price per token. Most of that cost is what the model reads, so reading less and redoing less saves the most.

## For leaders {#for-leaders}

- **The decision:** judge models and setups by what it costs to finish one task, not by the price per token. When a result is bad, try the cheaper fixes first (a missing rule, a missing check, a lost thread) before paying for a bigger model.
- **The risk:** in a long agent task, most of the tokens go to the model re-reading the same material. In my worked example, which uses round numbers I chose, reading was over 90% of the tokens. A cache can cut the bill a lot, but only while the start of the input stays unchanged.
- **The cost of doing it right:** mostly setup time and a habit of measuring. A fair comparison of models takes a few tasks, each run about three times.
- **Ask the team:** "What does one finished task cost us, and when did we last check that number?"

## What are you really paying for? {#problem}

A model comparison usually starts with a price list, which tells you how many dollars a model charges per million tokens. A **token** is a small piece of text, roughly a short word or part of one, and since models read and write in tokens, bills are counted in them as well. Tokens come in two kinds. **Input** tokens are what the model reads in a call, and **output** tokens are what it writes. The two are priced differently, and output is usually the more expensive per token.

The price list is the number you can look up, so it is the number people use. But you never buy tokens for their own sake. What you buy is a finished task, a bug fixed or a report written, and what matters is the total for that.

It is a poor guide to that total, for two reasons. A cheap model that fails the task and has to be asked again may cost more than a strong one that gets it right the first time. And in an agent, the number of tokens is not what you expect, as the next part shows.

### Where the tokens go in an agent

Why would the count surprise you? In a chat, you send a question and get an answer. In an agent loop ([chapter 2.1](2-1-agent-loop.html)), the model is called again after every tool result, and every call sends the whole conversation so far: the rules, your request, every file it read and every result. The model has no memory between calls, so this is the only way it knows what has happened. All of it has to fit in the **context window**, which is how much text the model can see at once. That window has a size limit of its own ([chapter 3.1](3-1-context-budget.html) is about managing it), and every call fills it again from the start.

::: figure 1-1-token-flow

Here is the arithmetic, with round numbers I chose to make it easy rather than numbers I measured. Say the rules and your request come to 10,000 tokens, and each tool result adds 5,000. Over 10 calls the model reads about 10,000 + 15,000 + 20,000 + ... = 325,000 tokens, but it writes perhaps a few hundred tokens per call. In this example reading is more than 90% of the tokens. The real share depends on your task, but the longer the loop runs, the more it leans toward reading.

Tokens are not the same as money, since output costs more per token. The shape holds all the same: a long agent task is mostly the model reading the same material again and again. That is why the second half of this chapter is about reading less.

I can also show one real case. In [chapter 2.3](2-3-subagents.html) I gave the same four tasks to a team of three agents with job titles and to a single agent. Both got every task right, yet the team used about 4.5 times as much. The largest waste was re-reading, because each new agent started with an empty context and had to read the same files again. These were four small tasks, each run once, so trust the direction and not the ratio.

### The prompt cache changes the sum

Because so much of every call is the same beginning, providers offer a **prompt cache**. It lets the provider remember a long beginning of your input, so that a later call starting with the same text can be charged less for it. On Anthropic's API, reading cached input costs a tenth of the base input price on most models, and less on some. Writing to the cache costs more than a normal read, 1.25 times for a five-minute cache and 2 times for a one-hour cache ([Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)).

Those prices reward a stable beginning. The cache works only on an exact match from the start of the input, so if you change something near the top, such as an edited rule or a different tool list, everything after it misses the cache. They also punish a pause. A cache lives only a short time, so a conversation you leave for an hour and return to may pay full price to rebuild it. And even a cache read is not free: **the cheapest token is still the one that is not sent**. Reading less is still the first thing to try.

To see how much the cache moves, take the same example with a cache that hits every time, counting input only and using the five-minute prices. The first call writes 10,000 tokens at 1.25 times, which is 12,500. In each of the next nine calls, the earlier text is read from the cache. The cached part grows from 10,000 to 50,000 tokens, 270,000 over the nine calls, and at 0.1 times the price that is 27,000. Each call also writes its 5,000 new tokens, 45,000 in all, which at 1.25 times is 56,250. The total is about 96,000 token-prices instead of 325,000, and the repeated reading is now less than a third of it.

So the cache changes where the money goes, away from re-reading and toward new material. That is why the earlier "more than 90%" is a count of tokens read, not a share of the bill, and why a team with a well-kept cache can read a lot and still pay little. Misses undo that. An edited rule near the top, or a pause long enough for the cache to expire, brings the cost back toward the 325,000.

## Where a task's cost comes from, and where to cut it {#how-it-works}

### What a task costs

With reading, writing and the cache in view, we can put together what one finished task costs. Think of it as three parts.

::: figure 1-1-cost-parts

1. **What the model reads**, across every call, discounted where the cache hits.
2. **What the model writes**: the answer, the code, the thinking.
3. **Redoing**, meaning a wrong answer, a lost thread or a repeated attempt. Redoing is a multiplier on parts 1 and 2.

Most savings come from the first and the third. A good rule of thumb is: **do things in the cheapest way that is enough**.

### When a strong model is cheaper

Redoing is also where the choice of model comes in. A stronger model costs more per token, yet it can still cost less per finished task when it gets the answer in one pass and the weaker one needs three. If the task was easy, though, it can also be a waste.

Where does it flip? I have no measurement of my own, so this is an argument, not a result. The way to find the point is to test it on your own tasks: run the same few tasks on two models and compare the cost per success, not the cost per call. [Chapter 6.4](6-4-variance.html) says how to do that honestly.

### Pick by task, and check the setting

My own rule of thumb, just as unmeasured, is to use a strong model for thinking (a plan, an approach, a hard bug) and a medium model for doing (a change whose plan is already clear). Some tools also let you set **reasoning effort**, a setting on some models that controls how long they think before they answer. More thinking usually means more output tokens and more time. I have not tested whether Copilot lets you set it from a harness, so check your own tool.

### How you are billed in Copilot (as of late October 2026)

What you actually pay depends on your plan, and for Copilot the plans change often, so check the date against your own.

- **Monthly Copilot plans:** since June 1, 2026, Copilot has been moving to usage-based billing. Premium request units were replaced by GitHub AI Credits, and usage is calculated from input, output and cached tokens at each model's listed API rates. Code completions and next edit suggestions stay included. ([GitHub blog](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/))
- **Annual Pro and Pro+ plans** stay on the older premium request model until they expire. There, each prompt you send counts as a request multiplied by the model's multiplier, while the tool calls the agent makes do not count. ([Copilot requests](https://docs.github.com/en/copilot/concepts/billing/copilot-requests))

The two models reward different habits. Under per-request billing a long autonomous run is cheap for you, so it can pay to do a big task in a single prompt. Under token billing, a long run costs in proportion to how much it reads. Which one you are on decides how much the rest of this chapter matters, and if your plan is billed by tokens, it matters a lot.

### When the result is wrong, change the model last

Back to choosing a model, then. When a result comes back wrong, the easy reaction is to switch to a bigger model. It is also the most expensive fix, and often the wrong one. Before reaching for it, look at what went wrong:

| What went wrong | Try first |
| --- | --- |
| It did not know a rule, a name or how the project does it | Write it into the rules or a knowledge file. A bigger model does not know it either |
| It said "done" and it was not | Add a check: run the tests ([chapter 5.4](5-4-self-checks.html)) |
| It lost the thread in a long session | Start a new session and carry the state in files ([chapter 3.2](3-2-long-sessions.html)) |
| It knew everything and still reasoned badly | Now try a stronger model |

### Four ways to save, and how each can go too far

Choosing the model is only one lever. The first of the four ways below comes before any of the three parts of a task's cost: not calling the model at all. The other three follow the parts in order. Each of the four can also go too far.

1. **Use the model less.** If code can do it, do not ask a model. Counting, copying files, converting a Word file into text and checking a format are jobs a script does the same way every time, using no tokens. The danger is moving judgment into code that cannot judge, and [chapter 5.9](5-9-who-decides.html) draws that line.
2. **Read less.** Keep the rules short, load details only when they are needed, and ask for a diff rather than the whole file. The danger is that if it reads too little, it guesses, and the rework costs more than the reading saved.
3. **Write less.** Ask for short answers, such as a one-line verdict or a short list. The danger is output so terse that the next step cannot use it.
4. **Redo less.** Agree the plan before the work starts, keep state in files so a lost session can be picked up, and cap the number of retries. The danger is a cap that cuts off useful work, so set caps from what you saw, not from fear.

Also mind the standing costs, which you pay on every call before any of these choices come in. Every tool the agent has adds its name, description and parameters to the input of every call ([chapter 1.2](1-2-tool-calling.html)), and every rule you inject rides along on every turn.

### When a bill surprises you

When a bill comes in higher than you expected, start with three questions.

1. Which call or turn read the most? Look at the usage page of your tool, and at the biggest tasks.
2. What was in the context that did not need to be there? Old tool results, a large file read in full, a long rules file?
3. Did the task get redone? If so, why did the first attempt fail?

The same habit of checking helps when you are choosing between two models, and for that a small experiment is enough. Take one task whose right answer you know, run it on two models three times each, and note the usage and whether the result was right. Then compare the cost per success, and do not decide from one run. A table with four columns will do:

| Run | Model | Usage (from your usage page) | Right? |
| --- | --- | --- | --- |
| 1 | A | | |
| 2 | A | | |
| 3 | A | | |
| 1 | B | | |
| 2 | B | | |
| 3 | B | | |

## What saving costs, and what I cannot see {#costs-and-traps}

Everything I have said about savings is "by design", not read off a bill, because of what my tools let me see. My own harness records no token counts in its log. For how much a task really used, I read the platform's session record, which reports credits and premium requests, and I do not convert those to money.

The savings also have costs of their own. A [hook](2-2-hooks.html) that runs on tool calls adds a small delay, independent checks call the model again, and rules injected on every prompt cost tokens on every prompt. I accept those on purpose, for control, but they are still costs.

The trap that looks most like thrift is reading too little. The cheapest call is the one that guesses wrong and is thrown away. If a task keeps failing for lack of context, the answer is to give it the right context, not less of it.

Prices and plans also change. The cache multipliers and the Copilot billing above are as of the dates in the sources, and I would expect them to move. What has been moving, though, is not only the prices but what gets counted.

## Is the market pricing it the same way? {#industry}
{status: industry}

The two providers this chapter leans on point the same way. Anthropic prices cached reads at a fraction of normal input, and says tool definitions are counted as input tokens on every request ([Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)). GitHub moved Copilot from counting requests to counting tokens ([GitHub blog](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)). In other words, the market now charges for what the model reads and writes, which is the argument of this chapter.

## When to delete these tricks {#when-to-delete-it}
{status: industry}

Much of this chapter is advice for a world where reading is expensive. If reading becomes so cheap that the extra work of trimming context costs more than it saves, drop the tricks, but keep the habit of measuring cost per finished task. I would also look again if a platform started showing per-task cost on its own, because then you would need to guess less.

## Try it on your own setup {#try-it}

::: prompt
Estimate what is sent to the model on every call in this repository, before I type anything. List each always-loaded item: instruction files, rules, tool and server definitions, anything injected automatically. Give each an approximate size in tokens (a rough count is fine) and sort the list from largest to smallest. Mark items that look stale, duplicated or rarely useful. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic docs: [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- GitHub: [Copilot is moving to usage-based billing](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)
- GitHub docs: [Copilot requests](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)

## Explore it in the harness {#explore}

My harness is built around reading less and redoing less. Rules are loaded in layers, state lives in files, and checks are off unless you ask for them. It also says plainly what it cannot see about cost. The harness can open the real files with you and show each of these from the inside.

::: prompt
/harness-rookie-wondering I have read the chapter "Choosing a model: cost per finished task". Teach me how this harness reads less, writes less and redoes less, and what it can and cannot tell me about the real usage of a task. Open the real files with me and draw how the pieces fit together.
:::
