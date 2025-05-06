# DEV_CONTAINER_STARTUP_FLOW_AND_ENVIRONMENT_BOOTSTRAP

## 🐳 Dev Container Startup: What Happens & Why

When you open this project in VS Code with a `.devcontainer` folder, the following sequence occurs automatically to create a fully isolated, reproducible dev environment.

---

### 🔁 1. VS Code Starts Remote Server

- VS Code launches a background process inside the container:
  `~/.vscode-server/`
- This allows extensions, the terminal, debugging, and IntelliSense to work like they do on your local machine.

---

### 🔌 2. Required Extensions Are Installed

VS Code reads the `devcontainer.json` and installs extensions such as:

- `ms-python.python` — Python support
- `zeshuaro.vscode-python-poetry` — Poetry UI integration
- `ms-toolsai.jupyter` — Notebook support
- `ms-vscode.azurecli`, `vscode-docker`, etc.

Extensions are installed **inside the container**, even if you already have them locally.

📝 _Tip: Speed this up by listing extensions explicitly in `devcontainer.json` under `"extensions"`._

---

### 🧪 3. `postCreateCommand` Bootstraps Environment

VS Code runs:

```bash
./.devcontainer/setupEnv.sh
```

This script performs structured environment setup:

1. ✅ Logs start and end of setup
2. 📦 Upgrades `pip` to latest (25.x)
3. 🧼 Installs key Python packages:
   - `bs4`, `soupsieve`, `beautifulsoup4`, `typing-extensions`
4. 📦 Installs latest `poetry`
5. ➕ Installs `poetry-plugin-export` for easy `requirements.txt` generation
6. 🔄 Uses `poetry install` to:
   - Install dependencies (if any)
   - Install the current project in editable mode
7. ✅ Ensures venv is located at `/workspace/.venv`
8. 🪝 Installs `pre-commit` to `.git/hooks/pre-commit`

📝 _All packages install using `--user` to avoid write issues in system-wide `site-packages`._

---

### 🐍 4. Python Toolchain Fully Initialized

- Your venv is now active at `/workspace/.venv`
- Poetry manages your Python project from `pyproject.toml`
- You’re ready to run scripts, notebooks, and CLI tools

If the environment ever seems stale, use:

- ⏮️ **Rebuild Container** for full image refresh
- 🔁 **Reopen in Container** to reload VS Code context

---

### ✅ Summary

| Step                          | Purpose                                                  |
|-------------------------------|----------------------------------------------------------|
| VS Code server launch         | Enables editing/debugging inside the container           |
| Extension install             | Makes Python, Docker, Azure tools available in-container |
| `setupEnv.sh` bootstrapping   | Pip upgrade, poetry install, plugin setup, and venv prep |
| Poetry install                | Provides Python project dependency management            |
| `.venv` configured            | Keeps dependencies isolated for tooling compatibility    |

---

## 🔄 DEV CONTAINER COMMAND COMPARISON

| Command                                       | Rebuild Image | Restart Container | Re-run `postCreateCommand` | Resets State | Use When...                                     |
|----------------------------------------------|---------------|-------------------|-----------------------------|--------------|------------------------------------------------|
| 🔁 **Reopen in Container**                    | ❌ No          | ✅ Yes            | ❌ No                        | ❌ No         | You just want to reload VS Code into the container. |
| 🧱 **Rebuild Container**                      | ✅ Yes         | ✅ Yes            | ✅ Yes                       | ✅ Yes        | You updated Dockerfile, devcontainer.json, or dependencies. |
| 🧼 **Rebuild Container Without Cache**        | ✅ Full Rebuild | ✅ Yes            | ✅ Yes                       | ✅ Yes        | You want to force a completely fresh build (e.g., Docker cache issues). |
| 🔌 **Reopen Folder in Container** (initial)   | ✅ Yes         | ✅ Yes            | ✅ Yes                       | ✅ Yes        | The first time you open the folder in a container. |

---

💡 **Tip:**
Rebuilding is slow but clean.
Reopening is fast but limited.
Pick the right one depending on what changed.
