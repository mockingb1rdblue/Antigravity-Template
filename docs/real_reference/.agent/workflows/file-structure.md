---
description: Naming conventions and folder organization
---

# /file-structure

## Conventions
- **Files**: kebab-case (e.g., `world-manager.ts`).
- **Directories**: kebab-case (e.g., `src/handlers/commands/`).
- **Standard Paths**:
  - `.agent/workflows/`: Mandatory governance workflows.
  - `.agent/skills/`: Custom agent capabilities.
  - `docs/`: User and technical documentation.
  - `src/`: Source code.
  - `src/handlers/commands/`: Isolated slash command logic.
  - `src/utils/`: Shared helper functions.
  - `scripts/`: Implementation/maintenance scripts.
- **Line Limit**: 🚨 **MAX 300 LINES PER FILE**.
  - **Service Extraction**: If a handler (e.g., `turn-coordinator.ts`) approaches this limit, extract logic into a dedicated service (e.g., `services/dice-engine.ts`) or model (e.g., `models/turn-state.ts`).
  - **Single Responsibility**: Handlers should coordinate calls, not contain core logic.
