This chapter assumes you have used an AI coding agent and have seen a usage or billing page for it. Nothing else.

## In one sentence {#in-one-sentence}

Judge a model by what it costs to get one task done, not by its price per token. Most of the cost is what the model reads, so reading less and redoing less saves the most.

## For leaders {#for-leaders}

- **The decision:** judge models and setups by what it costs to finish one task, not by the price per token. And when a result is bad, try the cheaper fixes (missing rule, missing check, lost thread) before paying for a bigger model.
- **The risk:** in a long agent task most of the tokens are the model re-reading the same material. In my worked example, with round numbers I chose, reading was over 90% of the tokens. A cache can cut the bill a lot, but only while the start of the input stays unchanged.
- **The cost of doing it right:** mostly setup time and a habit of measuring. A fair model comparison is a few tasks, run about three times each.
- **Ask the team:** "What does one finished task cost us, and when did we last check that number?"

## The problem {#problem}

A model comparison usually starts with a price list: so many dollars per million tokens. It is the number you can look up, so it is the number people use. But you never buy tokens for their own sake. You buy a task finished: a bug fixed, a report written. What matters is the total for that.

Two things make the price list a poor guide. A cheap model that fails the task and has to be asked again may cost more than a strong one that gets it right the first time. And in an agent, the number of tokens is not what you expect, as the next section shows.

### Five words first

- A **token** is a small piece of text, roughly a short word or part of one. Models read and write in tokens, and bills are counted in them.
- **Input** tokens are what the model reads in a call. **Output** tokens are what it writes. They are priced differently, and output is usually the more expensive per token.
- The **context window** is how much text the model can see at once: your request, the rules, the files it read, the results of earlier tools. It has a size limit. [Chapter 3.1](3-1-context-budget.html) is about managing it.
- **Reasoning effort** is a setting on some models that controls how long they think before they answer. More thinking usually means more output tokens and more time.
- The **prompt cache** lets the provider remember a long beginning of your input, so a later call that starts with the same text can be charged less for it.

### Where the tokens go in an agent

In a chat, you send a question and get an answer. In an agent loop ([chapter 2.1](2-1-agent-loop.html)) the model is called again after every tool result. And every call sends the whole conversation so far: rules, request, every file it read, every result. The model has no memory between calls, so that is the only way it knows what happened.

::: figure 1-1-token-flow

Here is the arithmetic with round numbers I chose to make it easy, not numbers I measured. Say the rules and your request are 10,000 tokens, and each tool result adds 5,000. Over 10 calls, the model reads about 10,000 + 15,000 + 20,000 + ... = 325,000 tokens, but writes perhaps a few hundred tokens per call. In this example reading is more than 90% of the tokens. The real share depends on your task, but the longer the loop, the more it leans toward reading.

Output costs more per token, so tokens are not the same as money. But the shape holds: a long agent task is mostly the model reading the same material again and again. That is why the chapter's second half is about reading less.

I can show one real case. In [chapter 2.3](2-3-subagents.html) I gave the same four tasks to a team of three agents with job titles and to a single agent. Both got every task right. The team used about 4.5 times as much. The largest waste was re-reading: each new agent started with an empty context and had to read the same files again. It was four small tasks, each run once, so trust the direction and not the ratio.

### The prompt cache changes the sum

Because so much of every call is the same beginning, providers offer a **prompt cache**. On Anthropic's API, reading cached input costs a tenth of the base input price on most models, and less on some. Writing to the cache costs more than a normal read: 1.25 times for a five-minute cache, 2 times for a one-hour cache. ([Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching))

Three things follow, and they change how you save money:

- **A stable beginning pays.** The cache works on an exact match from the start of the input. If you change something near the top (an edited rule, a different tool list), everything after it misses the cache.
- **A pause can cost you.** A cache lives for a short time. A conversation you leave for an hour and return to may pay full price to rebuild.
- **The cheapest token is one that is not sent.** Even a cache read is not free. Reading less is still the first thing to try.

Here is the same example with a cache that hits every time, counting input only and using the five-minute prices. The first call writes 10,000 tokens at 1.25 times, which is 12,500. Each of the next nine calls reads the earlier text from the cache (10,000 up to 50,000 tokens, 270,000 in all, at 0.1 times, which is 27,000) and writes its 5,000 new tokens (45,000 in all, at 1.25 times, which is 56,250). The total is about 96,000 token-prices instead of 325,000, and now the repeated reading is less than a third of it. So the cache changes where the money goes: from re-reading to new material. That is why the earlier "more than 90%" is a count of tokens read, not a share of the bill, and why a team with a well-kept cache can read a lot and still pay little. Misses, which the first two bullets describe, bring the cost back toward the 325,000.

## How it works {#how-it-works}

### What a task costs

Think of a task's cost as three parts.

::: figure 1-1-cost-parts

In detail:

1. **What the model reads**, across every call, discounted where the cache hits.
2. **What the model writes**: the answer, the code, the thinking.
3. **Redoing**: a wrong answer, a lost thread, a repeated attempt. Redoing is a multiplier on parts 1 and 2.

Most savings come from the first and the third. A good rule of thumb is: **do things in the cheapest way that is enough**.

### When a strong model is cheaper

A stronger model costs more per token. It can still cost less per finished task when it gets the answer in one pass and the weaker one needs three. It can also be a waste, if the task was easy.

I have no measurement of my own for where this flips. It is an argument, not a result, and the way to find the point is to test it on your own tasks: run the same few tasks on two models and compare the cost per success, not per call. [Chapter 6.4](6-4-variance.html) says how to do that honestly.

### Pick by task, and check the setting

My rule of thumb, which I have not measured: use a strong model for thinking (a plan, an approach, a hard bug) and a medium model for doing (a change whose plan is already clear). Some tools let you set reasoning effort too. I have not tested whether Copilot lets you set it from a harness, so check your own tool.

### How you are billed in Copilot (as of late October 2026)

This part changes often, so check the date and your own plan.

- **Monthly Copilot plans:** since June 1, 2026 Copilot has been moving to usage-based billing. Premium request units were replaced by GitHub AI Credits, and usage is calculated from input, output and cached tokens, at the listed API rates of each model. Code completions and next edit suggestions stay included. ([GitHub blog](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/))
- **Annual Pro and Pro+ plans** stay on the older premium request model until they expire. There, each prompt you send counts as a request multiplied by the model's multiplier, and the tool calls the agent makes do not count. ([Copilot requests](https://docs.github.com/en/copilot/concepts/billing/copilot-requests))

The two models reward different habits. Under per-request billing a long autonomous run is cheap to you, so doing big tasks in a single prompt can pay. Under token billing, a long run costs in proportion to how much it reads. Which one you are on decides how much the rest of this chapter matters. If your plan is billed by tokens, it matters a lot.

### When the result is wrong, change the model last

The easy reaction to a bad result is to switch to a bigger model. It is the most expensive fix, and often the wrong one. Look at what went wrong first:

| What went wrong | Try first |
| --- | --- |
| It did not know a rule, a name or how the project does it | Write it into the rules or a knowledge file. A bigger model does not know it either |
| It said "done" and it was not | Add a check: run the tests ([chapter 5.4](5-4-self-checks.html)) |
| It lost the thread in a long session | Start a new session and carry the state in files ([chapter 3.2](3-2-long-sessions.html)) |
| It knew everything and still reasoned badly | Now try a stronger model |

### Four ways to save, and how each can go too far

1. **Use the model less.** If code can do it, do not ask a model. Counting, copying files, converting a Word file into text, checking a format: a script does these the same way every time and uses no tokens. The danger is moving judgment into code that cannot judge. [Chapter 5.9](5-9-who-decides.html) draws that line.
2. **Read less.** Keep the rules short, load details only when needed, and ask for a diff and not the whole file. Danger: if it reads too little, it guesses, and the rework costs more than the reading saved.
3. **Write less.** Ask for short answers, a one-line verdict, a short list. Danger: terse output the next step cannot use.
4. **Redo less.** Agree the plan before the work starts, keep state in files so a lost session can be picked up, and cap the number of retries. Danger: caps that cut off useful work. Set them from what you saw, not from fear.

Also mind the standing costs. Every tool the agent has adds its name, description and parameters to the input of every call ([chapter 1.2](1-2-tool-calling.html)), and every rule you inject rides along on every turn.

### Test your own setup

**Three questions** when a bill surprises you:

1. Which call or turn read the most? Look at the usage page of your tool, and the biggest tasks.
2. What was in the context that did not need to be there? Old tool results, a large file read in full, a long rules file?
3. Did the task get redone? If so, why did the first attempt fail?

**A small experiment.** Take one task you know the right answer to. Run it on two models, three times each, and note the usage and whether it was right. Then compare cost per success. Do not decide from one run. A table with four columns is enough:

| Run | Model | Usage (from your usage page) | Right? |
| --- | --- | --- | --- |
| 1 | A | | |
| 2 | A | | |
| 3 | A | | |
| 1 | B | | |
| 2 | B | | |
| 3 | B | | |

## Costs and traps {#costs-and-traps}

**What I can and cannot see.** My own harness records no token counts in its log. For how much a task really used, I read the platform's session record, which reports credits and premium requests and which I do not convert to money. So everything I say about savings is "by design", not a bill.

**The savings are not free.** A [hook](2-2-hooks.html) that runs on tool calls adds a small delay. Independent checks call the model again. Rules injected on every prompt cost tokens on every prompt. I accept those on purpose, for control, but they are costs.

**Reading too little is the trap that looks like thrift.** The cheapest call is the one that guesses wrong and is thrown away. If a task keeps failing for lack of context, the answer is to give it the right context, not to give it less.

**Prices and plans change.** The cache multipliers and the Copilot billing above are as of the dates in the sources, and I would expect them to move.

## What the industry says {#industry}
{status: industry}

- **Anthropic** prices cached reads at a fraction of normal input, and says tool definitions are counted as input tokens on every request. ([Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview))
- **GitHub** moved Copilot from counting requests to counting tokens. ([GitHub blog](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/))

The direction is the same: the market now charges for what the model reads and writes, which is the argument of this chapter.

## When to delete it {#when-to-delete-it}
{status: industry}

Much of this chapter is advice for a world where reading is expensive. If reading becomes cheap enough that the extra work of trimming context costs more than it saves, drop the tricks and keep the habit of measuring cost per finished task. I would also look again if a platform started showing per-task cost on its own, because then you would need to guess less.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Estimate what is sent to the model on every call in this repository, before I type anything. List each always-loaded item: instruction files, rules, tool and server definitions, anything injected automatically. Give each an approximate size in tokens (a rough count is fine) and sort the list from largest to smallest. Mark items that look stale, duplicated or rarely useful. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic docs: [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- GitHub: [Copilot is moving to usage-based billing](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)
- GitHub docs: [Copilot requests](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)

## Explore it in the harness {#explore}

My harness is built around the idea of reading less and redoing less: rules are loaded in layers, state lives in files, checks are off unless you ask. It also says plainly what it cannot see about cost. The harness can show you each of these from the inside, with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Choosing a model: cost per finished task". Teach me how this harness reads less, writes less and redoes less, and what it can and cannot tell me about the real usage of a task. Open the real files with me and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.