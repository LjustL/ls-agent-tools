# Philosophy

Why this framework is shaped the way it is.

## 1. The experience should not depend on the harness or the model

A user should get roughly the same behavior whether they are in Claude Code, Copilot,
Cursor, or anything else, and whether they are on one model or another. If a model is
capable of the ask, the ask should work the same way everywhere.

This is why there is a redirect stub for each major harness pointing at a single
instructions file, rather than a separate set of instructions per tool. It is also why
skills are not registered through any harness-specific mechanism — registration that
only one tool understands makes the behavior available only in that tool.

## 2. The user should not have to know what the agent knows

Skills and instructions should just work. The user should not need to remember which
skills exist, name them, or invoke them explicitly to get their benefit. The agent is
responsible for recognizing when something applies and dispatching it.

This is why skills carry trigger phrases, and why reading instructions, session logs,
and plans **in full** is stated as mandatory rather than encouraged. Both exist so that
the right behavior fires without the user having to ask for it by name.

## 3. Customization belongs to the user, within team limits

An individual should be able to adjust how the agent works for them without changing it
for everyone else. Machine and environment setup, communication preferences, and
outright contradictions of the standing instructions are all legitimate personal
settings.

This is why `agents/personal-context.md` exists and is gitignored, and why it takes
precedence over the primary instructions. It gives you the effect of a personalized
`CLAUDE.md` without imposing it on the rest of the team.

## Who this is written for

These rules assume a team where one or two people drive the agent tooling and everyone
else simply benefits from it. Agent workflow is nobody's primary job here.

That assumption is doing real work in the design. The less the rest of the team has to
think about any of this, the better it is functioning.
