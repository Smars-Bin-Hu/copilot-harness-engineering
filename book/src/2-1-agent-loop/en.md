This chapter assumes you have used an AI coding agent, such as Copilot in agent mode. Nothing else.

## In one sentence {#in-one-sentence}

An agent is a loop: ask the model, run the tool it asks for, feed the result back. You steer it at a few points in each turn.

## For leaders {#for-leaders}

- **The decision:** when an agent misbehaves, ask which of four places to fix (what it reads, which tools it has, a check before a call, a check after a call) before asking for a bigger model or a longer prompt.
- **The risk:** the loop itself almost never breaks. In my reading, mistakes come from what is in the context or from what is allowed, and a rule written in a prompt is only a request. I have no counts of how often each happens.
- **The cost of doing it right:** mostly setup time. The cheapest lever, what the agent reads, is a few lines of written rules.
- **Ask the team:** "For the last bad result, was the fix a better context, a tighter tool list, or a check outside the model?"

## The problem {#problem}

When an agent does something wrong, it feels like a mind has made a bad choice. That feeling sends people to the wrong fix. They write a longer prompt, or add "be careful" in capital letters, or switch to a bigger model. Sometimes that helps. Often it does not, because the problem was not in the thinking.

It helps to know what the machine is. It is small and plain. This chapter draws it, and marks the few places where you can reach into it. Every later chapter in this part, and most chapters after it, work on one of those places.

Three words first.

- A **model** is the AI itself. It reads text and writes text. It does nothing else.
- A **tool** is one thing the agent can do in your project: read a file, search, change a file, run a command.
- A **tool call** is the model's request to use a tool, written as text: "read this file".

## How it works {#how-it-works}

### The loop

The model cannot touch your files. It can only write text. So the way an agent works is this. The model writes a tool call. A program around the model, the part that is not AI, reads that text and runs the tool for real. The program then pastes the result back in front of the model as more text. The model reads it, and writes the next tool call. This repeats until the model writes an answer with no tool call in it. That is the signal that it thinks it is done.

I call one trip around this loop a **turn**. Some people use the word for the whole exchange from your message to the final answer, and in one trip a model can ask for several tools at once; here a turn is one round of ask, run, feed back.

::: figure 2-1-loop

Two facts follow, and both matter later.

1. **Every action is a tool call.** The model has no other way to do anything. So there is a door that every action passes through. (For the built-in tools and for subagents I have seen every call pass the hook point; I have not tested MCP tools. [Hooks](2-2-hooks.html) has the details.) Whoever stands at that door can see, and stop, everything the agent does. A hook stands there. It is a small program of yours that the platform runs just before and just after each tool call, at fixed points; [Hooks](2-2-hooks.html) explains it.
2. **The model sees only text.** It does not see your screen or your disk. It sees what is in its context: the rules, your words, the results of earlier tool calls, its own earlier answers. Its context is its whole world, and it has a size limit. [The context is a budget](3-1-context-budget.html) is about that.

### When does it stop?

The ordinary stop is the model answering without asking for a tool. There are others: you press stop, the platform reaches a limit, or something refuses the stop.

That last one is useful. A hook can run when the agent is about to stop, look at the to-do list of the task (the steps it still has open), and say "not yet, step 4 is open". The loop then goes on. This is how an agent is made to work through a long list without you. [Use subagents sparingly](2-3-subagents.html) covers that case and its stop rules. I have not checked what limit on turns Copilot sets by default, so I do not give one here.

### Where you can step in

Look at the loop again. You cannot change how the model thinks. You can change four things around it.

1. **What it reads.** The rules and instructions that are put in its context, and the files it is pointed at. This is the most used lever, and the cheapest. [Instructions and skills](3-3-instructions-and-skills.html) is about it.
2. **Which tools exist.** An agent that has no tool for changing files cannot change files. And a tool's description and its error messages are the only manual the model gets for it ([Tool calling](1-2-tool-calling.html)). A custom agent is the way to give a role a shorter list ([Custom agents](2-4-custom-agents.html)).
3. **A hook before a call.** Code that sees the call before it runs and can refuse it. The platform guarantees that every call passes through this point, so a rule here is code that runs, not a request. A tool list or a command the agent runs to check itself is code too, but each covers a narrower range ([chapter 4.1](4-1-requests-and-rules.html)). Permission settings and sandboxes are another kind of lever: they do not read the call, they limit what any command can do. I have not tested them one by one on Copilot, so I leave them out of the four.
4. **A hook after a call.** Code that sees the result, can keep a record, and can add a note for the model. It cannot undo what happened.

A short way to remember it: two of the four decide what the model knows, and two decide what it is allowed to do. Words only change what it knows.

### Why most mistakes are not in the loop

Here is how I read an agent's mistakes. The loop itself almost never breaks. The mistakes come from what is in the context, or from what is allowed. This is the list I keep, from my own use. It is what I have seen, not a statistic:

| What you see | Usually why |
| --- | --- |
| It changed what it should not | It reasons about how to get the job done, not whether it is allowed. A rule in a prompt is only a request. |
| It forgot something from earlier | The context was compressed or the chat was too long. |
| It checked its own work and said it was fine | The same model with the same reasoning has the same blind spots. |
| It keeps retrying a refused action | It wants to finish the task. |
| It said "done" and it was not | In my experience models lean towards reporting success. |

Notice that few of these are about the model being unintelligent. The first and the last need a check outside the model. The second needs a better context ([Long chats get worse](3-2-long-sessions.html)). The third needs a second view ([Use subagents sparingly](2-3-subagents.html)). Only the fourth is close to a habit of the model itself. I do not have counts of how often each happens, so this is my reading of what I have seen, not a measurement.

### See the loop yourself

You do not need to install anything. In your agent's chat, ask: "Read the README and tell me what the project does." Watch the chat. You will see a line such as "Read README.md" before the answer. That line is one tool call, shown to you. Then ask a question that needs three files, and count the lines. Each is one turn of the loop, and each result is now in the context.

## Costs and traps {#costs-and-traps}

**Every turn rereads the context.** Each time around, the model reads the whole context again, now with one more result in it. A task of thirty turns is thirty reads of a growing text. This is why what the agent reads matters more than how clever the model is, and why [the model's price per token](1-1-models-and-cost.html) is the wrong number to look at alone. One correction: the reread is not always charged at full price. Providers cache a repeated beginning, and on Anthropic's API a cache read costs about a tenth of the base input price ([Models and cost](1-1-models-and-cost.html) has the sums). I have not checked how Copilot bills it. What the cache does not fix is the second cost: the model still has to attend to all of that text.

**Tool results are the biggest and the least watched part.** You wrote the prompt, so you know it. The file the agent read, or the log a command printed, you may never have seen. It is still in the context, and the model may act on it.

**An agent is not always the answer.** A loop that decides its own next step costs more and is harder to predict than a fixed series of model calls, or a single call. Anthropic's advice is to find the simplest solution possible and add complexity only when needed ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)). If the steps of a job never change, a script that calls the model at fixed points may serve you better than an agent.

**Do not read the loop as a plan.** The model does not plan the whole path and then follow it. It decides one turn at a time from what it sees. When it goes down a wrong path, it is usually because the result of an earlier turn led it there.

## When to delete it {#when-to-delete-it}
{status: industry}

The reasoning about the loop does not retire while agents work by calling tools. The practical parts may. Today I steer at four places because that is what the platform gives me. If the platform starts to offer a native way to enforce a rule, a budget or a stop condition, I will use that instead of my own hooks. I would then drop the hooks, not the loop picture.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Read this project's instruction files and settings. For each rule or limit you find, tell me which of four places it works at: what the agent reads, which tools exist, a check before a tool call, or a check after a tool call. Mark every rule that is only a written request with nothing outside the model enforcing it. List the five rules where a break would matter most. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). It defines agents as "LLMs autonomously using tools in a loop".
- Anthropic: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), on when a fixed workflow is enough
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)

## Explore it in the harness {#explore}

The loop is the same everywhere, but in the harness you can watch each turn from the side: what is injected into the context, and which call a hook saw and what it answered. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "The agent loop, and where you can step in". Teach me how this harness stands at the four places in the loop: what it puts into the context, which tools it allows, and what its hooks do before and after a call. Open the real files with me and draw how one turn passes through them.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
