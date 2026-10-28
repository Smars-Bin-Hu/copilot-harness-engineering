This chapter follows [A knowledge base](8-1-why-a-knowledge-base.html). It is step one and two of the road.

## In one sentence {#in-one-sentence}

Which objects exist, and who uses whom, has one right answer. So a script computes it, the same way every time, at no token cost. The scripts are called a toolkit, and it is code the team owns, written for your own technology stack.

## For leaders {#for-leaders}

- **The decision:** have the team own a small set of scripts that list which objects exist and who uses whom, instead of asking a model to work it out each time.
- **The risk:** a model asked for the map reads by judgment, can skip an object, and gives two different maps if asked twice. A script gives the same map every time and says what it could not read. On a small open-source project my sample found 58 objects in 35 files and all 6 known uses; that shows it runs, not that it works on your code.
- **The cost of doing it right:** the model writes the scripts and a person approves the design; the scripts then cost no tokens. They are code to maintain when the stack changes. I have not tested a very large code base.
- **Ask the team:** "Who owns the scripts that map our code, and which uses do we already know they must find?"

## The problem {#problem}

Before an agent can write a card about an object, someone has to answer two plain questions. Which objects are there? And for each one, what does it use?

Two words first.

- An **object** is a named thing in the code that other things can use (see [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)).
- A **use** is one object depending on another: a procedure calls another procedure, a class reads a table, a job runs a package.

Together, all the objects and all the uses are the **map** of the code (named in the previous chapter). It is the same thing as a dependency graph, if you know that term.

You could ask a model to produce the map by reading the code. It would do something reasonable. But it decides what to read next from what it just read. It can skip an object, follow a name that means two things, or stop early. It cannot say how much it missed. And ask it twice, and the two maps differ.

A script that parses every file does not have these problems. It gives the same map every time, for no tokens. And it can say what it could not read. That is the whole case for this chapter.

## How it works {#how-it-works}

### What the toolkit is

How a procedure, a job or a class looks inside a file depends on the stack. A call in one stack is `CALL name`, in another it is a method on an injected object. So there is no ready-made parser that covers every convention of your code. Where a language server or a code-search service already gives you objects and uses, use it first (see [When to delete it](#when-to-delete-it)). You write extractors for what they do not cover.

The **toolkit** is a small set of programs plus one config file, all inside the knowledge base:

- An **extractor** reads one kind of file and prints the objects it defines and the uses it finds.
- The **config file** says what an object is in your code, what kinds of use count, which types of object are **entry points** (the places the outside world calls in: a screen, an API, a scheduled job), which folders are retired, and which words to ignore in names.

A runner applies the extractors to each repository's main branch and saves the map in a cache. On the next run, only the files that changed since the last run are read again.

::: figure 8-2-code-to-map

### Who writes it: the model designs, a person approves, scripts run

You might expect to write the extractors yourself. In my setup the model writes them, in four moves:

1. **Survey.** A script counts the kinds of file in each repository. The model reads a few samples of each kind.
2. **Design.** The model writes down what objects and uses look like in this stack, with examples from the code. A person reads it and approves it. This is the moment to catch "that is not a use, that is a comment".
3. **Build.** The model writes the extractors.
4. **Run until the known uses are found.** See the next section.

The model is good at writing a parser once. It should not be the parser every time. After the build, only scripts touch the code.

### A test that stays: the uses a person knew

When the map is first made, how do you know it is not nonsense? A person writes down 5 to 10 uses they know are there, for example "procedure A calls procedure B". These go into a file in the toolkit. It is better to write them before the extractor exists, and not to show them to the model while it writes, so the extractor is not tuned to just these. Every run of the map must find all of them. If a later change to an extractor loses one, the run fails.

It is a regression test: a test that guards what already worked. It is small, and I do not pretend it measures the whole map. Whenever you meet a use the map missed, add it. [Chapter 8.3](8-3-kb-audit.html) measures how complete the map is.

The runner also reports, on every run:

- the files it could not read, and the files it read and found nothing in (both are suspicious);
- the names that are used but defined nowhere: they may be other systems, deleted code, or a form the extractor misreads. Look at a few.

### Two samples, only as examples

The harness ships no toolkit of its own, only two samples that show the shape.

- **SQL Server:** stored procedures, scheduled agent jobs, and integration packages.
- **Spring:** a Spring Boot service, with controllers, repositories, entities and tables.

I built the Spring sample on the open-source spring-petclinic project. On that code it found 58 objects in 35 files, and all 6 of the known uses; no file failed to read and none came back empty. That is a smoke test: it shows the toolkit runs on one small, tidy project. It does not show it works on yours. The hard cases (SQL built at run time, calls driven by configuration) are not in that project. Your stack, your conventions and your odd cases are what you write.

The real files of the Spring sample show the shape. First the known uses a person wrote down for it:

::: code harness .harness/examples/kb-toolkits/spring/facts.jsonl L4-L8 "Five of the sample's known uses: one object, the kind of use, the other object."

Then the function that reads one Java file and prints its objects and uses:

::: code harness .harness/examples/kb-toolkits/spring/extract_spring.py L50-L77 "The extractor for a Java file: find the class, its role, and the types it uses."

And the sample's own record of how it was built, including the first run that missed one use and what it cannot see:

::: code harness .harness/examples/kb-toolkits/spring/DESIGN.md L22-L30 "Two rounds of fixing the extractor, and the blind spots left."

### Why a general harness does not include a toolkit

I did not ship parsers for the common stacks. A parser that is almost right fails silently, and each team writes code a little differently. A toolkit the team owns and audits ([next chapter](8-3-kb-audit.html)) can be fixed when it misses, and it lives in the knowledge base, so upgrading the harness never overwrites it.

### Test your own setup

1. Pick one repository. Write down 5 to 10 uses you know are there, each with a file and line.
2. Ask an agent to draft what objects and uses look like in your stack, with examples from your code. Read it. Correct it.
3. Have the agent write the extractors. Run them, and check that all your known uses appear.
4. Run them twice. The two outputs must be identical.

## Costs and traps {#costs-and-traps}

- **The toolkit is code to maintain.** When your stack changes, so does it. That is the price of owning it.
- **It is only as good as its reading of the forms.** An extractor that handles three ways of writing a call and misses a fourth looks fine on the known uses. That is why we audit ([8.3](8-3-kb-audit.html)).
- **Some things no script can see.** A query built as a string at run time, or a call driven by a config table, is invisible to any parser. These are marked, not guessed ([8.3](8-3-kb-audit.html)).
- **I have not tested the toolkit on a very large code base.** The petclinic run is a small case.

## When to delete it {#when-to-delete-it}

If a tool you trust, such as your language server or a code-search service, already gives you objects and uses with a measured accuracy, feed its output into the map and drop your extractors. The rest of the road does not care where the map came from.

## Try it on your own setup {#try-it}

No harness needed. Open your agent in your own repository and paste:

::: prompt
Scan this repository for the kinds of dependency that a script reading the code cannot see: queries or commands built as text at run time, calls chosen by a variable or a configuration row, and names that resolve to something outside this repository. Give a rough count of each kind, with three example locations (file and line). Say what share of the code looks hard to map by script. Do not change any files.
:::

## Go deeper {#go-deeper}

- [A knowledge base: an honest index of the code](8-1-why-a-knowledge-base.html)
- [The audit](8-3-kb-audit.html): how to measure the map you just made.

## Explore it in the harness {#explore}

Copilot Harness has the commands that survey the code, build the map and run the checks, and the two sample toolkits. After the setup above, type:

::: prompt
/harness-rookie-wondering I have read the chapter "The toolkit: scripts that draw a map of the code". Teach me topic 16, parts 16.1 and 16.2: how the map is built and cached. Open the Spring sample toolkit and its known-uses file with me, and show me what an extractor looks like.
:::

It teaches one small piece at a time, stops to ask if you are following, and opens the files with you.
