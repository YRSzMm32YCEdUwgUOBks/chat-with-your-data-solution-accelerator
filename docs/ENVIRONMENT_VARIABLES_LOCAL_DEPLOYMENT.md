# Environment Variables in Docker‑Compose & Dev Container

> ℹ️ **Info:** This project is currently a stubbed-out framework. The local environment and Autogen load successfully, but core business logic and integrations are not yet implemented. See [LOCAL_DEPLOYMENT.md](./LOCAL_DEPLOYMENT.md) for the latest required environment variables and workflow.

> Primary docs: see [LOCAL_DEPLOYMENT.md](./LOCAL_DEPLOYMENT.md) for full Docker‑Compose profiles, port mappings, and workflow.

---

## Quick Reference: Key Environment Variables for Local Dev

The following variables are typically required for a working local setup.
See [LOCAL_DEPLOYMENT.md](./LOCAL_DEPLOYMENT.md#-environment-variables) for full details and descriptions.

| Variable                        | Example Value                | Service                        | Purpose / Notes                                 |
|----------------------------------|------------------------------|--------------------------------|-------------------------------------------------|
| `POSTGRESQL_PASSWORD`           | `postgres`                   | PostgreSQL (Local)             | Password for local PostgreSQL                   |
| `POSTGRESQL_USER`               | `postgres`                   | PostgreSQL (Local)             | Username for local PostgreSQL                   |
| `POSTGRESQL_DB`                 | `postgres`                   | PostgreSQL (Local)             | Database name for local PostgreSQL              |
| `POSTGRESQL_HOST`               | `localhost`                  | PostgreSQL (Local)             | Host for local PostgreSQL                       |
| `AZURE_BLOB_ACCOUNT_NAME`       | `devstoreaccount1`           | Azurite (Local Blob Storage)   | Azurite blob emulator account name              |
| `AZURE_BLOB_ACCOUNT_KEY`        | *(see .env.sample)*          | Azurite (Local Blob Storage)   | Azurite blob emulator account key               |
| `AZURE_BLOB_CONTAINER_NAME`     | `documents`                  | Azurite (Local Blob Storage)   | Blob container for document storage             |
| `AzureWebJobsStorage`           | *(see .env.sample)*          | Azurite (Local Blob Storage)   | Connection string for Azurite (local only)      |
| `VITE_BACKEND_URL`              | `http://localhost:8088`      | Frontend (Vite)                | Frontend API base URL (local Azure Function)    |
| `AZURE_OPENAI_API_KEY`          | *(your key or blank)*        | Azure OpenAI                   | Only needed if testing OpenAI locally           |
| `AZURE_OPENAI_MODEL_NAME`       | `gpt-4o-mini`                | Azure OpenAI                   | (Optional, defaults to `gpt-4o-mini`)           |
| `AZURE_OPENAI_EMBEDDING_MODEL`  | `text-embedding-3-large`     | Azure OpenAI                   | (Optional, defaults to `text-embedding-3-large`)|
| `CHAT_HISTORY_ENABLED`          | `true`                       | Application                    | Enables chat history in local dev               |

> 💡 **Tip:** Use `.env.sample` as a starting point for your `.env` file.
> Not all variables are required for local development—see the main doc for the minimum set.

---

## 1. Dev Container

    repo-root/.env
       │
       │  (1) devcontainer.json → runArgs ["--env-file","./.env"]
       ▼
    ┌────────────────────────┐
    │ Docker container OS    │
    │ ─────────────────────  │
    │ • all vars from .env   │
    │ • any containerEnv/    │
    │   remoteEnv entries    │
    └────────────────────────┘
       │
       │  (2) you open a terminal / debug in VS Code
       ▼
    ┌────────────────────────┐
    │ func start             │
    │ (Azure Functions Core) │
    │ ─────────────────────  │
    │ • reads FunctionApp/   │
    │   local.settings.json  │
    │ • injects values as    │
    │   process-env vars     │
    └────────────────────────┘

1. VS Code’s Dev Containers extension tells Docker to use your `.env` via `--env-file` (or via `envFile`, `containerEnv`, `remoteEnv`).
2. Inside the container, running `func start` loads `local.settings.json` into the function host’s process environment.

---

## 2. Docker‑Compose

    repo-root/.env
       │
       │  (1) docker-compose.local.yml
       │      env_file: ./.env
       ▼
    ┌────────────────────────┐
    │ Docker container OS    │
    │ (via docker-compose)   │
    │ ─────────────────────  │
    │ • sees vars from .env  │
    │ • sees vars from       │
    │   docker-compose.yml   │
    └────────────────────────┘
       │
       │  (2) services start via profiles:
       │      - frontend
       │      - azure_function
       │      - postgres
       │      - azurite
       ▼
    ┌──────────────────────────────────────────────────────┐
    │ Azure Functions Core Tools                           │
    │ (inside container)                                   │
    │ ──────────────────────────                           │
    │ • relies solely on container env vars                │
    │ • `local.settings.json` is ignored unless mounted    │
    └──────────────────────────────────────────────────────┘

> ⚠️ **Note:** In Docker Compose, `local.settings.json` is **not** used unless you explicitly mount it.
> All configuration should come from environment variables (see [LOCAL_DEPLOYMENT.md](./LOCAL_DEPLOYMENT.md)).

---

## Key Takeaways

- **Dev Container**: `.env` is first-class—every terminal, task, and debug session inside the container sees it automatically.
- **Docker‑Compose**: `.env` → container environment is automatic, but **no** `local.settings.json` unless you explicitly include it.

Use these diagrams to see exactly which file or setting is driving your function’s environment variables—and adjust your `devcontainer.json`, `docker-compose.yml`, or VS Code debug settings accordingly!
