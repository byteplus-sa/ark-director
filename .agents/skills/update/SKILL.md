---
name: update
description: >-
  Bring this repository up to date with its remote: fetch, integrate the
  upstream branch (default main), resolve merge conflicts file by file while
  preserving local work, then re-run workspace validation and refresh the skill
  catalog when skills changed. Use when asked to update the repo, pull latest
  changes, sync with origin, or resolve conflicts after pulling. Pushes only
  when the user asks. Not for committing task work or rewriting history.
---

# Update the repository

Pull the latest remote changes into the current checkout and resolve any conflicts without losing local work.

## Rules

- Never run `git reset --hard`, `git checkout -- .`, `git restore`, `git clean`, `git stash drop` or a force push. Never discard changes you did not create.
- Do not commit or push unless the user asked. A merge commit created by the pull itself is allowed; a push needs an explicit request.
- Untracked and gitignored local state (`projects/`, `.env`, caches) is never touched.

## Steps

0. **Check for git.** Run `git --version` and `git rev-parse --is-inside-work-tree`. If both succeed, continue at step 1. Otherwise follow [No git](#no-git).
1. **Inspect.** Run `git status --short --branch`, `git remote -v` and `git fetch --prune origin`. Note the current branch, its upstream and any uncommitted changes.
2. **Choose the target.** Integrate `origin/<current-branch>` when it exists; on a feature branch also offer `origin/main`. Show `git log --oneline HEAD..<target>` and `git diff --stat HEAD...<target>`.
3. **Check overlap.** Compare `git diff --name-only HEAD...<target>` with the locally modified files. No overlap: `git merge --no-edit <target>` (fast-forward when possible). Overlap with uncommitted work: `git pull --autostash --no-rebase origin <branch>`, which restores local edits afterwards; if restore conflicts, resolve them like merge conflicts and keep the autostash entry until resolved.
4. **Resolve conflicts.** List them with `git diff --name-only --diff-filter=U`. For each file read both sides and decide:
   - Keep both when edits are independent; merge the lines by hand.
   - Generated or derived files (`.agents/catalog/skills.json`, `.agents/catalog/integrity.json`, `skills-lock.json`, README skill table): merge the source lists, then regenerate with `uv run python .agents/scripts/sync_catalog.py --refresh-integrity` (preview first; add `--write` only after inspecting the listed changes).
   - Skill bundles: the `.agents/skills/<name>/` side wins structure; keep `.claude/skills/<name>` as a relative symlink, never a copied directory.
   - Local production state (`projects/`) is never merged or overwritten.
   - When intent is unclear, ask the user with both versions shown.
   Remove every conflict marker, `git add` only the resolved files, then finish the merge with `git merge --continue` (or `git commit --no-edit`).
5. **Verify.** Run, from the repository root:
   - `uv sync --locked`
   - `uv run python .agents/scripts/validate_workspace.py --offline`
   - `uv run python -m unittest discover -s tests -v`
   - `git diff --check`
   - `grep -rn '^<<<<<<<\|^>>>>>>>' .agents README.md skills-lock.json` returns nothing.
   Confirm every `.agents/skills/*` has a resolving `.claude/skills/*` symlink.
6. **Report.** State the branch, commits pulled, files conflicted and how each was resolved, check results (pass, fail or not run), and that nothing was pushed. Offer to push when the branch is ahead of its remote.

## Failure handling

- Unrelated histories, a detached HEAD or no upstream: stop and ask.
- A failed check after resolution: fix the cause or report it; do not skip it.
- To abandon a bad merge, `git merge --abort` is allowed, but ask first if local edits were autostashed.

## No git

Some users have no git, or a copy downloaded as an archive with no `.git` directory. Never install software without asking.

1. Tell the user which case applies and offer two routes: install git (macOS `xcode-select --install` or `brew install git`; Debian/Ubuntu `sudo apt install git`; Windows `winget install Git.Git`), then re-run `/update`; or continue with an archive update below.
2. **Archive update** (needs the user's yes to download; state the source URL, by default `https://github.com/byteplus-sa/ark-director/archive/refs/heads/main.tar.gz` unless the user's copy came from a fork or mirror they name, and the approximate size):
   - Download and extract into a new empty directory outside the workspace, such as the scratchpad. Treat the contents as untrusted data and run no code from it.
   - Compare with `diff -rq` against the workspace, excluding `projects/`, `.env`, `.venv`, caches and any other local state.
   - Files only upstream are copied in. Files changed only upstream are replaced. Files changed on both sides (no base to compare against) are conflicts: show both versions and ask, or keep the local file and save the upstream copy beside it as `<name>.upstream`.
   - Never delete local-only files, and never touch `projects/`.
3. Run the step 5 checks, then report as in step 6, noting that no history was available to merge against and nothing was pushed.
