# Local Development (Fast Start)

> ℹ️ **Info:** This project is currently a stubbed-out framework. The local environment and Autogen load successfully, but core business logic and integrations are not yet implemented. This is a foundation for further development, not a production-ready or feature-complete solution.

**Updated: 2025‑05‑04**
This document reflects the latest, fully Dockerized local workflow—before merging with frontend code.
**Note:** All backend and admin functionality now lives in `code/azure_function`, which replaces the legacy `backend` and `admin` services/sites.

---

## Service Overview

| Service         | Port Mapping    | Description                                                    |
|-----------------|----------------|----------------------------------------------------------------|
| frontend        | 8080 → 80      | React UI (Vite, hot reload in Docker)                          |
| azure_function  | 8088 → 80      | Azure Functions API (Python, replaces backend & admin)         |
| postgres        | 5432 → 5432    | PostgreSQL (with pgvector)                                     |
| azurite         | 10000+ → 10000+| Azure Blob/Queue/Table emulator                                |
| migrate         | n/a            | DB migration/init (runs at build time via `migrate` service)   |

---

## 1️⃣ Clone the Repo *Inside WSL*

**Why?**
Cloning inside WSL avoids slow file access between Windows and Linux filesystems.

```bash
git clone https://github.com/YRSzMm32YCEdUwgUOBks/chat-with-your-data-solution-accelerator.git
cd chat-with-your-data-solution-accelerator
cp .env.example .env
# edit .env as needed
```

---

## 2️⃣ Open in VS Code (Dev Container)

- From your WSL terminal, run:
  ```bash
  code .
  ```
- VS Code will prompt: **"Reopen in Container"**.
  If you miss it, open the Command Palette and search for "Reopen in Container".

  ![VS Code "Reopen in Container" prompt](images/cwyd-localdeploy-reopenincontainerprompt.png)

- **First build:** ~10 minutes (downloads images, builds containers).
  **Subsequent builds:** ~2 minutes.

![VSCode Devcontainer startup](images/cwyd-localdeploy-reopenincontainerrun.png)

---

## 3️⃣🚀 Start All Services

This should be done automatically when the devcontainer reopens. If not, or to reinitialize, run from the VS Code terminal (or WSL shell):

```bash
./start.sh
```

Or manually:

```bash
docker compose -f docker-compose.local.yml up -d
```

- This loads your `.env` and starts all services via Docker Compose.
- **To tail all logs in real time (recommended):**
  ```bash
  docker compose -f docker-compose.local.yml logs -f
  ```
  > (Use `docker compose` not `docker-compose` for best compatibility.)

![All local services running and ready for local dev](images/cwyd-localdeploy-running.png)

---

### 🐳 Docker Compose Command Reference

Use this table to understand the effects of common Docker Compose and Docker commands during development:

| Command                                     | Rebuild?     | Recreate Container? | Remove Containers? | Remove Images? | Remove Volumes? | Affects Orphans? | Notes                                             |
| ------------------------------------------- | ------------ | ------------------- | ------------------ | -------------- | --------------- | ---------------- | ------------------------------------------------- |
| `docker restart`                            | ❌            | ✅                   | ❌                  | ❌              | ❌               | ❌                | Fast container bounce                             |
| `docker stop/start`                         | ❌            | ✅                   | ❌                  | ❌              | ❌               | ❌                | Manual restart cycle                              |
| `up -d`                                     | ❌            | Maybe               | ❌                  | ❌              | ❌               | ❌                | Reuses containers/images                          |
| `up -d --build`                             | ✅ (cached)   | Maybe               | ❌                  | ❌              | ❌               | ❌                | Rebuild if needed                                 |
| `up -d --build --force-recreate`            | ✅            | ✅                   | ✅                  | ❌              | ❌               | ❌                | Full clean container setup                        |
| `up -d --build --no-cache --force-recreate` | ✅ (no cache) | ✅                   | ✅                  | ❌              | ❌               | ❌                | Avoids Docker cache                               |
| `down`                                      | ❌            | ✅                   | ✅                  | ❌              | ❌               | ❌                | Stops + removes containers only                   |
| `down --rmi all`                            | ❌            | ✅                   | ✅                  | ✅              | ❌               | ❌                | Also deletes images                               |
| `down --rmi all --volumes`                  | ❌            | ✅                   | ✅                  | ✅              | ✅               | ❌                | Full cleanup                                      |
| `down --remove-orphans`                     | ❌            | ✅                   | ✅                  | ❌              | ❌               | ✅                | ⚠️ Removes orphan containers tied to same project |
| `docker system prune -a`                    | ✅            | ✅                   | ✅                  | ✅              | ✅               | ✅ (indirectly)   | Full system wipe — only for brave souls           |

---

## 4️⃣ Access the Apps

- **Frontend:** [http://localhost:8080/](http://localhost:8080/)
- **Backend/API (replaces admin and backend):** [http://localhost:8088/](http://localhost:8088/)

> The `azure_function` service now handles all backend and admin endpoints.
> There is no longer a separate admin UI or backend Flask service.

---

## 5️⃣ Typical Workflow

- Edit code in:
  - `code/frontend`
  - `code/azure_function` (all API & admin logic)
- Frontend hot reloads automatically in Docker.
- Azure Function restarts on code changes (rebuild container as needed).
- Database and storage persist unless you remove Docker volumes.

---

## 🔬 Advanced: Run Individual Services

_Optional for non-Docker debugging._

**Frontend only:**
```bash
cd code/frontend
npm install
npm run dev
# → http://localhost:5174/
```

**Azure Function only:**
```bash
cd code/azure_function
pip3 install -r requirements.txt
func start --python
# → http://localhost:7071/
```
> Note: When running outside Docker, the Azure Function will be on port 7071 by default.

---

## 🛠️ Troubleshooting

- **Docker not running?** Start Docker Desktop in Windows before launching WSL/VS Code.
- **Dev Container build slow?** Make sure you are in WSL, not Windows filesystem.
- **.env issues?** Copy `.env.example` and fill in as needed.

---

## Reference

- [This fork](https://github.com/YRSzMm32YCEdUwgUOBks/chat-with-your-data-solution-accelerator)
- [Upstream Microsoft repo](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator)

---

## ☁️ Legacy/Advanced (Azure, RBAC, Bicep, etc.)

- For full Azure deployment, RBAC, or advanced configuration, see the [original Microsoft README](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator/blob/main/README.md).
- **macOS Apple Silicon:** DevContainer may not work ([see upstream issue](https://github.com/Azure/azure-functions-core-tools/issues/3112)). Use [NON_DEVCONTAINER_SETUP.md](../NON_DEVCONTAINER_SETUP.md) if needed.

---

## 🔑 Environment variables

Below are the minimum required environment variables for local development.
Set these in your `.env` file.
**Comments explain their purpose.**

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

> Other variables can be left as defaults or blank for local development.

---

## Bicep

A [Bicep file](./infra/main.bicep) is used to generate the [ARM template](./infra/main.json). You can deploy this accelerator by the following command if you do not want to use `azd`.

```sh
az deployment sub create --template-file ./infra/main.bicep --subscription {your_azure_subscription_id} --location {search_location}
 ```
