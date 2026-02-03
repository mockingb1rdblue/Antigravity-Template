---
description: Project goals, constraints, success criteria
---

# /intent - CarPiggy

## Goal
Build a scalable, AI-powered RPG playground on Discord using Cloudflare Workers, Durable Objects, and Gemini AI.

## Constraints
- **300-Line Rule**: No file shall exceed 300 lines (enforces modularity).
- **Environment**: Must remain within Cloudflare Workers/Durable Objects limits.
- **Ruleset**: Use GURPS-Lite as the mechanical foundation.
- **Governance**: Adhere to Antigravity Core Pillars.

## Success Criteria
- [ ] Seamless multi-player turn coordination via Durable Objects.
- [ ] Context-aware AI narration with < 5s latency (via deferred responses).
- [ ] Robust world state persistence in D1.
- [ ] Zero high-severity vulnerabilities (`npm audit`).
- [ ] Fully documented internal and user-facing features.
