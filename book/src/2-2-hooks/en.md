This chapter assumes you have read [How does an Agent actually work?](2-1-agent-loop.html), or know that an agent works by asking for tool calls.

## In one sentence {#in-one-sentence}

A hook is code the platform runs at fixed points in every turn, including inside subagents. It is where hard rules live, though it sees calls, not what a command does once it runs.

## For leaders {#for-leaders}

- **The decision:** decide which rules must hold every time, and put those in a hook (code the platform runs on every tool call) rather than in a prompt.
- **The risk:** a hook sees only the text of a call, and it can fail quietly. In Copilot as I saw it in October 2026, a hook that times out counts as a pass, while one that cannot start blocks every tool. In one small batch on one machine, about a third of prompts reached the model without the rules a hook was meant to add.
- **The cost of doing it right:** one small program and one configuration file, kept under code review.
- **Ask the team:** "What happens to our rules when the hook is slow or broken, and how do we know the model actually received them?"

## What makes a rule hold every time? {#problem}

You write a rule: "never edit files in the config folder". The agent follows it nine times. On the tenth it is deep in a task, the context is long and the rule is far away, so it edits the file. It can do that because the rule was only a sentence, one the model could weigh against all the other sentences. This time it weighed it lower.

What you need, then, is something that does not depend on the model's memory or mood: a piece of code that every tool call must pass and that says yes or no. That is a **hook**.

More exactly, a hook is a small program that you write and the platform runs for you at fixed moments. Each time, the platform hands it a piece of JSON (a plain text format for data) that says what is happening, such as "the agent wants to run this command". The hook answers, also in JSON, which the platform then acts on. It is the platform that runs the hook, not the model, so the model cannot skip it.

My first lesson about hooks, though, came from one that did not work. I used a hook to put the harness's rules in front of the model at the start of each prompt. On the surface it worked, since it ran every time and its output looked right. Yet when I looked at what the model had actually received, in a small batch of prompts on one machine in October 2026, about a third had no rules in them (read "a third" as "a lot", not as a rate). The cause turned out to be VS Code itself, which adds its own reminders to a prompt. Those reminders took the one slot the hook used. I fixed it by adding a second check at the last point before the text goes to the model. The whole text is visible there, so the check can put the rules back if they are missing.

That lesson holds for every hook: **check what the model received, not what the hook returned.** But if a hook that ran every time could still fail like this, how else can it fail, and what can it not see at all?

## What can a hook do, and what can it not? {#how-it-works}

### When a hook runs

::: figure 2-2-hook-points

A hook runs only at the moments the platform offers. The ones I use are below, with the names VS Code gives them in its docs.

| Moment | What happens | What I use it for |
| --- | --- | --- |
| A session starts | A new chat begins | Give the model the session's basic facts |
| A prompt is sent | You press Enter | Add the rules; note which task this is |
| **Before a tool call** | The model asked; nothing has run | **Refuse a call.** Every hard rule is here |
| After a tool call | The tool ran | Keep a record; add a note |
| A subagent starts or stops | A helper agent begins or ends | Hand it its package; record the end |
| The agent is about to stop | The model wrote an answer | Say "not yet", once, if work is open |

Of these, only the moment before a tool call can refuse one specific action. A rule needs a call that exists but has not happened yet, and only this moment has one. The other moments can watch, record and add words. (The stop moment can also say "not yet", as described below, but that is not a refusal of an action.) If you want to see these moments for yourself, the test at the end of this section shows them.

### What goes in and what comes out

What does the hook actually get at one of these moments? It receives JSON that says which event this is and which session, plus, for a tool call, the tool name and its arguments. Here is a real sample, recorded from VS Code, of what a hook is given after a command has run:

::: code harness .harness/eval/fixtures/hooks/copilot-sdk/payloads/PostToolUse.Bash.json L1-L15 "What a hook receives after a terminal command: the event, the tool name, the arguments and the result."

The hook answers in JSON too, and only three answers are useful:

- Let it through. An empty answer counts as no opinion, and the platform's normal permission checks still apply.
- Refuse, with a reason. The call does not run, and the reason is shown to the model and to you.
- Add a few words for the model to read, such as a reminder or a status line.

At the stop moment there is a fourth, which is to block the stop with a reason that is fed back to the model as if it were a new prompt. I allow this once per stop, because a hook that blocked every stop would keep the agent running for ever, with you paying for every turn.

**The reason is part of the design.** A refusal should say why the call was refused and what to do instead, or the agent tries the same thing again, or something worse ([Asking is not a limit](4-2-ask-vs-refuse.html)).

### Three ways a hook goes wrong

All of this assumes the hook works. A hook is software, though, so it will fail, and what the platform does then decides whether your rule is a fence or a decoration.

| What happens | What Copilot does (as I observed it in October 2026, and as the VS Code docs say) |
| --- | --- |
| The hook runs and refuses | The call is stopped, the reason is shown. This works in the default mode and in the modes that skip permission prompts. |
| The hook cannot start (for example, the language it is written in is not installed) | Treated as a refusal: no tool can run, and the screen says little more than "hook errored". |
| The hook takes too long | Treated as a pass, silently. |

Whether a broken hook should lock you out or leave the door open is therefore a design choice. [Enforcement design](4-4-enforcement-design.html) is about how to make it. It also describes the choice I made: let the call through and log the error, and warn when the slowest recent call nears the time limit.

### Inside subagents

A subagent is a second agent started for a piece of the work ([Use subagents sparingly](2-3-subagents.html)). Because it runs in its own session, you might expect it to be out of reach of the hooks. In Copilot today it is not, since its tool calls go through the hooks as well, with the event carrying the id of the parent session. So a rule set for the main agent also holds for the helpers it starts.

### What a hook cannot see

Of everything in this chapter, this is the part I most want you to remember.

::: figure 2-2-blind-spot

**It sees calls, not effects.** For a terminal command, the hook reads the text of the command, so it can see "write to this path". It cannot see a path built from variables, or a script that was written a minute ago and is only run now. Once the command is let through, the hook is out of the picture. A hook on terminal commands therefore stops the common spellings, but not an agent set on getting around it. The VS Code docs say the same: hooks are executable code and not a substitute for enforced permissions or sandboxing. For things that must never be touched, then, do not rely on the hook alone ([Least privilege](4-5-least-privilege.html)).

Even for the calls it does see, a hook does not know which agent is making them. In Copilot today the event does not carry the name of the main agent, so "this agent is allowed to" cannot be a rule, because any agent could pass for it. If rights must differ, they have to come from something the agent cannot set, such as a switch the person turns on in a terminal.

Some calls it never sees at all, because a hook does not run everywhere. In my measurements in October 2026, the repository's hooks did not run when I used the command-line mode of Copilot (no window), and a setting that looks like an off switch did not stop them in the newer sessions. A company policy can also turn hooks off for a workspace, and even a change to the hook file takes effect only after a reload, because the file is read when the window starts.

Finally, even when a hook runs and answers, its message can be lost on the way to the model, as in the story at the top of this chapter.

### Other things that stand in the loop

Is a hook, then, the only thing that stands between the model and the world? It is not. A **wrapper** (a small program you call instead of the raw command), an **MCP server** ([What should you think through before connecting an MCP server?](1-3-mcp.html)) and a **proxy** between the platform and the model all stand there too. But each of them sees only what is routed through it, and the agent can route around them. What sets the hook apart is that the platform promises to call it. For the built-in tools and for subagents I saw every call pass through it, although I have not tested MCP tools.

### A test you can run today

Write the smallest hook your platform allows, one that only appends the event name and the tool name to a file. Use your agent for a small task, then read the file. You will see every moment in the table above, in order, and how many there are, which makes it the quickest way to understand the loop. Follow the [VS Code hooks docs](https://code.visualstudio.com/docs/copilot/customization/hooks) for the file format.

## What a hook costs, and what to watch for {#costs-and-traps}

Of the three failures above, the one that matters most in a team is the timeout, because a timeout is a silent pass. So watch the time your hook takes.

Time matters for a second reason, too. A hook runs on every call, so if it is slow, everything is slow. Mine normally takes a few dozen milliseconds. Keep yours cheap, and put a limit on what it may do.

A hook is also code you must trust. It runs on your machine and reads whatever the agent sends, so never put the agent's text straight into a shell command inside a hook. In a team, treat the hook file like any other code that guards something, which means changing it through review. Hooks are also still in Preview in VS Code, so their behavior may change with the platform. What this chapter says about how Copilot behaves is only what I saw, so check it again after each update.

One last trap is in the reason itself, which can be too good. A refusal that explains exactly how to get around the rule teaches the model to do that. Say what to do instead, not how to dodge.

## What do the platform docs say? {#industry}
{status: industry}

VS Code lists the moments I used (session start, prompt submitted, before and after a tool, subagent start and stop, agent stop) and states that a `preToolUse` hook can return a deny with a reason. It also notes that a timeout falls through to normal permissions and that the feature is in Preview. ([Agent hooks in VS Code](https://code.visualstudio.com/docs/copilot/customization/hooks))

## Which parts to delete, and when {#when-to-delete-it}
{status: industry}

A hook for a rule stays as long as the platform lets rules in prompts be ignored. The parts I would delete first are the workarounds. The second check that puts back rules lost on the way goes when the platform delivers hook output reliably, and the timing watch goes when a timeout is reported instead of silently passing. If the platform one day offers a native, enforced policy (a rule file it checks itself), I would move the hard rules there and keep hooks for records and reminders.

## Try it on your own setup {#try-it}

::: prompt
Find out whether this project has agent hooks configured (look in the project and editor settings and any hooks folder). If it does, list each one: which moment it runs at, what it checks, what it does when it refuses, and what the reason it shows says. Then say what would happen if the hook program failed to start or ran too slowly, based on the platform docs. If there are no hooks, list the three rules in the instruction files that would be worth turning into one. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Agent hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- [Requests and rules](4-1-requests-and-rules.html): when to move a rule from words to code
- [Enforcement design](4-4-enforcement-design.html): what to do when the hook fails

## Explore it in the harness {#explore}

The harness has one hook entry for all moments, a gate that refuses calls, and the logs that show what it did.

::: prompt
/harness-rookie-wondering I have read the chapter "Hooks, the point every call passes through". Teach me how this harness uses hooks: which moments it listens to, what the gate refuses and why, and what happens when the hook itself fails. Open the real files with me and show me a refusal and its reason.
:::
