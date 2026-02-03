---
description: Lifecycle for prompt engineering, rule enforcement, and AI narrative quality control
---

# AI Agent Tuning Mega-Workflow

This workflow ensures the RPG's intelligence remains consistent, accurate to rules (GURPS), and immersive.

## 1. Prompt Design & Versioning
1. **Testing**: Test prompts in a playground (e.g., Google AI Studio) before embedding in code.
2. **Isolation**: Keep prompts in specialized template strings or JSON configs.

## 2. GURPS Rule Enforcement
1. **Roll Verification**: Ensure `DiceResolver` output matches player actions exactly.
2. **Skill Tiers**: Test that "Critical Success" and "Critical Failure" result in exponentially different narratives.

## 3. History & Continuity
1. **Context Extraction**: Verify the "Archivist" agent correctly identifies relevant plot threads vs. noise.

## 4. Latency & Performance
1. **Early Return**: Ensure the "Deferred Response" pattern is used for all AI generation.
2. **Async Loop**: Monitor Durable Object execution time for `processTurn`.
## 5. Self-Optimization Loop
This is a mandatory step for the agent at the end of every task or session:
1. **Reflect**: Identify any moment where work stalled (e.g., "Invalid API Key hangups", "Bundling errors").
2. **Automate**: If the struggle was procedural, update the relevant workflow (e.g., `dev-deploy-cycle.md`) immediately.
3. **Harden**: If the struggle was code-based, add a verification script (e.g., `verify-env.sh`) to prevent regression.
4. **Communicate**: Report the improvement in the session summary.
