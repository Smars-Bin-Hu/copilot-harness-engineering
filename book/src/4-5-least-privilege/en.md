This chapter assumes you have read [Hooks](2-2-hooks.html) and [Enforcement design](4-4-enforcement-design.html), or know that a hook can refuse a tool call but can itself fail.

## In one sentence {#in-one-sentence}

A hook only blocks what it can see. For things that must never be touched (production, credentials, other people's repositories), the best defence is never giving them to the agent.

## For leaders {#for-leaders}

- **The decision:** for production systems, credentials and other teams' repositories, decide that the agent is never given access at all, rather than given access with a hook to guard it.
- **The risk:** a hook sees the text of a call, not its effect, and it can fail. A guard that holds most of the time is the wrong tool for something that cannot be undone or is not yours. I have no count of incidents prevented.
- **The cost of doing it right:** people's time. A person runs the query and pastes the answer back, which is slower than a connection. A real sandbox is a bigger step, and I have not built one. So use this where harm is large or cannot be undone, not everywhere.
- **Ask the team:** "Make a list of everything this agent can open, run or connect to. Which of those must never be touched, and why can the agent reach them?"

## Why some things should not be guarded at all {#problem}

A good guard on a door is still only a guard. It can be tricked, it can fall asleep, and it can be handed the wrong list. A wall with no door has none of these problems.

Yet everything so far in this part has been a guard. A hook reads the text of a call but cannot see what the call will do ([Hooks](2-2-hooks.html)). And the hook itself is software that can fail ([Enforcement design](4-4-enforcement-design.html)). The VS Code docs say as much: hooks and instructions are "not substitutes for enforced permissions, sandboxing, or enterprise controls".

For most of what an agent does, though, an imperfect guard is enough. If a hook misses a file edit in a code project, the change shows up in the diff and you can revert it. But some things cannot be undone, and some are not yours. A production system is one, because a single wrong command there changes real data. Credentials are another: a leak cannot be taken back. And another team's repository is a place where you have no right to make a mistake.

For these, a guard that holds "most of the time" is the wrong tool. What they need is an idea older than agents, **least privilege**: give a program only what it needs for the job, and nothing else. The security guidance on prompt injection lists the same idea first among its defences, as "Enforce privilege control and least privilege access" ([OWASP](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)). If the agent cannot reach a thing, it cannot be talked, tricked or confused into touching it, so no hook has to catch anything.

For high-risk work, then, least privilege is the first choice, and the hooks of the earlier chapters come second. That leaves a practical question: the agent still has to do the work, so how do you take things away from it without taking away the job?

## Taking things out of the agent's reach {#how-it-works}

::: figure 4-5-reach

The method is a question you ask once for each dangerous thing: **can I arrange the work so the agent never needs it?** Often you can, in one of four ways.

### 1. Give it a copy of the files to change, not the whole workspace

Suppose the agent works on code that lives in a large shared repository. The easy way is to open that repository and let the agent roam, but then every file is in reach, the ones it should change and a thousand it should not.

The other way is to decide first what the work will touch and hand over only that. In my setup, when the work is in a target repository, the agent works from a plan that names the files to change. Only those files are fetched, as copies, into the task's own folder (see [Manage tasks, not chats](5-1-tasks.html)), and the agent edits the copies. Your working tree, your current branch and your existing commits are not changed.

Writing back to the real repository is a separate step that a person approves (the second gate in [Two gates](5-3-two-approvals.html)). It puts the files on a **new branch** and does not commit, so if anything is wrong, you delete the branch. The agent's mistakes are thus limited to a folder that exists only for this task. A hook still guards that folder, but if the hook fails, the worst case is a bad copy, not a bad repository.

The same goes for commands. Those that push, open a pull request, reset hard or clean are never run by the agent, only by a person. If a guard is wrong about a push, the leak cannot be fetched back. A command that is not available cannot be wrong.

### 2. Never connect to the environment; ask a person to run the query

What does the agent actually need from production? Usually not a connection, but a fact: "what is in this table", "which version is deployed", "does this job exist". And a fact is something a person can fetch.

My setup gives the agent no credentials and no tools to connect to an environment. That is a rule of use, not a sandbox guarantee, and I come back to the difference below. When the agent needs something only an environment can tell it, it writes the question in one fixed place. With it goes a command or a query that only reads, ready for the person to run as it is. The person runs it and pastes the answer back. The agent asks at its next stop, not in the middle of work.

::: figure 4-5-ask-a-person

This costs time, and I will not pretend otherwise: a person is slower than a connection. In return, you get three things. The agent has no path to production, so no injected text, no bad guess and no failing hook can reach it. Every fact that came from an environment is written down, along with who ran it. And the person sees the query before it runs, which is the review you wanted anyway. (The answer the person pastes back is itself untrusted text, though, as [Text the agent reads can give it orders](4-6-untrusted-input.html) explains.)

### 3. Keep credentials and keys out of the context

Taking away the connection still leaves the keys themselves. Anything in the agent's context can be sent somewhere else, whether written to a file, put in a command or repeated in a summary. A secret the agent has seen is therefore a secret that can leak, even when the agent is not malicious. A model that copies a token into a log line while debugging has already done the damage.

Four habits follow from this, and I offer them as a design, not as something I measured.

- Do not put secrets in files the agent reads. Rules, notes and knowledge files hold no values, only where a value lives and who owns it.
- Let the program that needs a secret get it at the moment of use, from the place meant for it, instead of passing it through the agent. The agent writes "run the deploy script", and the script holds the key.
- For the agent's own access, use a limited key: read-only, one project, and expiring soon. Then a leak is small.
- Keep secrets out of what the agent can read by accident, such as the environment variables of the shell it runs in and config files in the home folder. These are easy to forget.

### 4. Close the way out

Keeping secrets out of sight is one part. The way out is the other, because a secret that cannot be sent anywhere is much less dangerous. If the agent's commands can reach any address on the internet, anything it can read can be sent out. If they can reach only a short list, the damage is limited. This is the third circle in [Untrusted input](4-6-untrusted-input.html), and I treat it there. The point here is only that network access is a privilege like any other: ask what the agent needs, and give that.

### When it is time for a real sandbox

Everything above works by giving the agent less. As I said under the second way, that is a rule of use, not a guarantee. A **sandbox** or **container** is different. It is a boundary set by the operating system around everything the agent runs, so inside it the agent can do what it likes, and the walls hold even if a command is cleverly written. A hook cannot offer that, because it only reads the text.

My harness has no sandbox. Terminal commands can write any path the user can, while the hook stops only the common spellings. The harness's own design notes say plainly that for strong isolation you use the operating system or a container. Look at one sooner than I did if any of these is true:

- the agent runs commands without a person watching ([Use subagents sparingly](2-3-subagents.html) and the later chapters on unattended work);
- the project handles production, credentials or another team's repository;
- the agent can run code that came from somewhere you do not control.

Anthropic's write-up on sandboxing Claude Code makes a point worth copying: effective sandboxing needs both file system and network isolation. Without network isolation, a hijacked agent can send out your files. Without file system isolation, it can escape the sandbox to the network ([Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)). One without the other is not enough. In practice that means a container or a virtual machine with its own network rules, not just a folder.

Nor is a sandbox magic. The VS Code docs call theirs "an added layer", and "not a virtual machine or user-account boundary", so read what yours does and does not cover (I have not tested VS Code's).

### Test your own setup

For each thing that must never be touched, three questions are worth asking.

1. Is it in the agent's reach at all? List what the agent can open, run and connect to, and cross out what it does not need.
2. If your hook and your instructions both failed today, what is the worst thing the agent could do with it?
3. Is there a person-run step that could replace a connection or a key?

There is also a one-minute test you can run today. In a terminal opened the way your agent opens it, run `env` and look at the names of the variables. Then list the files in your home folder that hold keys or tokens, and ask whether the agent could read them. If you do not like the answer, that is your first fix, and it does not need a hook.

## What giving less costs, and where it falls short {#costs-and-traps}

Giving less has a price. Part of it is paid by the work, because an agent that cannot reach something it needs will stop or do a worse job. I have no numbers on how many tasks that costs, so watch for it when you remove access. Part of it is paid by people, because the ask-a-person step is slower than a connection. For production that is worth it. For a read of a public file it is not. Use the method where the harm is large or cannot be undone, not everywhere.

The copies bring a trap of their own. The agent works on copies of the files, so if the real repository moves while the work is going on, the write-back has to cope with that. Keep tasks short, and check the diff before the write-back.

Least privilege is also only as good as your list. If you forgot a key in a config file, the agent has it. Finding such things is what the test above is for.

None of this makes the hook unimportant. Not giving the thing is the best defence for what must never be touched, but for everything else the hook is the cheap, always-on check, and the next-best defence. I use both. The chapter's claim is about order: first remove, then guard.

I have not measured any of this or counted the incidents it prevented. What I can say is that the design is simpler to reason about: a thing that is not there cannot be misused.

## Do OWASP and VS Code agree? {#industry}
{status: industry}

Both sources have come up already in this chapter, and put side by side they point the same way. The OWASP list of defences against prompt injection includes "Enforce privilege control and least privilege access" and "Require human approval for high-risk actions" ([OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)). The VS Code docs say hooks and instructions "are not substitutes for enforced permissions, sandboxing, or enterprise controls", and describe their sandbox as "an added layer", not "a virtual machine or user-account boundary" ([Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks), [Security](https://code.visualstudio.com/docs/copilot/security)). Neither says that a hook is useless, only that it is not enough alone.

## When to delete the ask-a-person step {#when-to-delete-it}
{status: industry}

The step in which a person runs a query exists because I do not trust an agent with a live connection. If one day a platform offers a connection that is enforced read-only, scoped to one table, logged, and cannot be changed by the agent, the ask-a-person step can go for that data. The other part, not handing over what is not needed, does not retire. It is the principle, not a workaround.

## Try it on your own setup {#try-it}

::: prompt
List everything this agent could reach from the way it runs in this project: folders and files it can read or write, shell commands it can run, tools and servers it is connected to, accounts or credentials visible in its environment or config files, and network addresses it can call. Do this by reading the configuration and project files, not by connecting to anything. Mark each item as needed for the work, or not needed, and mark anything that is production, a credential, or another team's repository. Do not change any files and do not print secret values, only where they live.
:::

## Go deeper {#go-deeper}

- OWASP: [LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- VS Code docs: [Security](https://code.visualstudio.com/docs/copilot/security)
- [Untrusted input](4-6-untrusted-input.html): the chapter on what to do when the agent reads text that gives it orders

## Explore it in the harness {#explore}

The harness has the pieces for the first two ways: the copies in the task folder, the write-back to a new branch, the commands that only a person runs, and the place where the agent asks a person for facts from an environment.

::: prompt
/harness-rookie-wondering I have read the chapter "Some things you never hand over". Teach me how this harness keeps the agent away from the real repository and from any environment (topic 8, especially 8.5 and 8.7). Open the real files with me, and show me what the gate can see and what it cannot.
:::
