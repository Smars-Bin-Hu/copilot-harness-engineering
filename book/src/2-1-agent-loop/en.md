This chapter assumes only that you have used an AI coding agent, such as Copilot in agent mode.

## In one sentence {#in-one-sentence}

An agent is a loop: ask the model, run the tool it asks for, feed the result back. You steer it at a few points in each turn.

## For leaders {#for-leaders}

- **The decision:** when an agent misbehaves, ask which of four places to fix (what it reads, which tools it has, a check before a call, a check after a call) before asking for a bigger model or a longer prompt.
- **The risk:** the loop itself almost never breaks, but a rule that lives only in a prompt is a request the model may not follow.
- **The cost of doing it right:** mostly setup time. The cheapest lever, what the agent reads, takes only a few lines of written rules.
- **Ask the team:** "For the last bad result, was the fix a better context, a tighter tool list, or a check outside the model?"

## When an agent goes wrong, what is actually wrong? {#problem}

When an agent does something wrong, it is natural to picture a mind that has made a bad choice. The trouble is that this picture sends people to the wrong fix. They write a longer prompt, add "be careful" in capital letters, or switch to a bigger model. Sometimes that helps, but often it does not, because the problem was not in the thinking.

If the problem is not in the thinking, where is it? The answer lies in the machine. It turns out to be small and plain, with a few places where you can reach into it. Every later chapter in this part, like most of the chapters after it, works on one of them.

The machine starts with the **model**, the AI itself. It reads text and writes text and does nothing else, yet an agent plainly does more than write, since it reads files, searches, changes files and runs commands. Each of these is a **tool**, one thing the agent can do in your project. What joins the two is the **tool call**, which is the model's request to use a tool, written as text: "read this file". How a model that can only write text ends up changing your files is what the loop explains.

## What the machine is, and where you can reach into it {#how-it-works}

### Ask, run, feed back

The model cannot touch your files, because all it can do is write text. So an agent needs a program outside the model to do the acting for it. The model writes a tool call, and a program around the model, the part that is not AI, reads that text and runs the tool for real, then pastes the result back in front of the model as more text. The model reads that result and writes the next tool call. This repeats until the model writes an answer with no tool call in it, which is the signal that it thinks it is done.

I call one trip around this loop a **turn**. Not everyone uses the word this way. Some people mean the whole exchange from your message to the final answer, and in one trip a model can also ask for several tools at once. Here, a turn is one round of ask, run, feed back.

::: figure 2-1-loop

Two facts follow from this picture.

The first is that every action is a tool call. The model has no other way to do anything, so there is a door that every action passes through. Whoever stands at that door can see, and stop, everything the agent does. A **hook** stands there: a small program of yours that the platform runs at fixed points, just before and just after each tool call. (For the built-in tools and for subagents I have seen every call pass the hook point, though I have not tested MCP tools. The next chapter, [Hooks](2-2-hooks.html), has the details.)

The second is that the model sees only text. It does not see your screen or your disk, only what is in its context: the rules, your words, the results of earlier tool calls and its own earlier answers. That context also has a size limit, which is what [The context is a budget](3-1-context-budget.html) is about.

### When does it stop?

The ordinary stop is the one just described, the model answering without asking for a tool. But there are others. You can press stop, the platform can reach a limit, or something can refuse the stop.

That last one is useful. A hook can run when the agent is about to stop, look at the to-do list of the task (the steps it still has open), and say "not yet, step 4 is open", after which the loop goes on. This is how an agent is made to work through a long list without you, a case that [Use subagents sparingly](2-3-subagents.html) covers along with its stop rules. It is a first sign that the loop has places where your own code can step in.

### Where you can step in

Look at the loop again. You cannot change how the model thinks. What you can change are four things around it.

1. **What it reads.** The rules and instructions put in its context, and the files it is pointed at, make up the most used lever and also the cheapest. [Instructions and skills](3-3-instructions-and-skills.html) is about it.
2. **Which tools exist.** An agent that has no tool for changing files cannot change files. A tool's description and its error messages are also the only manual the model gets for it ([Tool calling](1-2-tool-calling.html)). To give a role a shorter list, you use a custom agent ([Custom agents](2-4-custom-agents.html)).
3. **A hook before a call.** Code here sees the call before it runs and can refuse it. Because the platform guarantees that every call passes through this point, a rule here is code that runs, not a request. A hook is not the only rule made of code, though. A tool list, or a command the agent runs to check itself, also counts, only each covers a narrower range ([chapter 4.1](4-1-requests-and-rules.html)). Permission settings and sandboxes are another kind of lever. They do not read the call but limit what any command can do, so I leave them out of the four.
4. **A hook after a call.** Code here sees the result, can keep a record, and can add a note for the model. It cannot undo what happened.

A short way to remember the four is that two of them decide what the model knows, and two decide what it is allowed to do. Words only change what it knows.

### Why most mistakes are not in the loop

That split, between what the model knows and what it is allowed to do, is also how I read an agent's mistakes. The loop itself almost never breaks. The mistakes come from what is in the context, or from what is allowed. Below is the list I keep from my own use. It records what I have seen, not a statistic.

| What you see | Usually why |
| --- | --- |
| It changed what it should not | It reasons about how to get the job done, not whether it is allowed. |
| It forgot something from earlier | The context was compressed or the chat was too long. |
| It checked its own work and said it was fine | The same model with the same reasoning has the same blind spots. |
| It keeps retrying a refused action | It wants to finish the task. |
| It said "done" and it was not | In my experience models lean towards reporting success. |

Few of these are about the model being unintelligent. The first and the last need a check outside the model. Of the rest, the second needs a better context ([Long chats get worse](3-2-long-sessions.html)) and the third a second view ([Use subagents sparingly](2-3-subagents.html)). Only the fourth is close to a habit of the model itself. So the opening question has its answer: the fix usually belongs at one of the four places, not in the model's thinking.

### See the loop yourself

You do not need to install anything to watch the loop go round. In your agent's chat, ask "Read the README and tell me what the project does" and watch the chat. Before the answer you will see a line such as "Read README.md". That line is one tool call, shown to you. Now ask a question that needs three files, and count the lines. Each is one turn of the loop, and each result is now in the context.

## What the loop costs, and how it is misread {#costs-and-traps}

The cost of the loop starts from that last point, that every result stays in the context. Each time around, the model reads the whole context again, now with one more result in it, so a task of thirty turns is thirty reads of a growing text. What the agent reads therefore matters more than how clever the model is, and [the model's price per token](1-1-models-and-cost.html) is the wrong number to look at alone.

The reread is not always charged at full price, though. Providers cache a repeated beginning, and on Anthropic's API a cache read costs about a tenth of the base input price ([Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)). So the cache lowers the bill. It does nothing for the other cost: the model still has to attend to all of that text.

And of all that text, tool results are the biggest part and the least watched. You wrote the prompt, so you know what is in it. The file the agent read, or the log a command printed, you may never have seen. It is still in the context, where the model may act on it.

An agent is not always the answer, either, because letting the model choose its own next step has a price. Such a loop costs more and is harder to predict than a fixed series of model calls, or a single call. Anthropic's advice is to find the simplest solution possible and add complexity only when needed ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)). If the steps of a job never change, a script that calls the model at fixed points may serve you better than an agent.

One more trap has nothing to do with cost. It is easy to read the loop as a plan, and it is not one. The model does not plan the whole path and then follow it. It decides one turn at a time from what it sees, so when it goes down a wrong path, it is usually because the result of an earlier turn led it there.

## When to delete my hooks, and what stays {#when-to-delete-it}
{status: industry}

Will any of this go out of date? The reasoning about the loop does not retire while agents work by calling tools, but the practical parts may. Today I steer at four places because that is what the platform gives me. If the platform starts to offer a native way to enforce a rule, a budget or a stop condition, I will use that instead of my own hooks.

## Try it on your own setup {#try-it}

::: prompt
Read this project's instruction files and settings. For each rule or limit you find, tell me which of four places it works at: what the agent reads, which tools exist, a check before a tool call, or a check after a tool call. Mark every rule that is only a written request with nothing outside the model enforcing it. List the five rules where a break would matter most. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). It defines agents as "LLMs autonomously using tools in a loop".
- Anthropic: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), on when a fixed workflow is enough
- VS Code docs: [Context engineering guide](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)

## Explore it in the harness {#explore}

The loop is the same everywhere, but in the harness you can watch each turn from the side: what is injected into the context, and which call a hook saw and what it answered.

::: prompt
/harness-rookie-wondering I have read the chapter "The agent loop, and where you can step in". Teach me how this harness stands at the four places in the loop: what it puts into the context, which tools it allows, and what its hooks do before and after a call. Open the real files with me and draw how one turn passes through them.
:::
