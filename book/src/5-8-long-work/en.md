This chapter assumes you know the task folder from [Manage tasks, not chats](5-1-tasks.html), and that a chat gets shortened or ends ([Long chats get worse](3-2-long-sessions.html)).

## In one sentence {#in-one-sentence}

Long work survives across sessions only if its memory is in files: the requirement, the plan, the to-do list, the handover file. Split big work into tasks small enough to accept one by one.

## For leaders {#for-leaders}

- **The decision:** for work that spans days, decide that its memory lives in files, and that big work is split into tasks small enough to accept one by one.
- **The risk:** a new session knows nothing unless a file tells it. A big job handed over in one go gets started all at once and left half done, and a later session can see progress and call the job done too early. In my setup a person's "passed" on a step is only text, with nothing in code behind it. That is the weakest link.
- **The cost of doing it right:** files cost effort: every step writes a little and a new session reads a little. For a job that fits in one session it is waste. I have not measured what a goal saves over starting a new chat.
- **Ask the team:** "For our longest-running job, which file tells a new session what step it is on, and who accepted the steps so far?"

## The problem {#problem}

A job that takes three days will not fit in one chat. The first session ends. Or the tool shortens it to make room, and the details go. A new session knows nothing, unless something tells it.

What can tell it? Not the agent's memory: it has none between sessions. Not your memory either, if you have to explain the background again every morning, and explain it slightly differently each time. The only thing that is the same every morning is a file.

There is a second problem, and it comes from the size of the job. Handed a big job in one go, an agent tends to start everything at once, run out of room halfway, and leave things half done. Anthropic saw the same on a long coding project: "the agent tended to try to do too much at once" ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). The same article describes the opposite failure, a later instance that would "declare the job done" too early; that one is the subject of [Unattended: when it must stop](5-7-when-to-stop.html).

## How it works {#how-it-works}

### What a conversation loses

A conversation holds four things that a later session needs: what was asked, what was decided and why, how far the work has got, and what comes next. When the conversation is shortened or ended, all four are at risk, and the agent does not know which ones it lost.

### What goes in the folder

Put those four things where they cannot be shortened.

::: figure 5-8-shared-folder

- **The requirement:** what was asked, in a form a person confirmed ([The requirement on one page](5-2-requirements.html)).
- **The plan:** how the work will be done, and what is out of scope.
- **The to-do list:** steps, each small, each with a status and a way to tell it is done.
- **The handover:** one short **handover file** (the one from [Manage tasks, not chats](5-1-tasks.html), which also explains why the disk wins; Anthropic calls its version a progress file) that says which step it is at and what comes next. It has to stay short, within one screen, or a new session spends its room reading it.

A fifth item helps: a change log, one entry per step finished, saying what changed. When someone asks "why is it like this?", the answer is there.

### What a new session reads

A new session reads the short handover file first, then the to-do list, and only then what the current step needs. It does not read the whole folder. Then it checks the file against the disk: does the file really exist, did the step really happen? **When the record and the disk disagree, the disk wins.** A handover file that says "step 4 done" does not make step 4 done.

Anthropic's team did three things I do not do the same way. They had the agent commit to git after each step, so every step left a clean state to return to. They had each new session first run a basic end-to-end test before starting new work, which is a check of the old state, not only a read of the file. And they kept the feature list in JSON, because the model was less likely to change a JSON file by mistake than a Markdown one. My files are Markdown, and I have not compared the two.

### Build the frame first, then step by step

Do not start with the work. Start with the frame:

1. Settle the central idea: goal, what is in scope, what is not, how the whole will be accepted.
2. Break it into small steps.
3. Have a person read both and confirm.
4. Then do one step: do it, check it, hand it to the person.
5. A step is done only when the person says it passed. Then write the log entry, update the handover file, and move to the next.

The person's "passed" is a gate ([Two gates](5-3-two-approvals.html)). In my setup that is text, not code: nothing in code stops an agent from writing "passed" for itself. I rely on the agent following the instruction, and on the person reading. This is a gap I know about.

### What is too big, and how to split it

Most jobs are one task, and a goal is for the rest. A job is too big for one task when one of these is true (these three are my rules of thumb, not tested):

- It cannot finish in one session, and nobody can say how far along it is.
- You cannot say how you would accept the whole of it at once.
- The plan keeps changing as you learn more.

The fix is a **goal**: the big thing as one set of files, with a few **tasks** under it. A task is one delivery, as in [Manage tasks, not chats](5-1-tasks.html): one folder, its own checks, its own acceptance. The goal holds the idea and the list; each task does one piece.

::: figure 5-8-goal-tasks

A good task is small enough that you can say, in a sentence, how you will accept it. The goal does not need to know the details of task 3 while you work on task 2. That is the point: the plan is allowed to change, one task at a time, without redoing what has been accepted. Steps already accepted are not rewritten; a redo is a new step.

### Common traps

- **All at once.** The agent tries to finish the goal in one session. The fix is the list: only one step is active.
- **Done said too early.** A new session sees progress and decides it is finished. The fix is the same as for unattended work ([when to stop](5-7-when-to-stop.html)): done is a state the files and the person confirm, not a thing the agent says.
- **A long handover file.** If the pointer grows past a screen, it stops being read. Move detail to the log.
- **Making a goal for a small job.** Most jobs need one task. A goal is for work that spans sessions and changes shape.

## Costs and traps {#costs-and-traps}

**Files cost effort.** Every step writes a little, and a new session reads a little. For a job that fits in one session, it is waste.

**A person's "passed" is only text.** [Two gates](5-3-two-approvals.html) binds an approval to the exact plan, and code checks it. The "passed" of a step here is not bound to anything; nothing in code stops an agent from writing it. It is the weakest link in this chapter.

**Files can lie.** The agent writes them, so they can be wrong or stale. That is why the disk wins, and why the person accepts step by step.

**Who starts it matters.** In my setup only the person starts a goal. An agent may suggest it when a job looks long, but cannot begin one. Otherwise every job would become a project.

**What I have not measured.** How much a goal saves over just starting a new chat and explaining. I think it saves the most when the job changes shape, but I have no numbers.

## When to delete it {#when-to-delete-it}

If the platform keeps a trustworthy memory of a long job across sessions, so that a new session can resume without reading files, the handover file can go. I would keep the requirement and the plan as files anyway: a person can read them too, and that is how you accept the work.

## Go deeper {#go-deeper}

- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Explore it in the harness {#explore}

The task folder and the goal files run in Copilot Harness. The harness can teach them to you from the inside, with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Long work across sessions". Teach me how this harness keeps long work in files (topic 9): the task folder, the handover file a new session reads, and the goal that groups several tasks. Open real files with me and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.