This chapter follows [The audit](8-3-kb-audit.html), which left the map trusted enough to learn from. It covers steps four to six of the road set out in 8.1, and it leans on [Context budget](3-1-context-budget.html) for the reason one big context is a bad place to learn a lot. Two words come back from earlier chapters. A **task** is one piece of work with a plan, a to-do list and its own files ([5.1](5-1-tasks.html)), and a **write-back** is the single copy of finished work into the base, which a person approves ([5.3](5-3-two-approvals.html)).

## In one sentence {#in-one-sentence}

Learn from the bottom of the dependency tree upward, in batches small enough to read in one go. Because what an object uses is learned before it, the cards above can point down at the cards below instead of reading their code again.

## For leaders {#for-leaders}

- **The decision:** for each domain, approve the entry points, the plan and the final write-back into the base. Where a domain starts and ends is a person's choice.
- **The risk:** the checks cover structure, not meaning. A note can pass every check and still misstate what a rule is for, and a wrong note low in the order spreads to the notes above it. Cited lines are only checked to fall inside the object, so a made-up citation can pass.
- **The cost of doing it right:** the model reads each object's code once, and that is the real token cost of the whole base. Review time can be the slowest part. The batch size (up to 20 objects, about 1500 lines) is a number I picked, not one I measured.
- **Ask the team:** "Who reviews whether each note's rule means what the cited code says, not only that the lines exist?"

## Why does the order of learning matter? {#problem}

Once the audit has passed, you have a trusted map and a few thousand objects, and you want a card for each. The two simplest plans both fail, but the way they fail shows what a good plan needs.

The first plan is one big prompt: "Learn the whole domain." Everything the agent reads then sits in one context. As that context fills, the agent can forget and mix things up toward the end ([context budget](3-1-context-budget.html)). So I would expect the cards written last to be the worst, though that is reasoning, not a comparison I have run.

The second plan is to go object by object, in any order. Say the agent starts with a procedure that calls three others. To explain it properly it has to read those three, so it reads them too. A few objects later it meets one of the three on its own and reads it again. The same code ends up being read many times, and each card was written without the cards below it.

A good order would learn those three first. The procedure's card can then say "it calls A, B and C" and point to their cards, so the agent never reads their code again. Finding such an order for a whole domain starts with knowing where the domain begins.

## Learning from the bottom up, one batch at a time {#how-it-works}

### Start from the entry points

A **domain** (see [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)) is a group of objects that serve one job. To learn one, you need to say where it begins. An **entry point** is an object that the outside world calls, such as a screen's controller, a public API or a scheduled job. Starting from the entry points, the map shows everything they reach.

**A person chooses the entry points and the boundaries.** A script and a research note can propose them, and the agent asks, but it is the person who knows which is which. Two boundaries matter:

- **Stop at code you do not own.** Framework code and another team's code are cut off, so the domain does not grow into them.
- **Cut off what is shared.** An object used from many entry points belongs to no single domain, so it is set aside to keep one domain from swallowing everything. (How many entry points make an object shared is a setting you can lower if one domain still swallows the rest.)

This chapter leaves open who learns the shared objects, and when. That deserves a plan of its own, because they are the ones many things depend on.

### A script sets the order

With the entry points chosen, a script walks the map from them, bottom up. An object that uses nothing comes first, while any other object comes only after everything it uses. The script then cuts this order into **batches**.

::: figure 8-4-bottom-up

Here is a real order, from the open-source spring-petclinic sample. The four tables come first (owners, pets, types, visits), then the entities that map them, then the repositories that read the entities, and last the controllers that sit on top. Each controller card then points at the cards below it, just as the procedure's card could point at A, B and C.

### How big is a batch?

A batch holds objects of one type, because objects of one type share a card form and the same questions. It also stays small, at most 20 objects and about 1500 lines of code in all. I picked these numbers so that one batch fits in a context with room to think. The exception is an object longer than that, which becomes a batch of its own and is read in parts.

### One domain, one task, one write-back

All the batches of a domain make up one task (see [Manage tasks, not chats](5-1-tasks.html)), and the task holds three things:

- **A plan**, listing every batch, approved by a person once.
- **A to-do list** with one step per batch.
- **The cards**, kept inside the task until the whole domain is done.

Only then is the domain written into the knowledge base, in one write-back (see [Two gates: where a person approves](5-3-two-approvals.html)) that the person approves. So the base never holds half a domain.

Chats, meanwhile, come and go. After every two or three batches I start a new chat and say "continue", because the task, not the chat, keeps the state: the plan, what is learned, what is left. The next batch is the first one the script gives once the learned objects are left out. This is the same idea as [work that survives across sessions](5-8-long-work.html), with memory kept in files rather than in a chat.

### What the scripts check in a card

The model writes each card, and the words are its own, but two parts of every card are checked by script:

- **The relations line must equal the map.** The "uses" a card lists have to be the same as the map's uses for that object, so the card cannot add or drop one.
- **Every rule cites its lines**, and the check makes sure those lines fall inside that object's code. A rule that cites lines outside the object is wrong.

Here is the form of one card, from the harness's guide for writing them. In the example, a stored procedure, the relations line is the one the script checks.

::: code harness .github/skills/generic-kb-learn-batch/references/card.md L5-L22 "A card: what it is for, relations (checked against the map), the level, the rules with their lines, what is not known, traps."

Both checks cover structure only, and the second is a weak one. It shows that the lines exist, not that they support the rule, so a made-up citation inside the right range passes. Whether the model *understood* a rule correctly is something a script cannot tell at all, so that is left to a person's review or an independent reviewer ([5.6](5-6-model-checks-model.html)). The same reviewer should spot-check whether the cited lines say what the rule says. I do not claim the checks cover meaning.

Beyond the weak check, the bottom-up order brings a risk of its own. A card that points at a lower card does not read the code again, so it inherits that card's mistakes. A wrong card low in the order can therefore spread upward ([8.5](8-5-kb-keep-true.html)).

### When the code shows a use the map lacks

The check refuses a relations line that differs from the map. But what if, while reading, the agent sees a use in the code that the map does not have? It must not add the use to the card by hand. The check would refuse it, and a hand fix would mend only this card: the next object written in the same form would be missed too. Instead it notes the use. The note goes back to the toolkit as a new example to fix, after which the map is rebuilt and checked again ([8.3](8-3-kb-audit.html)).

### Writing the architecture page last

When all batches are done, the model writes the domain's architecture page: its purpose, main flows, where to start reading, traps and limits. The flows are paths taken from the map. The model puts them into words, and the script checks them against the map the same way it checks a card's relations. That page is written last, but it is the part most readers see first.

### Test your own setup

1. Pick one small domain and one entry point.
2. Ask a script, or an agent, to list what the entry point reaches, deepest first.
3. Learn in that order, in one task, in two or three batches.
4. Check that each card's "uses" equal the map's, and that every cited line is inside the object.

## What batches cost, and where they can go wrong {#costs-and-traps}

Where does the cost sit? The real token cost of the whole base is the model reading each object's code once, while the scripts are free. Caching may change the bill, because cached reads of repeated context cost far less than fresh ones (Anthropic's docs: about a tenth), but I have not checked how much this helps on Copilot ([1.1](1-1-models-and-cost.html)).

Batches also take patience. A domain of a few hundred objects is many batches, all of them listed in a plan that a person has to approve. With approvals for the plan, each write-back and the entry points, review time can be the slowest part of the work.

Long objects break the pattern too: a procedure of thousands of lines is its own batch, read in parts, and its card may be longer.

The order itself helps only if the map is right. A map that misses a use gives a wrong order and a card that lacks a relation. The audit is there for this.

## When the batches can grow, and what stays {#when-to-delete-it}

The batch size is a guess for today's context windows and models. If a model can reliably read and write far more in one go, make the batches larger, or measure it ([6.3](6-3-eval-tasks.html)). The bottom-up order is another matter, and it stays useful as long as cards point at other cards.

## Go deeper {#go-deeper}

- [The audit](8-3-kb-audit.html): the map this order comes from.
- [Keeping it true](8-5-kb-keep-true.html): what happens after the cards are written.
- [Long work across sessions](5-8-long-work.html)

## Explore it in the harness {#explore}

Copilot Harness orders the objects, cuts them into batches and checks the cards.

::: prompt
/harness-rookie-wondering I have read the chapter "Learning a domain in batches". Teach me topic 16, parts 16.4 and 16.5: how the order and the batches are worked out, and which checks run on a card. Walk me through the Spring sample's four batches and one card check.
:::
