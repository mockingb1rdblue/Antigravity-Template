---
description: Kanban workflow (backlog → planning → doing → done)
---

# /project-management

## Workflow
All work must follow this status flow in documentation and `MASTER_PLAN.md`:

1.  **Backlog** `[ ]`: Identified ideas or bugs not yet scoped.
2.  **Planning** `[/]`: Technical specification being drafted in `docs/specs/`.
3.  **Doing** `[/]`: Feature actively being implemented.
4.  **Done** `[x]`: Feature verified, documented, and released.

## Categories

- **Specs**: Core logic definitions (`docs/specs/*.md`).
- **Tech Debt**: Refactoring tasks to ensure maintainability (e.g., Splitting large services).
- **Optimization**: Performance improvements (e.g., D1 Batching).

> [!IMPORTANT]
> **ROADMAP.md Ref**: All significant work items must be tracked in `ROADMAP.md` as the single source of truth.

## Daily Routine
- **Morning**: Run `npm run status` (or `pm_status.py`) to check blockers.
- **During**: Update `task.md` frequently.
- **Evening**: Update `STATUS.md` and sync `MASTER_PLAN.md`.
