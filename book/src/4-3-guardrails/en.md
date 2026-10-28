This chapter assumes you have read [Asking is not a limit](4-2-ask-vs-refuse.html): a limit is a refusal the agent cannot argue with.

## In one sentence {#in-one-sentence}

If the agent can edit the rules, the rules mean nothing. Keep the rules and the hook files out of its reach, and make any human override last one session, expire, and leave a record.

## For leaders {#for-leaders}

- **The decision:** decide that the agent may not edit the files that hold its rules, its hooks or its evidence, and that any human override is limited to one session, expires and leaves a record.
- **The risk:** a rule the agent can edit is a rule the agent can remove, and a "passed" record it can write is a pass it can give itself. I have no incident to report. The argument is the point, not a count.
- **The cost of doing it right:** a list of protected files, kept up to date as parts are added, and a way for a person to open the fence on purpose. My override depends on a person remembering to switch it off; a time limit and a second reader are better, and I do not have them.
- **Ask the team:** "Can the agent edit the files that hold its own rules and records, and can you show me a refusal when it tries?"

## The problem {#problem}

Who is the threat here? Mostly a careless agent, not a hostile one: an agent that is under pressure to finish a task and loosens a rule that is in the way. An agent led by injected text is a second case ([Text the agent reads can give it orders](4-6-untrusted-input.html)); it needs the same fence, and more.

You have a hook that refuses dangerous commands. It works. Now ask: where does the hook live? In a file. The configuration that tells the platform to run it is a file. The numbers it uses are a file. And the agent has an edit tool.

An agent that is stuck behind a refusal does not need bad intent to change the file. It only needs to be trying to finish the task, see that the rule is in the way, and do the sensible-looking thing: loosen the rule. I have no incident to report. The argument is the point: a rule the agent can edit is a rule the agent can remove.

The same is true of records. If a check leaves a "passed" file and the agent can write that file, the agent can pass itself. So the question is not only "which commands are refused", it is "who can change the things that do the refusing and the proving".

I call the files that must be out of reach **guardrail files**: a fence, in the sense that the agent works inside it and cannot move it.

If you only do one thing from this chapter: make the rule files and the hook files unwritable for the agent.

## How it works {#how-it-works}

### Which files are the fence

::: figure 4-3-fence

In my setup these are:

- the **hook configuration**, the file that tells the platform which hook to run;
- the **engine**, the code of the hook itself, and the commands the agent is allowed to call;
- the **policies**, the plain files that hold the numbers and patterns of the rules;
- the **runtime state**, the files the hook writes while it runs: session state, approval records and logs;
- the editor settings that could switch the hooks off;
- the license files of the repository.

Instruction files and skills are not on the list. They are text, a request, and the agent is meant to read them. Changing them does not change what the code refuses.

### How the fence is held

- **Edit tools: refused before the call.** This is the easy one. The path is in the call.
- **The terminal: the common spellings.** A redirect, `rm`, `mv`, `sed -i`, `cp`, `tee`, and so on. The limits in [Asking is not a limit](4-2-ask-vs-refuse.html) apply: an indirect spelling is not caught.
- **One form for a path before comparing.** The same file can be written with other letter case, with `..`, as an absolute path, or with the backslash of Windows. The rule brings them all to one form first. Otherwise the fence would have gaps in the spelling. Two more gaps worth checking in your own setup: a symbolic link that points into a guarded folder, and a disk that ignores letter case. I have not tested either.
- **A company can add paths, not take the defaults away.** Anyone who sets up a team can protect more files. An override that removes a default would be the same hole as an agent that can edit the rule.

This is a guard against mistakes. It is not a sandbox, and I do not call it one. An agent set on getting round it, with a script it writes first, can. For the strong version, see [Least privilege](4-5-least-privilege.html).

### Files only a command may write

Some files are not rules, but they are evidence: the state of a task, the verdicts of the independent checks ([Can a model check a model?](5-6-model-checks-model.html)), snapshots (copies of files taken at a point in time), the diff an approval is based on, the final report.

If the agent could write them, it could declare a check passed, or change what was approved. So the agent never writes them with its edit tools. A command writes them, and the command judges the result itself. "The agent recorded a result" means the agent asked the command to record it, and the command decided.

The same goes for folders that hold what the person brought: documents, reference code, results from a run. The agent reads them. The person (through a page or a command) writes them. Evidence that the agent could edit is not evidence.

### The breaker

When a refusal keeps coming, an agent may keep trying. A hook can only refuse a call; it cannot stop the agent. So when the same refusal comes up three times in a row (three is my setting), the **breaker** trips and the reason is replaced with a different one: stop trying this, and tell the person. It is a request in the form of a message, but it is the only thing a hook can do. It also keeps the log from filling with the same refusal.

### When a person must open the fence

Sometimes the rules themselves have to change. When I extend the harness, I change guardrail files. So there must be a way in. How do you give that right without giving it to the agent?

**Not by agent.** I first thought to let one named agent edit the fence. But in Copilot today the event a hook receives does not carry the name of the main agent ([Hooks](2-2-hooks.html)), so the hook cannot tell which agent is calling. Any agent could pass for the named one. Rights that follow a name can be claimed by anyone who uses the name.

**By session, set by the person.** The ground is a switch in the state of the session. Only the person can turn it on, by typing a code in their own terminal. The agent cannot run that command, and the hook refuses it if it tries. This is the same channel as in [Two approvals](5-3-two-approvals.html).

::: figure 4-3-admin

What makes the override safe:

1. **It belongs to a session, not to an agent.** It ends with that session.
2. **It is turned off when the work is done.** My rule is to switch it off, and then read the diff of what changed with git. I rely on that; I do not have a timer in my setup. This is the weak point of the design: it depends on a person remembering. A time limit is a better design, and the approval of git writes already uses one. For a team, add an expiry and a second person who reads the diff.
3. **It leaves a record.** While it is on, every logged call is marked as admin.
4. **Some doors stay shut.** In my setup even admin cannot write the runtime state, which holds the approval records. If it could, it could forge an approval. And no task can be opened in the same session, and no subagent called.

Each of these removes a way that a short exception turns into a standing hole.

### Test your own setup

In a copy of your project, ask your agent to loosen one rule in its own hook configuration. Does it succeed? If it does, your rules are a request. Then protect the file and try again.

## Costs and traps {#costs-and-traps}

**The fence is as good as its list.** A guardrail file missing from the list is open. When you add a part to the engine, add its path.

**Admin is real power.** It can change the engine, so what it does is not hard-limited. The control is a person reading the diff afterwards. I do not claim more than that.

**Spelling gaps remain.** Because the terminal is guarded by pattern, in theory a spelling it does not know could change a record that lives in a task folder (the folder that holds one piece of work; see [Manage tasks, not chats](5-1-tasks.html)). I have not tried to build one. The fix, again, is to keep what must never be touched out of reach altogether.

**A fence you cannot see is a puzzle.** If an agent hits a refusal on a file it does not know is guarded, the reason must say so and what to do. See the last chapter.

**I did not measure how often agents try to edit rules.** I wrote the fence because the argument is simple, not because I watched a specific incident.

## What the industry says {#industry}
{status: industry}

VS Code's hooks page says hooks and instructions are not substitutes for enforced permissions or sandboxing, and its security page recommends sandboxing over approval rules alone ([hooks](https://code.visualstudio.com/docs/copilot/customization/hooks), [security](https://code.visualstudio.com/docs/copilot/security)). A fence made of hooks is a fence inside the same machine the agent runs on. That is why this chapter says "out of reach" and not "safe".

## When to delete it {#when-to-delete-it}
{status: industry}

If the agent runs in an environment where the rule files are mounted read-only, or the hook runs outside the machine the agent can touch, the list of guarded paths is not needed; the environment is the fence. Keep the other lesson: any override a person grants should be bound to the session, time-limited, and recorded.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Find every file in this project that defines what the agent may or may not do: instruction files, hook scripts and their configuration, permission settings, editor settings, and any file that records a check or an approval. For each, tell me whether the agent's own edit tools and terminal could change it today, using the rules and permissions you can see. Output a list sorted by how bad it would be if the file were changed. Do not change any files, and do not try to edit them to find out.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks), [Security](https://code.visualstudio.com/docs/copilot/security)
- In this book: [Asking is not a limit](4-2-ask-vs-refuse.html), [Least privilege](4-5-least-privilege.html), [Two approvals](5-3-two-approvals.html)

## Explore it in the harness {#explore}

Copilot Harness has a list of guarded files, files only commands may write, a breaker, and an admin mode tied to the session. The harness can show you each of them in the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Guard the files that hold the rules". Teach me how this harness keeps its own rules out of the agent's reach: which files are guardrails and how they are protected (topic 7), the breaker, and admin mode (topic 8). Open the real policy and show me what the agent sees when it is refused.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.