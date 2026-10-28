This chapter assumes you have read [A rule in a prompt is a request](4-1-requests-and-rules.html): a rule that must hold has to be code, not words.

## In one sentence {#in-one-sentence}

"Ask me first" is not a limit, because people click Allow the hundredth time. A limit is a refusal the agent cannot argue with, graded by what the action can break.

## For leaders {#for-leaders}

- **The decision:** decide that "ask me first" is not a safety limit. Actions that must not happen get a refusal, graded by what a mistake costs. A question to a person is kept for the rare cases that need judgment.
- **The risk:** people click Allow the hundredth time, and the platform even offers ways to remove the box altogether. VS Code says global auto-approval "bypasses all user approvals, potentially leading to destructive actions". I did not measure how often people click without reading.
- **The cost of doing it right:** a short set of refusal rules, each with a written reason the agent can act on, plus someone who reads the logs for rules that fire too often. Isolation in a sandbox cuts the number of boxes as well. Anthropic reports 84% fewer permission prompts in its own internal use, though that is its number for its own tool.
- **Ask the team:** "Which actions can our agent take with no person in the loop, and are any of them impossible to undo?"

## Why does asking wear out? {#problem}

The obvious way to keep an agent safe is to make it ask. Before it runs a command, a box pops up with Allow and Deny, so you stay in charge and nothing happens without your click.

On the first day, it does its job. You read the first command and glance at the tenth, but by the hundredth you click Allow before the box has finished drawing, because ninety-nine of the last ones were fine (that is what I and many others see, and what the platform docs warn about, though I have not measured how often). This is not laziness. It is what anyone does when almost every question has the same right answer. By then the box is a delay, not a check.

A delay is annoying, so when the platform offers ways to remove it, you use them, and each goes further than the last. With Allow in this session, one click on a single box is enough to stop the same kind of action being asked about again in that chat. Allow all removes the box altogether. It is a single setting, and after it the action just runs. Autopilot goes further still: the agent keeps working with no one at the keyboard, so even when a box does appear, no one is there to read it.

The platform itself is plain about where this leads. VS Code warns that global auto-approval "bypasses all user approvals, potentially leading to destructive actions". It also admits that its own parsing of commands is only "best-effort" ([security](https://code.visualstudio.com/docs/copilot/security)). Its hooks page adds that `ask` "requires an interactive approval flow", so do not assume it pauses an unattended session ([hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)).

So what still holds once the box is gone? In the three modes I tried (default, Allow all and Autopilot), one thing held in all of them: a **refusal** from a hook. A box can be switched off, whereas a refusal cannot be clicked away in a pop-up. A person can still change the rule itself, and doing that safely is what [Guard the files that hold the rules](4-3-guardrails.html) is about. Before deciding what to refuse, though, it helps to be exact about how refusing differs from asking.

## What to refuse, and how {#how-it-works}

### Asking and refusing

To **ask** is to stop and wait for a person to say yes. To **refuse** is to say no without waiting, and to say it the same way every time. The difference lies in what can be argued with. The agent can talk a person into a yes (or the person can talk themselves into one), but as long as the program is running, the agent cannot talk it out of a no.

::: figure 4-2-ask-vs-refuse

That is why the two belong to different jobs. Refusing is for what must not happen, meaning the things you would never approve or cannot undo. Nobody should have to say no to those a hundred times when a program can say it once and keep saying it. Asking is for what depends on a person's judgment and comes up rarely, because a box only works when it is rare enough to be read. Spend it where it is worth a person's attention.

An ask that matters also has to reach the person through a channel the agent cannot press itself, since a box in the chat can be switched off by "allow for this session" (I come back to this in [Two gates](5-3-two-approvals.html)).

### The terminal is the hard case

How hard a refusal is to write depends on the tool. Edit tools are easy to guard, because the path is a field in the call and the rule can simply be "refuse this path".

The terminal is another matter. It is the strongest tool an agent has, because it can run anything you can run. It is also the hardest to guard, because one effect can be spelled in many ways, such as a redirect, `rm`, `sed -i`, or a script that runs another script. Can a hook not simply read the command? It can, and reading the text catches the common spellings. What it misses is a path built from variables, or a script written first and run later ([Hooks](2-2-hooks.html)). So rules on the terminal never reach "complete". That is no reason to skip them, but it is a reason to be honest about what they are: a guard against mistakes, not against an agent set on getting round them.

### Grade by consequence

If you cannot stop everything, stop things by how much a mistake costs, not by how hard the task is. Hard tasks can be harmless, while an easy command can ruin a day. Grading by consequence has another advantage: code can judge it from the path and the command, so you do not have to choose a level for each task by hand. The catch is that the code sees the words of a command, not its effect. The grade is a guess from text, and I come back to that among the costs below.

::: figure 4-2-grades

| Consequence | Example | What I do |
| --- | --- | --- |
| Reads only | Looking things up, reading files | Not stopped |
| Writes that can be undone | Editing in a work folder, writing a plan | Allowed, inside a defined area only |
| Writes to a real repository | Code that people will use | The agent writes in a work area first. A person approves before it is written back ([Two gates](5-3-two-approvals.html)) |
| Cannot be undone | Pushing, deleting a branch, resetting hard | Refused. The agent never gets a yes. A person does it |

Read down the table and the pattern shows. The more a mistake costs, the less the agent decides alone, until at the top grade there is no asking at all.

### git as an example

git makes a good case, because it has both ends. In my setup, with a repository connected, git commands fall into three groups.

- Reads pass. `status`, `diff`, `log` and the like are never stopped.
- Writes such as `add`, `commit` and switching branches are refused, but with a way forward. The refusal message holds the full command and a code, so the person can read it and approve by typing one command in their own terminal, within a time limit. The approval is for that command, not for git in general.
- Some commands can never be approved by the agent. These are `push`, opening a pull request, `reset --hard`, `clean`, and force options, and the person runs them themselves.

Why not simply ask for all of them? Because the three groups deserve different treatment. Reads are free, while writes are normal but must be seen. A push or a hard reset, though, is the kind of thing a hundredth click would let through, so for those only a refusal will do.

### Write the reason for the agent

A refusal has two readers, you and the agent. Of the two, the agent matters more, because it is the one that reads the message and decides what to do next.

If the message says only "denied", one of two things happens: the agent tries the same thing again, or it tries something worse. A good message avoids that by doing two jobs, saying in one sentence why the call was refused and what to do instead.

Say the agent writes to the code folder before the plan is approved. A good reason tells it that the plan is not approved yet (plan approval is the first gate in [Two gates](5-3-two-approvals.html)), and that it should write the plan, stop, and ask the person to approve it in their terminal. Now the agent knows the next step, so it goes that way instead of looking for a side door.

I write every refusal as if it were the only help the agent will get. It is the same split as in the last chapter, where the code stops and the words teach.

## What refusing costs, and where it falls short {#costs-and-traps}

Refusing has a price of its own. A refusal that is too wide stops real work, and the agent cannot argue its way past it. So keep the patterns narrow, keep a way for a person to approve what is wrong to refuse, and read the logs to see which rule fires.

Does that leave the box with no use at all? Not quite. I keep some "needs a person" steps as a reminder, but I never count them as protection, because anything that must hold gets a refusal.

The terminal patterns judge a command by its words, not by what it does. So they are always behind, and a new spelling will get through. The grade I said I would come back to has the same weakness, so a command that looks harmless can still do harm once its grade has let it through. For the things that must never be touched, then, do not rely on a pattern at all. Do not give the agent the thing ([Least privilege](4-5-least-privilege.html)).

One limit is in my own evidence. I have no numbers on approval fatigue, only what I and many others see and what the platform docs warn about.

## Why the docs point to a sandbox {#industry}
{status: industry}

If asking wears out and refusal patterns fall behind, where else can you turn? VS Code's security page answers with sandboxing, and recommends it over relying on approval rules alone. It is just as cautious about approvals themselves. It suggests scoping auto-approval to the session rather than the workspace or the user, and it calls model-assisted permissions "not a security boundary" ([security](https://code.visualstudio.com/docs/copilot/security)). That fits this chapter's split: asking is a convenience, refusing is a rule, and isolation is stronger than both.

Isolation also attacks approval fatigue at the root. Inside a sandbox the agent may be allowed far more without asking, so there are fewer boxes to click. Anthropic reports that in its internal use of Claude Code, sandboxing "safely reduces permission prompts by 84%", and that it needs both file system and network isolation to work ([Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)). That is Anthropic's own number for its own tool. I have not tested the sandbox VS Code offers.

## When the refusal patterns can go {#when-to-delete-it}
{status: industry}

A sandbox is also what decides when my own patterns can go. My refusal patterns for the terminal exist because I do not have a real sandbox. If your agent runs inside a container or a locked-down environment where it can reach only what you chose, most of them can go, because the boundary does the work. The grading by consequence stays either way, since it is a way of thinking, not a feature.

The other way out runs through the platform. If it lets you write refusals in its own permission settings, so that they hold in every mode, move your hook rules there and keep the reasons.

## Try it on your own setup {#try-it}

::: prompt
Inspect how this project's agent handles permissions: the editor and agent settings, allow and deny lists, auto-approve options, and any hooks that refuse. List what runs without asking, what asks a person, and what is refused. Flag anything that can be undone only with difficulty (push, delete, reset, deploy) and say which of the three groups it is in. Also say whether any setting would let the box be switched off for a whole session or for good. Do not change any files.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Security](https://code.visualstudio.com/docs/copilot/security), [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- In this book: [Hooks](2-2-hooks.html), [Guard the files that hold the rules](4-3-guardrails.html), [Least privilege](4-5-least-privilege.html)

## Explore it in the harness {#explore}

Copilot Harness grades by consequence, refuses on the terminal with a reason, and has a git ladder. The harness can walk you through the real rules and show you what the agent sees when it hits them.

::: prompt
/harness-rookie-wondering I have read the chapter "Asking is not a limit". Teach me how this harness handles permissions: why "ask first" is not a limit (topic 8), how it grades by consequence, how git commands are treated, and how the terminal is guarded (topic 5). Open the real rules and refusal messages with me, and show me what the agent sees when it is refused.
:::
