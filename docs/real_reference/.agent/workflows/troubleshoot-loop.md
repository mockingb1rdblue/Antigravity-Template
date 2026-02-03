---
description: Process for researching errors, applying identified fixes, and verifying resolution
---

# Troubleshoot Loop Mega-Workflow

This workflow guides the process of identifying, researching, and fixing complex errors.

## 1. Research (Perplexity)
When an error is obscure or relates to Cloudflare/AI SDKs:
1. **Query**: Use `@mcp:perplexity-ask:perplexity_ask` to research the specific error code or behavior.
2. **Context**: Provide the environment (Workers, TS, Wrangler) and relevant dependencies.
3. **Docs**: Cross-reference with `mcp:genkit-mcp-server:lookup_genkit_docs` if applicable.

## 0. Pre-Flight Check (The "Stupid" Stuff)
Before researching deep errors, check these common config traps:
1. **Wrangler Config**: Does `wrangler.toml` have syntax errors? Are bindings (`[[durable_objects.bindings]]`) correctly defined and named?
2. **Environment Types**: Does `src/index.ts` > `Env` interface match `wrangler.toml` bindings exactly?
3. **Build**: Run `npm run build` to catch TS errors before full deploy.

## 2. Targeted Fix
1. **Plan**: Add a sub-task to `task.md` outlining the fix.
2. **Safe Edits**: 
   - **View First**: Never edit lines without viewing them first.
   - **Targeted Fix**: Do NOT use `git restore` immediately. Fix errors in place to avoid losing other uncommitted progress.
   - **Restoration**: If you must restore, save a `git diff` first to recover lost work.
3. **300-Line Check**: Ensure the fix doesn't push a file over the 300-line limit.

## 3. Verify & Audit
1. **Build**: Run `wrangler deploy --dry-run`.
2. **Tail**: Run `wrangler tail` and trigger the failure point in Discord.
3. **Global Audit**: Search the project for the same "pattern" of error. If you found a missing token check, find all other places where that check should exist.
4. **Learn**: Update `PROJECT_MANUAL.md` or relevant reference docs if the fix was non-obvious.
