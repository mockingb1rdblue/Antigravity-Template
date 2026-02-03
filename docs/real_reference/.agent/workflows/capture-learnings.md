---
description: Lifecycle for prompt engineering, rule enforcement, and AI narrative quality control.
---

# Capture Learnings Workflow

Use this workflow at the end of a major feature implementation or after resolving a complex bug to persist "tribal knowledge" for future agent sessions.

## 1. Extract Pattern
Identify a recurring engineering pattern or a specific domain rule (e.g., "GURPS Hit Locations") that was crucial for the task.

1.  **Summarize**: Write a concise summary of the logic or pattern.
2.  **Refine**: Ensure the summary includes:
    - **Context**: Where/Why this pattern is used.
    - **Logic**: The deterministic or probabilistic rules.
    - **Code Reference**: Absolute path to the implementation.
3.  **Model Validation**: If the learning involves AI behavior, specify the exact model string used (e.g., `gemini-3-pro-preview`). Verify against [MODELS.md](docs/reference/MODELS.md) to ensure no deprecated models are cited.

## 2. Persist to Skill
If the knowledge is a **reusable capability** (e.g., "how to calculate damage"):

1.  **Create/Update Skill**: Add to `.agent/skills/[domain].md`.
2.  **Format**:
    - `# Skill: [Name]`
    - `## Pattern`: Description of the rule.
    - `## Constraints`: When NOT to use this.
    - `## Code`: Link to the service or model.

## 3. Persist to Workflow
If the knowledge is a **procedural step** (e.g., "how to deploy to dev"):

1.  **Create/Update Workflow**: Add to `.agent/workflows/[command].md`.
2.  **Format**:
    - Standard workflow frontmatter.
    - Step-by-step instructions.

## 4. Update Core Rules
If the learning is a **Global Rule Change** (e.g., "Never use X library"):

1.  **Update `STATUS.md`**: Note the new constraint in the "How to Continue" section.
2.  **Update System Prompt**: If you have access, propose an update to the project's core instructions.
