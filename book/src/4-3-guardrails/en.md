This chapter assumes you have read [Asking is not a limit](4-2-ask-vs-refuse.html): a limit is a refusal the agent cannot argue with.

## In one sentence {#in-one-sentence}

If the agent can edit the rules, the rules mean nothing. So keep the rule files and the hook files out of its reach, and make any human override last one session, expire, and leave a record.

## For leaders {#for-leaders}

- **The decision:** decide that the agent may not edit the files that hold its rules, its hooks or its evidence, and that any human override is limited to one session, expires and leaves a record.
- **The risk:** a rule the agent can edit is a rule it can remove, and a "passed" record it can write is a pass it can give itself. I have no incident to report, so the case rests on the argument, not on a count.
- **The cost of doing it right:** a list of protected files, kept up to date as parts are added, plus a way for a person to open the fence on purpose. My own override depends on a person remembering to switch it off. A time limit and a second reader would be better, but I do not have them.
- **Ask the team:** "Can the agent edit the files that hold its own rules and records, and can you show me a refusal when it tries?"

## What if the agent edits the rule? {#problem}

Say you have a hook that refuses dangerous commands. It works. Now ask where that hook lives. It lives in a file, and so does the configuration that tells the platform to run it. The numbers it uses are in a file too. And the agent has an edit tool.

The agent does not need bad intent to change those files. Picture one that is stuck behind a refusal and under pressure to finish its task. It sees that the rule is in the way and does the sensible-looking thing, which is to loosen the rule. A rule the agent can edit is a rule the agent can remove. I have no incident to report and did not measure how often agents try to edit rules, so the point rests on the argument alone.

Records have the same weakness. If a check leaves a "passed" file and the agent can write that file, then the agent can pass itself. So the question is not only which commands are refused. It is also who can change the things that do the refusing and the proving.

In both cases the threat is mostly a careless agent, not a hostile one. An agent led by injected text is a second case ([Text the agent reads can give it orders](4-6-untrusted-input.html)), one that needs the same fence and more.

I call the files that must be out of the agent's reach **guardrail files**. Together they are a fence, in the sense that the agent works inside it and cannot move it. That raises three questions: which files belong in the fence, how it is held, and how a person gets through when the rules themselves must change.

If you only do one thing after this chapter, make the rule files and the hook files unwritable for the agent.

## How the fence is built, and how a person gets through {#how-it-works}

### Which files are the fence

::: figure 4-3-fence

In my setup the fence is made of these files:

- the **hook configuration**, the file that tells the platform which hook to run;
- the **engine**, the code of the hook itself, and the commands the agent is allowed to call;
- the **policies**, the plain files that hold the numbers and patterns of the rules;
- the **runtime state**, the files the hook writes while it runs: session state, approval records and logs;
- the editor settings that could switch the hooks off;
- the license files of the repository.

You might expect instruction files and skills on the list, but they are not. They are text for the agent to read, a request rather than a limit. Changing them does not change what the code refuses.

### How the fence is held

Once the list is set, every way the agent could write to those files has to be stopped. How hard that is depends on the tool. Edit tools are the easy case, because the path is in the call and the hook can refuse the call before it runs.

The terminal is harder, because the same write can be spelled in many ways. The hook catches the common spellings, such as a redirect, `rm`, `mv`, `sed -i`, `cp` and `tee`. But the limits from [Asking is not a limit](4-2-ask-vs-refuse.html) apply here too, so an indirect spelling is not caught.

Even the path needs care, because the same file can be written with other letter case, with `..`, as an absolute path, or with the backslash of Windows. If the rule compared paths as they came, the fence would have gaps in the spelling, so it brings them all to one form before it compares. Two more gaps are worth checking in your own setup, although I have not tested either: a symbolic link that points into a guarded folder and a disk that ignores letter case.

One more rule governs the list itself. A company can add paths to it, but it cannot take the defaults away, because an override that removed a default would be the same hole as an agent that can edit the rule.

All of this guards against mistakes. It is not a sandbox, because an agent set on getting round it can do so with a script it writes first. For the strong version, see [Least privilege](4-5-least-privilege.html).

### Files only a command may write

Rules are not the only files worth guarding. Some files are evidence: the state of a task, the verdicts of the independent checks ([Can a model check a model?](5-6-model-checks-model.html)), snapshots (copies of files taken at a point in time), the diff an approval is based on and the final report.

If the agent could write them, it could declare a check passed, or change what was approved. So the agent never writes them with its edit tools. A command writes them instead and judges the result itself. When I say "the agent recorded a result", I mean that the agent asked the command to record it and the command made the decision.

Folders that hold what the person brought follow the same rule. Documents, reference code and results from a run are for the agent to read. The person writes them, through a page or a command. Evidence that the agent could edit is not evidence.

### The breaker

A fence that holds brings a new problem. When a refusal keeps coming, an agent may keep trying. A hook cannot stop it, because all a hook can do is refuse a call. So when the same refusal comes up three times in a row (three is my setting), the **breaker** trips and replaces the reason with a different one: stop trying this, and tell the person. That is still a request, in the form of a message, but it is all a hook can do. It also keeps the log from filling with the same refusal.

### When a person must open the fence

Sometimes, though, the rules themselves have to change. When I extend the harness, I change guardrail files, so there must be a way in. The question is how to give that right to a person without giving it to the agent.

My first thought was to let one named agent edit the fence. That does not work in Copilot today, because the event a hook receives does not carry the name of the main agent ([Hooks](2-2-hooks.html)). Since the hook cannot tell which agent is calling, any agent could pass for the named one. Rights that follow a name can be claimed by anyone who uses the name.

So the right follows the session instead, set by the person. It rests on a switch in the state of the session that only the person can turn on, by typing a code in their own terminal. The agent cannot run that command: if it tries, the hook refuses it. This is the same channel as in [Two gates](5-3-two-approvals.html).

::: figure 4-3-admin

Four things make the override safe:

1. It belongs to a session, not to an agent, so it ends with that session.
2. It is turned off when the work is done. My rule is to switch it off and then read, in git, the diff of what changed.
3. It leaves a record. While it is on, every logged call is marked as admin.
4. Some doors stay shut even then. In my setup even admin cannot write the runtime state, which holds the approval records, because if it could, it could forge an approval. And in the same session no task can be opened and no subagent called.

Each of these removes a way that a short exception turns into a standing hole. The second, though, is also the weak point of the design. There is no timer in my setup, so switching admin off depends on a person remembering. A time limit is a better design, and the approval of git writes already uses one. For a team, add an expiry and a second person who reads the diff.

### Test your own setup

In a copy of your project, ask your agent to loosen one rule in its own hook configuration. If it succeeds, your rules are a request, so protect the file and try again.

## Where the fence can still fail {#costs-and-traps}

Does a fence that passes that test hold everywhere? Not quite, and there are three places where it can still leak. The first is its list. A guardrail file missing from the list is open, so when you add a part to the engine, add its path too.

The second is the way through the fence, which is also a gap in it. Admin is real power: it can change the engine, so what it does is not hard-limited. The control is a person reading the diff afterwards, and I do not claim more than that.

The third is spelling. Because the terminal is guarded by pattern, in theory a spelling the hook does not know could change a record that lives in a task folder (the folder that holds one piece of work; see [Manage tasks, not chats](5-1-tasks.html)). I have not tried to build one. The fix, again, is to keep what must never be touched out of reach altogether.

One more trap is not a hole but a puzzle. If the agent hits a refusal on a file it does not know is guarded, the reason must say so and say what to do. The previous chapter covers how to write that reason.

## Why "out of reach" and not "safe" {#industry}
{status: industry}

How far can a fence made of hooks be trusted? VS Code's hooks page says hooks and instructions are not substitutes for enforced permissions or sandboxing, and its security page recommends sandboxing over approval rules alone ([hooks](https://code.visualstudio.com/docs/copilot/customization/hooks), [security](https://code.visualstudio.com/docs/copilot/security)). The trouble is that a fence made of hooks stands inside the same machine the agent runs on. So this chapter says "out of reach" and not "safe".

## When the list of guarded paths can go {#when-to-delete-it}
{status: industry}

The same point tells you when the list can go. If the agent runs in an environment where the rule files are mounted read-only, or the hook runs outside the machine the agent can touch, the list of guarded paths is not needed, because the environment is the fence. Keep the other lesson even then: any override a person grants should be bound to the session, time-limited, and recorded.

## Try it on your own setup {#try-it}

::: prompt
Find every file in this project that defines what the agent may or may not do: instruction files, hook scripts and their configuration, permission settings, editor settings, and any file that records a check or an approval. For each, tell me whether the agent's own edit tools and terminal could change it today, using the rules and permissions you can see. Output a list sorted by how bad it would be if the file were changed. Do not change any files, and do not try to edit them to find out.
:::

## Go deeper {#go-deeper}

- VS Code docs: [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks), [Security](https://code.visualstudio.com/docs/copilot/security)
- In this book: [Asking is not a limit](4-2-ask-vs-refuse.html), [Least privilege](4-5-least-privilege.html), [Two gates](5-3-two-approvals.html)

## Explore it in the harness {#explore}

Copilot Harness has a list of guarded files, files only commands may write, a breaker, and an admin mode tied to the session. The harness can show you each of them in the real files.

::: prompt
/harness-rookie-wondering I have read the chapter "Guard the files that hold the rules". Teach me how this harness keeps its own rules out of the agent's reach: which files are guardrails and how they are protected (topic 7), the breaker, and admin mode (topic 8). Open the real policy and show me what the agent sees when it is refused.
:::
