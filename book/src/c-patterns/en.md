This appendix is a shelf of small patterns, each set out the same way: the problem in a line, the pattern in a few lines, a real file from my harness to copy from, and the chapter that explains why. Most patterns also end with a **Limit** line, taken from the chapter it links to. Treat the patterns as examples to adapt rather than to paste. The files are the real ones at the pinned tag, so they are longer and more specific than your first version should be, and each one needs checking in your own setup after you copy it. If you do not know where to start, take the safety patterns first (refuse a command, keep approvals for the person), then the ones that save context, and then the ones for long work. The shelf below is not in that order.

## Put the core limits on one page {#core-limits}

**Problem.** The agent guesses paths and commands, or tidies files you changed.

**Pattern.** Keep a short page that is always loaded. Put in it only what the model would get wrong without it, and put it first. Two limits are enough to begin with.

::: code harness AGENTS.md L44-L45 "Two core limits from the shipped rules page: look before you act, and keep the user's own changes."

**Limit.** A page that grows long stops being read, so every line must earn its place.

More in [Instructions and skills](3-3-instructions-and-skills.html) and [A minimal harness](0-2-minimal-harness.html).

## Load rules only for the files they apply to {#rules-by-file}

**Problem.** A rule that matters for one kind of file costs room in every chat.

**Pattern.** Put the rule in an instruction file with an `applyTo` pattern. Then it loads only when the agent works on a matching file and costs nothing the rest of the time.

::: code harness .github/instructions/skills.instructions.md L1-L4 "The header of a file-based instruction: a description and an applyTo pattern."

**Limit.** It is a request to the model, not a rule the platform enforces.

More in [Instructions and skills](3-3-instructions-and-skills.html).

## One hook entry for every moment {#one-hook-entry}

**Problem.** Several hook scripts, each with its own timeout and shell, are hard to keep in step.

**Pattern.** Let the configuration file say only which moments to call, and point every moment at the same program. What to do at each moment is then up to the program. Two details matter here. Give the entry a time limit, and remember that the file is read when the window starts.

::: code harness .github/hooks/harness.json L40-L51 "The entry for the moment before a tool runs: it only names the program and its time limit."

**Limit.** A hook that times out is treated as a pass, so keep it fast.

More in [Hooks](2-2-hooks.html) and [Build the enforcement layer like software](4-4-enforcement-design.html).

## Refuse a dangerous command, with a reason {#refuse-with-reason}

**Problem.** A command whose damage cannot be undone, such as recursive deletion of a root or home folder, should never run.

**Pattern.** Write a pattern for each command, with a `why` sentence beside it. Because the agent reads the reason, say what the command would do. Keep the pattern narrow as well, because every false refusal leaves a task stuck.

::: code harness .harness/policies/gate.json L59-L62 "One real refusal rule: recursive force-delete of the root, home or current folder, with a reason the agent can read."

**Limit.** This is a speed bump, not a boundary, because it stops the common spellings of a command and not every spelling. So anything that must never be touched should not be handed over at all ([Some things you never hand over](4-5-least-privilege.html)).

More in [Asking is not a limit](4-2-ask-vs-refuse.html) and [Hooks](2-2-hooks.html).

## Keep approvals for the person's terminal {#person-only-commands}

**Problem.** If the agent can run the approval command, the approval means nothing.

**Pattern.** In the same hook, refuse every command that grants a right, with a reason that tells the agent to ask the person to run it in their own terminal. To test it, ask the agent to run one.

::: code harness .harness/policies/gate.json L83-L86 "A refusal for the commands only a person may run: approvals, waivers, switching unattended mode on."

**Limit.** It works only while the hook runs and its files are guarded.

More in [Two gates: where a person approves](5-3-two-approvals.html) and [Guard the files that hold the rules](4-3-guardrails.html).

## Mark a skill that only a person may start {#user-only-skill}

**Problem.** A skill that spends money or hands over rights should not start because the model thought it fit.

**Pattern.** Set `disable-model-invocation: true`. In the description, say that the agent must not call it.

::: code harness .github/skills/harness-autorun/SKILL.md L1-L8 "The top of a skill only the user may start: the flag in the header and the sentence in the description."

**Limit.** It limits who starts the skill, not what the skill does once started.

More in [Instructions and skills](3-3-instructions-and-skills.html) and [Unattended: when it must stop](5-7-when-to-stop.html).

## A read-only helper {#read-only-helper}

**Problem.** You want an agent to read a lot without being able to change anything.

**Pattern.** Create a custom agent whose `tools` list has only read and search, and which cannot call other agents. Only the tool list actually limits the helper. The "do not" lines in the body are requests. What the body is for is saying what the helper must hand back.

::: code harness .github/agents/mapper.agent.md L1-L8 "A read-only helper: the tool list is read and search only, and it calls no other agent."

**Limit.** Each helper starts with an empty context, so several helpers cost several times one agent.

More in [Custom agents](2-4-custom-agents.html) and [Use subagents sparingly](2-3-subagents.html).

## Give a helper a brief it can use alone {#helper-brief}

**Problem.** A helper cannot see your conversation, so a vague call gets a vague answer.

**Pattern.** Write down the question, the scope to read and the items to hand back. Add a length limit and ask for a source for every conclusion.

::: code harness .github/skills/generic-mapreduce/templates/brief.md L5-L18 "A brief for a read-only helper: question, scope, what to hand in, length and sources."

More in [Use subagents sparingly](2-3-subagents.html).

## A checker that answers PASS or FAIL {#pass-fail-checker}

**Problem.** A checker that writes essays gives a person nothing to count and a script nothing to read.

**Pattern.** Fix the first line to PASS or FAIL, and make every finding name a file, a line and the rule it breaks. Keep it within a length limit and leave out advice and fixes. Then a script can count the passes and drop any finding that points nowhere.

::: code harness .github/agents/reviewer.agent.md L58-L76 "The fixed output of an independent checker: a verdict line, findings with file and line, a length cap."

**Limit.** A model still makes mistakes as a checker. A false FAIL sends the author after a problem that is not there.

More in [Make a pass count](5-5-counted-checks.html) and [Can a model check a model?](5-6-model-checks-model.html).

## Write the requirement on one page and have the person confirm it {#requirement-page}

**Problem.** The request is vague and shifts, and nobody can say later what was agreed.

**Pattern.** The agent writes one page that says what to do, what not to do and when it is done, along with an honest "not clear yet" list. A line at the top records whether the person confirmed it.

::: code harness .harness/contracts/templates/task/en/REQ.md L1-L42 "The requirement page: what to do, what not to do, done when, not clear yet, and who confirmed it."

More in [The agent writes the requirement, the person confirms it](5-2-requirements.html).

## A handover file for the next session {#handover-file}

**Problem.** A new chat knows nothing about the work done in the old one.

**Pattern.** Keep one short file that a new session reads first, with the status, what is being done, the next step, what to read and what the person decided. Update it before every stop.

::: code harness .harness/contracts/templates/task/en/TASK.md L1-L23 "The handover file of a task: status, doing now, next step, files to read, decisions, open questions."

**Limit.** The agent writes it, so it can be wrong. Check what matters against the source instead of taking it on trust.

More in [Manage tasks, not chats](5-1-tasks.html) and [Long work across sessions](5-8-long-work.html).

## Write down the uses a person knew {#known-uses}

**Problem.** A map of the code that a model or a script produced looks fine, but if it loses something later, you have no way to know.

**Pattern.** Before the extractor exists, a person writes down a few uses they know are there, one per line. From then on, every run of the map must find all of them.

::: code harness .harness/examples/kb-toolkits/spring/facts.jsonl L4-L8 "Five known uses of the Spring sample: one object, the kind of use, the other object."

**Limit.** A short list shows that the map can find a use, not that it finds them all.

More in [The toolkit](8-2-kb-toolkit.html).

## Report an audit the same way every time {#audit-report}

**Problem.** A check of a model's output ends as a paragraph, so two audits cannot be compared.

**Pattern.** Use a fixed report: pass or fail, a score per type, each difference with its file and line, the patterns, and the readings that were corrected.

::: code harness .github/skills/generic-kb-toolkit-audit/templates/audit.md L1-L36 "The audit report template: result, score per type, misses, false uses, patterns, corrected readings."

**Limit.** A small sample shows only large gaps.

More in [Is the map right?](8-3-kb-audit.html).

## Make a stop explain itself {#stop-reason}

**Problem.** When an unattended run stops with "ran into a problem", the person is left to work out what happened.

**Pattern.** Tell the agent when to stop and when not to, and what the reason must contain: which step is stuck, why, and what the person must decide. This does not replace the hook. The hook still judges the stops that facts can show.

::: code harness .github/skills/harness-autorun/references/when-to-stop.md L11-L36 "When to stop by yourself, when not to, and how to write the reason for the person who comes back."

More in [Unattended: when it must stop](5-7-when-to-stop.html).
