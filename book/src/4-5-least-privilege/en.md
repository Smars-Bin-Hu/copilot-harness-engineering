This chapter assumes you have read [Hooks](2-2-hooks.html) and [Enforcement design](4-4-enforcement-design.html), or know that a hook can refuse a tool call but can itself fail.

## In one sentence {#in-one-sentence}

A hook only blocks what it can see. For things that must never be touched (production, credentials, other people's repositories), the best defence is never giving them to the agent.

## For leaders {#for-leaders}

- **The decision:** for production systems, credentials and other teams' repositories, decide that the agent is never given access at all, instead of guarding the access with a hook.
- **The risk:** a hook sees the text of a call, not its effect, and it can fail. A guard that holds most of the time is the wrong tool for something that cannot be undone or is not yours. I have no count of incidents prevented.
- **The cost of doing it right:** people time. A person runs the query and pastes the answer back, which is slower than a connection. A real sandbox is a bigger step, and I have not built one. Use this where harm is large or cannot be undone, not everywhere.
- **Ask the team:** "Make a list of everything this agent can open, run or connect to. Which of those must never be touched, and why can the agent reach them?"

## The problem {#problem}

A good guard on a door is still a guard. It can be tricked, it can be asleep, and it can be given the wrong list. A wall with no door has none of these problems.

Everything so far in this part is a guard. A hook reads the text of a call and cannot see its effect ([Hooks](2-2-hooks.html)), and the hook itself is software that can fail ([Enforcement design](4-4-enforcement-design.html)). Hooks and instructions are, in the words of the VS Code docs, "not substitutes for enforced permissions, sandboxing, or enterprise controls".

For most of what an agent does, this is fine. A missed stop on a file edit in a code project can be seen in the diff and undone. But some things cannot be undone, and some things are not yours:

- a production system, where one wrong command changes real data;
- credentials, where one leak cannot be taken back;
- another team's repository, where you have no right to make a mistake.

For these, a guard that holds "most of the time" is the wrong tool. The idea of this chapter is older than agents: **least privilege**. Give a program only what it needs for the job, and nothing else. The security guidance on prompt injection lists the same idea first among its defences: "Enforce privilege control and least privilege access" ([OWASP](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)). If the agent cannot reach a thing, it cannot be talked, tricked or confused into touching it, and no hook has to catch anything. For high-risk work this is the first choice, and the hooks of the earlier chapters come second. (A one-minute test is at the end of the chapter.)

## How it works {#how-it-works}

::: figure 4-5-reach

The method is a question you ask once for each dangerous thing: **can I arrange the work so the agent never needs it?** Often you can. Four ways.

### 1. Give it a copy of the files to change, not the whole workspace

Suppose the agent works on code that lives in a large shared repository. The easy way is to open that repository and let the agent roam. Every file is then in reach: the ones it should change, and a thousand it should not.

The other way is to decide first what the work will touch, and hand over only that. In my setup, for a target repository, the agent works from a plan that names the files to change. Only those files are fetched, as copies, into the task's own folder (see [Manage tasks, not chats](5-1-tasks.html)). The agent edits the copies. Your working tree, your current branch and your existing commits are not changed.

The write-back to the real repository is a separate step that a person approves (the second gate in [Two gates](5-3-two-approvals.html)). It writes the files on a **new branch** and does not commit. If anything is wrong, you delete the branch. So the agent's mistakes are limited to a folder that exists only for this task. A hook still guards that folder, but if the hook fails, the worst case is a bad copy, not a bad repository.

Also here: commands that push, open a pull request, reset hard or clean are never run by the agent. A person runs them. A guard that is wrong about a push is a leak you cannot fetch back. A command that is not available cannot be wrong.

### 2. Never connect to the environment; ask a person to run the query

What does the agent need from production? Usually not a connection. It needs a fact: "what is in this table", "which version is deployed", "does this job exist". A fact can be fetched by a person.

My setup gives the agent no credentials and no tools to connect to an environment. This is a rule of use, not a sandbox guarantee (see the last section). When it needs something only an environment can tell it, it writes the question in one fixed place. Each question comes with a command or a query that only reads, which the person can run as it is. The person runs it and pastes the answer back. The agent asks at its next stop, not in the middle of work.

::: figure 4-5-ask-a-person

This costs time, and I will not pretend otherwise: a person is slower than a connection. In return, three things become true. The agent has no path to production, so no injected text, no bad guess and no failing hook can reach it. (The answer a person pastes back is itself untrusted text; see [Text the agent reads can give it orders](4-6-untrusted-input.html).) Every fact that came from an environment is written down, with who ran it. And the person sees the query before it runs, which is the review you wanted anyway.

### 3. Keep credentials and keys out of the context

Anything in the agent's context can be sent somewhere else: written to a file, put in a command, repeated in a summary. So a secret that the agent has seen is a secret that can leak, and the agent does not have to be malicious. A model that copies a token into a log line while debugging has done the damage.

I describe this as a design, not as something I measured:

- **Do not put secrets in files the agent reads.** Rules, notes and knowledge files hold no values, only where a value lives and who owns it.
- **Let the program that needs the secret get it,** at the moment of use, from the place meant for it, instead of passing it through the agent. The agent writes "run the deploy script"; the script holds the key.
- **For the agent's own access, use a limited key:** read-only, one project, and expiring soon. Then a leak is small.
- **Keep the secrets out of what the agent can read by accident:** environment variables of the shell it runs in, config files in the home folder. These are easy to forget.

### 4. Close the way out

Reading is not the only danger. A secret that cannot be sent anywhere is much less dangerous. If the agent's commands can reach any address on the internet, then anything it can read can be sent out. If it can reach only a short list, the damage is limited. This is the third circle in [Untrusted input](4-6-untrusted-input.html), and I treat it there. The point here is that network access is a privilege like any other: ask what the agent needs, and give that.

### When it is time for a real sandbox

The measures above give the agent less. A **sandbox** or **container** is different: it is a boundary set by the operating system, around everything the agent runs. Inside it, the agent can do what it likes, and the walls hold even if the command is cleverly written. A hook cannot offer that, because it only reads the text.

My harness has none. Terminal commands can write any path the user can, and the hook stops only the common spellings. The design notes say plainly that for strong isolation you use the operating system or a container. Look at one sooner than I did if:

- the agent runs commands without a person watching ([Use subagents sparingly](2-3-subagents.html) and the later chapters on unattended work);
- the project handles anything the three lists above name;
- the agent can run code that came from somewhere you do not control.

Anthropic's write-up on sandboxing Claude Code makes a point worth copying: effective sandboxing needs both file system and network isolation. Without network isolation, a hijacked agent can send out your files; without file system isolation, it can escape the sandbox to the network ([Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)). One without the other is not enough. In practice that means a container or a virtual machine with its own network rules, not just a folder.

Note what the VS Code docs say about sandboxing: it is "an added layer", and "not a virtual machine or user-account boundary". A sandbox is not magic either. Read what yours does and does not cover. I have not tested VS Code's sandbox.

### Test your own setup

**Three questions** for each thing that must never be touched:

1. Is it in the agent's reach at all? List what the agent can open, run and connect to, and cross out what it does not need.
2. If your hook and your instructions both failed today, what is the worst thing the agent could do with it?
3. Is there a person-run step that could replace a connection or a key?

**A test you can run today.** In a terminal opened the way your agent opens it, run `env` and look at the names of the variables. Then list the files in your home folder that hold keys or tokens. Ask: could the agent read these? If you do not like the answer, that is your first fix, and it does not need a hook.

## Costs and traps {#costs-and-traps}

**Less access can also mean a task that fails.** An agent that cannot reach something it needs will stop or do a worse job. I have no numbers on how many tasks that costs; watch for it when you remove access.

**Less access means more work for people.** The ask-a-person step is slower than a connection. It is worth it for production. It is not worth it for a read of a public file. Use the method where the harm is large or cannot be undone, not everywhere.

**A copy can drift from the original.** The agent works on copies of the files. If the real repository moves while the work is going on, the write-back has to cope with that. Keep tasks short, and check the diff before the write-back.

**Least privilege is only as good as your list.** If you forgot a key in a config file, the agent has it. The test above is for finding such things.

**The hook still matters.** Not giving the thing is the best defence for what must never be touched. For everything else, the hook is the cheap, always-on check, and the next-best defence. I use both. The chapter's claim is about order: first remove, then guard.

**I have not measured any of this.** I have no count of incidents prevented. I know the design is simpler to reason about: a thing that is not there cannot be misused.

## What the industry says {#industry}
{status: industry}

The OWASP list of defences against prompt injection includes "Enforce privilege control and least privilege access" and "Require human approval for high-risk actions". ([OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)) The VS Code docs say hooks and instructions "are not substitutes for enforced permissions, sandboxing, or enterprise controls", and describe their sandbox as "an added layer", not "a virtual machine or user-account boundary". ([Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks), [Security](https://code.visualstudio.com/docs/copilot/security)) Neither says that a hook is useless; both say it is not enough alone.

## When to delete it {#when-to-delete-it}
{status: industry}

A step in which a person runs a query exists because I do not trust an agent with a live connection. If one day a platform offers a connection that is enforced read-only, scoped to one table, logged, and cannot be changed by the agent, the ask-a-person step can go for that data. The other part, not handing over what is not needed, does not retire. It is the principle, not a workaround.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
List everything this agent could reach from the way it runs in this project: folders and files it can read or write, shell commands it can run, tools and servers it is connected to, accounts or credentials visible in its environment or config files, and network addresses it can call. Do this by reading the configuration and project files, not by connecting to anything. Mark each item as needed for the work, or not needed, and mark anything that is production, a credential, or another team's repository. Do not change any files and do not print secret values, only where they live.
:::

## Go deeper {#go-deeper}

- OWASP: [LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- VS Code docs: [Security](https://code.visualstudio.com/docs/copilot/security)
- [Untrusted input](4-6-untrusted-input.html): the chapter on what to do when the agent reads text that gives it orders

## Explore it in the harness {#explore}

The harness has the pieces for the first two ways: the copies in the task folder, the write-back to a new branch, the commands that only a person runs, and the place where the agent asks a person for facts from an environment. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Some things you never hand over". Teach me how this harness keeps the agent away from the real repository and from any environment (topic 8, especially 8.5 and 8.7). Open the real files with me, and show me what the gate can see and what it cannot.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.