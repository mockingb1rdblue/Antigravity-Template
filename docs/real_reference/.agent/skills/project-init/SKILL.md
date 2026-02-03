---
name: project-init
description: Automates the research and setup of project-specific infrastructure after bootstrapping
---

# Project Initialization Skill

This skill customizes a newly bootstrapped project by researching best practices and setting up the development environment.

## Usage

Run this skill immediately after running the `bootstrap-project.sh` script (or manually copying workflows).

## Steps

### 1. Context Gathering
1.  **Read Intent**: Analyze `.agent/workflows/intent.md` to understand the project type (Web App, CLI, API, Library) and goals.
2.  **Read Status**: Check `STATUS.md` for current state.

### 2. Research (Perplexity)
Use `perplexity_ask` to research best practices for the specific project type.
*   **Query**: "Best practices and folder structure for a modernized [Project Type] using [Tech Stack] in 2024+?"
*   **Query**: "Essential dev dependencies and ease-of-use scripts for [Project Type]?"

### 3. Environment Setup
Based on research:
1.  **Dependencies**: Suggest `npm install` or `pip install` commands for critical tools (e.g., `vitest`, `ruff`, `husky`).
2.  **Scripts**: Create helper scripts in `scripts/`:
    *   `scripts/dev.sh`: One-command dev server start.
    *   `scripts/test.sh`: Standardized test runner.
    *   `scripts/check.sh`: Linting and formatting check.

### 4. Skill Generation
Create project-specific skills in `.agent/skills/` if frequent complex tasks are anticipated (e.g., `component-gen` for React, `migration-gen` for DBs).

### 5. Finalize
1.  Update `STATUS.md`: Mark initialization as complete.
2.  Update `README.md`: Add "Getting Started" section using the new scripts.
