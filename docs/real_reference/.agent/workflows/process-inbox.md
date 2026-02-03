---
description: Process raw files from _INBOX into actionable specs or ideas
---

# /process-inbox

## Goal
Transform raw dumps, pastes, and brain-dumps in `_INBOX/` into structured project documents, **while preserving the original context.**

## Workflow

1.  **Select Item**: Pick a file from `_INBOX/`.
2.  **Archive First**: Move the file to `docs/archive/legacy/_INBOX/` immediately.
    ```bash
    mv _INBOX/filename.md docs/archive/legacy/_INBOX/
    ```
3.  **Analyze & Extract**: Read the *archived* content to understand intent.
4.  **Triage & Link**:
    *   **Feature/Idea**: Add to `docs/ideas.md`. **MUST** include a link to the archived file.
        > `- [ ] Idea Description ([Source Context](../docs/archive/legacy/_INBOX/filename.md))`
    *   **Technical Spec**: Create spec in `docs/specs/`. **MUST** add a header link.
        > `> **Source Context**: [Original Draft](../archive/legacy/_INBOX/filename.md)`
    *   **Bug Report**: Log in `docs/issues-and-enhancements.md` with link.
5.  **Completion**: The item is now processed, but the full raw context is preserved in the archive forever.

## Why Link Back?
We treat `_INBOX` items as "Raw Data" and Specs/Ideas as "Processed Data". Logic and nuance are often lost in summary. The link ensures we can always check *why* something was suggested.
