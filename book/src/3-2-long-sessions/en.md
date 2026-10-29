This chapter assumes you have used an AI coding agent in a long chat, and read [the context budget](3-1-context-budget.html) (the window has a size limit, and everything in it competes for room).

## In one sentence {#in-one-sentence}

Long chats get worse. Do not trust the model to remember: write what matters into files, clear old tool results, or start a fresh chat.

## For leaders {#for-leaders}

- **The decision:** require that anything that matters lives in a file, not only in the chat, and agree on when to start a fresh chat.
- **The risk:** long chats get worse, and when a platform summarises a chat, the summary drops details such as your exact words and the reason for a choice. I have not measured how fast quality falls in my own setup, so I give no rate.
- **The cost of doing it right:** a short notes file for each piece of work, updated after each finished step. If you cannot write the handover in half a page, the work is not yet clear enough.
- **Ask the team:** "If this chat disappeared now, what would we lose?"

## Why does an agent get worse as the chat goes on? {#problem}

You have been working with an agent for two hours. It started out sharp, but now it asks about something you settled at the start, repeats a mistake it had already fixed, or edits the wrong file. Nothing broke. The chat just got long.

Why should length alone make a difference? Because everything the agent works with sits in its **context window**, the text the model can see at one time, and that window has a size limit. The biggest things in it are usually **tool results**, what comes back each time the agent uses a tool (both terms are defined in [Context is a budget](3-1-context-budget.html)). When the window is nearly full, the platform falls back on **compaction**: it asks a model to summarise the chat so far and then carries on from the summary.

I have not measured how fast quality falls in my own setup, so I will not give you a number. But the shape of the problem is clear enough to act on, and the people who build the models describe it the same way (more under [Do the model makers see it the same way?](#industry)).

### What happens to the window as the chat grows

It is easiest to see as a picture of the same chat at three moments.

::: figure 3-2-context-rot

Four things happen together. The first is that the useful part does not grow, while the rest does. What the task needs right now (the request, the rule you gave, the file being edited) stays about the same size, but around it pile up the files read an hour ago, a test output that was long and is now irrelevant, and three wrong attempts.

That would matter less if the model could put old things away in a filing cabinet, but it has none: on every turn it reads the whole window again. The more old text there is, the more the one line that matters has to compete with it. (A cache can make the rereading cheaper in money, as [Models and cost](1-1-models-and-cost.html) explains, but it does not make the window less crowded.) The name for this is **context rot**: as the window fills, the model's recall of what is in it gets less reliable.

Things said early also end up far from where they are needed. A rule from your first message is still there, but it is now thousands of lines back from the step where it applies. This point is my own reading of what I see, with no source behind it.

And when the window is nearly full, compaction loses detail. A summary keeps what its writer judged important. Your exact words, the reason for a choice and the one odd constraint are the first things a summary drops, without telling you which ones it dropped.

None of this is a bug in one product. It comes from how the window works, so it applies to every agent. What, then, can you do about it?

## Keep what matters out of the chat {#how-it-works}

The answer is not "a bigger window" or "a smarter summary". It is to stop depending on the chat as the place where important things live. There are four moves for that. The first is a habit to keep all the time, while the other three are for when the chat grows, going from lightest to heaviest.

::: figure 3-2-four-moves

### 1. Write down what matters, in a file

Start with a question: if this chat disappeared now, what would I lose? Whatever the answer is should not live only in the chat. That means what was decided and why, what is done and what comes next, and where things are (which files, which commands).

All of this goes in a file the agent can read again, such as a short notes file in the task's folder, or its to-do list (both are explained in [Manage tasks, not chats](5-1-tasks.html)). A file does not get compacted, and a new chat can read it in a second. When it is read again, its text also lands near the end of the window, close to where it is needed.

In my setup, every piece of work has a folder holding a **handover file** that records how far the work has got, the next step and what is decided. A new chat reads that file first and carries on from there. Because of this, losing a chat costs me a few minutes, not the work.

Keep the note short. One page is better than ten, because the new chat has to read it and the note takes room too. Write what is true now rather than the story of how you got there, and put the next step at the top.

Make the agent do it. Ask it to update the notes after each finished step, not at the end, because the end is when you are tired and the chat is longest. One sentence is enough to set this up: "After each finished step, update the notes file: what is decided, what is done, the next step."

Anthropic describes the same habit for long-running agents, built on a progress file and the git history that the agent reads first when a new session starts ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). Here is the template for the handover file in my setup:

::: code harness .harness/contracts/templates/task/en/TASK.md L1-L23 "A handover file template: status, what is happening now, the next step, the files to read, what is decided, and open questions."

### 2. Clear old tool results

Most of the window is usually old tool output. The agent read a file to find one function, but the whole file is still there. A test run printed pages of output, of which only the one failing line mattered.

Dropping that output is the lightest form of compaction and also the safest, because the decisions and the conclusions stay and only the raw material goes. If the agent needs the file again, it can read it again. On Anthropic's API this is a feature called context editing, in which a strategy named `clear_tool_uses` removes the oldest tool results once the input passes a size you set. The feature is in beta, and clearing has a price, because it invalidates the cached beginning ([Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)). Whether your own tool does anything like it, and when, is something to check rather than assume; I have not tested what Copilot does today (see [Where these moves can let you down](#costs-and-traps)).

You can also get the same effect by hand. When a long read is done, ask the agent to write down only what it found, then carry on in a new chat that has the finding but not the reading.

### 3. Send a big read to a subagent

If the next step is to read a lot, do not do the reading in your main chat. Hand it to a **subagent**, a second agent that starts with an empty window and sends back only a short report. The reading stays in its window while your main chat gets the conclusion. This is the "parallel reading" case in [Use subagents sparingly](2-3-subagents.html), with the same two limits: it only works when a short report is enough, and it costs more in total.

Some platforms make this a setting. In VS Code, a skill can declare `context: fork` in its header to run in a subagent of its own instead of in your chat ([Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills); the docs mark it experimental). That suits a skill that reads a lot and reports a little. I have not tried it, though, so I do not know how it counts usage or how hooks see it.

### 4. Start a fresh chat

Sometimes the right move is to stop. These are the signs that it is time:

- The agent repeats something you already settled.
- It undoes a fix from an hour ago.
- You catch yourself re-explaining.
- The task changed (a new task is a new chat).

A fresh chat starts with an empty window and the rules. Give it only what it needs to carry on: point it at the notes file. In my experience (I have not measured it), it often does better than the old chat was doing at the end, because it is reading a clean page.

Starting fresh can feel like losing progress, so it is worth comparing what you actually lose. The progress is in the files and in the code. The chat only held the memory of it, a memory that was already worn.

For long work that I split into steps, I start fresh at planned points instead of waiting for the chat to degrade. Learning a large code base, for example, goes in batches, and I begin a new chat every two or three batches. Since the state is in the task and not in the chat, nothing is lost at the boundary.

### What to hand over

If you do start a fresh chat, the next question is what to give it. It needs a small, fixed set of things:

1. The request, in a few lines.
2. What is decided, and what is not.
3. What is done, and the next step.
4. Where the files are.

If you cannot write these four in half a page, that is the real finding. The work is not yet clear enough to hand over to anyone, including yourself tomorrow.

### A one-hour test of your own setup

How can you tell whether your chat is already doing worse than your files? There is a cheap test for it. It needs no extra setup, and one person can do it in an hour. Pick a rule with two or three parts that you gave early in a long chat. After an hour of work, ask the agent to state it without looking back. Then start a new chat, give it only your notes file, and ask the same question. Score each answer by how many of the parts it got right. If the second one is more accurate, your chat is doing worse than your files.

While you are at it, check where your instructions live. A rule given only in the conversation is lost when the chat is compacted, but a rule in a file that the platform reads again is not. Claude Code's documentation says exactly this about its project instruction file. So if you want a rule to survive, put it in a file.

## Where these moves can let you down {#costs-and-traps}

Before reaching for any of these moves, ask why the chat got long. If it is because the task is too big, the fix is a smaller task. Better note-taking would only hide a bad habit.

Even when the task is the right size, the notes themselves can be wrong. If the agent writes "tests pass" in the notes when they did not pass, the next chat starts from a false fact. Notes are the agent's report, so check the ones that matter. [Memory](3-5-memory.html) is about this problem at length.

And a correct note still has a cost of its own: it takes room. A notes file that grows without trimming becomes the very thing that fills the window, so keep it short and cut what is done.

A notes file can also hold things you would not want shared, so think before it goes into a shared repository.

And a fresh chat, however good the notes, loses the feel of the old one. The old chat knew how you phrase things and what you meant by "the usual way". If that matters, write it down, because it is likely a rule.

Then there is what I did not test. I have not measured how my platform compacts: what it keeps, what it drops, and whether it clears old tool results by itself. Until you have checked this for your own tool, treat compaction as lossy.

## Do the model makers see it the same way? {#industry}
{status: industry}

Anthropic's engineering team describes this problem and the same fixes. They use the term context rot, meaning that as the window fills, "the model's ability to accurately recall information from that context decreases". They name compaction ("taking a conversation nearing the context window limit, summarizing its contents"), call tool result clearing "one of the safest lightest touch forms of compaction", and describe note-taking, where "the agent regularly writes notes persisted to memory outside of the context window". ([Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))

Claude Code's documentation adds a practical detail, the one behind the check on where your instructions live. The project instruction file at the root is read again from disk after compaction, while an instruction given only in the conversation is gone. ([How Claude remembers your project](https://code.claude.com/docs/en/memory))

For long tasks that need many sessions, Anthropic describes a progress file plus git history that each new session reads first. ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)) And on the API, tool result clearing is available as context editing, in beta. ([Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing))

These sources agree with each other and with this chapter. None of them gives a rule for when a chat is too long. I do not give one either, so judge by the signs above.

## Which parts you can delete, and which stay {#when-to-delete-it}
{status: industry}

Some of what these moves do is the platform's job and will be done better by it: clearing old tool results, compacting, and carrying key facts across. When your tool does those well and you have checked what it keeps, stop doing them by hand.

The core stays, though. If the work matters, its state belongs in a file you can read, not in a chat. A bigger window and better compaction make chats last longer, but they do not make a summary as good as the original, nor do they give a new chat your last two hours. I would look at this again if a platform showed, measured on my own tasks, that its compacted chats lose nothing I care about.

## Try it on your own setup {#try-it}

::: prompt
Imagine this chat is lost and a new agent must carry on. From what you can see in this repository (recent commits, open changes, any notes or task files, the instruction files), write the handover that agent would need: the request in a few lines, what is decided, what is done and the next step, and where the files are. Then list what you could not tell from the repository, as the gaps a person must fill. Print it only. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Claude Code docs: [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- In this book: [Use subagents sparingly](2-3-subagents.html), [Memory](3-5-memory.html)

## Explore it in the harness {#explore}

Copilot Harness keeps the state of every task in files, so a chat can end at any time. The harness can show you where those files are and how a new chat picks up from them.

::: prompt
/harness-rookie-wondering I have read the chapter "Long chats get worse". Teach me how this harness keeps the state of a task in files: what the handover file holds, how a new session reads it to carry on, and what it does about a window that fills up (topics 1 and 9). Open the real files with me.
:::
