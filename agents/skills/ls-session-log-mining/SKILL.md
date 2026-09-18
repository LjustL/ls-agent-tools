# Skill: Session Log Mining

**Use when:** asked to mine session logs, or when looking for recurring problems worth
turning into durable guidance. This is periodic maintenance, not per-session work.

Session logs record everything that happened over the life of a branch, including the
wrong turns. That makes them the only place where two things are written down: what
misled you while debugging, and what a review let through that turned out to be a bug.
Mining recovers those without anyone having to remember them.

## What to extract

Three categories, and nothing else:

- **Debugging pitfalls.** Wrong turns, misleading symptoms, false starts, environment
  traps. Record what the symptom looked like, what it was mistaken for, and what
  actually resolved it. The last part is what makes the entry useful later.
- **Review misses.** Something a review passed that later turned out to be wrong.
  Record what the defect was and why the review did not catch it — a check that was
  missing, a check that fired and was skipped, or a class of problem nobody was looking
  for.
- **Remarkable comments.** Statements from the user with durable value beyond the task
  at hand. The bar is high. Most user comments are about the work in front of them and
  do not belong here.

Do not summarize the work itself. "Implemented the parser" is not a finding, and a pass
that returns a narrative of the branch has failed.

## Pass 1: read each log

Mining state lives in the log itself. A mined log carries a marker on its very first
line:

```
[last mined 2026-09-07]
```

Find the logs that need mining:

```
grep -L '^\[last mined' agents/cache/session-*.md   # never mined
head -n 1 agents/cache/session-*.md                 # when each was last mined
```

A log needs mining if it has no marker, or if it has entries dated after the marker.

**Dispatch one subagent per log, and use a cheap model.** This pass is reading and
extraction, not judgment — Haiku-class is the right tier unless the user says
otherwise. Logs are long, there are many of them, and running this pass on a large
model is the reason people stop doing it. Each subagent reads its log in full and
returns findings in the three categories above.

Once a log's findings come back, write the marker: add
`[last mined <yyyy-mm-dd>]` as the first line if it is absent, or update the date in
place if it is already there. Do not add a second marker.

## Pass 2: aggregate

Do this pass yourself, not in a subagent — it is the part that needs judgment, and it
needs all the findings at once.

Compare findings across logs and look for recurrence. A pitfall that appeared once was
a bad day; the same pitfall in three branches is a property of the codebase, and that
distinction is the whole point of the second pass. Group findings that are the same
underlying problem described differently, and note how many logs each came from.

Surface a single occurrence only when it is severe enough to matter on its own, and
label it as a single occurrence when you do.

## Present, do not install

Bring the aggregated results to the user with a proposed destination for each. Do not
create the resource entries or checks yourself — the user decides what is worth
carrying forward.

The destination follows from the category:

- **Recurring debugging pitfalls** become entries in
  [`resources/debugging-pitfalls.md`](../../resources/debugging-pitfalls.md). These are
  facts that save rediscovery; they are knowledge, not enforcement.
- **Recurring review misses** become a new check under
  `agents/skills/ls-review/checks/`, or an addition to an existing one. A review miss that
  keeps happening is exactly the thing a check exists to catch, and putting it in a
  resource instead means relying on someone remembering to look.
- **Remarkable comments** have no fixed home. Propose one and say why.

For each proposal, show the evidence: which logs it came from and what happened in
each. A proposal the user cannot trace back to real incidents is a guess.
