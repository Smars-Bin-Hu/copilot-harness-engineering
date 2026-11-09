This chapter assumes only that you've used an AI coding agent, such as Copilot in agent mode.

## In one sentence {#in-one-sentence}

An agent is a loop in which the model decides what to do, a program outside the model does it, and the result goes back to the model so it can decide the next step. There are four places on that loop you can change, so when an agent gets something wrong, work out which of them to fix before you reach for a different model or a longer prompt.

## For leaders {#for-leaders}

- **The decision:** when an agent goes wrong, ask which of the four places needs fixing (what it reads, which tools it has, the check before a call, the check after a call) before you pay for a pricier model or ask for a longer prompt.
- **The risk:** the loop itself rarely breaks, and what breaks is usually one of the four things around it. A rule written in a prompt is only a request the model may not follow, and the loop stops when the model no longer wants a tool, not when the work is actually finished, so an agent that says "done" shouldn't be taken at its word.
- **The cost of doing it right:** mostly setup time. The cheapest fix is changing what the agent reads, which can take a few lines of rules. The checks before and after a call are code, and someone has to maintain them.
- **Ask the team:** "The last time a result was bad, did we fix the context or the tool list, or did we add a check outside the model?"

## When an agent goes wrong, don't rush to blame the model {#problem}

When an agent makes a mistake, people tend to assume the model behind it got something wrong, so they keep adding lines to the prompt to guard against it, like "be careful" or "don't do XX", or they switch to a smarter model, say from Sonnet to Opus with thinking effort turned all the way up. Sometimes that helps, but it doesn't touch the root cause, because what an agent ends up doing depends not only on the model but also on what the model has read, which tools it has, and whether anything checks a tool call before and after it runs, and all of that sits outside the model, where switching to another model can't reach it.

An AI agent really has two parts, the model (the LLM) and the tools (Tool Calling). You send a prompt and the model thinks, but a model on its own is a brain with no hands: it can't look up a file, change a file, run a terminal command, open a browser or drive your whole computer through Computer Use by itself, and Tool Calling is how it gets those things done. Once the model has decided what to do, it issues a call through the tool interface it has been given, and a program outside the model actually runs it (Claude Code and Copilot's agent mode are both programs like this). The result comes back as the model's next input, the model reads it and thinks again, and it decides either to call another tool or that the task is done, in which case it writes you a reply, and that reply is the answer you see.

That process is what we call the **Agent Loop**.

There are four places on this loop you can change: what the model reads, which tools it gets, the check before a tool call, and the check after one. In this chapter I want to teach you to read that loop, so that the next time an agent goes wrong, you first work out which of the four to fix, and only then think about switching models or adding to the prompt.

## How the loop runs, and how to change its four places {#how-it-works}

::: figure 2-1-loop

### On every turn, the model reads the prompt from scratch

This book calls one trip around the loop a **turn**. The program assembles the prompt and sends it to the model, the model writes back some text, possibly with one or more tool calls in it, and the program runs those tools, records the results and decides whether to go on. The VS Code team draws the same line when they describe Copilot's loop, though they call it a round, and they say the prompt is rebuilt on every round ([The Coding Harness Behind GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode)). The model remembers nothing from one turn to the next, and anything that isn't in this turn's prompt doesn't exist as far as it's concerned, so the system instructions, the rules, what you said, and every earlier tool call along with its result all have to be put back in on every turn. Watch the word when you read the docs, though: Claude Code's and Copilot's documentation usually say turn for the whole stretch from the message you send to the answer you get back, which can hold many of this book's turns.

Two things follow from this. The first is that every action the agent takes is a tool call, because the model has no other way to do anything, and since the tools are run by a program outside the model, a call can be stopped before it runs. That's where a **hook** sits: a small program you write that the platform runs at fixed moments, such as before and after every tool call ([Hooks, the point every call passes through](2-2-hooks.html)). The second is that the model sees nothing but the text in the prompt. It can't see your screen or your disk, so its picture of the project is whatever the context says, and the context has a size limit ([Context is a budget](3-1-context-budget.html)).

Whether a hook catches every call depends on the platform. Claude Code's docs say outright that tool calls inside subagents and MCP tools fire the same hooks ([Hooks reference](https://code.claude.com/docs/en/hooks)). Copilot's docs only say that hooks fired inside a subagent get a few extra input fields, and the tool names they list are all built-in tools, with no mention of MCP ([GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference)). On Copilot I've seen calls from built-in tools and from subagents go through hooks, but I haven't tested MCP tools. Two kinds of action skip this path entirely. One is server-side tools, which run at the provider with none of your code in between ([When an Agent misuses a tool, check its description and errors first](1-2-tool-calling.html)). The other is a file you reference with `@` in Claude Code, which by default goes straight into the context without any tool call, so a hook that guards file reads never fires.

### The loop stops when the model stops asking for tools

There's only one normal way for the loop to end, and that's a turn in which the model asks for no tool. On Anthropic's API the loop keeps going as long as `stop_reason` is `tool_use`, and once the model writes its answer, `stop_reason` becomes `end_turn` and the loop exits ([How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)). Copilot works the same way: when a turn has no tool calls, its text is the final answer. So a stopped loop only tells you that the model thinks it's done, not that the work is done, and nothing along the way has checked the result for you.

The other two ways to stop aren't the model's call. One is you pressing stop, and the VS Code docs are clear that stopping doesn't undo actions already completed, or changes already made to external services ([Build with AI in VS Code](https://code.visualstudio.com/docs/agents/overview)). The other is a platform limit: VS Code's `chat.agent.maxRequests` caps how many requests the agent can make, and the default is 25 ([AI settings reference](https://code.visualstudio.com/docs/agents/reference/ai-settings)).

There's also the opposite case, in which the model wants to stop and gets sent back. Copilot's `agentStop` and Claude Code's `Stop` are hooks that run when the model finishes its answer, and they can return `block` with a reason, which goes back to the model as a new prompt, so the loop carries on. That's a useful spot to have. When the model says it's done, the hook can check the to-do list or run the tests, and if something's missing it can answer "not done yet, step 4 is still open", which lets an agent work through a long list without you watching over it ([Use subagents sparingly](2-3-subagents.html)). The price is that the agent might never stop, and every turn costs money, so Copilot CLI and Claude Code both have a safety valve that forces the stop after 8 blocks in a row, and a hook can tell from the `stop_hook_active` field that the current turn is one that was already sent back ([GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference), [Hooks reference](https://code.claude.com/docs/en/hooks)).

### There are four places on the loop you can change

You can't change how the model thinks. What you can change are the four things around it.

1. **What it reads.** Rules files, skills and the files you point it at are all text placed in its context, and this is the most used and the cheapest of the four, since a few lines of rules can tell it things it would never guess on its own ([Instructions and skills, load only what you need](3-3-instructions-and-skills.html)). The weakness is that all this text is only a request the model may not follow, and once a conversation gets long, both VS Code and Claude Code compact its earlier part into a summary, which can lose details and instructions from the start.
2. **Which tools it has.** The model can only call the tools it has been given, and a tool's description and error messages are the only way it learns what that tool does ([When an Agent misuses a tool, check its description and errors first](1-2-tool-calling.html)). To give a role a fixed, shorter tool list, you use a custom agent ([Custom agents](2-4-custom-agents.html)). The weakness is that a tool can often do more than its name says: take away the file-editing tool but leave the terminal, and the agent can still edit files with commands.
3. **The check before a call.** Before a tool runs, a hook sees the tool's name and arguments, and it can let the call through or refuse it with a reason that goes back to the model. The platform runs the hook and the model can't skip it, so a rule here is code that runs, not a request. Hooks aren't the only way to enforce a rule in code, either: the tool list, and a command the agent runs to check itself, also count, they just cover narrower ground ([A rule in a prompt is a request](4-1-requests-and-rules.html)). The platform's own approval rules sit here too, such as VS Code's auto-approve rules, which match on the text of a command. The weakness is that the check sees only the text of the call and not what the command does once it's running, and the VS Code docs say plainly that hooks aren't a substitute for enforced permissions, sandboxing or enterprise controls ([Security](https://code.visualstudio.com/docs/agents/run/security)).
4. **The check after a call.** After a tool runs, a hook sees the result. It can keep a record or add a note for the model, and in Copilot and Claude Code it can even rewrite the result the model reads. The weakness is that it can't undo what has already happened, as the VS Code docs also point out ([Hooks](https://code.visualstudio.com/docs/agent-customization/hooks)), so any action you need to stop has to be stopped before the call.

Places 1 and 4 change what the model knows, and places 2 and 3 change what it can do. Anything that lives only in a rules file changes nothing but what it knows.

A sandbox is a different kind of thing. It doesn't look at calls at all but limits what a command can touch once it's running, so I haven't counted it among the four ([Some things you never hand over](4-5-least-privilege.html)).

### When something goes wrong, first find which place to fix

The loop itself rarely goes wrong. Anthropic's docs give its standard form as a `while` loop on `stop_reason`, only a few lines of code, and nearly every problem turns up at one of the four places instead. The table below comes from my own use of agents, so it records what I've seen rather than any statistics.

| What you see | Usually why | Fix this first |
| --- | --- | --- |
| It changed something it shouldn't have | It's thinking about how to get the job done, not about whether it's allowed to | The check before a call, or a shorter tool list |
| It forgot something said earlier | The context was compacted, or the conversation ran too long | What it reads: put what matters in a file instead of leaving it in the chat ([Long chats get worse](3-2-long-sessions.html)) |
| It checked its own work and said it was fine | The same model with the same reasoning has the same blind spots | A check from another angle: a second agent, or a command ([Use subagents sparingly](2-3-subagents.html)) |
| It keeps retrying an action that was refused | It wants to finish the task | Make the refusal's reason say what to do instead ([Asking is not a limit](4-2-ask-vs-refuse.html)) |
| It said "done" and it wasn't | The loop only asks whether the model wants another tool, and models lean towards reporting success | A check when it stops, and letting it run the tests itself ([Let the agent check its own work](5-4-self-checks.html)) |

The third and the last rows aren't only my experience, because Anthropic has written about both. They found that agents grading their own work skew positive, confidently praising work that's only mediocre ([Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)), and that Claude tends to mark a feature as complete without testing it properly ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). Few of these come down to the model not being clever enough, so switching models belongs after you've checked all of them ([Don't pick a model by token price alone](1-1-models-and-cost.html)).

### Watch the loop go round once yourself

You don't need to install anything to see the loop in action. In your agent's chat, ask "Read the README and tell me what this project does", and before the answer appears you'll see a line like "Read README.md". That line is one tool call, and VS Code collapses its details by default, so expand it to see the input and output ([Use tools with agents](https://code.visualstudio.com/docs/agents/run/tools)). Then ask a question that needs three files and you'll see three calls, which may be bunched into a single turn, and all three results are now sitting in the context. To see exactly what the model receives each time, run **Developer: Show Chat Debug View** in VS Code. It lists every model interaction with its system prompt, prompt, context, response and tool inputs and outputs, and paging through them one at a time shows you what each turn added ([Debug chat interactions](https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view)). The view contains your code and file paths, so look it over before you share it.

## The loop costs more with every turn, and it isn't a plan {#costs-and-traps}

Most of what the loop costs goes on rereading. On every turn the model reads the whole context again, now with the last turn's results added, so the amount it reads grows faster than the number of turns. Using the numbers from the worked example in [Don't pick a model by token price alone](1-1-models-and-cost.html), 10 turns read 325,000 tokens in total and 20 turns read 1,150,000, about 3.5 times as much. Prompt caching makes the rereading much cheaper: on Anthropic's API a cache read costs a tenth of the base input price on most models, and a twentieth on Opus 5.5 and Sonnet 5.5 ([Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)). But caching only saves money. The text still fills the context window and still pulls on the model's attention, and Anthropic says context "must be treated as a finite resource with diminishing marginal returns" ([Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

Of all that text, the part nobody watches much is the tool results. You wrote the prompt, so you know what's in it, but the files the agent read and the logs a command printed may be things you've never seen. They take up the window all the same, and the model may act on the words in them ([Text the agent reads can give it orders](4-6-untrusted-input.html)). As for how much room they take, Anthropic has one figure: in a 100-turn web search evaluation, automatically clearing stale tool results as the context neared its limit cut token use by 84% ([Managing context on the Claude Developer Platform](https://claude.com/blog/context-management)).

Letting the model choose its own next step has a price of its own. Anthropic says agentic systems trade latency and cost for better task performance, and recommends finding the simplest solution possible and adding complexity only when it's needed ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)). If the steps of a job never change, a script that calls the model at fixed points may suit you better than an agent, because it's cheaper and easier to predict.

The other trap is reading the loop as a plan. The model doesn't work out the whole route first and then follow it. On each turn it decides the next step from that turn's prompt, and even if it wrote a plan at the start, the plan is just a piece of text in the context. So when an agent heads down the wrong path, it was usually led there by the result of some earlier turn, and that result is still in the context, read again on every turn that follows.

## Once the platform has it built in, delete your own hooks {#when-to-delete-it}
{status: industry}

As long as agents work by calling tools, the loop and its four places won't go out of date. What will is the part I wrote myself. Today I use hooks to block calls and to push the agent to keep going because those are the places the platform leaves me, and if the platform offers a native way to enforce rules, budgets or stop conditions, I'll switch to it and drop my own hooks. That has already started. VS Code's Autopilot approves every tool and keeps the agent going until the task is complete, and with `chat.autopilot.advanced.enabled` turned on, a separate model judges whether the request is complete ([Security](https://code.visualstudio.com/docs/agents/run/security), [AI settings reference](https://code.visualstudio.com/docs/agents/reference/ai-settings)). Claude Code's `/goal` is, in effect, a built-in Stop hook ([Hooks reference](https://code.claude.com/docs/en/hooks)).

## Try it on your own setup {#try-it}

::: prompt
Read this project's instruction files and settings. For each rule or limit you find, tell me which of the four places it works at: what the agent reads, which tools it has, the check before a tool call, or the check after a tool call. Mark every rule that is only a written request, with nothing outside the model enforcing it. List the five rules whose failure would do the most damage. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), which defines agents as "LLMs autonomously using tools in a loop"
- Anthropic: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), on when a fixed workflow is enough
- Anthropic docs: [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works), the standard way to write the loop
- VS Code blog: [The Coding Harness Behind GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode)
- Claude Code docs: [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- VS Code docs: [Set up a context engineering flow in VS Code](https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide)

## Explore it in the harness {#explore}

The loop is the same everywhere, but in my harness you can watch it from the side: what each turn puts into the context, and which calls a hook saw and how it answered.

::: prompt
/harness-rookie-wondering I have read the chapter "How does an Agent actually work?". Teach me how this harness stands at the four places in the loop: what it puts into the context, which tools it allows, and what its hooks do before and after a call. Open the real files with me and draw how one turn passes through them.
:::
