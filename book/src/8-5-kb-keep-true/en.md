This chapter follows [Learning in batches](8-4-kb-learning.html) and is step seven of the road, a step that never ends. Why notes in general should carry a source and a date is covered in [What an agent should remember](3-5-memory.html), while this chapter shows what that looks like for code.

## In one sentence {#in-one-sentence}

Knowledge goes stale, so each card records the commit it was read at. When the code changes, you can then list the stale cards and fix only the lines that changed.

## For leaders {#for-leaders}

- **The decision:** name an owner for the knowledge base, and agree how often stale notes are refreshed and who may mark a note as checked.
- **The risk:** a base that was true once and is never checked can be worse than none, because people believe it. A stamp that says "checked" is only as good as the check before it. The list of stale notes also misses the callers of a changed object, and I have not tested how often that leaves a note wrong.
- **The cost of doing it right:** each refresh reads only what changed in the code, not the whole file, and works in tasks of at most about 20 notes. Making the list of stale notes costs no reading at all.
- **Ask the team:** "How many of our notes are older than the code they describe, and who is responsible for them?"

## Which cards are still true? {#problem}

Say a team writes good cards in March. By June, a third of the files they came from have been changed. Nobody can say which cards are now wrong, so readers lose trust in all of them and the base is ignored, or worse, its wrong cards are believed.

Two ways of dealing with this both fail. Rewriting everything now and then costs as much as the first build did. Hoping people fix cards when they notice a mistake fails too, because they do not notice.

The fix is to make staleness *visible and cheap*. If a card says exactly which version of the code it read, a script can answer the question "what has moved?". You can try the idea without any tool, by writing down the commit a note was read at and later running `git diff <that commit>..HEAD -- <the file>`. If the diff is empty, the note's source has not changed. For a whole base, though, the version has to be kept somewhere a script can read it.

## Making staleness visible and cheap {#how-it-works}

### The version on the card

So where does the version live? In three places. The first is the **object index**, the list a script builds of every object and its source file. (Commits and shas were covered in [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html).)

- **Every line of the object index** keeps the sha the source file had when the card was written.
- **Every card** carries a mark saying that it was verified against the code and at which commit it was read, so the reader can tell whether the card was checked against code or not.
- **The domain** records, for each repository, the commit it was learned at.

### Listing the stale cards

Because every index line holds a sha, a script can compare it with the file as it is now on the base branch (the main line of the code). A card is **stale** when its source has changed. A card whose source was deleted is listed too.

::: figure 8-5-stale-cards

Only the cards that changed need attention, so a small change in a big code base means a short list. Its length, as a share of all cards, is the number to put on a board. There is one gap to know about, though: the list names the cards whose own source changed, not the cards of their callers (see [What the list misses, and what still needs a person](#costs-and-traps)).

### Refresh: read the diff, not the file

Why not just read the file again? Because the **diff**, exactly what changed in the source since the card was written, is cheaper, and it also points at the lines of the card that may now be wrong.

If the change does not touch what the card says (a comment, formatting, a part the card does not cover), the text stays as it is. When it does touch the card, the agent changes only the lines it touches. After that, it **stamps** the card, recording that the card was checked against the code as it is now. A stamp is a claim, so it belongs only on cards the agent really checked. Stamp a card nobody read, and a wrong card stays hidden until the next change.

A refresh is a task like any other. Its plan lists each card and what is expected to change, a person approves that plan, and then the result is written back ([Two gates: where a person approves](5-3-two-approvals.html)). A task holds at most about 20 cards. If more are stale, do the most used first.

A card whose source is gone needs one more decision. The agent first checks whether the file was renamed, and if so it updates the path. If the file was removed, the agent asks a person whether to drop the card or keep it. A card that is kept is marked "source gone" and its mark becomes *unknown*, so it does not read like checked knowledge.

### What a finished task teaches

A changed source is not the only way a card goes wrong. While doing a task, an agent may find that a card is wrong or missing and note this in the task's log as it works. When the task ends, a separate step (I call it **capture**) picks out what is worth keeping and **drafts** it for a person to approve. Nothing goes into the base by itself. "It will still be true next month" is only a prediction by the model, so the person's approval is the real check.

Capture keeps an item only if all of these hold: a future agent would get it wrong without it, the task holds the evidence (a file and line), it is not already recorded, and it will still be true next month. "Nothing here is worth keeping" is a good answer. The general rules for what to remember are in [What an agent should remember](3-5-memory.html).

### The requests list: what the code cannot tell

Some of the base cannot come from code at all, because it comes from people and from running systems. By my own guess this is a small part, though I have not measured it. So each domain has a **requests list**, with one row for each thing a person must give. A row has:

- a **kind**: *code* (a source that is in no repository), *runtime* (a value from one environment), *history* (something to find in git), or *decision* (a choice someone must make);
- a read-only command or query the person can run as it is;
- a **status**: *open*, *answered* (when, by whom, where it went), or *declined* (and then it is not asked again).

The rows come from the places where the map is blind ([8.3](8-3-kb-audit.html)): dynamic names, outside names and deleted sources. The agent asks at its next stop, never in the middle of work.

Whatever comes back goes into a second file of **environment facts**, one fact per row, such as whether a job is enabled or what a rule table holds. Each row records the environment, the date, the object, the sha of its code that day, and who gave it. When the code moves on, that sha shows the fact was seen against older code. What a person pastes back is still untrusted text, though. It can hold dirty data or even instructions, so treat it as in [Text the agent reads can give it orders](4-6-untrusted-input.html).

### Bringing in a base you already have

If you already have notes about the code, they can be moved into this form. Set each sha to the commit the old notes were written at, not to today. The stale list is then honest from the first day, because what it shows is what changed since the notes were written. The catch is that old notes often do not say which commit they came from, and then you must guess. A wrong guess hides stale cards, so expect this to be harder than it sounds.

### Test your own setup

1. Take three cards and write down the commit each was read at.
2. Change one source file, then list the cards whose source changed.
3. Refresh from the diff only, and count how many lines you read compared with the whole file (`git diff --stat` shows the lines changed; `wc -l` shows the file).
4. Add one row to a requests list, with a kind, a read-only query and a status.

## What the list misses, and what still needs a person {#costs-and-traps}

Because staleness is counted per source file, the list itself has a gap. If object A calls B and only B changes, B's card is listed but A's is not, even though A's card might need a change too if the meaning of the call moved. I have not tested how often this leaves a caller's card wrong. Cards that only point down, without copying the lower card's content, lose less. The map already knows who uses B, so a cheap fix would be to list the callers of every stale card as "may be stale", although I have not built or tested that.

A stamp can lie, because it is only as good as the check before it. So stamp only what you read, decide who may stamp, and keep a record of who did. You can also have an independent reviewer re-read a few stamped cards against the code, as in the audit ([8.3](8-3-kb-audit.html)).

The rest is not a gap in the list but work only a person can do. Someone must own the refresh, because the list shows what is stale and fixes nothing. A declined request is a loss, not a fix. Its row stays visible, so the gap is honest. Capture, too, can fill the base with noise. The four conditions above are there to keep it small.

## When to delete your own comparison {#when-to-delete-it}

If a platform tracks which stored notes are older than the code they describe, use it and drop your own comparison. The habit of recording a version with every fact still applies.

## Try it on your own setup {#try-it}

::: prompt
Find the documents in this repository that describe the code (design notes, READMEs of modules, architecture pages, runbooks). For each, use git history to tell me when it was last changed and how many commits have touched the code it describes since then. Rank them from most to least out of date. Mark any that state no date or commit they were written against. Do not change any files.
:::

## Go deeper {#go-deeper}

- [What an agent should remember](3-5-memory.html): sources, dates and review for notes in general.
- [Learning in batches](8-4-kb-learning.html): where the cards come from.
- [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)

## Explore it in the harness {#explore}

Copilot Harness lists stale cards, refreshes them from the diff, drafts what a task taught, and keeps the requests list.

::: prompt
/harness-rookie-wondering I have read the chapter "Keeping the knowledge base true". Teach me topic 16, part 16.7: how stale cards are found, how a refresh works, and what the requests file looks like. Open the refresh and capture skills with me.
:::
