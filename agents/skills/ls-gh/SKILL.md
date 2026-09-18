# Skill: `gh` CLI

**Use when:** any interaction with GitHub — pull requests, issues, comments, reviews,
checks, releases, or the GitHub API. Reach for `gh` rather than the web UI, and rather
than raw `curl` against `api.github.com`.

## Attribution is mandatory

Everything `gh` publishes — PR descriptions, issue bodies, comments, review bodies —
carries the signature described under Attribution in `agents/agent-instructions.md`.
Nothing posts without one. If you are assembling a body from a file, the signature goes
in the file.

## Non-interactive by default

There is no TTY. Any command that would prompt will hang or fail.

- Pass every value as a flag. Never rely on `gh` prompting for a title, body, or
  confirmation.
- Long bodies go through `--body-file`, using `-` to read stdin from a heredoc. Avoid
  quoting long markdown inline in `--body`.
- `gh` respects `GH_PAGER`; set `GH_PAGER=cat` if a command tries to page.
- Do not use `--watch` on `gh pr checks` or `gh run watch` — they block. Poll instead.

## Read structured output, not prose

Parse `--json` with `--jq` rather than scraping human-readable output, which changes
between versions.

```
gh pr view 123 --json number,title,state,headRefName,body
gh pr list --state open --json number,title,author --jq '.[] | "\(.number) \(.title)"'
gh run list --limit 5 --json status,conclusion,displayTitle
```

`gh <command> --json` with no field list prints the available fields — use that instead
of guessing field names.

## Common operations

```
gh auth status                      # confirm auth before assuming a failure is your fault
gh repo view --json nameWithOwner   # confirm which repo you are acting on

gh pr diff 123                      # the diff, for review
gh pr view 123 --comments           # existing discussion before adding to it
gh pr checks 123                    # CI state
gh pr create --title "..." --body-file -
gh pr comment 123 --body-file -
gh issue create --title "..." --body-file -
gh issue comment 123 --body-file -
```

Anything `gh` does not wrap is reachable through `gh api`, which handles auth and
pagination:

```
gh api repos/{owner}/{repo}/pulls/123/files --paginate
```

## Before acting outward

Creating a PR, posting a comment, merging, or closing something is visible to other
people and is not cleanly reversible — a deleted comment was still delivered by email.
Confirm with the user before the first outward action of a session unless they have
already told you to proceed without asking.

Read before writing: check `gh pr view --comments` or the issue thread before adding to
it, so you are not answering something already resolved.
