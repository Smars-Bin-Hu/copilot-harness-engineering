This chapter follows [The toolkit: scripts that draw a map of the code](8-2-kb-toolkit.html) and is step three of the road. You need no statistics for it, since recall and precision are explained here in plain words. Nor is the method tied to code maps: it fits any list that a model or a script produces and that you can check against a source.

## In one sentence {#in-one-sentence}

No map of code is complete, but you can measure how accurate it is and where it is blind. Take a sample of objects and have an agent read them blind, then compare its reading with the map, and check every difference at its line.

## For leaders {#for-leaders}

- **The decision:** require that the map of the code is measured before anyone learns from it, and set the bar it must pass. I use 0.95, a line I chose rather than derived.
- **The risk:** a map can find the ten uses you knew and still miss a third of the rest, and then every note built on it inherits the hole. Passing on a sample of 20 to 40 objects is a floor for starting, not a proof.
- **The cost of doing it right:** each time the toolkit changes, an agent reads 20 to 40 sampled objects once, and a person or a script checks every difference at its line.
- **Ask the team:** "How many uses does our map miss or invent, and how was that measured by a reader that never saw the map?"

## Can you trust the map yet? {#problem}

Say you have built a map with [the toolkit](8-2-kb-toolkit.html) and it finds all five or ten of the uses you knew about. Can you trust it?

Not yet, because those known uses only prove that the toolkit *can* find a use. They say nothing about how many it misses, or whether some of what it found is not really there. A map that finds the 10 uses you knew and misses a third of the rest looks perfect on that test.

If you then learn from a map that misses a third of the uses, the hole does not stay in the map, because every card built on it inherits it. So measure the map before you learn from it. That measuring is the audit, and its first job is to settle what the map should be measured against.

## Measuring the map with a blind reader {#how-it-works}

### Ask a reader who has not seen the map

The map is one opinion about what the code says, so the thing to measure it against is a second opinion that does not copy the first. An agent reads the code of some objects and writes down every use it sees, after which we compare the two lists.

That second opinion is worth something only if it is **blind**, which means the agent writes down every use it finds *before* it looks at the map. A reading made after looking at the map simply copies it. The two lists then agree only because one was copied from the other, and the audit measures nothing. The same reasoning is behind an independent reviewer ([Can a model check a model?](5-6-model-checks-model.html)): the checker must not see the thing it is checking.

### What gets sampled

Keeping the reader blind starts with the sample. A script, not the agent, picks it: a few objects of each type (for example 5 per type, so about 20 to 40 in all). The script hands the agent only the file and line range of each object, not its uses. The pick is random but made with a **seed** (a number that fixes the random choice), so a second audit with another seed picks different objects.

### Reading blind

For each object, the agent reads its lines and writes one record per use: what it uses, which kind of use it is, and the line number. If an object uses nothing, it writes "none". Two cases need special handling:

- A name built at run time. The agent writes down the part that is fixed and marks the use **dynamic**, and that use is not scored.
- A short name that could mean several objects. The agent writes it in full, with the database or package it resolves to, because otherwise the score cannot tell whether the map picked the right one.

### Recall and precision, in plain words

To score the reader's list against the map, think of a library with a card catalogue. The shelves are the code, and the catalogue is the map.

- **Recall** asks: of the books on the shelves, how many are in the catalogue? Low recall means the map **missed** things.
- **Precision** asks: of the entries in the catalogue, how many are really on the shelves? Low precision means the map **made things up**.

Each is a fraction. Here is an example to show the arithmetic, not a result. Suppose the code in the sample has 20 uses, and the map lists 22 entries: 19 of the 20, plus 3 that are not real. Recall is then 19 out of 20, or 0.95, while precision is 19 out of 22, about 0.86. The "20" itself is not certain either. It is the blind reader's list after every difference has been checked (next section), so these numbers are estimates of the truth.

::: figure 8-3-blind-vs-map

You need both numbers, because either one alone can look perfect. A map can have perfect recall by listing everything, true or not, and perfect precision by listing three safe uses. Only the pair tells you the truth. They are also scored **per type**, since a toolkit can be good at one kind of object and poor at another, and an average hides that.

### The reader can be wrong too

This is the part I want to be plain about. The blind reader is a model, so it can misread, miss a use, or invent one. If we scored the raw differences, we would blame the map for the reader's mistakes.

So after scoring, **every difference is checked again at its line**. What you do next depends on which list the use appears in:

- **In the map but not in the reader's list.** Look in the file. If the use is there, the reader missed it, so add it to the reader's list and write a note. If it is not there, it is a false use in the map.
- **In the reader's list but not in the map.** Look at the line again. If the reader was wrong, correct the list and write a note. If the use is there, the map really missed it.

When you score again, only what is left counts against the map. The notes about the reader's own mistakes stay in the report. They are useful in their own right, because they tell you how far a reading can be trusted.

### The bar, and what to do with the differences

The bar I use is 0.95 for both recall and precision, in every type, and a type that falls below it fails the audit. I chose that line rather than derived it. Where a line like this belongs should depend on what a mistake costs. A missed use leaves a card without a relation, a made-up use adds one that is not there, and an object on shared data deserves a higher bar. Still, I did not weigh recall and precision differently. A finer weighting would not show up anyway, because with only 20 to 40 objects, 0.95 and 0.90 cannot be told apart. The audit shows large gaps, not small ones.

A failure is not bad news, since the differences are a list of real examples of what the toolkit gets wrong, each with a file and a line. Look for what they have in common, such as one form of call or one kind of file. Those are the examples to fix the extractor with. Then audit again with another seed, so that you do not tune the toolkit to one lucky sample.

### What no map sees

Some uses no fix to the extractor will reach, because they are out of reach of any static map, however good:

- SQL built as a string at run time and then executed;
- calls driven by a row in a configuration table;
- a package or class chosen by a variable;
- synonyms and linked servers the toolkit was not taught.

These are marked, not guessed. A name that resolves to something outside the repository is marked **outside**, and one that is built at run time is marked **dynamic**. Each becomes an entry in the requests list ([8.5](8-5-kb-keep-true.html)), so that a person can answer it with a read-only query against the real system.

### What the report looks like

All of this ends in one report: the pass or fail, the score per type, every miss and false use with its file and line, the patterns, and the readings that were corrected.

::: code harness .github/skills/generic-kb-toolkit-audit/templates/audit.md L1-L36 "The audit report template: result, score per type, misses, false uses, patterns, corrected readings, what was not counted."

### Test your own setup

1. Take your map, and pick 5 objects of each type at random.
2. In a fresh chat, without showing the map, ask an agent to list every use in each, with line numbers.
3. Compare the two lists, and check each difference at its line.
4. Compute recall and precision per type, as above.
5. Repeat with another random sample, and see whether the numbers move.

## What the audit costs, and what it cannot promise {#costs-and-traps}

None of this is free. The audit reads about 20 to 40 objects, and those are real tokens, spent again each time the toolkit changes. It also depends on a rule that is easy to break. If the agent opens the map "just to check", the audit is spoiled, so hold the line.

Even a clean audit is only as wide as its sample. It cannot see types or forms that are not in it, so if a rare form matters, take more objects per type, or pick them by hand. For the same reason, passing 0.95 is not safety. It is a statement about the sample, and I treat it as a floor for starting to learn, not as a proof.

The reader and the toolkit may also share a blind spot. Both are built by models, so they could miss the same odd form. Checking every difference at its line helps, but it cannot catch a use that both overlooked. Two cheap ways reduce it: use a different model or prompt for the reader, and have a person read a few objects by hand as an anchor.

Whether you need the audit at all depends on where the map came from.

## When to delete the audit {#when-to-delete-it}

If the map comes from a tool whose accuracy someone else has measured, on code like yours, skip the audit. Otherwise, rerun it whenever the toolkit changes.

## Go deeper {#go-deeper}

- [The toolkit: scripts that draw a map of the code](8-2-kb-toolkit.html): where the map comes from.
- [Learning a domain in batches](8-4-kb-learning.html): the next step, and where a missed use found later goes back to the toolkit.
- [Can a model check a model?](5-6-model-checks-model.html): why the second reader must not see the first.

## Explore it in the harness {#explore}

Copilot Harness has an audit that samples, scores per type and lists every difference with its line.

::: prompt
/harness-rookie-wondering I have read the chapter "Is the map right? A blind audit". Teach me topic 16, part 16.3: how the audit samples objects, why the reading must be blind, and how a score is worked out. Open the audit skill with me and walk through one example of checking a difference at its line.
:::
