---
triggers: agents/agent-instructions\.md, agents/resources/, CLAUDE\.md, AGENTS\.md, \.github/copilot-instructions\.md
applies-when: Modifying the core instructions or the framework's own structure. Does not apply to typo, grammar, or formatting corrections.
---

# Check: Philosophy Adherence

Read `agents/resources/philosophy.md`. Verify the change against each tenet.

## 1. The experience should not depend on the harness or the model

- Does the change introduce behavior that only works in one harness?
- Does it put instructions somewhere only one tool reads, rather than in
  `agents/agent-instructions.md` behind the shared redirect?
- Does it rely on a registration or configuration mechanism specific to one tool?
- Would a user on a different harness get a materially different result?

An entry point stub that gains content beyond the redirect is a failure of this tenet.

## 2. The user should not have to know what the agent knows

- Does the change require the user to invoke something by name to get its benefit?
- If a skill or resource was added, is it indexed in the corresponding table in
  `agents/agent-instructions.md`? An unindexed file will not be found.
- Does the added entry state *when* it applies clearly enough that an agent can
  recognize the situation without being told?
- Were any "read in full" requirements weakened to "skim" or "as needed"?

## 3. Customization belongs to the user, within team limits

- Is this a personal preference being written into team-level instructions? If it
  describes one person's machine, environment, or communication style, it belongs in
  `agents/personal-context.md` instead.
- Does the change reduce what a personal context file can override?

## Report

For each tenet, state whether it holds and why. If a change trades one tenet against
another, say so explicitly rather than picking a side silently — that tradeoff is the
user's call.
