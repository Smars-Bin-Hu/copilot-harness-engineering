This chapter assumes you have used an AI coding agent, and that you know a hook is code the platform runs before a tool call ([Hooks](2-2-hooks.html)).

## In one sentence {#in-one-sentence}

Manage tasks, not chats: one folder per task. What the work could break decides which gates it passes; its kind decides what counts as done.

## For leaders {#for-leaders}

- **The decision:** approve the job, not the chat, as the unit of work. That means one folder per task with a handover file, and care that follows what a mistake could break.
- **The risk:** a chat gets shortened or ends, and a new one knows nothing. The other trap is process that is too heavy. My first design had a heavy level with a team of role agents, and in a small test it cost about 4.5 times the usage and 6 times the time, with no gain on tasks with a clear request (four tasks, one run each, so read the direction, not the ratio).
- **The cost of doing it right:** the first step is only a folder per task with one handover file. More files are added only when the task earns them, and quick questions open nothing. In return, the agent must keep the files true, and a person has to read them when it matters.
- **Ask the team:** "If the agent's chat disappeared tonight, could someone pick the job up tomorrow from files alone?"

## If not the chat, what holds the work? {#problem}

Say you ask an agent to change a pipeline. It reads, makes a plan and starts editing, and the chat grows as it goes. The next morning you open a new chat to ask a follow-up, but the new agent has never seen the first one. Or the tool has shortened the first chat in the meantime, and the agent no longer remembers why it chose what it chose ([Long chats get worse](3-2-long-sessions.html)).

Either way, the chat turns out to be the wrong thing to manage. It gets compressed, it ends, and one chat can hold three unrelated jobs. What you actually care about is the job itself: what was asked, what was decided, how far it has got and whether it was checked.

So I stopped treating the chat as the unit of work. The unit is a **task**, one job with one **task folder**. The requirement, the plan, the progress and the results are all files in that folder, so any session, today or next week, picks the task up by reading the folder.

That settles where the work lives. It is also the whole of the first step: one folder per task, with one handover file in it. Everything below is what I added on top of that, and you can add it one piece at a time.

But a second question follows, because not every job needs the same care. Fixing a typo in a note is not the same as writing to a shared repository, and the two should not get the same amount of process.

## How much process does each job get? {#how-it-works}

### My first answer was levels, and it was wrong

My first answer was three **levels**, from a light level 1 up to a heavy level 3 with a team of role agents ([Use subagents sparingly](2-3-subagents.html)). You picked one at the start of every job.

After some use, three things were clear. The first was that only the middle level got used, while the other two sat idle most of the time. The second was that the heavy level did not earn its weight. On tasks with a clear request it was no better than one agent, yet it cost about 4.5 times the usage and 6 times the time. The test behind that was small, four tasks with one run each, so read the direction rather than the ratio ([Use subagents sparingly](2-3-subagents.html)). The third was that having to choose first added one more step every time. Worse, with two sets of rules side by side, the agent got unsure, and gave wrong explanations of which one applied.

The deepest problem, though, was in the idea itself. How hard a job is cannot be known before you start, but a level asks you to guess it up front.

So I removed the levels. Care is now decided by two other things, neither of which asks you to guess difficulty.

### Care follows what a mistake costs

The first of the two is **what the action can break**. Nobody has to pick it, because code makes a rough judgment of it from the paths and commands. That judgment is a heuristic, not a proof, and the section on the folder below says where it can be fooled.

| What the work does | Example | How it is guarded |
| --- | --- | --- |
| Reads only | A question, a look-up in notes | Nothing stops it |
| Changes the task folder | Writing an analysis, a design, a plan | Nothing stops it |
| Changes a real repository | Code, a knowledge base ([A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)) | It is written in the folder first. Writing it back needs a person to approve ([Two gates](5-3-two-approvals.html)) |
| Touches git history or production | Commit, push, switch branch | Stopped by a hook; a person approves, and some commands are always refused |

This is the same idea as the grading in [Asking is not a limit](4-2-ask-vs-refuse.html): the more a mistake costs, the harder the stop. A stop like that is a **gate**, a point the task cannot pass until a person approves ([Two gates](5-3-two-approvals.html)).

### The kind sets the standard for done

The second thing is the **kind** of task, which says what counts as done, because a question and a code change are not finished in the same way.

| Kind | Done when |
| --- | --- |
| Question | The answer has a source |
| Root-cause analysis | There is a chain of evidence: what was seen, the logs, the cause, how it was verified |
| Design or plan | There are options and a reason for the choice |
| Development | The change matches the approved plan, and there is a record of testing it |
| Testing | The cases and their results are on disk |
| Knowledge update | The source is clear, and it goes through the same write-back gate ([Two gates](5-3-two-approvals.html)) |

Without a list like this, "done" is whatever the agent feels like saying. With it, a reader and a checker both know what to look for ([Counted checks](5-5-counted-checks.html)).

### The size sets how many files the folder has

Those two settle how carefully a task is guarded and when it is done. They do not settle how much paperwork it carries. That differs too, since a question does not need a requirement file, a plan and a to-do list, but a development task does. So each task also has a **size**. It is not a third measure of care, because it decides nothing except which files the folder holds.

- **Light:** one handover file, saying how far the task is, what the next step is and what has been decided.
- **Medium:** adds the requirement and its source documents, reference material, and a log.
- **Full:** adds a to-do list, a working copy of the code, and test results.

Each kind starts at a default size, and a task that grows can be raised, with the missing files added then, but it never goes down. That keeps the cheap path cheap, while the heavy path is still there when a task earns it. You might wonder whether this is the old levels coming back under a new name. It is not, because nobody guesses the size at the start. The kind sets it, and it only moves up when the work shows it needs more.

### The folder is the workspace

For a task that changes a real repository, the folder is also where the work is done. The files to change are copied in and changed there, and only after approval do they go back. Until then, the real repository is not touched.

::: figure 5-1-lifecycle

That promise is weaker than it sounds. The folder is held by rules in the gate, not by the operating system, so a command spelled in an indirect way may get past it, because a hook sees calls, not effects ([Hooks](2-2-hooks.html)). So the rule keeps a careful agent in its place, but it does not contain a determined one. For things that must never be touched, see [Least privilege](4-5-least-privilege.html).

### Why files are the handover

The folder holds more than the files being changed. Whatever its size, it also keeps the state of the task, in files rather than in the conversation, and three of those files do the handing over.

- A **handover file** says how far the task is and what comes next. A fresh session reads only this to pick the task up.
- A **requirement file** holds what was agreed ([The agent writes the requirement](5-2-requirements.html)).
- A **state file for programs** is where the list of tasks, and what each one waits for, is read from, rather than from the Markdown. Progress that an agent writes by hand in prose misses ticks and gets things wrong, while progress a program records does not.

When a written record says one thing and the files actually on disk say another, the disk wins. This is the same idea as the progress file in Anthropic's long-running agent work, where state lives in files outside the chat ([Long work across sessions](5-8-long-work.html)). What I add is the kind, the size and the gates.

### A session holds one task; a task can have many sessions

Sessions and tasks are kept apart on purpose. A session holds only one task at a time, but it can switch to another without closing the first. While it holds a task, the edit tools can write only that task's folder. A task, in turn, outlives its sessions: closing it only changes its state, so the folder stays and the task can be opened again. And at the start of each prompt, a hook tells the agent how far its task is, or, if it has none, which tasks are still open.

The one cost of the separation is that a task can be left without any session, if its session moved on to another task or the session's record was lost, and then nothing notes that the agent stopped. My board of tasks ([Ten things at once: parallel tasks](7-2-many-tasks.html)) shows these tasks as having no session, along with how long nobody has touched them, so that a person can see them.

None of this applies to quick questions that write nothing. They open no task at all, because a task would only slow them down for nothing.

### Try it without any setup

You can test the handover idea in your own tool. At the end of a long chat, ask the agent to write into one file what was asked, what was decided, how far it got and what comes next. Then open a new chat and tell it to read only that file and carry on. If the second chat goes wrong, the file was missing something, and whatever it missed is what a handover file must hold.

## What the folder costs, and what it cannot promise {#costs-and-traps}

That small test also shows the first cost. A folder is useful only if its handover file is true, so the agent has to keep the files up to date. A reminder when the agent stops helps, but it does not guarantee it. When it matters, I read the files rather than taking the agent's word.

The folder also adds steps, because opening one, writing the requirement and waiting at gates is slower than just making a small change in a chat. That is why light tasks exist, and why a question opens nothing.

And although nobody guesses difficulty any more, the kind is still a guess, because a job often starts as a question and turns into a change. So the kind can change. The size can too, but only upward. I have not measured how often people pick the wrong kind.

Finally, the folder is not a sandbox in the security sense, for the reasons given above under "The folder is the workspace".

## Which parts to delete, and what stays {#when-to-delete-it}

Not all of this has to last. Two parts of it are scaffolding for today's platform. The first is the handover file, together with the reminder at each prompt. Both exist because chats are compressed and sessions end. If the platform keeps a memory of its own that survives both, and that a person can read, drop my files and keep the idea.

The second is the playbook each kind has, the written-out steps for doing that kind of task. As models need such steps less, you can shorten the playbooks. Keep the lists of what counts as done, though, because they say what you want, not how to get it.

What does not retire is the unit itself. Whatever the platform does, a job has a requirement, a plan and a result, and a person wants to find them.

## Go deeper {#go-deeper}

- [Long chats get worse](3-2-long-sessions.html): why a chat is a poor place to keep state.
- [Two gates](5-3-two-approvals.html): what happens at write-back.
- [Long work across sessions](5-8-long-work.html): when one task is too big.

## Explore it in the harness {#explore}

Everything here runs in Copilot Harness, from the task folder, the kinds and the sizes to the handover file and the board of tasks. The harness can teach it to you from the inside, with the real files.

::: prompt
/harness-rookie-wondering I have read the chapter "Manage tasks, not chats". Teach me how this harness builds what it describes: the task folder, the kinds and tiers, and why sessions and tasks are separate (topic 9). Open a real task's files with me and draw how they fit together.
:::
