This chapter assumes you have read [A rule in a prompt is a request](4-1-requests-and-rules.html): a rule that must hold has to be code, not words.

## In one sentence {#in-one-sentence}

"Ask me first" is not a limit, because people click Allow the hundredth time. A limit is a refusal the agent cannot argue with, graded by what the action can break.

## For leaders {#for-leaders}

- **The decision:** decide that "ask me first" is not a safety limit. Actions that must not happen get a refusal, graded by what a mistake costs. A question to a person is kept for rare judgment calls.
- **The risk:** people click Allow the hundredth time, and the platform offers ways to remove the box altogether. VS Code says global auto-approval "bypasses all user approvals, potentially leading to destructive actions". I did not measure how often people click without reading.
- **The cost of doing it right:** a short set of refusal rules, each with a written reason the agent can act on, plus someone to read the logs for rules that fire too often. Isolation in a sandbox cuts the number of boxes: Anthropic reports 84% fewer permission prompts in its own internal use, which is its number for its own tool.
- **Ask the team:** "Which actions can our agent take with no person in the loop, and are any of them impossible to undo?"

## The problem {#problem}

The obvious way to keep an agent safe is to make it ask. Before it runs a command, a box pops up: Allow or Deny. You are in charge, and nothing happens without your click.

It works on the first day. The first command, you read. The tenth, you glance. By the hundredth you click Allow before the box has finished drawing, because ninety-nine of the last ones were fine. This is not laziness. It is what people do when almost every question has the same right answer. The box has become a delay, not a check. (This is what I and many others see, and what the platform docs warn about. I did not measure how often; see the end.)

Then the platform gives you ways to remove the delay, and you use them, because the delay is annoying:

- **Allow all.** One setting, and no box ever appears. The action just runs.
- **Allow in this session.** One click on a single box, and the same kind of action is not asked again in that chat.
- **Autopilot.** The agent keeps working with no one at the keyboard. A box may appear, but no one is there to read it.

VS Code says it plainly: global auto-approval "bypasses all user approvals, potentially leading to destructive actions", and its command parsing is "best-effort" ([security](https://code.visualstudio.com/docs/copilot/security)). Its hooks page adds that `ask` "requires an interactive approval flow", so do not assume it pauses an unattended session ([hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)).

In the three modes I tried (default, Allow all, Autopilot), one thing held: a **refusal** from a hook. A box can be switched off. A refusal cannot be clicked away in a pop-up. (A person can still change the rule itself, and [Guard the files that hold the rules](4-3-guardrails.html) is about doing that safely.)

## How it works {#how-it-works}

### Asking and refusing

Two words to pin down. To **ask** is to stop and wait for a person to say yes. To **refuse** is to say no without waiting, and to say it the same way every time. The agent can talk a person into a yes (or the person can talk themselves into one). It cannot talk a program out of a no, as long as the program is running.

::: figure 4-2-ask-vs-refuse

So the two are for different jobs.

- **Refuse** what must not happen. Things you would never approve, or that you cannot undo. No one should be asked to say no to these a hundred times; the program says it once, always.
- **Ask** what depends on a person's judgment, and is rare. Asking only works when the box is rare enough to be read. Spend it where it is worth a person's attention.

An ask that matters needs one more thing: it must reach the person through a channel the agent cannot press itself. A box in the chat can be switched off by "allow for this session". I come back to this in [Two approvals](5-3-two-approvals.html).

### The terminal is the hard case

Edit tools are easy to guard. The path is a field in the call, and the rule is "refuse this path".

The terminal is not. It is the strongest tool an agent has, because it can run anything you can run. It is also the hardest to guard, because one effect can be spelled in many ways: a redirect, `rm`, `sed -i`, a script that runs another script. A hook reads the text of the command. It catches the common spellings, and it does not catch a path built from variables or a script written first and run later ([Hooks](2-2-hooks.html)). So rules on the terminal never reach "complete". That is not a reason to skip them. It is a reason to be honest about what they are: a guard against mistakes, not against an agent set on getting round them.

### Grade by consequence

If you cannot stop everything, stop by how much a mistake costs. Do not grade by how hard the task is. Hard tasks can be harmless, and easy commands can ruin a day. Code can judge consequence from the path and the command, so you do not have to choose a level for each task by hand. Note the limit: the code sees the words of a command, not its effect. The grade is a guess from text (see the traps below).

::: figure 4-2-grades

| Consequence | Example | What I do |
| --- | --- | --- |
| Reads only | Looking things up, reading files | Not stopped |
| Writes that can be undone | Editing in a work folder, writing a plan | Allowed, inside a defined area only |
| Writes to a real repository | Code that people will use | The agent writes in a work area first. A person approves before it is written back ([Two gates](5-3-two-approvals.html)) |
| Cannot be undone | Pushing, deleting a branch, resetting hard | Refused. The agent never gets a yes. A person does it |

The pattern: the more a mistake costs, the less the agent decides alone. At the top there is no asking at all.

### git as an example

git has both ends, so it makes a good case. In my setup, with a repository connected:

- **Reads pass.** `status`, `diff`, `log` and the like are never stopped.
- **Writes are refused with a way forward.** `add`, `commit`, switching branches. The refusal message holds the full command and a code. The person reads it, and approves by typing one command in their own terminal, within a time limit. The approval is for that command, not for git in general.
- **Some are never approvable by the agent.** `push`, opening a pull request, `reset --hard`, `clean`, and force options. The person runs these themselves.

Why not ask for all of them? Because the three groups deserve different treatment. Reads are free. Writes are normal and must be seen. A push or a hard reset is the kind of thing a hundredth click would let through.

### Write the reason for the agent

A refusal has two readers: you, and the agent. The agent matters more. It reads the message and decides what to do next.

A message that says only "denied" gets one of two results: the agent tries the same thing again, or it tries something worse. A good message does two jobs:

1. **Why** it was refused, in one sentence.
2. **What to do instead.**

For example, if the agent writes to the code folder before the plan is approved, a good reason says: the plan is not approved yet (plan approval is the first gate in [Two gates](5-3-two-approvals.html)); write the plan, stop, and ask the person to approve it in their terminal. The agent now knows the next step, so it goes that way rather than finding a side door.

I write every refusal as if it were the only help the agent will get. This is the same split as in the last chapter: the code stops, the words teach.

## Costs and traps {#costs-and-traps}

**Refusing is not free.** A refusal that is too wide stops real work, and the agent cannot argue its way past it. Keep the patterns narrow, keep a way for a person to approve what is wrong to refuse, and read the logs to see which rule fires.

**A box still has a use.** I keep some "needs a person" steps as a reminder. But I never count them as protection. If something must hold, it is a refusal.

**The patterns are always behind.** For the terminal, a new spelling will get through. For the things that must never be touched, do not rely on a pattern at all. Do not give the agent the thing ([Least privilege](4-5-least-privilege.html)).

**The grade is a guess from text.** Code judges a command by its words, not by what it does. A command that looks harmless can do harm after it is let through.

**I do not have numbers on approval fatigue.** The claim that people click Allow without reading is something I and many others see, and it is what the platform docs warn about. I have not measured how often.

## What the industry says {#industry}
{status: industry}

VS Code's security page recommends sandboxing over relying on approval rules alone, and suggests scoping auto-approval to the session rather than the workspace or the user. It calls model-assisted permissions "not a security boundary" ([security](https://code.visualstudio.com/docs/copilot/security)). This fits the chapter: asking is a convenience, refusing is a rule, and isolation is stronger than both.

Isolation also attacks approval fatigue at the root. Inside a sandbox, the agent may be allowed far more without asking, so there are fewer boxes to click. Anthropic reports that, in its internal use of Claude Code, sandboxing "safely reduces permission prompts by 84%", and that it needs both file system and network isolation to work ([Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)). That is Anthropic's own number for its own tool; I have not tested the sandbox VS Code offers.

## When to delete it {#when-to-delete-it}
{status: industry}

My refusal patterns for the terminal exist because I do not have a real sandbox. If your agent runs inside a container or a locked-down environment where it can only reach what you chose, most of them can go; the boundary does the work. The grading by consequence stays, since it is a way of thinking, not a feature.

If a platform lets you write refusals in its own permission settings, so they hold in every mode, move your hook rules there and keep the reasons.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Inspect how this project's agent handles permissions: the editor and agent settings, allow and deny lists, auto-approve options, and any hooks that refuse. List what runs without asking, what asks a person, and what is refused. Flag anything that can be undone only with difficulty (push, delete, reset, deploy) and say which of the three groups it is in. Also say whether any setting would let the box be switched off for a whole session or for good. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Security](https://code.visualstudio.com/docs/copilot/security), [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- In this book: [Hooks](2-2-hooks.html), [Guard the files that hold the rules](4-3-guardrails.html), [Least privilege](4-5-least-privilege.html)

## Explore it in the harness {#explore}

Copilot Harness grades by consequence, refuses on the terminal with a reason, and has a git ladder. The harness can walk you through the real rules and what the agent sees when it hits them. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Asking is not a limit". Teach me how this harness handles permissions: why "ask first" is not a limit (topic 8), how it grades by consequence, how git commands are treated, and how the terminal is guarded (topic 5). Open the real rules and refusal messages with me, and show me what the agent sees when it is refused.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.