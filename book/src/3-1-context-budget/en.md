This chapter assumes you have read [The agent loop](2-1-agent-loop.html), or know that an agent reads text and answers with text.

## In one sentence {#in-one-sentence}

Rules, knowledge, files and tool results all share one window, and each one crowds the others out. So manage context like a budget: fetch it when needed instead of loading it all.

## For leaders {#for-leaders}

- **The decision:** treat what the agent reads as a budget, and decide what is always loaded and what is fetched only when a task needs it.
- **The risk:** everything shares one window, and having room left does not make a window perform well. A rule buried in a long, noisy context is more likely to be missed. I have no number for how much. The advice comes from the platform makers and my own design, not from a test of mine.
- **The cost of doing it right:** mostly setup time, spent layering the rules, shortening tool output and keeping any index true. Loading too little has its own price, because then the agent guesses.
- **Ask the team:** "What is loaded on every turn, and how much of it applies to the task in front of us?"

## Why can more information make the answer worse? {#problem}

When an answer comes back weak, the usual advice is "give the AI more information". So you paste the whole style guide, add every rule and let it read all the files. It feels safe, because more facts ought to mean fewer mistakes.

It often goes the other way. Think of a desk. You can lay out every document for a project on it, but then you cannot find the one you need, and there is no room left to write. The agent's version of that desk is called the **context window**: all the text the model can look at in one turn. The rules are on it, along with your words, the files the agent read, the results of its tool calls and its own earlier answers. The desk has a size limit. And, as I will show, it has a second limit that is not about size.

I did not run a clean experiment for this chapter, so what I can say comes from two other places. The first is the people who build these tools. Anthropic writes that context "must be treated as a finite resource with diminishing marginal returns" ([Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)), and VS Code's guide says to "avoid context overload that can dilute focus" ([Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)). The second is the way I built my own setup, where almost every design choice is a way to put less into the window. Cost points the same way: most of what a task costs is what the model reads ([Models and cost](1-1-models-and-cost.html)). Before we get to the second limit, though, it helps to see what actually fills the window.

## What fills the window, and how to put less in it {#how-it-works}

### What is in the window

::: figure 3-1-window

Six things share the window:

1. Rules and instructions that the platform puts in every time.
2. The list of tools, with each tool's description. The model needs it to know what it can ask for, and with many tools, for example from several MCP servers, this list can be a large part of the window: Anthropic's example is 58 tools at about 55K tokens. Tool search in Claude Code and in VS Code (on Claude Sonnet 4.5, Opus 4.5 and later) loads a full definition only when the tool is needed ([What should you think through before connecting an MCP server?](1-3-mcp.html)).
3. Your messages.
4. Files the agent read. A file goes in as whole text, however much of it matters.
5. Tool results, such as search listings, command output and test logs. These are often the biggest part, and the part nobody looks at.
6. The agent's own earlier answers.

Each turn of the loop adds one more result and takes nothing out, and the model reads all of it again (what that costs is in [Models and cost](1-1-models-and-cost.html)). So the window only grows, until it is full. Then the platform has to cut or summarise the oldest parts, and details are lost. That is what [Long chats get worse](3-2-long-sessions.html) is about.

### Two limits, not one

Then why not simply use a bigger window? Because running out of room is only the obvious limit. The second one is attention, and Anthropic describes it as an "attention budget" that the model draws on when it reads a lot of text. In practice this means that a window with room left is not the same as a window that performs well. A rule buried in a long, noisy context is more likely to be missed than the same rule in a short one.

I take this as a reason to put less in, even when it all fits, although that step is my own inference and not something Anthropic says. How big the effect is depends on the model and the task.

### Load everything, load an index, or both

If less is better even when everything fits, the question becomes what to leave out. That choice sits behind most of the decisions in this part of the book.

The simplest answer is to leave nothing out, so that the agent starts with all the rules and all the notes in the window and never has to look anything up. The trouble is that the window is spent before work starts, most of it on things this task does not need.

The opposite answer is to load an index and fetch what the task needs. The agent starts with a short list of the things that exist, each with a name and a one-line description. When the task needs one of them, it opens that one. Anthropic calls this a "just in time" approach, in which the agent keeps lightweight identifiers (a file path, a name) and loads the data at run time. It works the way a library does, where nobody carries the whole library to a desk. You use the catalog, then fetch the one book.

Between those two ends, Anthropic's own suggestion is a mix. In their words, "the most effective agents might employ a hybrid strategy, retrieving some data up front for speed", and then explore further on their own. Their example is Claude Code, which drops its instruction file into the context up front and uses search tools to find the rest as it goes.

Loading everything still wins in some cases. For a small task, or a small set of rules, it is simpler and costs little. And where a missed fact is expensive, I would rather pay for it to be in the window than bet on the agent opening the right file.

Cost adds one more point in its favour. A beginning that is loaded every time and never changes can be cached, and a cache read is much cheaper than a normal read ([Models and cost](1-1-models-and-cost.html)). So if the beginning stays stable, loading everything is cheaper than the token count suggests. I have not tested the cache on Copilot, though. And even a cache leaves the attention limit above untouched.

::: figure 3-1-load-when

Whichever mix you choose, the index part only works if three things are true. First, the index entry has to say when to open the thing, because the agent decides from that one line alone. A vague line means it opens the wrong thing or never opens the right one, which is why the description of a skill matters so much ([Instructions and skills](3-3-instructions-and-skills.html)). Second, the fetch has to be cheap and exact. If fetching means reading a whole folder, the index saved nothing. Third, the agent has to know that it does not know, because an index cannot help with a thing the agent does not realise is missing. That is the real risk, and I come back to it below.

### Ways to read less

An index is only one way to keep the window small. Each of the ones I use below either keeps a thing out of the window or takes it out. If you want somewhere to start, the two cheapest are layering your rules and shortening tool output.

- **Rules by layers.** Keep a small set of rules always loaded, and put the rest where they are read only for the files or the job they apply to. Rules that never change the next step are only noise. (How: [Instructions and skills](3-3-instructions-and-skills.html).)
- **Search first, then read.** Ask the agent to find where something is, then read only that part of the file, not the whole file. Or give it a short map of the project written ahead of time, which is an index in the sense above. A map only wins if reading it beats searching, and it only stays true if someone keeps it true. I have not tested whether mine wins ([A knowledge base from code](8-1-why-a-knowledge-base.html)).
- **Make tool output short.** A command that prints 2,000 lines puts 2,000 lines in the window, so filter it, or print only the failures.
- **Remind with a few lines, not a page.** In my setup, only a short piece of the rules is added to each prompt, and when there is a task ([Manage tasks, not chats](5-1-tasks.html)), it says how far the task has got. It is a reminder. The full text is read when it is needed.
- **Hand a big read to a subagent** ([Use subagents sparingly](2-3-subagents.html), [Long chats get worse](3-2-long-sessions.html)).
- **Write state into files**, so a new chat reads one short file and not the old conversation. A new chat is an empty window. When to start one, and what to carry over, is in [Long chats get worse](3-2-long-sessions.html).

### Three questions and a test

How does your own setup spend its window? Three questions help answer that:

1. What is loaded every time? Count the lines of your always-on rules, and ask how much of that applies to the task you are doing now. (In Claude Code, the `/context` command shows what is using the window. I have not checked what Copilot offers.)
2. What was the biggest thing the agent read last time? Was it a file, or a log, and was all of it needed?
3. If the agent started a new chat now, what would it have to read to carry on? Is that in a file?

There is also a test you can run today. Take a task you know the answer to and run it twice, in a new chat each time. In the first run, paste the whole file or doc into the prompt. In the second, name the file and the part, and let the agent read only that. For each run, write down four things: whether the answer was right, the time, the usage your tool shows, and anything the agent missed. To trust the difference, repeat each a few times and score both runs the same way. Then compare the answer, the time and the usage.

## What loading less can cost {#costs-and-traps}

The first cost of putting less in the window is the risk I promised to come back to: loading less can lose something the agent needed. An index is a bet that the agent will open the right thing. When it does not, the agent works from a guess. The fix is better descriptions, and then a check that the thing was opened when it should have been. To make that check, run a task you know needs a certain file, look at the tool's log of what was opened, and count how often it was not. A new chat, a rule or a skill can be lost in the same way, because each of them also depends on the agent reading the right thing at the right time.

Summaries carry a similar risk, because a subagent's report and a platform's compression both make text shorter and can both drop the one line that mattered. Use them where a short version is enough.

An index also has to be kept true. A map that is out of date costs more than it saves, because the agent trusts it. [Keep it true](8-5-kb-keep-true.html) is about that.

As I said at the start, there are no numbers behind any of this. For Copilot's models, I know of no clean measure of how much attention is lost as a window fills.

## Do the platform makers agree? {#industry}
{status: industry}

Both makers came up at the start of this chapter. Side by side, their advice reads like this. Anthropic says context is "a finite resource with diminishing marginal returns" and that agents can load data "just in time" by keeping light references ([Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)). VS Code's guide says: "Start with concise context and expand only when needed." ([Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide))

They agree on the direction. Neither, though, gives a number I can quote for how much to load. That leaves a practical question: how long will the manual work in this chapter be needed?

## When the manual work can be deleted {#when-to-delete-it}
{status: industry}

The reasoning itself stays as long as the window has a size and the model reads it every turn. What may go is my own effort, the manual layering of rules and the manual new chats. If the platform loads rules by relevance well and compresses without dropping what matters, I will stop doing it by hand. A very large window, however, does not remove the second limit by itself, so before relying on one I would want to see a test of that.

## Try it on your own setup {#try-it}

::: prompt
Look at the commands this project uses to test, lint, build and search. For each, tell me roughly how much text it prints when it succeeds and when it fails, and whether that output would flood your context window if you ran it. Suggest a quieter way to run each one, such as printing only failures or a summary. Rank the three noisiest. Do not change any files, and do not run anything that changes state.
:::

## Go deeper {#go-deeper}

- Anthropic: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)
- [Long chats get worse](3-2-long-sessions.html): what happens as the window fills

## Explore it in the harness {#explore}

The harness is built around loading little. Its always-on rulebook is short, its README is only an index, and its skills are read by name and description first. You can see each one and how much it loads.

::: prompt
/harness-rookie-wondering I have read the chapter "Context is a budget". Teach me what this harness loads into the context every time, and what it leaves to be read when needed. Open the real files with me, count what is always on, and show me how a new session picks up a task.
:::
