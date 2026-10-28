This chapter assumes you have used an AI coding agent in a long chat, and read [the context budget](3-1-context-budget.html) (the window has a size limit, and everything in it competes for room).

## In one sentence {#in-one-sentence}

Long chats get worse. Do not trust the model to remember: write what matters into files, clear old tool results, or start a fresh chat.

## For leaders {#for-leaders}

- **The decision:** require that anything that matters lives in a file, not only in the chat, and agree when to start a fresh chat.
- **The risk:** long chats get worse, and a platform's summary of a chat drops details such as your exact words and the reason for a choice. I have not measured how fast quality falls in my own setup, so I give no rate.
- **The cost of doing it right:** a short notes file per piece of work, updated after each finished step. If you cannot write the handover in half a page, the work is not yet clear enough.
- **Ask the team:** "If this chat disappeared now, what would we lose?"

## The problem {#problem}

You have worked with an agent for two hours. It started sharp. Now it asks about something you settled at the start, repeats a mistake it fixed, or edits the wrong file. Nothing broke. The chat just got long.

Three words first. The first two are defined in [Context is a budget](3-1-context-budget.html); here they are in brief.

- The **context window** is the text the model can see at one time. It has a size limit.
- A **tool result** is what comes back when the agent uses a tool. These are usually the biggest items in the window.
- **Compaction** is what a platform does when the window is nearly full. It asks a model to summarise the chat so far, and continues from the summary.

I have not measured how fast quality falls in my own setup, and I will not give you a number. The shape of the problem is clear enough to act on, and the people who build the models describe it the same way (see [what the industry says](#industry)).

### Why a long chat gets worse

It is easiest to see as a picture: the same chat at three moments.

::: figure 3-2-context-rot

Four things happen together.

1. **The useful part does not grow; the rest does.** What the task needs right now (the request, the rule you gave, the file being edited) stays about the same size. Everything else piles up around it: files read an hour ago, a test output that was long and is now irrelevant, three wrong attempts.
2. **The model reads all of it, every time.** It has no filing cabinet. On every turn the whole window is read again. The more old text there is, the more the one line that matters competes with it. (A cache can make the rereading cheaper in money, [Models and cost](1-1-models-and-cost.html), but not less crowded.) The name for this is **context rot**: as the window fills, the model's recall of what is in it gets less reliable.
3. **Early things are far from where they are needed.** A rule from the first message is now thousands of lines behind. It is still there, but it is far from the step where it applies. This one is my own reading of what I see; I have no source for it.
4. **Compaction loses detail.** A summary keeps what its writer judged important. Your exact words, the reason for a choice and the one odd constraint are the first things a summary drops, and you cannot know which it dropped.

None of this is a bug in one product. It comes from how the window works, so it applies to every agent.

## How it works {#how-it-works}

The answer is not "a bigger window" or "a smarter summary". It is to stop depending on the chat as the place where important things live. There are four moves. The first is a habit to keep all the time. The other three you use as the chat grows, from lightest to heaviest.

::: figure 3-2-four-moves

### 1. Write down what matters, in a file

Ask: if this chat disappeared now, what would I lose? Whatever the answer is should not live only in the chat.

- **What was decided** and why.
- **What is done and what is next.**
- **Where things are** (which files, which commands).

These go in a file the agent can read again: a short notes file in the task's folder, or its to-do list (both are explained in [Manage tasks, not chats](5-1-tasks.html)). A file does not get compacted, and a new chat can read it in a second. When it is read again, its text sits near the end of the window, close to where it is needed.

In my setup, every piece of work has a folder with a **handover file**: how far it is, the next step, and what is decided. A new chat reads that file first and continues. Because of this, losing a chat costs me a few minutes, not the work.

**How to write the note.** Short. State what is true now, not the story of how you got there. Put the next step at the top. One page is better than ten, because the new chat has to read it, and it takes room too.

**Make the agent do it.** Ask it to update the notes after each finished step, not at the end. The end is when you are tired and the chat is longest. You can say it in one sentence: "After each finished step, update the notes file: what is decided, what is done, the next step."

Anthropic describes the same habit for long-running agents: a progress file and the git history, which the agent reads first when a new session starts ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). Here is the template for the handover file in my setup:

::: code harness .harness/contracts/templates/task/en/TASK.md L1-L23 "A handover file template: status, what is happening now, the next step, the files to read, what is decided, and open questions."

### 2. Clear old tool results

Most of the window is usually old tool output. The agent read a file to find one function; the whole file is still there. A test run printed pages of output; only the one failing line mattered.

Dropping these is the lightest form of compaction, and the safest: the decisions and the conclusions stay, and only the raw material goes. If the agent needs the file again, it can read it again. On Anthropic's API this is a feature called context editing: a strategy named `clear_tool_uses` removes the oldest tool results once the input passes a size you set. It is in beta, and clearing invalidates the cached beginning, so it has a price ([Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)). Whether your tool does something like it, and when, is something to check, not assume. I have not tested what Copilot does today (see [Costs and traps](#costs-and-traps)).

You can get the same effect by hand. When a long read is done, ask the agent to write down only what it found, and then continue in a new chat that has the finding but not the reading.

### 3. Send a big read to a subagent

If the next step is to read a lot, do not read it in your main chat. A **subagent** is a second agent that starts with an empty window and sends back only a short report. The reading stays in its window, and your main chat gets the conclusion. This is the "parallel reading" case in [Use subagents sparingly](2-3-subagents.html), with the same limits: it only works when a short report is enough, and it costs more in total.

Some platforms make this a setting. In VS Code, a skill can declare `context: fork` in its header, and it then runs in a subagent of its own instead of in your chat ([Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills); the docs mark it experimental). A skill that reads a lot and reports a little is a good fit. I have not tried it, so I do not know how it counts usage or how hooks see it.

### 4. Start a fresh chat

Sometimes the right move is to stop. Signs it is time:

- The agent repeats something you already settled.
- It undoes a fix from an hour ago.
- You catch yourself re-explaining.
- The task changed (a new task is a new chat).

A fresh chat starts with an empty window and the rules. Give it only what it needs to continue: point it at the notes file. In my experience it often does better than the old chat did at the end, because it is reading a clean page. I have not measured this.

Compare the cost. Starting fresh feels like losing progress. But the progress is in the files and in the code; the chat held only the memory of it, and that memory was already worn.

**When to start fresh in a planned way.** For long work that I split into steps, I do not wait for the chat to degrade. Learning a large code base, for example, goes in batches, and I begin a new chat every two or three batches. The state is in the task, not the chat, so nothing is lost at the boundary.

### What to hand over

When you change chats, the new one needs a small, fixed set:

1. The request, in a few lines.
2. What is decided, and what is not.
3. What is done, and the next step.
4. Where the files are.

If you cannot write these four in half a page, that is the real finding: the work is not yet clear enough to hand over to anyone, including yourself tomorrow.

### Test your own setup

A cheap test, with no extra setup, that one person can do in an hour. Pick a rule you gave early in a long chat, one with two or three parts. After an hour of work, ask the agent to state it without looking back. Then start a new chat, give it only your notes file, and ask the same. Score each answer by how many of the parts it got right. If the second is more accurate, your chat is doing worse than your files.

Also check where your instructions live. A rule given only in the conversation is lost when the chat is compacted; a rule in a file the platform reads again is not. Claude Code's documentation says exactly this about its project instruction file. If you want a rule to survive, put it in a file.

## Costs and traps {#costs-and-traps}

**Do not hide a bad habit.** If chats get long because the task is too big, the fix is a smaller task, not better note-taking.

**A note can be wrong.** If the agent writes "tests pass" in the notes and they did not, the next chat starts from a false fact. Notes are the agent's report; check the ones that matter. [Memory](3-5-memory.html) is about this problem at length.

**Notes cost room too.** A notes file that grows without trimming becomes the thing that fills the window. Keep it short and cut what is done. And a notes file can hold things you would not want shared, so think before it goes into a shared repository.

**A fresh chat loses the feel.** The old chat knew how you phrase things and what you meant by "the usual way". If that matters, write it down; it is likely a rule.

**What I did not test.** I have not measured how my platform compacts: what it keeps, what it drops, and whether it clears old tool results by itself. Treat compaction as lossy until you have checked it for your tool.

## What the industry says {#industry}
{status: industry}

Anthropic's engineering team describes this problem and the same fixes. They use the term context rot: as the window fills, "the model's ability to accurately recall information from that context decreases". They name compaction ("taking a conversation nearing the context window limit, summarizing its contents"), call tool result clearing "one of the safest lightest touch forms of compaction", and describe note-taking, where "the agent regularly writes notes persisted to memory outside of the context window". ([Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))

Claude Code's documentation adds a practical detail: the project instruction file at the root is read again from disk after compaction, while an instruction given only in the conversation is gone. ([How Claude remembers your project](https://code.claude.com/docs/en/memory))

For long tasks that need many sessions, Anthropic describes a progress file plus git history that each new session reads first. ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)) On the API, tool result clearing is available as context editing, in beta. ([Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing))

They agree with each other and with this chapter. None gives a rule for when a chat is too long, and I do not either; judge by the signs above.

## When to delete it {#when-to-delete-it}
{status: industry}

Part of this is the platform's job and will be done better by it: clearing old tool results, compacting, and carrying key facts across. When your tool does those well, and you have checked what it keeps, stop doing them by hand.

The core stays: if the work matters, its state belongs in a file you can read, not in a chat. A bigger window and better compaction make chats last longer. They do not make a summary as good as the original, and they do not give a new chat your last two hours. I would look again if a platform showed that its compacted chats lose nothing I care about, measured on my own tasks.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Imagine this chat is lost and a new agent must carry on. From what you can see in this repository (recent commits, open changes, any notes or task files, the instruction files), write the handover that agent would need: the request in a few lines, what is decided, what is done and the next step, and where the files are. Then list what you could not tell from the repository, as the gaps a person must fill. Print it only. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Claude Code docs: [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- In this book: [Use subagents sparingly](2-3-subagents.html), [Memory](3-5-memory.html)

## Explore it in the harness {#explore}

Copilot Harness keeps the state of every task in files, so a chat can end at any time. The harness can show you where those files are and how a new chat picks up from them. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Long chats get worse". Teach me how this harness keeps the state of a task in files: what the handover file holds, how a new session reads it to carry on, and what it does about a window that fills up (topics 1 and 9). Open the real files with me.
:::

It teaches one small piece at a time and opens the files with you.
