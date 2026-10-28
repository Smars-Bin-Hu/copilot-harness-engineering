This chapter assumes you have read [The agent loop](2-1-agent-loop.html), or know that an agent works by asking for tool calls.

## In one sentence {#in-one-sentence}

A hook is code the platform runs at fixed points in every turn, including inside subagents. It is where hard rules live, and it sees calls, not what a command does once it runs.

## For leaders {#for-leaders}

- **The decision:** decide which rules must hold every time, and put those in a hook (code the platform runs on every tool call) instead of in a prompt.
- **The risk:** a hook sees the text of a call, not what a command does once it runs. It can also fail quietly. In Copilot as I saw it in October 2026, a hook that times out counts as a pass, and one that cannot start blocks every tool. In one small batch on one machine, about a third of prompts reached the model without the rules a hook was meant to add; read that as "a lot", not as a rate.
- **The cost of doing it right:** one small program and one configuration file, kept under code review. Mine normally runs in a few dozen milliseconds.
- **Ask the team:** "What happens to our rules when the hook is slow or broken, and how do we know the model actually received them?"

## The problem {#problem}

You write a rule: "never edit files in the config folder". The agent follows it nine times. On the tenth, it is deep in a task, the context is long, and the rule is far away. It edits the file. The rule was a sentence the model could weigh against other sentences, and this time it weighed it lower.

What you need is something that does not depend on the model's memory or mood: a piece of code that every tool call must pass, which says yes or no. That is a **hook**.

A hook is a small program that you write and the platform runs for you at fixed moments. The platform hands it a piece of JSON (a plain text format for data) that says what is happening, such as "the agent wants to run this command". The hook answers, also in JSON. The platform then acts on the answer. The model does not run the hook and cannot skip it.

My first lesson came from a hook that did not work. I used a hook to put the harness's rules in front of the model at the start of each prompt. It ran every time and its output looked right. But when I looked at what the model had actually received, in a small batch of prompts on one machine in October 2026, about a third had no rules in them. I did not keep the exact count, so read "a third" as "a lot", not as a rate. VS Code adds its own reminders to a prompt, and they took the one slot the hook used. The hook returned the right answer and nothing happened. I fixed it by adding a second check at the last point before the text goes to the model, where the whole text is visible, and putting the rules back if they were missing.

The lesson is for every hook: **check what the model really received, not what the hook returned.** The rest of this chapter is about what a hook can do, how it fails, and what it cannot see.

## How it works {#how-it-works}

### The moments

::: figure 2-2-hook-points

A platform offers a list of moments. These are the ones I use, with the names VS Code gives them in its docs.

| Moment | What happens | What I use it for |
| --- | --- | --- |
| A session starts | A new chat begins | Give the model the session's basic facts |
| A prompt is sent | You press Enter | Add the rules; note which task this is |
| **Before a tool call** | The model asked; nothing has run | **Refuse a call.** Every hard rule is here |
| After a tool call | The tool ran | Keep a record; add a note |
| A subagent starts or stops | A helper agent begins or ends | Hand it its package; record the end |
| The agent is about to stop | The model wrote an answer | Say "not yet", once, if work is open |

Only the moment before a tool call can refuse one specific action. It has the one thing a rule needs: the call exists, and has not happened yet. The other moments can watch, record, and add words. (The stop moment can also say "not yet", as described below, but that is not a refusal of an action.) You can see these moments for yourself with the small test at the end of this chapter.

### What goes in and what comes out

The hook receives JSON: which event this is, the session, and for a tool call, the tool name and its arguments. Here is a real sample, recorded from VS Code, of what a hook is given after a command has run:

::: code harness .harness/eval/fixtures/hooks/copilot-sdk/payloads/PostToolUse.Bash.json L1-L15 "What a hook receives after a terminal command: the event, the tool name, the arguments and the result."

The hook answers with JSON. There are really only three useful answers:

- **Let it through.** (An empty answer counts as no opinion. The platform's normal permission checks still apply.)
- **Refuse, with a reason.** The call does not run. The reason is shown to the model and to you.
- **Add a few words** for the model to read: a reminder, a status line.

At the stop moment there is a fourth: block the stop, with a reason that is fed back to the model as if it were a new prompt. I allow this once per stop. A hook that blocked every stop would keep the agent running for ever, and you would pay for every turn.

**The reason is part of the design.** Say why it was refused and what to do instead, or the agent tries the same thing again, or something worse ([Asking is not a limit](4-2-ask-vs-refuse.html)).

### Three ways a hook goes wrong

A hook is software. It will fail. What the platform does then decides whether your rule is a fence or a decoration.

| What happens | What Copilot does (as I observed it in October 2026, and as the VS Code docs say) |
| --- | --- |
| The hook runs and refuses | The call is stopped, the reason is shown. This works in the default mode and in the modes that skip permission prompts. |
| The hook cannot start (for example, the language it is written in is not installed) | Treated as a refusal: no tool can run, and the screen says little more than "hook errored". |
| The hook takes too long | Treated as a pass, silently. The VS Code docs describe it as falling through to normal permissions. |

So the same failure can lock you out or leave the door open, and it depends on how it fails. Which one you want is a design choice. What to choose, and what I chose (let the call through and log the error, and warn when the slowest recent call nears the time limit), is the subject of [Enforcement design](4-4-enforcement-design.html).

### Inside subagents

A subagent is a second agent started for a piece of the work ([Use subagents sparingly](2-3-subagents.html)). It runs in its own session. In Copilot today, its tool calls go through the hooks as well, and the event carries the id of the parent session. So a rule set for the main agent also holds for the helpers it starts. I would not assume this on another platform without testing it. I have not.

### What a hook cannot see

This is the part I most want you to remember.

::: figure 2-2-blind-spot

**It sees calls, not effects.** For a terminal command, the hook reads the text of the command. It can see "write to this path". It cannot see a path built from variables, or a script that was written a minute ago and is only run now. Once the command is let through, the hook is out of the picture. So a hook on terminal commands stops the common spellings. It does not stop an agent set on getting around it. The VS Code docs say the same: hooks are executable code and not a substitute for enforced permissions or sandboxing. For things that must never be touched, do not rely on the hook alone ([Least privilege](4-5-least-privilege.html)).

**It does not know which agent is calling.** In Copilot today, the event does not carry the name of the main agent. So "this agent is allowed to" cannot be a rule: any agent could pass for it. If rights must differ, they have to come from something the agent cannot set, such as a switch the person turns on in a terminal.

**It does not run everywhere.** In my measurements, the repository's hooks did not run when I used the command-line mode of Copilot (no window). A setting that looks like an off switch did not stop them in the newer sessions. A company policy can turn hooks off for a workspace. And the hook file is read when the window starts, so a change needs a reload. These are the facts as I found them in October 2026; they will change. Look at the platform's current docs, which also say hooks are in Preview today.

**It can lose its message.** The story at the top: output from a hook may never reach the model. Test the delivery, not only the hook.

### Other things that stand in the loop

A hook is not the only thing between the model and the world. A **wrapper** (a small program you call instead of the raw command), an **MCP server** ([MCP](1-3-mcp.html)) and a **proxy** between the platform and the model each see only what is routed through them, and the agent can route around them. The difference: the platform promises to call the hook. For the built-in tools and for subagents, I saw every call pass through it; I have not tested MCP tools.

### Test your own setup

**Three questions** for any rule you care about:

1. Is it written in a prompt, or in a hook? If it is in a prompt, it is a request.
2. What does the hook see when the rule is broken? The call text, or the effect?
3. What happens when the hook itself breaks or is slow?

**A test you can run today.** Write the smallest hook your platform allows. It only appends the event name and the tool name to a file. Use your agent for a small task, then read the file. You will see every moment in the table above, in order, and how many there are. It is the quickest way to understand the loop. Follow the [VS Code hooks docs](https://code.visualstudio.com/docs/copilot/customization/hooks) for the file format.

## Costs and traps {#costs-and-traps}

**A timeout is a silent pass.** Of the three failures above, this is the one that matters most in a team: a rule that is not enforced and nobody is told. Watch the time your hook takes, and read [Enforcement design](4-4-enforcement-design.html) before you choose what happens on failure.

**A hook runs on every call.** If it is slow, everything is slow. Mine normally takes a few dozen milliseconds. Keep it cheap, and put a limit on what it may do.

**A hook is code you must trust.** It runs on your machine and reads whatever the agent sends. Never put the agent's text straight into a shell command inside a hook. In a team, treat the hook file like any other code that guards something: change it through review.

**A hook is a feature of a platform that is still changing.** VS Code labels it Preview. What I wrote in the failure table is what I saw; check it again after each update.

**The reason can be too good.** A refusal that explains exactly how to get around the rule teaches the model to do that. Say what to do instead, not how to dodge.

## What the industry says {#industry}
{status: industry}

VS Code lists the moments I used (session start, prompt submitted, before and after a tool, subagent start and stop, agent stop) and states that a `preToolUse` hook can return a deny with a reason. It also notes that a timeout falls through to normal permissions and that the feature is in Preview. ([Agent hooks in VS Code](https://code.visualstudio.com/docs/copilot/customization/hooks))

I have not compared this with other platforms' hooks in detail here. Their event names and what they cover differ.

## When to delete it {#when-to-delete-it}
{status: industry}

A hook for a rule stays as long as the platform lets rules in prompts be ignored. The reasoning does not retire. The parts I would delete first are the workarounds: the second check for lost injection goes when the platform delivers hook output reliably, and the timing watch goes when a timeout is reported instead of silently passing. If the platform one day offers a native, enforced policy (a rule file it checks itself), I would move the hard rules there and keep hooks for records and reminders.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Find out whether this project has agent hooks configured (look in the project and editor settings and any hooks folder). If it does, list each one: which moment it runs at, what it checks, what it does when it refuses, and what the reason it shows says. Then say what would happen if the hook program failed to start or ran too slowly, based on the platform docs. If there are no hooks, list the three rules in the instruction files that would be worth turning into one. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Agent hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- [Requests and rules](4-1-requests-and-rules.html): when to move a rule from words to code
- [Enforcement design](4-4-enforcement-design.html): what to do when the hook fails

## Explore it in the harness {#explore}

The harness has one hook entry for all moments, a gate that refuses calls, and the logs that show what it did. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Hooks, the point every call passes through". Teach me how this harness uses hooks: which moments it listens to, what the gate refuses and why, and what happens when the hook itself fails. Open the real files with me and show me a refusal and its reason.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
