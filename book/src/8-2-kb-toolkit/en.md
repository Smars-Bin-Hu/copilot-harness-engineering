This chapter follows [A knowledge base](8-1-why-a-knowledge-base.html). On the road set out there, it covers the first two steps.

## In one sentence {#in-one-sentence}

Which objects exist and who uses whom is a question with one right answer, so a script computes it, the same way every time and at no token cost. Those scripts are called a toolkit, and the toolkit is code the team owns, written for your own technology stack.

## For leaders {#for-leaders}

- **The decision:** have the team own a small set of scripts that list which objects exist and who uses whom, instead of asking a model to work it out each time.
- **The risk:** a model asked for the map reads by judgment. It can skip an object, and if you ask twice you get two different maps. A script gives the same map every time and says what it could not read. On a small open-source project my sample found 58 objects in 35 files and all 6 known uses, which shows that it runs, not that it works on your code.
- **The cost of doing it right:** the model writes the scripts and a person approves the design, after which the scripts cost no tokens. They are still code, and they have to be maintained when the stack changes. I have not tested a very large code base.
- **Ask the team:** "Who owns the scripts that map our code, and which uses do we already know they must find?"

## Why not let the model draw the map? {#problem}

Before an agent can write a card about an object, someone has to answer two plain questions. Which objects are there? And for each one, what does it use? Here an **object** is a named thing in the code that other things can use (see [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)), and a **use** is one object depending on another, as when a procedure calls another procedure, a class reads a table or a job runs a package. Put all the objects and all the uses together and you have the **map** of the code, the name the previous chapter gave it. If you know the term dependency graph, it is the same thing.

The obvious way to get a map is to ask a model to read the code and produce one, and it would do something reasonable. But it decides what to read next from what it just read, and along that path it can skip an object, follow a name that means two things, or stop early. It cannot say how much it missed either, and if you ask it twice, the two maps differ.

A script that parses every file has none of these problems. It gives the same map every time, for no tokens, and it can say what it could not read. That is the whole case for scripts. But where does the script itself come from?

## How scripts draw the map {#how-it-works}

### What the toolkit is

That depends on your stack, since each stack writes a procedure, a job or a class into a file in its own way. A call is `CALL name` in one stack and a method on an injected object in another, so there is no ready-made parser that covers every convention of your code. Where a language server or a code-search service already gives you objects and uses, use it first (see [When to delete your extractors](#when-to-delete-it)). Only what it does not cover needs scripts of your own.

What you write is the **toolkit**, a small set of programs plus one config file, all kept inside the knowledge base. Each program is an **extractor**, which reads one kind of file and prints the objects it defines and the uses it finds. The **config file** says what an object is in your code and what kinds of use count. It also names the types of object that are **entry points** (the places the outside world calls in, such as a screen, an API or a scheduled job), the folders that are retired, and the words to ignore in names.

A runner applies the extractors to each repository's main branch and saves the map in a cache. That way, on the next run, only the files that changed since the last run are read again.

::: figure 8-2-code-to-map

### Who writes it: the model designs, a person approves, scripts run

You might expect to write the extractors yourself. In my setup the model writes them, in four moves. The first is a survey, in which a script counts the kinds of file in each repository and the model reads a few samples of each kind. With those samples read, the model writes a design that sets down what objects and uses look like in this stack, with examples from the code. A person reads the design and approves it, and this is the moment to catch "that is not a use, that is a comment". Then the model builds the extractors. The last move, the subject of the next section, is to run them until the known uses are found.

The model is good at writing a parser once, but it should not be the parser every time. After the build, only scripts touch the code.

### A test that stays: the uses a person knew

When the map is first made, how do you know it is not nonsense? A person writes down 5 to 10 uses they know are there, for example "procedure A calls procedure B", and these go into a file in the toolkit. It is better to write them before the extractor exists, and not to show them to the model while it writes, so that the extractor is not tuned to just these. Every run of the map must find all of them. If a later change to an extractor loses one, the run fails.

This file of known uses is a regression test, a test that guards what already worked. It is small, and I do not pretend it measures the whole map. What it can do is grow: whenever you meet a use the map missed, add it. Measuring how complete the map is comes later, in [Chapter 8.3](8-3-kb-audit.html).

The known uses are not the only check. On every run the runner reports two more things. One is the files it could not read, or read without finding anything, and either kind is suspicious. The other is the names that are used but defined nowhere. They may be other systems, deleted code, or a form the extractor misreads, so look at a few.

### Two samples, only as examples

The harness ships no toolkit of its own (why, comes after the samples), only two samples that show the shape. One is for SQL Server, with stored procedures, scheduled agent jobs and integration packages. The other is for Spring, covering a Spring Boot service with controllers, repositories, entities and tables.

I built the Spring sample on the open-source spring-petclinic project. On that code it found 58 objects in 35 files and all 6 of the known uses, and no file failed to read or came back empty. That is a smoke test: it shows that the toolkit runs on one small, tidy project, not that it works on yours. The hard cases (SQL built at run time, calls driven by configuration) are not in that project. Your stack, your conventions and your odd cases are what you write.

Here is what that shape looks like in the Spring sample. First come the known uses a person wrote down for it:

::: code harness .harness/examples/kb-toolkits/spring/facts.jsonl L4-L8 "Five of the sample's known uses: one object, the kind of use, the other object."

Then the function that reads one Java file and prints its objects and uses:

::: code harness .harness/examples/kb-toolkits/spring/extract_spring.py L50-L77 "The extractor for a Java file: find the class, its role, and the types it uses."

And last, the sample's own record of how it was built, including the first run that missed one use and what it cannot see:

::: code harness .harness/examples/kb-toolkits/spring/DESIGN.md L22-L30 "Two rounds of fixing the extractor, and the blind spots left."

### Why a general harness does not include a toolkit

I did not ship parsers for the common stacks. A parser that is almost right fails silently, and each team writes code a little differently. A toolkit the team owns and audits ([next chapter](8-3-kb-audit.html)) can instead be fixed when it misses. It also lives in the knowledge base, so upgrading the harness never overwrites it.

### Draw and check a map of one repository

1. Pick one repository and write down 5 to 10 uses you know are there, each with a file and line.
2. Ask an agent to draft what objects and uses look like in your stack, with examples from your code. Read the draft and correct it.
3. Have the agent write the extractors. Run them, and check that all your known uses appear.
4. Run them twice. The two outputs must be identical.

## What owning a toolkit costs, and what it cannot see {#costs-and-traps}

If scripts give the same map every time for no tokens, where is the cost? The plainest one is that the toolkit is code to maintain. When your stack changes, so does it, and that is the price of owning it.

Maintenance keeps the toolkit in step with the stack, but it does not make it read every form correctly. An extractor that handles three ways of writing a call and misses a fourth still looks fine on the known uses. That gap is what the audit is for ([8.3](8-3-kb-audit.html)).

And some things are beyond any reading of forms. A query built as a string at run time, or a call driven by a config table, is invisible to any parser. These are marked, not guessed ([8.3](8-3-kb-audit.html)). All of this comes from a small project. I have not tested the toolkit on a very large code base.

## When to delete your extractors {#when-to-delete-it}

Your own extractors are only one way to get the map. If a tool you trust, such as your language server or a code-search service, already gives you objects and uses with a measured accuracy, feed its output into the map and drop your extractors. The rest of the road does not care where the map came from.

## Try it on your own setup {#try-it}

::: prompt
Scan this repository for the kinds of dependency that a script reading the code cannot see: queries or commands built as text at run time, calls chosen by a variable or a configuration row, and names that resolve to something outside this repository. Give a rough count of each kind, with three example locations (file and line). Say what share of the code looks hard to map by script. Do not change any files.
:::

## Go deeper {#go-deeper}

- [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)
- [The audit](8-3-kb-audit.html): how to measure the map you just made.

## Explore it in the harness {#explore}

Copilot Harness has the commands that survey the code, build the map and run the checks, as well as the two sample toolkits.

::: prompt
/harness-rookie-wondering I have read the chapter "The toolkit: scripts that draw a map of the code". Teach me topic 16, parts 16.1 and 16.2: how the map is built and cached. Open the Spring sample toolkit and its known-uses file with me, and show me what an extractor looks like.
:::
