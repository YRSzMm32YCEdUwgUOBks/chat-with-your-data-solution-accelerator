# 📜 Poetry Workflow Cheat Sheet (with Azure Context)

This repo uses [Poetry](https://python-poetry.org/) for local development — but the Azure Function runtime uses `pip` with `requirements.txt` during deployment. Here's how to navigate both worlds. 💡

---

## 👩‍💻 Local Dev Workflow with Poetry

### ➕ Add a Dependency

```bash
poetry add packagename
```

- Updates `pyproject.toml` and `poetry.lock`
- Installs into Poetry-managed virtualenv

---

### ➖ Remove a Dependency

```bash
poetry remove packagename
```

- Cleans up `pyproject.toml` and `poetry.lock`
- Uninstalls from your virtualenv

---

### 🔄 Sync Lockfile (if editing pyproject manually)

```bash
poetry lock
```

---

### 📦 Install All Dependencies

```bash
poetry install
```

- Uses `poetry.lock` to install exact versions
- Run after cloning repo or switching branches

```bash
poetry install --no-root
```

- Skips installing the current project as a package (handy for notebooks, scripts)

---

## ☁️ Azure / CI Requirements

### 📁 Export to `requirements.txt` (for deployment)

```bash
poetry export -f requirements.txt --without-hashes -o requirements.txt
```

- Azure Functions and containers use this file to install packages via pip
- Run this anytime dependencies change to keep it fresh

> ⚠️ **Always run this after `poetry add` or `poetry remove`**

---

## 🧪 Optional: Validate the Setup

```bash
poetry check
```

- Validates `pyproject.toml` syntax and dependency compatibility

---

## 🧠 Developer Tips

- Run scripts with Poetry like this:

```bash
poetry run python script.py
```

- Enter the virtual environment:

```bash
poetry shell
```

- View info about the active env:

```bash
poetry env info
```

---

## 🔁 TL;DR Update Cycle

```bash
poetry add <package>      # or remove
poetry lock
poetry export -f requirements.txt --without-hashes -o requirements.txt
```

Then test locally with:

```bash
poetry install && poetry run python ...
```

---

🪶 *Keep Poetry and pip worlds in sync — Poetry for dev, `requirements.txt` for deployment.*
