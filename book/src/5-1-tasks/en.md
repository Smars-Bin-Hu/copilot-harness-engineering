This chapter assumes you have used an AI coding agent, and that you know a hook is code the platform runs before a tool call ([Hooks](2-2-hooks.html)).

## In one sentence {#in-one-sentence}

Manage tasks, not chats: one folder per task. What the work could break decides which gates it passes; its kind decides what counts as done.

## For leaders {#for-leaders}

- **The decision:** approve the job, not the chat, as the unit of work: one folder per task, with a handover file, and care that follows what a mistake could break.
- **The risk:** a chat gets shortened or ends, and a new one knows nothing. The other trap is process that is too heavy: my first design had a heavy level with a team of role agents, which in a small test cost about 4.5 times the usage and 6 times the time with no gain on tasks with a clear request (four tasks, one run each, so read the direction, not the ratio).
- **The cost of doing it right:** the first step is only a folder per task with one handover file. More files are added only when the task earns them, and quick questions open nothing. The agent must keep the files true, and a person has to read them when it matters.
- **Ask the team:** "If the agent's chat disappeared tonight, could someone pick the job up tomorrow from files alone?"

## The problem {#problem}

You ask an agent to change a pipeline. It reads, plans, edits, and the chat grows. The next morning you open a new chat to ask a follow-up. The new agent has never seen the first one. Or the first chat was shortened by the tool, and it has forgotten why it chose what it chose ([Long chats get worse](3-2-long-sessions.html)).

A chat is the wrong thing to manage. It gets compressed, it ends, and one chat can hold three unrelated jobs. What you actually care about is the job: what was asked, what was decided, how far it has got, whether it was checked.

So I stopped treating the chat as the unit of work. The unit is a **task**: one job, with one **task folder**. The requirement, the plan, the progress and the results are all files in that folder. Any session, today or next week, picks the task up by reading the folder.

That solves where the work lives. A second question follows: not every job needs the same care. Fixing a typo in a note and writing to a shared repository are different. How do you decide how much process each one gets?

You can start with the first step alone: one folder per task, with one handover file in it. Everything below is what I added on top of that, and you can add it one piece at a time.

## How it works {#how-it-works}

### My first answer was levels, and it was wrong

My first design had three **levels**. Level 1 was light, level 3 was heavy with a team of role agents ([Use subagents sparingly](2-3-subagents.html)). You picked a level at the start of every job.

After some use, three things were clear:

- Only the middle level got used. The other two sat idle most of the time.
- The heavy level was no better than one agent on tasks with a clear request, and it cost about 4.5 times the usage and 6 times the time. That test was small (four tasks, one run each), so read only the direction, not the ratio ([Use subagents sparingly](2-3-subagents.html)).
- Choosing first was one more step every time. Worse, with two sets of rules side by side the agent got unsure, and gave wrong explanations of which applied.

There is also a deeper problem. How hard a job is cannot be known before you start. A level asks you to guess it up front.

So I removed the levels. Care is now decided by two other things, neither of which asks you to guess difficulty.

### Care follows what a mistake costs

The first thing is **what the action can break**. Code makes a rough judgment of this from the paths and commands, so nobody picks it. It is a heuristic, not a proof; the section on the folder below says where it can be fooled.

| What the work does | Example | How it is guarded |
| --- | --- | --- |
| Reads only | A question, a look-up in notes | Nothing stops it |
| Changes the task folder | Writing an analysis, a design, a plan | Nothing stops it |
| Changes a real repository | Code, a knowledge base ([A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)) | It is written in the folder first. Writing it back needs a person to approve ([Two gates](5-3-two-approvals.html)) |
| Touches git history or production | Commit, push, switch branch | Stopped by a hook; a person approves, and some commands are always refused |

This is the same idea as the grading in [Ask or refuse](4-2-ask-vs-refuse.html): the more a mistake costs, the harder the stop. Such a stop is a **gate**: a point the task cannot pass until a person approves ([Two gates](5-3-two-approvals.html)).

### The kind sets the standard for done

The second thing is the **kind** of task. A question and a code change are not finished in the same way, so the kind says what counts as done.

| Kind | Done when |
| --- | --- |
| Question | The answer has a source |
| Root-cause analysis | There is a chain of evidence: what was seen, the logs, the cause, how it was verified |
| Design or plan | There are options and a reason for the choice |
| Development | The change matches the approved plan, and there is a record of testing it |
| Testing | The cases and their results are on disk |
| Knowledge update | The source is clear, and it goes through the same write-back gate ([Two gates](5-3-two-approvals.html)) |

Without this, "done" is whatever the agent feels like saying. With it, a reader and a checker know what to look for ([Counted checks](5-5-counted-checks.html)).

### The size sets how many files the folder has

A question does not need a requirement file, a plan and a to-do list. A development task does. So each task also has a **size**, which only decides which files its folder holds.

- **Light:** one handover file: how far it is, the next step, what is decided.
- **Medium:** adds the requirement and its source documents, reference material, and a log.
- **Full:** adds a to-do list, a working copy of the code, and test results.

Each kind has a default size. A task that grows can be raised, and the missing files are added. It never goes down. So the cheap path stays cheap, and the heavy path is there when the task earns it. This is not the old level coming back: nobody guesses the size at the start, the kind sets it, and it only moves up when the work shows it needs more.

### The folder is the workspace

For a task that changes a real repository, the folder is also the place where the work is done. The files to change are copied in, the changes are made there, and only after approval do they go back. The real repository is not touched until then.

::: figure 5-1-lifecycle

I want to be honest about how strong this is. The folder is held by rules in the gate, not by the operating system. A command spelled in an indirect way may get past it, as [Hooks](2-2-hooks.html) explains: a hook sees calls, not effects. It keeps a careful agent in its place. It does not contain a determined one. For things that must never be touched, see [Least privilege](4-5-least-privilege.html).

### Why files are the handover

The state of a task is kept in files, not in the conversation:

- A **handover file** says how far the task is and what comes next. A fresh session reads only this to pick up.
- A **requirement file** holds what was agreed ([The agent writes the requirement](5-2-requirements.html)).
- A **state file for programs**. A list of tasks and what each waits for is read from this, not from the Markdown. Progress that an agent writes by hand in prose misses ticks and gets things wrong; progress a program records does not.

When the written record and the disk disagree, the disk wins. This is the same idea as the progress file in Anthropic's long-running agent work: state lives in files outside the chat ([Long work across sessions](5-8-long-work.html)). What I add is the kind, the size and the gates.

### A session holds one task; a task can have many sessions

These are separate on purpose.

- A session holds one task at a time. It can switch to another without closing the first. While it holds a task, the edit tools can write only that task's folder.
- A task outlives its sessions. Closing a task only changes its state; the folder stays, and it can be opened again.
- At the start of each prompt a hook tells the agent how far its task is, or which tasks are still open if it has none.

One cost: a task can be left without any session, if the session moved on to another task or its record was lost. Nothing then notes that the agent stopped. My board of tasks ([Ten things at once: parallel tasks](7-2-many-tasks.html)) shows these as having no session, with how long nobody has touched them, so a person can see them.

Not every chat needs a task. Quick questions that write nothing do not open one; that would slow them down for nothing.

### Try it without any setup

At the end of a long chat, ask the agent to write what was asked, what was decided, how far it got and what comes next into one file. Open a new chat and tell it to read only that file and carry on. If the second chat goes wrong, the file was missing something; that tells you what the handover file must hold.

## Costs and traps {#costs-and-traps}

- **The agent must keep the files up to date.** A folder is useful only if the handover file is true. A reminder when the agent stops helps; it does not guarantee it. I read the files, not the agent's word, when it matters.
- **A task folder adds steps.** Opening one, writing the requirement, and waiting at gates is slower than just doing a small change in a chat. That is why light tasks exist, and why a question opens nothing.
- **Kinds are a guess too.** A job often starts as a question and turns into a change. The kind can change, and the size can only go up. I have not measured how often people pick the wrong kind.
- **The folder is not a sandbox in the security sense.** See above.

## When to delete it {#when-to-delete-it}

Two parts of this are scaffolding for today's platform.

- **The handover file and the reminder at each prompt.** They exist because chats are compressed and sessions end. If the platform keeps memory of its own that survives both and that a person can read, drop my files and keep the idea.
- **Kind-specific playbooks.** As models need written-out steps less, shorten them. Keep the lists of what counts as done: they say what you want, not how to get it.

What does not retire is the unit itself. Whatever the platform does, a job has a requirement, a plan and a result, and a person wants to find them.

## Go deeper {#go-deeper}

- [Long chats get worse](3-2-long-sessions.html): why a chat is a poor place to keep state.
- [Two gates](5-3-two-approvals.html): what happens at write-back.
- [Long work across sessions](5-8-long-work.html): when one task is too big.

## Explore it in the harness {#explore}

Everything here runs in Copilot Harness: the task folder, kinds and sizes, the handover file, and the board of tasks. The harness can teach it to you from the inside, with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Manage tasks, not chats". Teach me how this harness builds what it describes: the task folder, the kinds and tiers, and why sessions and tasks are separate (topic 9). Open a real task's files with me and draw how they fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.