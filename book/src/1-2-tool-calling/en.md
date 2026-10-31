This chapter assumes only that you know an AI coding agent can read files and run commands.

## In one sentence {#in-one-sentence}

The model only asks for tool calls and a program outside it runs them, and since the model can only work from a tool's name, description and error messages, how well those words are written decides how well the tool gets used.

## For leaders {#for-leaders}

- **The decision:** treat the tools you give an agent as a product, with someone responsible for the descriptions and error messages, and decide which fixed steps become commands rather than lines in a prompt.
- **The risk:** the model can only guess from a tool's name and description, so a vague tool gets used wrongly or not at all. A rule in a prompt is only a request, while a step done by a command can't be skipped, as long as the work goes through that command.
- **The cost of doing it right:** rewriting descriptions and error messages costs very little. Commands are code, and someone has to maintain and test them.
- **Ask the team:** "If you saw only a tool's name and description, would you know when to use it? And what do its error messages say?"

## The model can't touch your files on its own {#problem}

When you watch an agent edit a file, it looks like the model did it, but the model is just a program that reads text and writes text. It can't open a file or run a command by itself. What it can do is write a structured request that amounts to "call the tool `read_file` with the path `src/app.py`", and that's a **tool call**. The program around the model (the first meaning of harness in [What is Harness Engineering?](0-1-the-gap-and-the-map.html)) reads this request, goes and reads the file, and puts the contents back into the conversation as a **tool result**, and the model reads that and decides what to do next. Reading files, searching, editing files, running commands, fetching web pages: anything an agent can ask for this way is called a **tool**.

Two things follow from this. First, every action the agent takes has to go through a call, and calls are carried out outside the model, so the program can check, refuse or change them, and that's what makes it possible to enforce rules on an agent at all. Second, when the model uses a tool, all it has is the tool's name, description and parameter list. It isn't a programmer who has read the docs and can ask a colleague. It's a user guessing from those few lines, so how well they're written directly decides whether the tool gets used well.

### One round trip

::: figure 1-2-tool-call

Take Anthropic's API as an example. When the model wants a tool, its response comes back with `stop_reason` set to `tool_use` and a `tool_use` block that gives the tool name and arguments. Your code runs the tool and sends the result back in a `tool_result` block ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)). Tools that run on your side like this are called client tools, and most of what an agent in your editor does happens this way, on your machine. There's a second kind, **server tools**, such as Anthropic's `web_search`, which run on the provider's side and return the result directly with none of your code in between, so you have no chance to step in before or after they run.

## Where you can step in, and how to write the tools {#how-it-works}

### Where you can step in

With client tools the program sits between the request and the action, which gives you two places to step in. Before a tool runs, the program can allow, refuse or change the call, usually through a hook, and when it refuses, the reason goes back to the agent ([Hooks, the point every call passes through](2-2-hooks.html)). After a tool runs, the program can trim, filter or add to the result before the model reads it. Rules placed here are code that runs, whereas rules in a prompt are only requests ([A rule in a prompt is a request](4-1-requests-and-rules.html)). But a hook can only judge a call the model has already made. Whether the model makes the right call depends on what it sees before the call and what it gets back after, and you write both of those.

### The model has only your words to go on

Someone using a command line can read the docs, ask a colleague and sense when something's off. The model has a tool's name, a description and a parameter list, and that's all. It uses those to decide when to call the tool and guesses the arguments from context, it knows nothing the tool doesn't tell it, it reads everything that comes back as plain text, and however big the result is, that's how much of the context window it takes. So it guesses wrong. Anthropic's docs give the example of `get_weather`, which needs a location: if you ask "What's the weather?" without saying where, Opus is more likely to ask you, while Sonnet might fill in New York by itself ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)).

The flip side is that changing those few lines pays off well. Anthropic says "even small refinements to tool descriptions can yield dramatic improvements", and Claude Sonnet 3.5 got the best score of its time on the SWE-bench Verified evaluation after they made precise changes to the tool descriptions ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)). The five rules below follow the order of a single call.

### 1. Write the description like handover notes for a new hire

Before the call, the description is the only place the model can learn what a tool is for, so it needs to say what the tool does, when to use it and when not to. A vague description gets the tool used wrongly or not at all. Parameter names work the same way: Anthropic's example is to call a parameter `user_id` and not `user`, because `user` could be a name, an email address or an ID. And if two tools look alike, each description should say how it differs from the other.

### 2. Write error messages for the agent to read

When a call fails, the error is the next thing the model reads. A person who sees a stack trace stops to think, but the model takes the text and carries on. If the error just says `Error 400`, it can only guess, and it often guesses the same wrong value again. If the error says what was wrong and what to try next, it can fix the call. The same goes for refusals, which should say what to do instead ([Asking is not a limit](4-2-ask-vs-refuse.html)).

### 3. Keep the output short, and make it pageable

When a call succeeds, the model reads the output. Everything a tool returns goes into the context window ([Context is a budget](3-1-context-budget.html)) and gets read again on every later turn ([Don't pick a model by token price alone](1-1-models-and-cost.html)), so if the agent wants one line and the tool returns a whole large file, you don't just waste tokens, you may also push useful things out of the window. The fix is to put limits on results, such as a default cap, paging, range selection or filters. Claude Code limits tool responses to 25,000 tokens by default, and wherever you set your limit, say so when you cut something off, and tell the agent how to narrow its query. Anthropic has one more idea, a `response_format` parameter that lets the agent choose concise or detailed. In their example the detailed response is 206 tokens and the concise one is 72, about a third ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)).

### 4. Fewer tools mean better choices

More tools have a price. Every tool's name, description and parameters go to the model on every call, so the more tools you have, the more tokens you spend and the more chances the model has to pick the wrong one, especially when they overlap. VS Code also has a hard limit of 128 enabled tools per request, and you can turn off the ones you don't need in the tool picker ([Agent tools](https://code.visualstudio.com/docs/copilot/agents/agent-tools)). So prefer a small set of clearly different tools, and merge what you can. Anthropic's examples are a `search_contacts` tool instead of `list_contacts`, and a single `schedule_event` tool that both finds a free slot and books it. When you do have a lot of tools, giving related ones a shared name prefix also helps the agent tell them apart, though Anthropic says whether a prefix or a suffix works better varies by model, so decide with your own evals ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)).

### 5. Put fixed steps in a command, not a prompt

Of the five, this is the one I most want to stress. Some work has the same steps every time and a clear right and wrong, such as creating a folder for a new task, copying files, computing a hash, writing a record, or checking that everything's ready before writing back. You can put those steps in the instructions and ask the agent to follow them, and most of the time it will, but you can also write them once as a **command**, a small program the agent runs as a tool. The command does the steps itself, checks the preconditions and returns a short result. When the work goes through the command, the agent can't skip a step and can't write a wrong state, because it isn't the one writing the state.

::: figure 1-2-prompt-vs-command

This suits steps that take no judgment. If a step needs the agent to make a decision, leave that part to it and let the command do the fixed work around it. My harness works this way: a command-line tool creates task folders ([Manage tasks, not chats](5-1-tasks.html)), fetches files, computes diffs and tallies checks, and the model just runs the commands and reads the results. Progress is the best example. The task list reads a data file the command writes, not a Markdown note the agent wrote by hand, because hand-written progress misses checkboxes and gets things wrong.

A command's output should ideally say what to do next, so the agent doesn't have to guess. The same command gets read by people in a terminal and by scripts through a pipe, so it can print aligned text in a terminal and JSON on a pipe, with the same fields in both.

A command's weakness is that it only helps when the agent actually uses it, and it only guards what passes through it. If the agent has another way to do the same thing, such as editing the file by hand, the command is a convenience and not a limit ([A rule in a prompt is a request](4-1-requests-and-rules.html)).

### How to check your own tools

For any tool you give an agent, start with three questions. Going by the name and description alone, would you know when to use it and when not to? When it fails, does the message tell the agent what to do next? How big can its output get, and if that's very big, what happens to the context?

The quickest experiment needs no setup. Have the agent call one of your tools in a way you know is wrong, look at what comes back, and ask whether that message would tell you what to do if you were the agent. If it wouldn't, that's the message to rewrite.

If you build your own tools, Anthropic's method is the same idea at a bigger scale: write tasks based on real use, run them, read the raw transcripts (the calls and results, not just the final answer), and change the descriptions and error messages wherever the agent went wrong. They also paste those transcripts into Claude Code and have it improve the tools, and most of the advice in their article came from doing that ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)).

## Good tools have costs, and you can't fully trust the arguments the model picks {#costs-and-traps}

However good a description is, it costs tokens, because it's sent on every call, so write only what the model needs to choose and use the tool, and put the long manual in a file the agent can read when it needs to. A command costs you something else. It's code to maintain, it can break when the project changes, and it breaks in ways a prompt never does, so keep each command small and write tests for it.

You also can't treat a tool call as what the user wants, because the model chose the arguments, and the text it read before choosing could have come from anywhere ([Text the agent reads can give it orders](4-6-untrusted-input.html)). On Anthropic's API, `strict: true` guarantees that a call matches the tool's schema, but that only covers the format, and the values are still the model's choice ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)).

One more practical trap: tool names change between versions, so if your rules or hooks match on tool names, keep that mapping in one place and a rename touches only that place.

## Model providers treat a tool's words as part of the interface too {#industry}
{status: industry}

Two Anthropic sources say the same thing: a tool is an interface, and its words are part of that interface. Their article on writing tools treats tool design as part of the work, and holds that descriptions and error messages are worth testing the way you test code ([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)). The tool use docs say client tools are run by your application, which sends the results back, and warn that the model "might guess values you didn't supply" ([Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)).

## When to delete a command {#when-to-delete-it}
{status: industry}

Commands are the part most likely to go out of date, because a command that checks preconditions is scaffolding built around a weakness of the model. If models become reliable enough at following multi-step instructions, a command may stop being better than a good prompt. Even then, I'd still use commands for anything that has to be exactly the same every time or has to leave a record. Descriptions and error messages are different, and for as long as models read text, that advice holds.

## Try it on your own setup {#try-it}

::: prompt
Find every tool, command or script in this repository that an agent is expected to run (look at agent files, scripts, task runners and instruction files). Judge each one on four things: whether the name and description make clear when to use it and when not to; whether its error messages say what to do next; how large its output can get; and whether a fixed multi-step process described in the instructions should become a command. List the worst three and say how to fix each. Do not change any files.
:::

## Go deeper {#go-deeper}

- Anthropic: [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Anthropic docs: [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- VS Code docs: [Agent tools](https://code.visualstudio.com/docs/copilot/agents/agent-tools)

## Explore it in the harness {#explore}

My harness gives the agent a command-line tool for the steps that have to be exact, and a hook that sits in front of every tool call. The harness can open the real files with you and show you both from the inside.

::: prompt
/harness-rookie-wondering I have read the chapter "When an Agent misuses a tool, check its description and errors first". Teach me what tools this harness gives the agent: the built-in ones, and its own command-line tool. Open the real files with me, show me a refusal and its reason, and draw how one tool call travels.
:::
