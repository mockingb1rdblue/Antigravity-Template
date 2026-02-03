---
description: How to maintain the project roadmap and track feature progress.
---

# Roadmap Maintenance Workflow

Use this workflow to ingest new ideas, update feature status, and keep `ROADMAP.md` as the single source of truth.

## 1. Ingest New Ideas
When a new idea or feature request comes in:

1.  **Add to `/docs/ideas.md`**:
    - Add under "## New Ideas".
    - Include a brief description and potential impact.
2.  **Review**:
    - Does it align with the "State-First" vision?
    - Does it conflict with existing systems?
3.  **Approve/Reject**:
    - If Approved: Move to "## Approved Ideas" in `docs/ideas.md`.
    - If Rejected: Move to "## Deferred/Rejected" with a reason.

## 2. Promote to Roadmap
When an approved idea is ready for planning:

1.  **Create Specification**:
    - Create a new file in `docs/specs/[feature-name].md`.
    - Define the technical implementation (Schema, Logic, Commands).
    - Use the `docs/specs/template.md` (if available) or existing specs as a guide.
2.  **Update `ROADMAP.md`**:
    - Add the feature under the appropriate Phase.
    - Link to the growing spec file: `**Spec**: [Feature Name](docs/specs/feature-name.md)`.
    - Add high-level checklist items for implementation steps.

## 3. Track Progress
During development:

1.  **Mark In-Progress**:
    - In `ROADMAP.md`, change `[ ]` to `[/]` (or `[IN PROGRESS]`) for items being worked on.
2.  **Mark Complete**:
    - In `ROADMAP.md`, change `[ ]` to `[x]` when the feature is merged and verified.
3.  **Update Spec**:
    - If implementation details change, update the spec file to reflect reality.

## 4. Archive Old Items
When a Phase is fully complete:

1.  **Move to History**:
    - Move completed items to a "## Changelog" or "## Completed History" section at the bottom of `ROADMAP.md` (or a separate `HISTORY.md` file) to keep the main view clean.

## 5. Validation & Audit
To prevent "documentation rot":

1.  **Link Validation**:
    - Every time the roadmap is updated, verify that all file links (e.g., `[Spec](docs/specs/...)`) actually exist.
2.  **Live Capabilities Sync**:
    - Ensure the "## 🧩 Current System Capabilities" section at the top matches the actual features implemented and verified in the codebase.
3.  **Audit Log**:
    - Update the `> verified via codebase scan: [DATE]` timestamp whenever a full audit of live systems is performed.
