# Pre-commit Formatting & Linting: How to Avoid Staging Pitfalls

## Overview

This repository uses **pre-commit hooks** to enforce code quality and formatting standards before allowing commits. Two key tools are used:

- [`black`](https://black.readthedocs.io/en/stable/) 🎨: An uncompromising Python code formatter.
- [`flake8`](https://flake8.pycqa.org/en/latest/) 🔍: A Python linter for style and programming errors.

You can find the `flake8` configuration in `.flake8`. The `black` configuration is typically managed by pre-commit (see `.pre-commit-config.yaml` if present).

---

## ⚠️ The Issue: Partial Staging and `black`

When you attempt to commit **only part of a file** (using `git add -p` or the VS Code source control UI), but have **unstaged changes** in the same file, the `black` pre-commit hook will reformat the **entire file**. This can cause conflicts because:

- `black` rewrites the whole file, not just the staged changes.
- Pre-commit tries to stash your unstaged changes, run `black`, and then restore your changes.
- If there are conflicts or mismatches, the commit fails and your changes are rolled back.

You may see output like:
```
[WARNING] Unstaged files detected.
black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted code/azure_function/function_app.py
```

---

## 💡 How to Avoid This Problem

**Best Practice:**
Always stage the **entire file** when committing changes to Python files that are auto-formatted by `black`.

### To Stage the Entire File

```sh
git add path/to/your_file.py
```

### To Check What Is Staged vs. Unstaged

```sh
git status
git diff --staged path/to/your_file.py   # Shows staged changes
git diff path/to/your_file.py            # Shows unstaged changes
```

If `git diff path/to/your_file.py` returns nothing, the whole file is staged.

### If You Need to Commit Only Part of a File

1. **Stash your unstaged changes (keep staged changes):**
   ```sh
   git stash -k
   ```
2. **Commit your staged changes:**
   ```sh
   git commit
   ```
3. **Re-apply your stashed changes:**
   ```sh
   git stash pop
   ```

This workflow allows `black` to safely reformat and commit only what you intend, without losing your unstaged work.

---

## 🔧 Where is `black` Configured?

- `black` is usually configured in `.pre-commit-config.yaml` or `pyproject.toml`.
- If you want to adjust `black`'s behavior, check those files or add configuration as needed.

---

## 📝 Summary

- `black` formats the whole file, so always stage the whole file before committing.
- Use `git stash -k` if you need to commit only part of a file.
- Check `.pre-commit-config.yaml` or `pyproject.toml` for `black` settings.

Happy coding! 🚀
