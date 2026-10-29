This chapter assumes you have read [Ask or refuse](4-2-ask-vs-refuse.html) and [Guardrails](4-3-guardrails.html): why "ask me first" is not a limit, and why the agent must not be able to edit the rules.

## In one sentence {#in-one-sentence}

Put a person at the points that cost money, grant power or cannot be undone. Make the approval come through a channel the agent cannot reach, and bind it to exactly the plan that was approved.

## For leaders {#for-leaders}

- **The decision:** where a person must approve. Put them at the points that cost money, grant power or cannot be undone, and nowhere else. The approval must come through a channel the agent cannot reach, and it must belong to exactly the plan or change the person read.
- **The risk:** a confirmation box can be switched off for the session without anyone noticing, and an approval the agent can give itself is not an approval. Even a real approval has a weak spot, because a tired person can still approve without reading. Binding the approval to the content stops a swap, not a careless yes.
- **The cost of doing it right:** each gate costs a person one read and one command, and with too many gates people stop reading. In my setup, snapshots at the gates are kept for 14 days by default.
- **Ask the team:** "Which approvals in our flow could the agent give itself or switch off, and does an approval still count if the plan changes afterwards?"

## Why a confirmation box is not an approval {#problem}

You want a person to approve the important steps, and the obvious tool is already in front of you: the confirmation box that the agent tool shows, asking "Allow this?" It does not work well, for two reasons. The first is that people click Allow. By the hundredth box they are no longer reading it ([Ask or refuse](4-2-ask-vs-refuse.html)). The second is that many tools let you tick "allow for this session", after which the box never appears again. The approval you relied on is gone, and nothing tells you.

A third problem is subtler. Suppose that instead of a box, the approval is a command the person types. If the agent can run commands, it can type that command too. An approval that the agent can give is not an approval.

Where, then, should the person stand? And how can their yes become something the agent can neither produce nor reuse?

## Where to put the person, and how to make the yes count {#how-it-works}

### Where to put the person

The first question has a short answer. A person's attention is the scarcest thing in the system, so spend it on three kinds of point and nowhere else. Some points cost money, such as starting an expensive run. Some grant power, such as letting the agent write to a shared repository. And some cannot be undone: once the step is done, nothing takes it back.

Most of the agent's work is none of these, since everything inside a task folder is cheap to redo and the agent can work there freely ([Manage tasks, not chats](5-1-tasks.html)). A task that changes a real repository, though, has two points of this kind. I call each of them a **gate**, because the task cannot pass it until a person approves.

::: figure 5-3-two-gates

### Gate 1: approve the plan

The first gate comes before any work file changes. The agent writes the requirement and a plan and then stops, and until the person has read the plan and approved it, the agent may draft and read but may not start on the changes.

The reason for stopping here is cost, since a wrong plan is cheap to fix while it is still a paragraph but expensive to fix once it has become a finished change. In my setup the plan also stands on a confirmed requirement ([The agent writes the requirement](5-2-requirements.html)), so one approval can confirm both.

### Gate 2: approve the write-back

By the second gate, the agent has made its changes in the task folder and the checks have run. What is left is to copy the result to the real repository, a step called the **write-back**. Before that happens, the person reads the exact **diff**, which is the list of lines that would change, and then approves it.

Even an approved write-back does not go straight to the main branch. It goes to a new branch of the repository and is left uncommitted. And before anything is written, code checks that:

- the working tree is clean,
- the branch name is free,
- none of the files to change has moved on the main branch since it was copied.

If any repository fails a check, nothing is written. This is also where two people, or two tasks, changing the same file are found, by the program here rather than later in a review.

### Why the approval is typed in a terminal

Now the second question. How do you make a yes the agent cannot produce? A confirmation box in the chat can be switched off by "allow for this session", but a code that the person types in a terminal cannot. That is why the approval is a command that needs a real terminal. The design stands on two legs, though, and the terminal is only the first.

On its own, the terminal is not a wall. A check that "this is a terminal" is not a security boundary, because a determined program can imitate one. So what stops a program that pretends?

That is the second leg, a hook. When an agent tries to run the approval command, this piece of code refuses the attempt outright. It must sit outside the agent's reach, as [Guardrails](4-3-guardrails.html) explains: if the hook is gone, or the agent can edit it, the approval is only a polite request. Neither leg is enough alone.

The hook, in turn, has to keep refusing when something goes wrong. The enforcement layer lets a call through when it breaks itself ([Build the enforcement layer like software](4-4-enforcement-design.html)), so the refusal of the approval command belongs on the short list of rules that must block even when the hook errors. Otherwise this leg breaks exactly when it is needed.

None of this means the person reads the plan in the terminal. Plans and diffs are hard to read there, so the person reads them in an editor, while the terminal shows only the file path and the code to type. Reading and approving are separate acts on purpose.

### Tie the approval to what was read

That leaves reuse. Suppose the person approves a plan, and then the agent edits the plan. Is the approval still good? It should not be. That is why the code the person types is derived from the plan's content. It is a hash, a fingerprint that changes if a single character changes, so when the plan changes after approval, the approval no longer matches and the gate closes again.

The same goes for the write-back, where the approval belongs to the exact diff that was shown. This is what "bind it to exactly the plan that was approved" means. Without it, a person approves one thing and the agent delivers another.

### Snapshots at the gates

Besides deciding what may go forward, the gates are where the work is saved. When the plan is approved, before each check, and before the dry run of a write-back, a copy of the work (a snapshot) is saved automatically, so that when something breaks, the state of that moment can be found again. In my setup they are kept for 14 days by default.

Finding a state again is not the same as going back to it, though. A failure in the middle of a write to several repositories is not rolled back by itself. Instead the task goes to a "partly written" state, and a person runs a recovery. I chose not to guess at an automatic undo.

### Several rounds

A task does not always end at the write-back. The same goal can come back, because a reviewer finds a defect or someone asks for a change. In that case a new round starts, in which the old work moves aside, a new plan is written and both gates apply again. A different goal, by contrast, is a new task.

Testing in other environments looks like another round, but it is not. The agent cannot run anything there, so the person does the running, and the work becomes its own task of kind *testing*, in which the agent writes the instructions, waits for the person's results and judges them. If a test fails, it goes back to the development task as a new round.

### Without any of this machinery

The habit behind the gates works by hand too. Read the plan before you tell the agent to go, read the diff before you commit, and do not tick "allow for this session" on a tool that writes. The machinery above only makes sure these things happen when you are tired or not there.

## What the gates cost, and where they can still fail {#costs-and-traps}

The plainest cost is time. Each gate holds the agent until a person has done one read and typed one command, and that is the price of the design. If you put gates everywhere, people stop reading, which brings you back to the hundredth box.

The gates also hold only while the refusing hook is there. If the hook that refuses the approval command is removed, edited or fails, an agent that can run commands could approve for itself. So protect that hook as the rules in [Guardrails](4-3-guardrails.html) say, and test it. A test is cheap: ask the agent to run the approval and check that it is refused.

Even with the hook in place, a person can approve without reading. Binding the approval to the plan stops a swap, but it does not stop a tired yes. Making the diff short and the gates few helps, yet nothing here removes the problem. One idea I have not tried is to record how long each approval took and how big the diff was, because a very fast yes on a big diff is a signal worth looking at.

The last two limits came up above. The terminal check protects against accidents, not against an attack ([Least privilege](4-5-least-privilege.html)), and a partial failure across repositories still needs a person.

## When to delete the typed approval {#when-to-delete-it}

Of all this, the typed approval is the part that depends on the platform. It exists because a platform's own confirmation can be switched off for a session and cannot be tied to a plan's hash. If a platform offers an approval that the agent cannot dismiss, that records what was shown, and that stops being valid when the content changes, use that and drop mine.

The idea stays either way: a person at the three kinds of point, and an approval that belongs to exactly what they read.

## Try it on your own setup {#try-it}

::: prompt
Walk through how work moves from this agent's changes to the main branch or to production in this project: pull requests, required reviews, CI, deploy steps, and any approval prompts in the agent tools. For each point where money is spent, power is granted or something cannot be undone, say who approves, through what channel, and whether the agent could give or skip that approval. Also say whether the approval would still stand if the change were edited after it was given. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Guardrails](4-3-guardrails.html): why the hook and its files must be out of the agent's reach.
- [Ask or refuse](4-2-ask-vs-refuse.html): why a confirmation box is not a limit.
- [Counted checks](5-5-counted-checks.html): the checks that run before the second gate.
- VS Code docs: [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks), which say hooks and instructions are not substitutes for enforced permissions.

## Explore it in the harness {#explore}

The two gates, the typed approval, the plan hash, and the snapshots run in Copilot Harness.

::: prompt
/harness-rookie-wondering I have read the chapter "Two gates". Teach me how this harness builds the two approvals (topic 9, and topic 8 on permissions): why they are typed in a terminal, what the approval is bound to, and which hook refuses the agent. Walk me through a real task going through both gates, and draw it.
:::
