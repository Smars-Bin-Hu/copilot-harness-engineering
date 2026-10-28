This chapter follows [The audit](8-3-kb-audit.html). The map is now trusted enough to learn from. This is steps four to six of the road. It leans on [Context budget](3-1-context-budget.html) for why one big context is a bad place to learn a lot. Two words from earlier: a **task** is one piece of work with a plan, a to-do list and its own files ([5.1](5-1-tasks.html)); a **write-back** is the single copy of finished work into the base, which a person approves ([5.3](5-3-two-approvals.html)).

## In one sentence {#in-one-sentence}

Learn from the bottom of the dependency tree upward, in batches small enough to read in one go. What an object uses is learned before it, so the cards above can point down at the cards below instead of reading their code again.

## For leaders {#for-leaders}

- **The decision:** approve, for each domain, the entry points, the plan, and the final write-back into the base. A person chooses where a domain starts and ends.
- **The risk:** the checks cover structure, not meaning. A note can pass every check and still misstate what a rule is for, and a wrong note low in the order spreads to the notes above it. Cited lines are checked only to fall inside the object, which a made-up citation can pass.
- **The cost of doing it right:** the model reads each object's code once, which is the real token cost of the whole base. Review time can be the slowest part. The batch size (up to 20 objects, about 1500 lines) is a number I picked, not a measured one.
- **Ask the team:** "Who reviews whether each note's rule means what the cited code says, not only that the lines exist?"

## The problem {#problem}

You have a trusted map and a few thousand objects, and you want a card for each. Two simple plans do not work.

**Plan one: one big prompt.** "Learn the whole domain." One context holds everything the agent reads. As it fills, the agent can forget and mix things up toward the end ([context budget](3-1-context-budget.html)), so I expect the cards written last to be the worst ones. That is reasoning; I have not compared the plans.

**Plan two: object by object, in any order.** Say the agent starts with a procedure that calls three others. To explain it properly, it has to read those three. So it reads them too. A few objects later it meets one of those three on its own and reads it again. The same code is read many times, and each card was written without the cards below it.

A good order would learn the three first. Then the procedure's card can say "it calls A, B and C" and point to their cards. The agent never reads their code again.

## How it works {#how-it-works}

### Start from the entry points

A **domain** (see [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)) is a group of objects that serve one job. To learn one, you need to say where it begins. An **entry point** is an object that the outside world calls: a screen's controller, a public API, a scheduled job. Starting from entry points, the map shows everything they reach.

**A person chooses the entry points and the boundaries.** A script and a research note can propose them, and the agent asks, but it is the person who knows which is which. Two boundaries matter:

- **Stop at code you do not own.** Framework code and another team's code are cut off, so the domain does not grow into them.
- **Cut off what is shared.** An object used from many entry points belongs to no single domain. It is set aside, so that one domain does not swallow everything. (How many entry points make an object shared is a setting you can lower if one domain still swallows the rest.) Who learns the shared objects, and when, is left open in this chapter; they are the ones many things depend on, so it should be planned.

### A script sets the order

A script walks the map from the entry points, bottom up. An object that uses nothing comes first. An object comes only after everything it uses. Then the script cuts this order into **batches**.

::: figure 8-4-bottom-up

Here is a real order, from the open-source spring-petclinic sample. Four tables first (owners, pets, types, visits). Then the entities that map them. Then the repositories that read the entities. Then the controllers that sit on top. Each controller card points at the cards below it.

### How big is a batch

A batch is objects of **one type**, at most **20 objects** and about **1500 lines** of code in all. I picked these numbers so that one batch fits in a context with room to think. An object longer than that is a batch of its own and is read in parts.

One type per batch helps because objects of one type share a card form and the same questions.

### One domain, one task, one write-back

All the batches of a domain are one **task** (see [Manage tasks, not chats](5-1-tasks.html)). The task has:

- **A plan**, listing every batch, approved by a person once.
- **A to-do list** with one step per batch.
- **The cards**, kept inside the task until the whole domain is done.

Then the domain is written into the knowledge base in **one write-back** (the single copy of the finished cards into the base, see [Two gates: where a person approves](5-3-two-approvals.html)), which the person approves. So the base never holds half a domain.

Chats come and go. After every two or three batches I start a new chat and say "continue". The task keeps the state: the plan, what is learned, what is left. The next batch is the first one the script gives once the learned objects are left out. This is the same idea as [work that survives across sessions](5-8-long-work.html): memory in files, not in a chat.

### Checks on what the model writes

The model writes each card. Its words are its own, but two parts are checked by script:

- **The relations line must equal the map.** The "uses" a card lists have to be the same as the map's uses for that object. The card cannot add or drop one.
- **Every rule cites its lines**, and the check makes sure those lines fall inside that object's code. A rule that cites lines outside the object is wrong. This is a weak check: it shows the lines exist, not that they support the rule. A made-up citation inside the right range passes. A person or an independent reviewer should spot-check whether the cited lines say what the rule says.

The flows on the architecture page also come from paths on the map, and are checked in the same way.

Here is the form of one card, from the harness's guide for writing them. The example is a stored procedure; the relations line is the one the script checks.

::: code harness .github/skills/generic-kb-learn-batch/references/card.md L5-L22 "A card: what it is for, relations (checked against the map), the level, the rules with their lines, what is not known, traps."

A card that points at a lower card inherits that card's mistakes, since it does not read the code again. A wrong card low in the order can therefore spread upward ([8.5](8-5-kb-keep-true.html)).

What remains unchecked is whether the model *understood* a rule correctly. A script cannot tell. That is for a person's review, or an independent reviewer ([5.6](5-6-model-checks-model.html)). I do not claim the checks cover meaning.

### When the code shows a use the map lacks

While reading, the agent may see a use in the code that the map does not have. It must not add the use to the card by hand. The check would refuse it, and the next object written in the same form would be missed too. It notes the use, and the note goes back to the toolkit as a new example to fix. Then the map is rebuilt and checked again ([8.3](8-3-kb-audit.html)).

### The last step: the architecture page

When all batches are done, the model writes the domain's architecture page: its purpose, main flows, where to start reading, traps and limits. The flows are paths taken from the map, and the model puts them into words. That page is the part most readers see first.

### Test your own setup

1. Pick one small domain and one entry point.
2. Ask a script, or an agent, to list what the entry point reaches, deepest first.
3. Learn in that order, in one task, in two or three batches.
4. Check that each card's "uses" equal the map's, and that every cited line is inside the object.

## Costs and traps {#costs-and-traps}

- **The model reads each object's code once.** That is the real token cost of the whole base. The scripts are free.
- **Batches take patience.** A domain of a few hundred objects is many batches. The plan lists them all, and a person must approve it. With approvals for the plan, each write-back and the entry points, review time can be the slowest part of the work.
- **Caching may change the bill.** Cached reads of repeated context cost far less than fresh ones (Anthropic's docs: about a tenth). I have not checked how much this helps on Copilot ([1.1](1-1-models-and-cost.html)).
- **A long object breaks the pattern.** A procedure of thousands of lines is its own batch, read in parts. Its card may be longer.
- **Order helps only if the map is right.** A map that misses a use gives a wrong order and a card that lacks a relation. The audit is there for this.
- **Unchecked meaning.** See above. A card can pass every check and still misstate what a rule is for.

## When to delete it {#when-to-delete-it}

The batch size is a guess for today's context windows and models. If a model can reliably read and write far more in one go, make the batches larger, or measure it ([6.3](6-3-eval-tasks.html)). The bottom-up order stays useful as long as cards point at other cards.

## Go deeper {#go-deeper}

- [The audit](8-3-kb-audit.html): the map this order comes from.
- [Keeping it true](8-5-kb-keep-true.html): what happens after the cards are written.
- [Long work across sessions](5-8-long-work.html)

## Explore it in the harness {#explore}

Copilot Harness orders the objects, cuts them into batches and checks the cards. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Learning a domain in batches". Teach me topic 16, parts 16.4 and 16.5: how the order and the batches are worked out, and which checks run on a card. Walk me through the Spring sample's four batches and one card check.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
