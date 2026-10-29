This chapter is the first of a case study and builds on the general ideas in [Context budget](3-1-context-budget.html) and [What an agent should remember](3-5-memory.html). It is written for a team with a large, old code base. If yours is small, read it to decide that you do not need this. Either way, the most useful part is the small experiment in [Find out first whether you need one](#test), because you can run it before you build anything.

## In one sentence {#in-one-sentence}

The code is the truth, and a knowledge base is only an index and summary of it that should be cheaper to read. Rather than trying to be complete on day one, it tries to be honest: each card says which version of the source file it read, and each gap is written down where the next reader will see it.

## For leaders {#for-leaders}

- **The decision:** whether to fund a knowledge base (a folder of short notes about the code, written for agents), and who will own it. Before that, test whether searching the code is already enough.
- **The risk:** searching starts to hurt when the code base is large, when the same exploration is paid for in every session, or when a wrong answer is expensive. I have not measured a knowledge base against plain search, so this is a bet, not a proven win. And a base nobody refreshes becomes confidently wrong.
- **The cost of doing it right:** the model reads each object's code once. For a large domain that is real money, and I have not priced it. Someone must also own the refresh, and the notes need the same access rules as the code.
- **Ask the team:** "On ten questions we know the answers to, how often does an agent with plain search get it right?"

## What does an agent need to know before it changes one object? {#problem}

Say a team owns a code base with a few thousand objects, where an **object** is a named thing in the code that other things use: a stored procedure, a scheduled job, a class, a table. You ask an agent to change one of them. To do it safely, the agent has to know what the object does, who uses it and what breaks if it changes, yet a new agent session starts knowing none of this. The obvious way to fill that gap is to let it search.

### Why not just let the agent search the code?

An agent can search. It can run `grep` (find every line that contains a word), open files and follow names. For many jobs that is the right answer, and it costs nothing to set up. That is why I want to say clearly when it is enough. Searching does not have to mean bare `grep`, either. A language server (the editor service that answers "where is this defined, who uses it") or a code-search service can help, as can a short, good rules page. The knowledge base has to beat that combination, not bare `grep`.

Searching is enough when the code base is small or the part you need fits in one context, when you know the name of what you are looking for, or when the task is a one-off, so nobody pays for the same exploration twice.

Outside those cases, searching starts to hurt, and the first reason lies in how an agent searches. It decides what to read next from what it just read, so it can miss an object, follow a name that means something else, or stop too early. It cannot tell you how much it missed. Ask it twice and you may get two different answers.

A search that goes well still has to be repeated. Every new session starts with an empty context ([context budget](3-1-context-budget.html)), so the agent finds the same things again and pays for the same exploration in every session.

Some things, though, are not in the code at all: which environment runs a job, why a rule exists, what failed last year. No search finds them, because they are not written there.

And some answers are expensive to get wrong. If the object touches shared data, a guess from a partial search is not good enough.

A **knowledge base** works the other way round. It is a folder of plain text files about the code, written for agents to read. The idea is to pay once for the exploration, keep the result, and read the result first, because it should be cheaper than the code.

I say "should" because I have not run the same questions once with plain search and once with a knowledge base, so I do not know by how much the second one wins, if it does. What I have is the reasoning above, plus a way for you to test it on your own code (see [Find out first whether you need one](#test)). Treat the knowledge base as a bet that pays off under the conditions above, not as a proven win.

## How a knowledge base is built to be honest {#how-it-works}

### The shape of a knowledge base

If you do place the bet, what are you building? A knowledge base has layers, and a reader goes down them only as far as the task needs.

::: figure 8-1-kb-layers

At the top, the **overview** lists the **domains** and has a glossary. A domain is a group of objects that serve one job, such as "orders" or "payroll". Each domain has an **architecture page** that says what the domain is for, its main flows, where to start reading, its traps and its limits.

One layer down, a **card** is a short entry about one object: what it is for, its rules, who it uses, its traps. Each rule cites the lines of code it comes from. Cards are grouped by type, one file per type. To find one, an agent walks down: the overview, then the domain's page, then the card by its id.

At the bottom is **the code**, the source of truth, so if a card and the code disagree, the code wins. That makes a card a promise with a date rather than a replacement for the code. When an agent needs more, it reads the code.

### Scripts do the structure, the model does the meaning

Who writes the cards, then? Two kinds of work go into a card, and they are different.

**Structure** has one right answer: which objects exist, who uses whom (together, the **map** of the code), in what order to learn them, whether a card lists the right relations. A script can compute this, giving the same answer every time at no token cost. A model asked to do it walks the code by judgment and may miss things.

**Meaning** is the opposite. It has no single answer: what an object is for, what its rule is, which trap catches people. Only a model, reading the code, can write it.

The rest of this part follows from that split. [The toolkit](8-2-kb-toolkit.html) is how scripts draw the map that [the audit](8-3-kb-audit.html) then measures. [Learning in batches](8-4-kb-learning.html) is where the model writes the meaning, with scripts checking what they can. [Keeping it true](8-5-kb-keep-true.html) is about what happens after the code changes.

### Honest, not complete

How much of a base can come from the code? My guess is most of it, though that is a guess, not a measurement. The rest cannot: what runs in which environment, what failed and why, what someone decided. That part comes over time, from finished tasks, from root-cause reports and from what people export. So the base is never finished on day one, and pretending it is would make it worse, because a base that looks complete gets believed.

Two habits keep it honest. One is that every card says which version of its source file it read. It records a commit (a saved version of the code, named by a short id called a sha). To check that later, the scripts keep an **object index**: a list of every object, the source file it lives in, and that file's sha. That is how you can list the cards the code has moved past.

The other habit is that every gap is written down. What the code cannot tell goes into a **requests list**, with one row per thing a person must give, the kind of thing it is, and a read-only way to get it. The agent asks for these at its next stop, never in the middle of work. The details of both habits are in [Chapter 8.5](8-5-kb-keep-true.html).

### Every step is a task a person approves

Building the base is not one big prompt. Each step is a task (see [Manage tasks, not chats](5-1-tasks.html)) with a plan the person approves and a write-back the person approves, where the write-back copies the finished work into the base (see [Two gates: where a person approves](5-3-two-approvals.html)). Scripts check what can be checked: the form of the files, the relations, the cited lines.

I keep one more limit on every step: the agent never connects to a live environment. When something only an environment can tell is needed, a person runs it and hands the result over.

### The road

Put in order, the steps make a road:

1. Build a toolkit, once per code base (8.2).
2. Compute the map, before each use (8.2).
3. Audit the map (8.3).
4. Split the code into domains, once (8.4).
5. Learn each domain in batches (8.4).
6. Write the architecture page (8.4).
7. Keep it true: refresh, capture, requests (8.5).

### Find out first whether you need one {#test}

Before you set off on that road, a small test can tell you whether you need it.

1. Write 10 questions about your code whose right answers you know. Mix kinds: "what calls X?", "what happens if Y changes?", "why does Z skip this case?".
2. Ask an agent each question in a fresh chat, with plain search only. Score each answer right or wrong against what you know.
3. Write cards for one small domain, by hand or with the agent. Then ask the same questions again in fresh chats, with the cards available.
4. Compare right answers, usage (the token numbers your tool shows for a run) and time.

A few cautions make the test worth trusting. Ask the questions in a form that cannot be answered from one file, such as "what breaks if Y changes?", and let someone who has not read the cards choose them. Because an agent does not do the same thing twice, run each condition several times rather than once (see [Variance](6-4-variance.html)). Ten questions can only show a large difference anyway. If search alone scores about the same, do not build the base.

## What it costs, and how it can go wrong {#costs-and-traps}

Even when the test says build, the base does not stay right by itself. It needs upkeep, because a base nobody refreshes becomes confidently wrong. If your code changes daily and nobody will own the refresh, search is the better choice.

A card that is up to date can still be wrong, since it is a model's reading of the code. The checks catch the structure, not whether a rule is understood right, so a person's review, or an independent reviewer ([a model checking a model](5-6-model-checks-model.html)), has to cover that. And because the agent reads the card first, a card can anchor it: the agent may look at less code and keep a wrong card's view. For work where a mistake is expensive, have it re-read the lines a card cites.

Every card the agent reads costs tokens, so a base that is too long only moves the cost. Cards should be short, and the agent should open the lower layers only when it needs them.

Those are the costs of keeping and using a base. Building one is a separate cost: the model reads each object's code once, so for a large domain that is real money, spent on a bet that the reading will be reused. A rough size is every object read once, plus the files that change each month, though I have not priced it. Prompt caching may lower both the building and the reading. Anthropic's docs say a cached read costs about a tenth of the base price (see [Choosing a model](1-1-models-and-cost.html)), though I have not checked this on Copilot. So test with it on, as you would really run.

Ownership is the last thing to settle. Someone must own the base, and because a card is a summary of internal code, the cards need the same access rules as the code. Decide who refreshes them and who may read them.

## When to delete the cards, and what to keep {#when-to-delete-it}

If your own test shows that search alone gives the same answers at the same cost, delete the cards and keep only the requests list, because that is the part search can never give. And if the platform one day builds and refreshes a code index that you can measure as accurate, use it instead of keeping your own.

## Try it on your own setup {#try-it}

::: prompt
Judge whether this repository would gain from a written knowledge base of the code, or whether search is enough. Estimate how many objects it has (modules, jobs, tables, services) and how large the code base is. Name the kinds of facts that are not in the code at all, such as which environment runs a job or why a rule exists. Say how often the code changes. Then give a verdict: search is enough, or a base is worth testing, with the reasons. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Context budget](3-1-context-budget.html): why reading less matters, and the search-or-map choice in general.
- [What an agent should remember](3-5-memory.html): memory in general; a knowledge base is one kind.
- [The toolkit](8-2-kb-toolkit.html), the first step of the road.

## Explore it in the harness {#explore}

Copilot Harness builds a knowledge base from code along the road above. It can teach you how from the inside, with the real files and commands.

::: prompt
/harness-rookie-wondering I have read the chapter "A knowledge base: an honest index of the code". Teach me topic 16, the knowledge base from code. Open the real skills and files with me, show me the road step by step, and draw how the pieces fit together.
:::
