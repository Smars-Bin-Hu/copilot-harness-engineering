This chapter assumes you know what a tool is. If not, read [Tool calling](1-2-tool-calling.html) first.

## In one sentence {#in-one-sentence}

MCP is not a new power. It is a standard plug for tools, and it brings other people's code, permissions and text into your agent.

## For leaders {#for-leaders}

- **The decision:** treat every MCP server as a dependency you approve, like a library you did not write, and prefer a plain command when one does the job.
- **The risk:** a server brings in other people's code, their permissions, and text the model will read and obey. Its tool list can also change after you approved it. I have not tested whether a hook guards MCP tools like built-in ones.
- **The cost of doing it right:** a short review per server (who wrote it, what it can touch, where the credentials live) and a periodic re-read of the tool list.
- **Ask the team:** "Which servers are connected, who approved each, and what can each one touch?"

## The problem {#problem}

An agent is only as useful as the tools it has. You may want yours to read your issue tracker, query a database, or drive a browser. Someone has to write each of those tools, and each platform (VS Code Copilot, Claude Code, Codex) has its own way to accept a tool.

Without a shared standard the work multiplies. Three platforms and three tools could need nine separate connectors. Each connector is code someone must write and keep up to date, and every new platform or tool adds a row or a column.

::: figure 1-3-mcp-plug

The **Model Context Protocol (MCP)** is the standard that fixes this. A tool is written once as an **MCP server**. A platform learns the protocol once. After that, any server works with any platform that speaks MCP. Think of a USB socket: the plug is the standard, and it says nothing about what you plug in.

### Three words first

- An **MCP server** is a program that offers capabilities to an agent in the standard way. It can run on your machine or elsewhere.
- An **MCP host** is the AI application, such as VS Code. It makes one **client** for each server it connects to. A client holds the connection.
- A **protocol** is an agreed way of sending messages, so two programs written by different people can work together.

This chapter keeps one idea in view. MCP usually does not give the agent a power that it could not have (a remote service with its own sign-in is the exception: it can offer access you have no other way to). It changes how tools are *plugged in*. Everything in the next sections follows from that.

## How it works {#how-it-works}

### What a server can offer

The protocol defines three things a server can expose. ([Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture))

- **Tools:** functions the agent can call to do something: file operations, API calls, database queries. This is the one most people mean by MCP, and it is the same kind of tool as in [chapter 1.2](1-2-tool-calling.html).
- **Resources:** data the agent can read for context, such as file contents or database records.
- **Prompts:** reusable templates that help structure a conversation, such as a system prompt or few-shot examples.

The agent's side first asks the server what it has (for tools, a `tools/list` request), and gets back each tool's name, description and the parameters it accepts. When the model asks for a call, the host sends a `tools/call` to the right server and puts the answer back into the conversation as text. From the model's point of view this looks like any other tool.

### Local and remote

A server can run in two ways.

- **Local (stdio).** The host starts the server as a program on your machine and talks to it through its standard input and output (the plain text pipes every command line program has). Typically one host uses it.
- **Remote (Streamable HTTP).** The server runs somewhere else and the host talks to it over ordinary web requests (HTTP), usually with sign-in. One remote server can serve many users.

The protocol is the same on both. The difference matters for safety: a local server is code that runs on your computer with your rights, while a remote one is someone else's service that you send data to.

### What you take in when you plug one in

This is the point of the chapter. A server is not a feature you switch on; it is a **dependency**, like a library you did not write. Four things come in with it.

::: figure 1-3-what-comes-in

1. **Other people's code.** A local server runs on your machine. VS Code's own documentation says: "Local MCP servers can run code on your machine, and tools can access external services using your permissions." ([MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers))
2. **Other people's permissions.** The server acts with whatever access you gave it: your database login, your token for the issue tracker. The agent now has that access, through the server.
3. **Other people's words, as instructions.** A server's tool descriptions are text the model reads and takes seriously. And what a tool returns (an issue body, a web page) is text from whoever wrote it. Text the model reads can contain commands for it. [Chapter 4.6](4-6-untrusted-input.html) is about this.
4. **A standing cost.** Each tool's name, description and parameters are sent to the model on every call. A server with many tools you rarely use still costs tokens on every turn, and many tools make it harder for the model to choose ([chapter 1.2](1-2-tool-calling.html)). The protocol's own docs mention that clients with many servers can use progressive tool discovery instead of loading every tool up front. ([Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)) Anthropic's post [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) names tool definitions overloading the context window as a problem, and describes loading only the tools needed, or having the agent call servers through code. I only point to them here. The size of the cost depends on how many tools you connect, so count yours.

### What to check before you add one

Four questions, in the order I would ask them.

- **Who wrote it, and who keeps it up to date?** VS Code's advice is to review "the publisher, command or endpoint, and requested access" before you install or start a server.
- **What can it touch?** Prefer a server limited to what the job needs. A server for reading issues should not hold a token that can delete repositories.
- **Where do the credentials live?** Not in the chat and not committed to your project. VS Code warns against pasting credentials into chat or committing them.
- **Can what it returns be trusted?** If the text comes from outside (the public web, tickets that anyone can file), treat it as untrusted.

### MCP, or just a command?

Not every tool needs a server. Many things your agent needs already exist as command-line programs: `git`, a test runner, a cloud CLI. An agent that can run a terminal can use them with no server at all.

| Reach for | When |
| --- | --- |
| A command line program | It already exists, runs locally, and its output is short and clear. Fewer moving parts |
| An MCP server | You want the same tool across several platforms, or it needs structured inputs, a discoverable list of capabilities, or sign-in to a remote service |

I lean towards the command first, because it adds less code and fewer permissions to your setup. Moving to MCP is worth it when the shared plug starts to pay for the extra dependency.

### What I have not tested

Until you have tested it, do not count on a hook to protect you from an MCP tool. My own harness builds no MCP server. A company sets them up for its own environment, and some company environments forbid unofficial ones. I have **not tested** whether MCP tool calls pass through a hook the way built-in tool calls do, nor whether the hook sees their arguments in full. If you rely on a hook to guard MCP tools, test that first, with a harmless server.

### Test your own setup

**Three questions** about every server you have connected:

1. Do I know who wrote it and what it can touch?
2. Could a command-line program do the same job?
3. How many of its tools do I really use?

**A zero-install check.** List the tools your agent currently has (most editors show them in the chat's tools picker; check your editor's docs for where). Count them. Then ask which ones you used in the last week. The rest are cost and risk without benefit.

## Costs and traps {#costs-and-traps}

**More plugs, more attack surface.** Each server is a path for outside text and for outside code to reach your agent. A server you added to try something and forgot is still there.

**"Official" does not mean safe for you.** A server published by a respected company is still given your credentials and still returns text from other people.

**A server's tool list can change.** The protocol lets a server tell the client that its tools changed. A tool that was fine when you reviewed it may not be the one you have next month. A server can also change a tool's description after you approved it, and the description is text the model obeys (this kind of attack is often called a rug pull or tool poisoning; [chapter 4.6](4-6-untrusted-input.html) covers the idea). Re-read the list now and then, and pin the version of a server where you can.

**A shared standard is not shared behavior.** Platforms differ in which parts of the protocol they support, in how they ask for approval, and in where they store the settings. Check the current documentation for yours.

## What the industry says {#industry}
{status: industry}

- **The protocol's own docs** describe MCP as a protocol for context exchange, and say it "does not dictate how AI applications use LLMs or manage the provided context". The host decides what to load and how to ask you. ([Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture))
- **VS Code** treats servers as code to review: look at the publisher and the access requested, and approve only actions you understand. ([MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers))

The two agree on the split of jobs: the protocol makes plugging in easy, and deciding what to plug in is still yours.

## When to delete it {#when-to-delete-it}
{status: industry}

Remove a server when you stop using its tools, or when a plain command does the job. The caution also loosens if a platform starts to sandbox servers by default, so a bad one cannot do much harm. I would still check publisher and access before adding one.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Find every MCP server configured for this project or editor (look in the editor and project settings and any MCP config files). For each one, tell me: who publishes it, whether it runs locally or remotely, what credentials it uses and where they are stored, how many tools it exposes, and whether a plain command-line program could do the same job. Flag any credential stored in a committed file. Do not print secret values, and do not change any files.
:::

## Go deeper {#go-deeper}

- Model Context Protocol: [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)
- VS Code docs: [MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- Anthropic: [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

## Explore it in the harness {#explore}

My harness gives the agent three kinds of tools: the built-in ones, its own command line, and optionally MCP. It builds no MCP server itself. The harness can show you where MCP would plug in and how the other tools are sorted, with the real files. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "MCP servers: a standard plug for tools". Teach me the three kinds of tools in this harness and where MCP fits. Open the real files with me, and show me how tool names are sorted into kinds.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.