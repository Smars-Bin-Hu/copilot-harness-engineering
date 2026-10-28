This chapter is the first of a case study. It assumes you have read [Context budget](3-1-context-budget.html) and [What an agent should remember](3-5-memory.html), which give the general ideas. It fits a team with a large, old code base. If your code base is small, read it to decide that you do not need this. The most useful part is the small experiment in [Test your own setup](#test): you can run it before you build anything.

## In one sentence {#in-one-sentence}

The code is the truth. A knowledge base is only an index and summary of it, which should be cheaper to read. It does not try to be complete on day one. It tries to be honest: each card says which version of the source file it read, and each gap is written down where the next reader will see it.

## For leaders {#for-leaders}

- **The decision:** whether to fund a knowledge base (a folder of short notes about the code, written for agents), and who will own it. Test first whether searching the code is already enough.
- **The risk:** searching starts to hurt when the code base is large, the same exploration is paid for in every session, or a wrong answer is expensive. I have not measured a knowledge base against plain search, so this is a bet, not a proven win. A base nobody refreshes becomes confidently wrong.
- **The cost of doing it right:** the model reads each object's code once; for a large domain that is real money, and I have not priced it. Someone must own the refresh, and the notes need the same access rules as the code.
- **Ask the team:** "On ten questions we know the answers to, how often does an agent with plain search get it right?"

## The problem {#problem}

Say a team owns a code base with a few thousand objects. An **object** is a named thing in the code that other things use: a stored procedure, a scheduled job, a class, a table. You ask an agent to change one of them. To do it safely, the agent has to know what the object does, who uses it, and what breaks if it changes.

A new agent session starts knowing none of this. The first question is the obvious one.

### Why not just let the agent search the code?

An agent can search. It can run `grep` (find every line that contains a word), open files, and follow names. For many jobs that is the right answer, and it costs nothing to set up. I want to say clearly when it is enough. Searching also does not have to be bare `grep`: a language server (the editor service that answers "where is this defined, who uses it") or a code-search service can help, and a short, good rules page helps too. The knowledge base has to beat that combination, not bare `grep`.

**Searching is enough when:**

- The code base is small, or the part you need fits in one context.
- You know the name of what you are looking for.
- The task is a one-off, so nobody pays for the same exploration twice.

**It starts to hurt when:**

- **The agent decides what to read next from what it just read.** It can miss an object, follow a name that means something else, and stop too early. It cannot tell you how much it missed. Ask it twice and you may get two different answers.
- **The same exploration is paid for in every session.** Every new session starts with an empty context ([context budget](3-1-context-budget.html)), so the agent finds the same things again.
- **Some things are not in the code.** Which environment runs a job, why a rule exists, what failed last year. No search finds them, because they are not written there.
- **A wrong answer is expensive.** If the object touches shared data, a guess from a partial search is not good enough.

A **knowledge base** is a folder of plain text files about the code, written for agents to read. The idea is to pay once for the exploration, keep the result, and read the result first because it should be cheaper than the code. I have not measured that.

**I have not measured it against searching.** I have not run the same questions once with plain search and once with a knowledge base, and I do not know by how much the second one wins, if it does. What I have is the reasoning above, and a way for you to test it on your own code (see [Test your own setup](#test)). Treat the knowledge base as a bet that pays off under the conditions above, not as a proven win.

## How it works {#how-it-works}

### The shape of a knowledge base

A reader goes down only as far as the task needs.

::: figure 8-1-kb-layers

- **The overview** lists the **domains** and has a glossary. A domain is a group of objects that serve one job, such as "orders" or "payroll".
- **The architecture page** of a domain says what the domain is for, its main flows, where to start reading, its traps and its limits.
- **A card** is a short entry about one object: what it is for, its rules, who it uses, its traps. Each rule cites the lines of code it comes from. One file holds the cards of one type. An agent finds a card by walking down: overview, then the domain's page, then the card by its id.
- **The code** is at the bottom. It is the source of truth. If a card and the code disagree, the code wins.

So a card is a promise with a date, not a replacement for the code. An agent that needs more reads the code.

### Scripts do the structure, the model does the meaning

Two kinds of work go into a card, and they are different.

- **Structure** has one right answer: which objects exist, who uses whom (together, the **map** of the code), in what order to learn them, whether a card lists the right relations. A script can compute this. It gives the same answer every time and costs no tokens. A model asked to do it walks the code by judgment, and may miss things.
- **Meaning** has no single answer: what an object is for, what its rule is, which trap catches people. Only a model, reading the code, can write it.

The rest of this part follows from that split. [The toolkit](8-2-kb-toolkit.html) is how scripts draw the map. [The audit](8-3-kb-audit.html) measures that map. [Learning in batches](8-4-kb-learning.html) is where the model writes the meaning, with scripts checking what they can. [Keeping it true](8-5-kb-keep-true.html) is what happens after the code changes.

### Honest, not complete

My guess is that most of a base can come from the code. That is a guess, not a measurement. The rest cannot: what runs in which environment, what failed and why, what someone decided. That part comes over time, from finished tasks, from root-cause reports, from what people export. So the base is never finished on day one, and pretending it is would make it worse, because a base that looks complete gets believed.

Two habits keep it honest:

1. **Every card says which version of its source file it read.** It records a commit (a saved version of the code, named by a short id called a sha). The scripts also keep an **object index**: a list of every object, the source file it lives in, and that file's sha. That is how you can later list the cards the code has moved past. [Chapter 8.5](8-5-kb-keep-true.html) shows how.
2. **Every gap is written down.** What the code cannot tell goes into a **requests list**: one row per thing a person must give, with the kind of thing it is and a read-only way to get it. The agent asks for these at its next stop, never in the middle of work. [Chapter 8.5](8-5-kb-keep-true.html) has the details.

### Every step is a task a person approves

Building the base is not one big prompt. Each step is a task (see [Manage tasks, not chats](5-1-tasks.html)) with a plan the person approves and a write-back the person approves (the write-back copies the finished work into the base; see [Two gates: where a person approves](5-3-two-approvals.html)). Scripts check what can be checked: the form of the files, the relations, the cited lines. And I do not let the agent connect to a live environment. What only an environment can tell, a person runs and hands over.

### The road

1. Build a toolkit, once per code base (8.2).
2. Compute the map, before each use (8.2).
3. Audit the map (8.3).
4. Split the code into domains, once (8.4).
5. Learn each domain in batches (8.4).
6. Write the architecture page (8.4).
7. Keep it true: refresh, capture, requests (8.5).

### Test your own setup {#test}

Before you build anything, find out whether you need it.

1. Write 10 questions about your code whose right answers you know. Mix kinds: "what calls X?", "what happens if Y changes?", "why does Z skip this case?".
2. Ask an agent each question in a fresh chat, with plain search only. Score each answer right or wrong against what you know.
3. Write cards for one small domain by hand or with the agent. Ask the same questions again with the cards available, in fresh chats.
4. Compare: right answers, usage (the token numbers your tool shows for a run), time.

Two cautions. Ask the questions in a form that cannot be answered from one file, such as "what breaks if Y changes?", and let someone who has not read the cards choose them. Ten questions can only show a large difference.

Do each condition several times, not once, because an agent does not do the same thing twice (see [Variance](6-4-variance.html)). If search alone scores about the same, do not build the base.

## Costs and traps {#costs-and-traps}

- **It needs upkeep.** A base nobody refreshes becomes confidently wrong. If your code changes daily and nobody will own the refresh, search is the better choice.
- **A card can be wrong.** It is a model's reading of the code. The checks catch the structure, not whether a rule is understood right. A person's review, or an independent reviewer ([a model checking a model](5-6-model-checks-model.html)), has to cover that.
- **A card can anchor the agent.** An agent that reads a card first may look at less code and keep a wrong card's view. For work where a mistake is expensive, have it re-read the lines a card cites.
- **Reading cards costs tokens too.** A base that is too long only moves the cost. Cards should be short, and the agent should open the lower layers only when it needs them.
- **Building has a price.** The model reads each object's code once. For a large domain that is real money. It is a bet that the reading will be reused. A rough size: every object read once, plus the files that change each month. I have not priced it. Prompt caching (Anthropic's docs say a cached read costs about a tenth of the base price; I have not checked this on Copilot; see [Choosing a model](1-1-models-and-cost.html)) may lower both the building and the reading, so test with it on, as you would really run.
- **Someone must own it, and the cards need the same access rules as the code.** A card is a summary of internal code. Decide who refreshes it and who may read it, the same way you do for the code.

## When to delete it {#when-to-delete-it}

If your own test shows that search alone gives the same answers at the same cost, delete the cards and keep only the requests list, because that is the part search can never give. And if the platform one day builds and refreshes a code index that you can measure as accurate, use it instead of keeping your own.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Judge whether this repository would gain from a written knowledge base of the code, or whether search is enough. Estimate how many objects it has (modules, jobs, tables, services) and how large the code base is. Name the kinds of facts that are not in the code at all, such as which environment runs a job or why a rule exists. Say how often the code changes. Then give a verdict: search is enough, or a base is worth testing, with the reasons. Do not change any files.
:::

## Go deeper {#go-deeper}

- [Context budget](3-1-context-budget.html): why reading less matters, and the search-or-map choice in general.
- [What an agent should remember](3-5-memory.html): memory in general; a knowledge base is one kind.
- [The toolkit](8-2-kb-toolkit.html), the first step of the road.

## Explore it in the harness {#explore}

Copilot Harness builds a knowledge base from code with the road above. It can teach you how from the inside, with the real files and commands. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "A knowledge base: an honest index of the code". Teach me topic 16, the knowledge base from code. Open the real skills and files with me, show me the road step by step, and draw how the pieces fit together.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
