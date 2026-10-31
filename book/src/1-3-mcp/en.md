This chapter assumes you know what a tool is. If not, start with [When an Agent misuses a tool, check its description and errors first](1-2-tool-calling.html).

## In one sentence {#in-one-sentence}

MCP is not a new power. It is a standard plug for tools, and it brings other people's code, permissions and text into your agent.

## For leaders {#for-leaders}

- **The decision:** treat every MCP server as a dependency you approve, like a library you did not write, and prefer a plain command when one does the job.
- **The risk:** a server brings in other people's code, their permissions, and text the model will read and obey, and its tool list can change after you approved it. I have not tested whether a hook guards MCP tools the way it guards built-in ones.
- **The cost of doing it right:** a short review per server (who wrote it, what it can touch, where the credentials live), and a re-read of the tool list every so often.
- **Ask the team:** "Which servers are connected, who approved each, and what can each one touch?"

## Why would tools need a standard plug? {#problem}

An agent is only as useful as the tools it has. Sooner or later you will want yours to read your issue tracker, query a database or drive a browser, and someone has to write each of those tools. The trouble is that each platform (VS Code Copilot, Claude Code, Codex) has its own way to accept a tool.

So without a shared standard, the work multiplies. Three platforms and three tools could need nine separate connectors, each of them code that someone must write and then keep up to date. Every new platform adds a row, and every new tool adds a column.

::: figure 1-3-mcp-plug

The **Model Context Protocol (MCP)** is the standard that fixes this. It gives both sides one **protocol**, an agreed way of sending messages, so that two programs written by different people can work together. A tool is then written once, as an **MCP server**, and a platform learns the protocol once. After that, any server works with any platform that speaks MCP. Think of a USB socket: the plug is the standard, and it says nothing about what you plug in.

On the tool's side, an MCP server is a program that offers capabilities to an agent in the standard way, and it can run on your machine or somewhere else. On the other side is the **MCP host**, the AI application, such as VS Code. It makes one **client** for each server it connects to, and that client holds the connection.

Does a standard plug give the agent new powers, then? Usually not. MCP rarely gives an agent a power it could not have otherwise (a remote service with its own sign-in is the exception, since it can offer access you have no other way to get). What it changes is how tools are *plugged in*. If that is all it changes, the question that matters is what comes through the plug along with the tool.

## What you actually plug in {#how-it-works}

### What a server can offer

To see what comes through, start with what a server can send across. The protocol defines three things a server can expose. ([Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)) The one most people mean when they say MCP is **tools**: functions the agent can call to do something, such as file operations, API calls and database queries. They are the same kind of tool as in [When an Agent misuses a tool, check its description and errors first](1-2-tool-calling.html). A server can also offer **resources**, which are data the agent can read for context, such as file contents or database records, and **prompts**, which are reusable templates that help structure a conversation, such as a system prompt or few-shot examples.

Before any of these is used, the agent's side asks the server what it has. For tools that is a `tools/list` request, and what comes back is each tool's name, its description and the parameters it accepts. Later, when the model asks for a call, the host sends a `tools/call` to the right server and puts the answer back into the conversation as text. So from the model's point of view, an MCP tool looks like any other tool.

### Local and remote

A server can run in one of two ways, and the protocol is the same on both. A **local (stdio)** server is one the host starts as a program on your machine. The host talks to it through its standard input and output, the plain text pipes every command line program has. Typically only that one host uses it. A **remote (Streamable HTTP)** server runs somewhere else, and the host talks to it over ordinary web requests (HTTP), usually with sign-in. One remote server can serve many users.

The difference matters for safety. A local server is code that runs on your computer with your rights, while a remote one is someone else's service that you send data to.

### What you take in when you plug one in

Local or remote, though, a server is not a feature you switch on. It is a **dependency**, like a library you did not write, and four things come in with it.

::: figure 1-3-what-comes-in

1. It brings other people's code, because a local server runs on your machine. VS Code's own documentation says: "Local MCP servers can run code on your machine, and tools can access external services using your permissions." ([MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers))
2. It brings other people's permissions. The server acts with whatever access you gave it, such as your database login or your token for the issue tracker, so through the server the agent has that access too.
3. It brings other people's words, and the model treats them as instructions. A server's tool descriptions are text the model reads and takes seriously, and what a tool returns (an issue body, a web page) is text from whoever wrote it. Text the model reads can contain commands for it. [Chapter 4.6](4-6-untrusted-input.html) is about this.
4. It brings a standing cost. Each tool's name, description and parameters are sent to the model on every call, so a server with many tools you rarely use still costs tokens on every turn, and many tools make it harder for the model to choose ([When an Agent misuses a tool, check its description and errors first](1-2-tool-calling.html)). There are ways around it, and I only point to them here. The protocol's own docs mention that clients with many servers can use progressive tool discovery instead of loading every tool up front ([Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)). Anthropic's post [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) names tool definitions overloading the context window as a problem, and describes loading only the tools needed, or having the agent call servers through code. How big the cost is depends on how many tools you connect, so count yours.

### What to check before you add one

If a server is a dependency, it deserves the questions you would ask of any dependency. Here are four, in the order I would ask them.

- Who wrote it, and who keeps it up to date? VS Code's advice is to review "the publisher, command or endpoint, and requested access" before you install or start a server.
- What can it touch? Prefer a server limited to what the job needs. A server for reading issues should not hold a token that can delete repositories.
- Where do the credentials live? Keep them out of the chat and out of your project's commits, as VS Code's docs also warn.
- Can what it returns be trusted? If the text comes from outside, such as the public web or tickets that anyone can file, treat it as untrusted.

### MCP, or just a command?

There is also a question to ask before any of these four: does this tool need a server at all? Many things your agent needs already exist as command-line programs, such as `git`, a test runner or a cloud CLI, and an agent that can run a terminal can use them with no server.

| Reach for | When |
| --- | --- |
| A command line program | It already exists, runs locally, and its output is short and clear. Fewer moving parts |
| An MCP server | You want the same tool across several platforms, or it needs structured inputs, a discoverable list of capabilities, or sign-in to a remote service |

I lean towards the command first, because it adds less code and fewer permissions to your setup. Moving to MCP is worth it once the shared plug starts to pay for the extra dependency.

### Will a hook guard an MCP tool?

You might hope that a hook would catch a bad MCP call the way it catches a bad built-in one. I cannot tell you that it will, because I have **not tested** it. My own harness builds no MCP server, since a company sets them up for its own environment, and some company environments forbid unofficial ones. So I do not know whether MCP tool calls pass through a hook the way built-in tool calls do, nor whether the hook sees their arguments in full. Until you have tested it yourself, with a harmless server, do not count on a hook to guard an MCP tool.

### How to check your own setup

The servers you have already connected deserve a look too. For each one, ask three questions:

1. Do I know who wrote it and what it can touch?
2. Could a command-line program do the same job?
3. How many of its tools do I really use?

The third one you can answer without installing anything. List the tools your agent currently has (most editors show them in the chat's tools picker, though where exactly depends on the editor, so check its docs) and count them. Then ask which of them you used in the last week. The rest are cost and risk without benefit.

## Where more plugs go wrong {#costs-and-traps}

The risk starts with the servers themselves. Each server is a path for outside text and outside code to reach your agent, so every plug you add widens the attack surface. That includes the one you added to try something and then forgot, because it is still there.

A famous name is no reason to skip the review. A server published by a respected company is "official", yet it is still given your credentials and still returns text from other people. Official does not mean safe for you.

Even a server you reviewed carefully can change under you. The protocol lets a server tell the client that its tools changed, so a tool that was fine when you looked at it may not be the one you have next month. A server can also change a tool's description after you approved it, and the description is text the model obeys (this kind of attack is often called a rug pull or tool poisoning, and [chapter 4.6](4-6-untrusted-input.html) covers the idea). Re-read the list now and then, and pin the version of a server where you can.

The last trap is assuming that a shared standard means shared behavior. Platforms differ in which parts of the protocol they support, in how they ask for approval and in where they store the settings, so check the current documentation for yours.

## Do the protocol and VS Code see it this way? {#industry}
{status: industry}

The protocol's own docs describe MCP as a protocol for context exchange, and say it "does not dictate how AI applications use LLMs or manage the provided context". In other words, the host decides what to load and how to ask you. ([Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)) VS Code, one such host, treats servers as code to review: look at the publisher and the access requested, and approve only actions you understand. ([MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers))

So the two agree on how the jobs are split. The protocol makes plugging in easy, and deciding what to plug in is still yours.

## When to delete a server {#when-to-delete-it}
{status: industry}

Deciding what to plug in includes deciding what to unplug. Remove a server when you stop using its tools, or when a plain command does the job. The caution itself can loosen if platforms start to sandbox servers by default, so that a bad one cannot do much harm. Even then, I would check the publisher and the access before adding one.

## Try it on your own setup {#try-it}

::: prompt
Find every MCP server configured for this project or editor (look in the editor and project settings and any MCP config files). For each one, tell me: who publishes it, whether it runs locally or remotely, what credentials it uses and where they are stored, how many tools it exposes, and whether a plain command-line program could do the same job. Flag any credential stored in a committed file. Do not print secret values, and do not change any files.
:::

## Go deeper {#go-deeper}

- Model Context Protocol: [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)
- VS Code docs: [MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- Anthropic: [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

## Explore it in the harness {#explore}

My harness gives the agent three kinds of tools: the built-in ones, its own command line, and optionally MCP. It builds no MCP server itself. The harness can open the real files with you and show you where MCP would plug in and how the other tools are sorted.

::: prompt
/harness-rookie-wondering I have read the chapter "MCP servers: a standard plug for tools". Teach me the three kinds of tools in this harness and where MCP fits. Open the real files with me, and show me how tool names are sorted into kinds.
:::
