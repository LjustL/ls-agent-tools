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

## Writing for GitHub readers

Follow **Writing for Humans** in `agents/agent-instructions.md`. On top of that:

- If the repo has a PR or issue template, fill it in rather than replacing it.
- Review comments carry one issue each, anchored to the line it is about, and start
  with a Conventional Comments label: `issue (blocking):`, `suggestion:`, `nit:`,
  `question:`.
- When a fix is concrete, propose it as a suggested change (below) rather than
  describing it.
- Posted text is addressed to the reader. Never mention your own tooling, skills, or
  review process in it.

## Suggested changes

Whenever a fix is concrete and confined to contiguous lines in the diff, post it as a
suggested change so the author can accept it with one click. Put **one fix per
comment**. If you bundle fixes, the author cannot accept one and decline another.

A suggestion is a fenced block with the `suggestion` language tag. It replaces the
commented line range exactly, so write whole lines with their original indentation:

````
nit: `len()` is already an int; the cast is redundant.

```suggestion
    count = len(items)
```
````

For a multi-line range, set `start_line` as well as `line`. Both must be lines in the
diff, on the `RIGHT` side for new code.

`gh pr comment` cannot anchor to a line. Post inline comments as a review through the
API instead. Every comment body carries the attribution signature, placed outside the
suggestion block:

```
gh api repos/{owner}/{repo}/pulls/123/reviews --input - <<'EOF'
{
  "event": "COMMENT",
  "body": "No blocking issues; two nits inline.\n\n_(Authored by ...)_",
  "comments": [
    {
      "path": "src/foo.py",
      "line": 42,
      "side": "RIGHT",
      "body": "nit: ...\n\n```suggestion\n    count = len(items)\n```\n\n_(Authored by ...)_"
    }
  ]
}
EOF
```

Omitting `event` leaves the review pending and invisible to the author.

## Before acting outward

Creating a PR, posting a comment, merging, or closing something is visible to other
people and is not cleanly reversible — a deleted comment was still delivered by email.
Confirm with the user before the first outward action of a session unless they have
already told you to proceed without asking.

Read before writing: check `gh pr view --comments` or the issue thread before adding to
it, so you are not answering something already resolved.
