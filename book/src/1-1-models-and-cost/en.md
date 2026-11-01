This chapter assumes only that you have used an AI coding agent and have looked at its usage or billing page.

## In one sentence {#in-one-sentence}

Choose a model by what it costs to finish a task, not by the price of a token, and since most of that money goes to what the model rereads, reading less and redoing less save the most.

## For leaders {#for-leaders}

- **The decision:** judge models and setups by the cost of finishing a task, not by the price per token. When results are poor, try the cheap fixes first (a missing rule, a missing check, a lost thread), and only then pay for a bigger model.
- **The risk:** on a long agent task, most of the money goes to the model rereading the same material. In my worked example (round numbers I picked), reading takes more than 95% of the money. Caching can bring the bill down to about a quarter, but only if the start of the input stays the same.
- **The cost of doing it right:** mainly setup time, plus a habit of measuring. A fair comparison of models means picking a few tasks and running each about three times.
- **Ask the team:** "What does it cost us to finish a task, and when did we last check that number?"

## Where your money goes {#problem}

People usually start choosing a model from the price list: Sonnet 5.5 is $2 per million input tokens and $10 per million output tokens, and Opus 5.5 is $4 and $20 ([Pricing](https://platform.claude.com/docs/en/about-claude/pricing), prices as of late October 2026). A token is the unit a model reads and writes, roughly a short English word or part of a word. What the model reads is input tokens, what it writes is output tokens, and output usually costs much more. List prices are easy to look up, so everyone compares them, but you're not really buying tokens. You're buying a finished job, such as a fixed bug, so what you need to compare is what the whole job cost. That number is a long way from the unit price, for two reasons: a cheap model that botches the job has to run again, which can end up costing more than an expensive model that gets it right the first time, and an agent uses far more tokens than you'd think, most of them on reading.

### Where the tokens go in an agent

In a chat, you ask a question, the model answers, and that's one call. An agent runs a loop ([The agent loop, and where you can step in](2-1-agent-loop.html)): the model asks to read a file, a program reads it and sends back the result, and the model decides what to do next, so every tool result means calling the model again. The model has no memory between calls, so each call sends the whole conversation so far all over again: the rules, the request, every file it has read and every tool result. All of this sits in the **context window**, the full text the model can see at once. The window has a size limit ([Context is a budget](3-1-context-budget.html)), and you pay for what's in it every time you make a call.

::: figure 1-1-token-flow

Let's work it out with round numbers, which I picked to keep the arithmetic easy and did not measure. Say the rules and the request come to 10,000 tokens, each tool result adds 5,000, and a task makes 10 calls to the model, writing 300 tokens each time. The model reads 10,000 + 15,000 + ... + 55,000 = 325,000 tokens in total and writes only 3,000. In money the gap is just as wide: at Sonnet 5.5 prices, reading costs $0.65 and writing only $0.03, because although output costs 5 times as much per token, the model reads more than 100 times as much. The longer the loop runs, the further the money tilts toward reading, because every extra call rereads everything before it.

### Prompt caching changes the math

The start of every call is almost the same, so model providers offer **prompt caching**: the provider remembers the start of your input, and if the next call begins with exactly the same text, that part is charged at a very low price. Anthropic's prices work like this. Writing to the cache costs more than normal input, 1.25 times for a 5-minute cache and 2 times for a 1-hour cache, while reading from the cache costs far less: a tenth of the input price on most models, and a twentieth on Opus 5.5 and Sonnet 5.5 ([Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)).

Take the same example at Sonnet 5.5 prices and assume every call hits the cache. The first call writes 10,000 tokens to the cache. Each of the next nine calls reads everything before it from the cache, 270,000 tokens across the nine, and writes its new 5,000 tokens to the cache, 45,000 across the nine. That comes to $0.1375 for writes and $0.027 for cache reads, about $0.16 in all, a quarter of the original $0.65. Most of that $0.16 is the write charge for new content, which caching can't save and only reading less can, so even with every call hitting the cache, reading less is still the first thing to try.

Caching also breaks easily, in three ways. The first is that the start changed: the cache matches only identical content, in the order tool definitions, system prompt, conversation messages, and a change at one level invalidates that level and everything after it, so editing one tool's description loses the whole cache, and a rules file shouldn't start with something that changes every time, such as the current time. The second is stopping for too long: the default cache lives 5 minutes and is renewed for free each time it's used, so if you go to a meeting, it expires. The third is a start that's too short: below the minimum length nothing is cached, and you get no error. For Sonnet 5.5 the minimum is 512 tokens, and some older models need 4,096. If you keep missing the cache, the cost goes back to around $0.65 or even higher, because a cache write costs more than normal input.

## How to add up a task's cost, and where to save {#how-it-works}

::: figure 1-1-cost-parts

A task's cost has three parts: what the model reads (all calls added up, with cache hits discounted), what it writes (answers, code, thinking), and rework (wrong answers, lost threads, repeated attempts). Rework isn't a separate charge. It's a multiplier on the other two, because every time you redo something, you pay for both again. Most of the savings are at the two ends, reading and rework, and a good rule of thumb is to use the cheapest approach that's good enough.

### When the expensive model is cheaper

An expensive model costs more per token, but if it gets the job right the first time, it can cost less per finished task. The math is simple: the cost of finishing a task is the cost of one run divided by the success rate. Opus 5.5 costs twice as much per token as Sonnet 5.5, so if one run uses about the same tokens on both, Opus is cheaper only when Sonnet's success rate is less than half of Opus's. If Opus gets 80% of tasks right, for example, Sonnet has to be below 40%. That's only the token bill. Add the time you spend watching it and cleaning up after it, and the break-even point moves further toward the expensive model. On the other hand, if the task is simple enough that both models get it right the first time, the expensive one is money wasted.

You can only measure success rates on your own tasks: run the same few tasks several times on both models, and compare the cost per success, not the cost per call ([One run proves nothing](6-4-variance.html)).

### Choose the model by the task, then check the reasoning effort

My own rule of thumb is a strong model for thinking, such as making a plan, working out an approach or digging into a hard bug, and a mid-level model for doing, such as a change the plan has already made clear. There's also a setting called **reasoning effort** (thinking effort), which controls how long the model thinks before it answers. More thinking usually means more output tokens and more time. In VS Code you set it in the model picker, through the arrow next to the model name, and models that don't support it don't show the option ([AI language models](https://code.visualstudio.com/docs/copilot/customization/language-models)). The highest setting isn't always better: in the LangChain experiment in [What is Harness Engineering?](0-1-the-gap-and-the-map.html), running at the top level throughout actually scored lower, because many tasks timed out.

### How Copilot bills (as of late October 2026)

Since June 1, 2026, Copilot's monthly plans have been on usage-based billing. GitHub AI Credits replaced premium requests, 1 credit is worth $0.01, and usage is calculated from input, output and cached tokens at each model's published API rates. Pro, for example, is $10 a month and includes $10 of credits, and code completions and Next Edit suggestions don't use credits ([GitHub blog](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/), [Usage-based billing](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals)). Annual Pro and Pro+ plans stay on the old premium request model until they expire, with 300 requests a month on Pro and 1,500 on Pro+. Each prompt you send counts as one request, times the model's multiplier, and the tool calls the agent makes on its own don't count ([Copilot requests](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)).

The two models encourage different habits. When you pay per request, a long autonomous run is cheap for you, so putting a big job into one prompt can be a good deal. When you pay per token, a run costs in proportion to what it reads, and the savings in this chapter matter a lot.

### When the result is wrong, change the model last

When the result is wrong, the first idea that comes to mind is to switch to a bigger model, but that's the most expensive fix and it often doesn't help, so look first at what actually went wrong:

| What went wrong | Try first |
| --- | --- |
| It doesn't know a rule, a name, or how the project does something | Write it into the rules or a knowledge file. A bigger model wouldn't know it either |
| It says "done" and it isn't | Add a check: run the tests ([Let the agent check its own work](5-4-self-checks.html)) |
| It loses the thread in a long session | Start a new session and carry the state over in a file ([Long chats get worse](3-2-long-sessions.html)) |
| It knows everything and still reasons badly | Now try a stronger model |

### Four ways to save, and how each can go too far

The first way comes before the three parts of the cost: don't call the model at all. The other three map to reading, writing and rework, and all four can go too far.

1. **Use the model less.** If code can do it, don't ask the model. Counting, copying files, converting a Word file to text and checking a format are jobs a script does the same way every time, at no token cost. Going too far means handing a judgment call to code that can't judge ([Who decides: code, a cheap model, the main model, a person](5-9-who-decides.html)).
2. **Read less.** Keep rules short, load details when they're needed, and ask for a diff rather than a whole file. Going too far means the agent guesses when it lacks information, and the rework costs more than the reading you saved.
3. **Write less.** Ask for a one-sentence conclusion or a short list. Going too far means the output is too thin for the next step to use.
4. **Redo less.** Agree on a plan before starting, keep state in files so work survives a lost session, and put a limit on retries. Going too far means the limit cuts off useful work, so set it from what you've seen, not from what you fear.

There's also a fixed cost you pay on every call, whatever you choose during the task. Once a tool is loaded into the context, its name, description and parameters count toward the input of every call ([When an Agent misuses a tool, check its description and errors first](1-2-tool-calling.html)), and every rule you inject comes along on every turn, so remove the tools and rules you don't use. Not every tool has to be loaded, though, because Claude Code and VS Code (Claude Sonnet 4.5, Opus 4.5 and later) use tool search by default, which holds some tools back and loads a full definition only when the model searches for it ([What should you think through before connecting an MCP server?](1-3-mcp.html)).

### When the bill surprises you

If the bill is higher than you expected, ask yourself three questions. First, which call or turn read the most? Look at your tool's usage page and at your biggest tasks. Second, what's in the context that doesn't need to be there, such as old tool results, big files read in full, or a long rules file? Third, was any task redone, and if so, why did the first attempt fail?

When you're choosing between two models, a small experiment is enough: pick a task you know the right answer to, run it three times on each model, record the usage and whether the result was right, and compare the cost per success. Don't decide from one run. A four-column table will do:

| Run | Model | Usage (from your usage page) | Right? |
| --- | --- | --- | --- |
| 1 | A | | |
| 2 | A | | |
| 3 | A | | |
| 1 | B | | |
| 2 | B | | |
| 3 | B | | |

## Saving has costs too, and the easiest trap is reading too little {#costs-and-traps}

The easiest trap to fall into is reading too little. The cheapest call may well be the one that guessed wrong and got thrown away, so if a task keeps failing for lack of context, the fix is to give it the right context, not less of it.

Controls cost money too: a [hook](2-2-hooks.html) that runs on tool calls adds a little delay, an independent check means another model call, and a rule injected into every prompt costs tokens on every prompt. I accept these on purpose in exchange for control, but they're still costs.

The prices and Copilot's billing above are as of late October 2026, and they will change. What gets counted changes too, as Copilot's move from counting requests to counting tokens showed.

## Model providers charge this way too {#industry}
{status: industry}

Anthropic prices cache reads at a small fraction of normal input and states that tool definitions count as input tokens too ([Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)). GitHub moved Copilot from per-request to per-token billing ([GitHub blog](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)). The market now charges by what the model reads and writes, which is why counting cost per task is what lines up with the bill.

## When to delete these cost-saving tricks {#when-to-delete-it}
{status: industry}

Much of this chapter is advice for a world where reading is expensive. If reading ever gets so cheap that trimming context takes more effort than it saves, drop these tricks and keep only the habit of counting the cost of each finished task. And if a platform starts showing the cost of each task by itself, I'll think again, because then you'll have less to guess.

## Try it on your own setup {#try-it}

::: prompt
Estimate what is sent to the model on every call in this repository, before I type anything. List each always-loaded item: instruction files, rules, tool and server definitions, anything injected automatically. Give each an approximate size in tokens (a rough count is fine) and sort the list from largest to smallest. Mark items that look stale, duplicated or rarely useful. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic docs: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing), [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- GitHub: [Copilot is moving to usage-based billing](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)
- GitHub docs: [Usage-based billing](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals), [Copilot requests](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)

## Explore it in the harness {#explore}

My harness is built around reading less and redoing less. Rules are loaded in layers, state lives in files, and checks are off unless you ask for them. It also says plainly what it cannot see about cost. The harness can open the real files with you and show each of these from the inside.

::: prompt
/harness-rookie-wondering I have read the chapter "Don't pick a model by token price alone". Teach me how this harness reads less, writes less and redoes less, and what it can and cannot tell me about the real usage of a task. Open the real files with me and draw how the pieces fit together.
:::
