This chapter assumes you have read [The agent loop](2-1-agent-loop.html), or know that an agent reads text and answers with text.

## In one sentence {#in-one-sentence}

Rules, knowledge, files and tool results all share one window, and each one crowds the others out. So manage context like a budget: fetch it when needed instead of loading it all.

## For leaders {#for-leaders}

- **The decision:** treat what the agent reads as a budget. Decide what is always loaded and what is fetched only when a task needs it.
- **The risk:** everything shares one window, and a window with room left is not one that performs well, so a rule buried in a long, noisy context is more likely to be missed. I have no number for how much; the advice comes from the platform makers and my own design, not from a test of mine.
- **The cost of doing it right:** mostly setup time: layering the rules, shortening tool output, and keeping any index true. Loading too little has its own price: the agent guesses.
- **Ask the team:** "What is loaded on every turn, and how much of it applies to the task in front of us?"

## The problem {#problem}

The usual advice for a weak answer is "give the AI more information". Paste the whole style guide. Add every rule. Let it read all the files. It feels safe: more facts, fewer mistakes.

It often goes the other way. Think of a desk. You can lay out every document for a project, and then you cannot find the one you need, and there is no room to write. An agent has a desk like that. It is called the **context window**: all the text the model can look at in one turn. It holds the rules, your words, the files the agent read, the results of its tool calls and its own earlier answers. It has a size limit. And, as I will show, it has a second limit that is not about size.

What I can say comes from two places. The first is from the people who build these tools. Anthropic writes that context "must be treated as a finite resource with diminishing marginal returns" ([Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)). VS Code's guide says to "avoid context overload that can dilute focus" ([Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)). The second is the way I built my own setup: almost every design choice in it is a way to put less into the window. The cost side of the same idea is in [Models and cost](1-1-models-and-cost.html): most of what a task costs is what the model reads. I did not run a clean experiment for this chapter.

## How it works {#how-it-works}

### What is in the window

::: figure 3-1-window

Six things share it:

1. **Rules and instructions** that the platform puts in every time.
2. **The list of tools**, with each tool's description. The model needs it to know what it can ask for. With many tools, for example from several MCP servers ([MCP](1-3-mcp.html)), this list can be a large part of the window. I have not measured how large.
3. **Your messages.**
4. **Files the agent read.** A file goes in as whole text, however much of it matters.
5. **Tool results:** search listings, command output, test logs. These are often the biggest part, and the part nobody looks at.
6. **The agent's own earlier answers.**

Each turn of the loop the model reads all of it again, plus one more result (the cost of this is in [Models and cost](1-1-models-and-cost.html)). So the window only grows, until it is full. Then the platform has to cut or summarise the oldest parts, and details are lost. [Long chats get worse](3-2-long-sessions.html) is about that.

### Two limits, not one

Size is the obvious limit. The second one is attention. Anthropic describes it as an "attention budget" that the model draws on when it reads a lot of text. The practical meaning: a window that still has room is not a window that performs well. A rule buried in a long, noisy context is more likely to be missed than the same rule in a short one. I take this as a reason to put less in, even when it all fits. That step is my own inference, not something Anthropic says. How big the effect is depends on the model and the task, and I have not measured it.

### Load everything, load an index, or both

Here is the choice behind most of the decisions in this part of the book.

**Load everything first.** The agent starts with all the rules and all the notes in the window. It never has to look anything up. But the window is spent before work starts, most of it on things this task does not need.

**Load an index, fetch what the task needs.** The agent starts with a short list: names and one-line descriptions of the things that exist. When the task needs one of them, it opens that one. Anthropic calls this a "just in time" approach: the agent keeps lightweight identifiers (a file path, a name) and loads the data at run time.

**Both.** Anthropic's own suggestion is a mix: "the most effective agents might employ a hybrid strategy, retrieving some data up front for speed" and exploring further on their own. Their example is Claude Code, which drops its instruction file into the context up front and uses search tools to find the rest as it goes.

The other side wins in some cases. For a small task, or a small set of rules, loading everything is simpler and costs little. And where a missed fact is expensive, I would rather pay for it to be in the window than bet on the agent opening the right file.

One more point on cost. A beginning that is loaded every time and never changes can be cached, and a cache read is much cheaper than a normal read ([Models and cost](1-1-models-and-cost.html)). So "load everything" is cheaper than the token count suggests, if the beginning stays stable. The attention limit above does not go away with a cache. I have not tested the cache on Copilot.

::: figure 3-1-load-when

It is the same as a library. You do not carry the whole library to your desk. You use the catalog, then fetch the one book.

For this to work, three things must be true.

- **The index entry must say when to open the thing.** The agent decides from the one line alone. A vague line means it opens the wrong thing or never opens the right one. This is why the description of a skill matters so much ([Instructions and skills](3-3-instructions-and-skills.html)).
- **The fetch must be cheap and exact.** If fetching means reading a whole folder, the index saved nothing.
- **The agent must know it does not know.** An index cannot help with a thing the agent does not realise is missing. That is the real risk, and I come back to it below.

### Ways to read less

These are the ones I use. Each is a way to keep a thing out of the window, or to take it out. The two cheapest to start with are layering your rules and shortening tool output.

- **Rules by layers.** Keep a small set of rules always loaded. Put the rest where they are read only for the files or the job they apply to. Rules that never change the next step are only noise. (How: [Instructions and skills](3-3-instructions-and-skills.html).)
- **Search first, then read.** Ask the agent to find where something is, then read only that part of the file, not the whole file. Or give it a short map of the project written ahead of time: an index in the sense above. It only wins if reading it beats searching, and it only stays true if someone keeps it true. I have not tested whether mine wins ([A knowledge base from code](8-1-why-a-knowledge-base.html)).
- **Make tool output short.** A command that prints 2,000 lines puts 2,000 lines in the window. Filter it, or print only the failures.
- **Remind with a few lines, not a page.** In my setup, only a short piece of the rules is added to each prompt. With a task ([Manage tasks, not chats](5-1-tasks.html)), it says how far the task has got. It is a reminder, and the full text is read when it is needed.
- **Hand a big read to a subagent** ([Use subagents sparingly](2-3-subagents.html), [Long chats get worse](3-2-long-sessions.html)).
- **Write state into files**, so a new chat reads one short file and not the old conversation. A new chat is an empty window; when to start one, and what to carry over, is in [Long chats get worse](3-2-long-sessions.html).

### Test your own setup

**Three questions:**

1. What is loaded every time? Count the lines of your always-on rules. How much of that applies to the task you are doing now? (In Claude Code, the `/context` command shows what is using the window. I have not checked what Copilot offers.)
2. What was the biggest thing the agent read last time? A file? A log? Was all of it needed?
3. If the agent started a new chat now, what would it have to read to carry on? Is that in a file?

**A test you can run today.** Take a task you know the answer to. Run it twice in a new chat each time. In the first, paste the whole file or doc in the prompt. In the second, name the file and the part, and let the agent read only that. Compare the answer, the time and the usage. To trust the difference, repeat it a few times each, and score both runs the same way. For each run, write down four things: whether the answer was right, the time, the usage your tool shows, and anything the agent missed.

## Costs and traps {#costs-and-traps}

**Loading less can lose something the agent needed.** An index is a bet that the agent will open the right thing. When it does not, it works from a guess. The fix is better descriptions, and a check that the thing was opened when it should be. To check, run a task you know needs a certain file, look at the tool's log of what was opened, and count how often it was not. A new chat, a rule or a skill is lost the same way.

**Summaries lose details.** A subagent's report and a platform's compression both shrink text, and both can drop the one line that mattered. Use them where a short version is enough.

**An index must be kept true.** A map that is out of date costs more than it saves, because the agent trusts it. [Keep it true](8-5-kb-keep-true.html) is about that.

**No numbers here.** I know of no clean measure of how much attention is lost as a window fills, for Copilot's models. The advice in this chapter comes from the platform makers and from my own design, not from a test of mine.

## What the industry says {#industry}
{status: industry}

- **Anthropic:** context is "a finite resource with diminishing marginal returns", and agents can load data "just in time" by keeping light references. ([Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))
- **VS Code:** "Start with concise context and expand only when needed." ([Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide))

The two agree on the direction. Neither gives a number I can quote for how much to load.

## When to delete it {#when-to-delete-it}
{status: industry}

The reasoning stays as long as the window has a size and the model reads it every turn. What may go is my own effort: manual layering of rules and manual new chats. If the platform loads rules by relevance well, and compresses without dropping what matters, I will stop doing it by hand. A very large window does not remove the second limit by itself. I would want a test of that first.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Look at the commands this project uses to test, lint, build and search. For each, tell me roughly how much text it prints when it succeeds and when it fails, and whether that output would flood your context window if you ran it. Suggest a quieter way to run each one, such as printing only failures or a summary. Rank the three noisiest. Do not change any files, and do not run anything that changes state.
:::

## Go deeper {#go-deeper}

- Anthropic: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- [Long chats get worse](3-2-long-sessions.html): what happens as the window fills

## Explore it in the harness {#explore}

The harness is built around loading little: a short always-on rulebook, a README that is only an index, and skills whose name and description are read first. You can see each one and how much it loads. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Context is a budget". Teach me what this harness loads into the context every time, and what it leaves to be read when needed. Open the real files with me, count what is always on, and show me how a new session picks up a task.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
