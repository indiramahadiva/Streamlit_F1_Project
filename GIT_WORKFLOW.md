# Git Workflow Guide — Development Branch

A practical guide for working with feature branches that flow into `development`, then into `main`.

---

## Branch Structure

```
main               ← stable, production-ready code (only merge tested code here)
  ↑
development        ← integration branch (where features come together)
  ↑
feat/your_feature  ← your personal feature branch (where you do your work)
```

**Rule of thumb:** Never commit directly to `main` or `development`. Always work on a feature branch.

---

## First-Time Setup

Run these commands once when you start a new feature.

```bash
# 1. Switch to development and grab the latest version
git checkout development
git pull origin development

# 2. Create your feature branch from development
git checkout -b feat/your_name_feature
# Examples:
#   feat/indira_pitstops
#   feat/julius_eda
#   feat/maria_dashboard

# 3. Push your new branch to GitHub (the -u sets up tracking)
git push -u origin feat/your_name_feature
```

Naming convention: `feat/yourname_what-it-does`. Lowercase, underscores or dashes, no spaces.

---

## Daily Workflow

### Starting a Work Session

```bash
# 1. Switch to your feature branch
git checkout feat/your_name_feature

# 2. Sync with what teammates merged into development
git fetch origin
git merge origin/development
```

**Why merge `development` in?** While you were away, teammates may have merged their work into `development`. Pulling their changes into your branch *now* (in small doses) prevents huge merge conflicts later when you open your PR.

**When to skip the merge:** If nothing has changed in `development` since your last sync, the merge will just say "Already up to date" — harmless. You can also skip it on solo projects.

### While Working

Commit often as you finish small logical pieces of work.

```bash
# Stage specific files (preferred)
git add src/f1_monza/components/visualizations/pitstops.py

# Or stage everything that's changed
git add .

# Check what's staged before committing
git status

# Commit with a clear message
git commit -m "Add starting tyres donut chart"

# Push to GitHub regularly
git push origin feat/your_name_feature
```

### Push Frequency

**Push often, not just at the end.** Pushing is free and gives you:

- Backup if your laptop dies or files get corrupted
- Visibility for teammates on what you're working on
- A way to share your branch when you need help debugging

A reasonable rhythm: commit when you finish a small logical piece (a function works, a bug is fixed), and push every commit or every few commits.

---

## Writing Good Commit Messages

Keep them short and descriptive. Use the imperative mood ("Add", "Fix", "Update").

**Good:**
- `Add pit stop duration visualization`
- `Fix tyre compound color mapping`
- `Update README with setup instructions`

**Avoid:**
- `stuff`
- `update`
- `fixed it`
- `asdf`

---

## Opening a Pull Request

When your feature is done and ready for review:

```bash
# 1. Sync with development one more time
git fetch origin
git merge origin/development

# 2. Resolve any conflicts (if there are any), then commit and push
git push origin feat/your_name_feature
```

Then on GitHub:

1. Go to your repository
2. Click **"Pull requests"** → **"New pull request"**
3. Set base branch to `development` and compare branch to `feat/your_name_feature`
4. Write a clear title and description of what you built
5. Request review from a teammate
6. Once approved, click **"Merge pull request"**

---

## Promoting Development to Main

Done less frequently (e.g., end of sprint, end of project, before a release).

```bash
# 1. Update both branches locally
git checkout development
git pull origin development

git checkout main
git pull origin main

# 2. Merge development into main
git merge development

# 3. Push the updated main
git push origin main
```

For team projects, prefer a Pull Request from `development` → `main` instead, so the team can review what's about to land in production.

---

## Common Scenarios

### "I forgot to switch branches and committed to development"

```bash
# Don't panic. Move your last commit to a new branch:
git branch feat/your_name_feature        # save your work to a new branch
git reset --hard origin/development      # rewind development to match GitHub
git checkout feat/your_name_feature      # switch to your new branch with the work
```

### "I have uncommitted changes but need to switch branches"

```bash
# Option A: Stash them temporarily
git stash
git checkout other-branch
# ...do stuff...
git checkout feat/your_name_feature
git stash pop                             # restore your changes

# Option B: Commit them as a WIP
git add .
git commit -m "WIP: half-finished pitstops feature"
```

### "Merge conflict — what now?"

```bash
# 1. Git will mark conflicting files. Open them and look for:
#    <<<<<<< HEAD
#    your version
#    =======
#    incoming version
#    >>>>>>> branch-name

# 2. Edit the file to keep what you want, remove the markers

# 3. Mark as resolved and continue
git add path/to/conflicted-file.py
git commit                                # finishes the merge
git push origin feat/your_name_feature
```

### "I pushed something I shouldn't have"

```bash
# Undo the last commit but keep the changes locally
git reset --soft HEAD~1

# Force-push the corrected state (use with caution!)
git push --force-with-lease origin feat/your_name_feature
```

⚠️ **Never force-push to `main` or `development`** — only to your own feature branch, and only if no one else is working on it.

---

## Quick Command Reference

| Task | Command |
|---|---|
| See current branch | `git branch` |
| See all branches | `git branch -a` |
| Switch branch | `git checkout branch-name` |
| Create + switch | `git checkout -b new-branch` |
| Check status | `git status` |
| See changes | `git diff` |
| Stage file | `git add file.py` |
| Stage everything | `git add .` |
| Commit | `git commit -m "message"` |
| Push first time | `git push -u origin branch-name` |
| Push subsequent | `git push` |
| Pull latest | `git pull` |
| See history | `git log --oneline` |
| Discard local changes | `git checkout -- file.py` |

---

## Golden Rules

1. **Never work directly on `main` or `development`** — always use a feature branch.
2. **Pull before you push** — keeps you in sync with the team.
3. **Commit small, push often** — easier to undo, easier to review.
4. **Write meaningful commit messages** — your future self will thank you.
5. **Open PRs for code review** — even on small teams, a second set of eyes catches bugs.
6. **Resolve conflicts as they come up** — don't let your branch drift far from `development`.
7. **Communicate with your team** — say in chat when you're about to merge something big.
