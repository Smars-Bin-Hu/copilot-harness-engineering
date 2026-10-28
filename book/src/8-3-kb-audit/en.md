This chapter follows [The toolkit](8-2-kb-toolkit.html). It is step three of the road. The ideas of recall and precision are explained in plain words here; you need no statistics. The method is not tied to code maps: it fits any list a model or a script produces that you can check against a source.

## In one sentence {#in-one-sentence}

No map of code is complete, but you can measure how accurate it is and where it is blind. Take a sample of objects, have an agent read them blind, check every difference at its line, and compare with the map.

## For leaders {#for-leaders}

- **The decision:** require that the map of the code is measured before anyone learns from it, and set the pass bar. I use 0.95, a line I chose and did not derive.
- **The risk:** a map can find the ten uses you knew and still miss a third of the rest, and every note built on it inherits the hole. A pass on a sample of 20 to 40 objects is a floor for starting, not a proof.
- **The cost of doing it right:** an agent reads 20 to 40 sampled objects, once per toolkit change, and a person or script checks every difference at its line.
- **Ask the team:** "How many uses does our map miss or invent, and how was that measured by a reader that never saw the map?"

## The problem {#problem}

You built a map ([the toolkit](8-2-kb-toolkit.html)). The five or ten known uses are all found. Can you trust it?

Not yet. Those known uses prove the toolkit *can* find a use. They say nothing about how many it misses, or whether some of what it found is not there. A map that finds the 10 uses you knew and misses a third of the rest looks perfect on that test.

If you learn from a map that misses a third of the uses, every card built on it inherits the hole. So measure first. The audit is the measuring.

## How it works {#how-it-works}

### The idea: ask an independent reader, then compare

The map is one opinion about what the code says. Get a second opinion that does not copy the first. An agent reads the code of some objects and writes down every use it sees. Then we compare the two lists.

For that second opinion to be worth anything, it must be **blind**. The agent writes down every use it finds *before* it looks at the map. A reading made after looking at the map copies the map. The two lists then agree because one was copied from the other, and the audit measures nothing. The same reasoning is behind an independent reviewer ([a model checking a model](5-6-model-checks-model.html)): the checker must not see the thing it is checking.

### What gets sampled

A script picks the sample: a few objects of each type (for example 5 per type, so about 20 to 40 in all). It hands the agent only the file and line range of each object, not its uses. The sample is picked at random with a **seed** (a number that fixes the random choice), so a second audit with another seed picks different objects.

### Reading blind

For each object the agent reads its lines and writes one record per use: what it uses, which kind of use, and the line number. If an object uses nothing, it writes "none". Two special cases:

- A name built at run time: the agent writes what is fixed and marks it **dynamic**. It is not scored.
- A short name that could mean several objects: the agent writes it in full, with the database or package it resolves to. Otherwise the score cannot tell if the map picked the right one.

### Recall and precision, in plain words

Think of a library with a card catalogue. The shelves are the code. The catalogue is the map.

- **Recall** asks: of the books on the shelves, how many are in the catalogue? Low recall means the map **missed** things.
- **Precision** asks: of the entries in the catalogue, how many are really on the shelves? Low precision means the map **made things up**.

Each is a fraction. An example to show the arithmetic, not a result: suppose the code has 20 uses in the sample, and the map lists 22 entries: 19 of the 20, plus 3 that are not real. Recall is 19 out of 20, which is 0.95. Precision is 19 out of 22, which is about 0.86. The "20" is not known for certain either: it is the blind reader's list after every difference was checked (next section), so these numbers are estimates of the truth.

::: figure 8-3-blind-vs-map

You need both. A map can have perfect recall by listing everything, true or not. It can have perfect precision by listing three safe uses. Only the pair tells you the truth. And they are scored **per type**, because a toolkit can be good at one kind of object and poor at another, and an average hides that.

### The reader can be wrong too

This is the part I want to be plain about. The blind reader is a model. It can misread, miss a use, or invent one. If we scored raw differences, we would blame the map for the reader's mistakes.

So after scoring, **every difference is checked again at its line**:

- **In the map but not in the reader's list.** Look in the file. If the use is there, the reader missed it: add it to the reader's list and write a note. If it is not there, it is a false use in the map.
- **In the reader's list but not in the map.** Look at the line again. If the reader was wrong, correct the list and write a note. If the use is there, it is a real miss of the map.

Then score again. Only what is left counts against the map. The notes about the reader's own mistakes stay in the report. They tell you how far a reading can be trusted, which is itself useful.

### The bar, and what to do with the differences

The bar I use is 0.95 for both recall and precision, in every type. This is a line I chose; I did not derive it. Below it, the audit fails for that type. The line should depend on what a mistake costs: a missed use leaves a card without a relation, a made-up use adds a relation that is not there, and an object on shared data deserves a higher bar. I did not weigh recall and precision differently. With 20 to 40 objects, 0.95 and 0.90 cannot be told apart; the audit shows large gaps, not small ones.

A failure is not bad news. The differences are a list of real examples of what the toolkit gets wrong, each with a file and a line. Look for what they have in common: one form of call, one kind of file. Those are the examples to fix the extractor with. Then audit again with another seed, so you do not tune the toolkit to one lucky sample.

### What no map sees

Some uses are out of reach of any static map, however good:

- SQL built as a string at run time and then executed;
- calls driven by a row in a configuration table;
- a package or class chosen by a variable;
- synonyms and linked servers the toolkit was not taught.

These are marked, not guessed. A name that resolves to something outside the repository is marked **outside**; one that is built at run time is marked **dynamic**. Each becomes an entry in the requests list ([8.5](8-5-kb-keep-true.html)), so that a person can answer it with a read-only query against the real system.

### What the report looks like

The audit ends in one report: the pass or fail, the score per type, every miss and false use with its file and line, the patterns, and the readings that were corrected.

::: code harness .github/skills/generic-kb-toolkit-audit/templates/audit.md L1-L36 "The audit report template: result, score per type, misses, false uses, patterns, corrected readings, what was not counted."

### Test your own setup

1. Take your map. Pick 5 objects of each type at random.
2. In a fresh chat, without showing the map, ask an agent to list every use in each, with line numbers.
3. Compare. Check each difference at its line.
4. Compute recall and precision per type, as above.
5. Repeat with another random sample and see if the numbers move.

## Costs and traps {#costs-and-traps}

- **A sample is a sample.** The audit cannot see types or forms that are not in it. If a rare form matters, take more objects per type, or pick them by hand.
- **The audit reads about 20 to 40 objects.** That is real tokens, spent once per toolkit change.
- **The blind rule is easy to break.** If the agent opens the map "just to check", the audit is spoiled. Hold the line.
- **Passing 0.95 is not safety.** It is a statement about the sample. I treat it as a floor for starting to learn, not as a proof.
- **The reader and the toolkit may share a blind spot.** They are both built by models, so they could miss the same odd form. Checking every difference at its line helps, but cannot catch a use both overlooked. Two cheap ways to reduce it: use a different model or prompt for the reader, and have a person read a few objects by hand as an anchor.

## When to delete it {#when-to-delete-it}

If the map comes from a tool whose accuracy has been measured by someone else, on code like yours, skip the audit. Otherwise rerun it whenever the toolkit changes.

## Go deeper {#go-deeper}

- [The toolkit](8-2-kb-toolkit.html): where the map comes from.
- [Learning in batches](8-4-kb-learning.html): the next step, and where a missed use found later goes back to the toolkit.
- [A model checking a model](5-6-model-checks-model.html): why the second reader must not see the first.

## Explore it in the harness {#explore}

Copilot Harness has an audit that samples, scores per type and lists every difference with its line. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "Is the map right? A blind audit". Teach me topic 16, part 16.3: how the audit samples objects, why the reading must be blind, and how a score is worked out. Open the audit skill with me and walk through one example of checking a difference at its line.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.