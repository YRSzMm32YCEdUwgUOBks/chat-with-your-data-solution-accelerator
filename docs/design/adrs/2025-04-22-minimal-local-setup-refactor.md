# Minimal Local Setup & Dev Experience Refactor

* **Status:** accepted
* **Proposer:** @your-github-handle
* **Date:** 2025-04-22
* **Technical Story:** [Enable minimal local onboarding for CWYD](https://github.com/YRSzMm32YCEdUwgUOBks/chat-with-your-data-solution-accelerator/pull/XXX)

## Context and Problem Statement

Onboarding new contributors—especially frontend developers—was slow and error-prone due to cloud dependencies, complex infra, and inconsistent local environments. The goal was to enable anyone to run and develop the full stack locally, with minimal setup and no Azure subscription required.

## Decision Drivers

* Fast, reliable onboarding for all contributors
* Local/cloud parity for backend and infra
* Minimal external dependencies (no Azure required for local dev)
* Automated, reproducible environment setup
* Code quality and consistency

## Considered Options

* Continue with Azure-first, cloud-dependent onboarding
* Provide scripts for partial local emulation
* Full dev container and Docker Compose refactor for local-first onboarding

## Decision Outcome

Chosen option: **Full dev container and Docker Compose refactor**
This approach enables all services (frontend, backend, admin, Postgres, Azurite) to run locally with a single command, using a standardized `.env` and pre-installed tools.

## Pros and Cons of the Options

### Full dev container & Docker Compose refactor

* Good, because onboarding is now <5 minutes for anyone with WSL/Docker
* Good, because all services run identically in local and cloud (parity)
* Good, because no Azure subscription or secrets are needed for local dev
* Good, because code quality gates (linting, pre-commit) are enforced
* Bad, because some Azure-specific infra (Bicep, RBAC) is now less emphasized in local docs
* Bad, because some modules (e.g., Azure Search) are present but not used in local runs

### Continue with Azure-first onboarding

* Good, because it matches production infra
* Bad, because onboarding is slow and error-prone for new contributors

### Provide scripts for partial local emulation

* Good, because it reduces some friction
* Bad, because it’s inconsistent and hard to maintain

## Links

* [PR: Minimal Local Setup & Dev Experience Refactor](https://github.com/YRSzMm32YCEdUwgUOBks/chat-with-your-data-solution-accelerator/pull/XXX)
* [Upstream repo](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator)
