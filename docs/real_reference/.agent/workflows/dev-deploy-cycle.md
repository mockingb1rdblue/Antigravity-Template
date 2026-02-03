---
description: Build, deploy, and verify RPG features across dev/prod environments
---

# Dev-Deploy Cycle Mega-Workflow

This workflow covers the transition from code implementation to live verification.

## 1. Modular Command Implementation
Follow the **Modular Dispatcher Pattern** defined in `PROJECT_MANUAL.md`.
1. **New Command**: Create `src/handlers/commands/[name].ts`.
2. **Standard**: Ensure file is < 300 lines. Use `resolveWorld(guildId, channelId, env)` from `src/utils/world-utils` for isolation.
3. **Register**: Run `node scripts/register-commands.mjs development` to update your test server.

## 2. Environment Management
1. **Secrets**: Use `wrangler secret put NAME` for `DISCORD_BOT_TOKEN`, `GEMINI_API_KEY`, and `DEEPSEEK_API_KEY`.
2. **Compatibility**: Ensure `wrangler.toml` has `nodejs_compat` enabled and uses a recent `compatibility_date`.
3. **Switching**: Use `wrangler deploy` for Dev and `wrangler deploy --env production` for Prod.

## 3. Mandatory Isolation Audit
🚨 **BEFORE ANY DEPLOYMENT**, run the environment verification:
1. **Command**: `npm run verify-env` (checks vars) and `npm run verify-ai` (checks connectivity).
2. **Setup**: Reference `docs/env-setup.md` to ensure secrets are segmented.

## 5. Promotion to Production
Trigger this ONLY when requested (e.g., "Push test to prod"):
1. **Sync Secrets**: Before deploying, ensure all production API keys (Gemini, Discord, DeepSeek) are pushed to the production environment via `wrangler secret put`. **Do not assume parity with dev.**
2. **Clean State**: Ensure all changes are committed in Git. `verify-env` will block production deploys from a dirty state.
3. **Register**: `npm run register:prod`. (Requires `dotenv` in script for CLI context).
4. **Deploy**: `npm run deploy:prod`.
5. **Sign-off**: Verify in the live server and update `STATUS.md`.

## Troubleshooting
- **401 Unauthorized**: Check bot tokens and Public Keys in secrets.
- **D1 Table Errors**: Verify D1 schema exists in production via `wrangler d1 execute [db] --command="..." --remote --env production`.
- **"Application Did Not Respond"**: This usually indicates the worker is crashing or missing a handler. Check `wrangler tail` for `Module not found` errors.
- **Bundling Chaos**: Avoid dynamic `import()` for core handlers; use static registry in `router.ts` to ensure Cloudflare bundles all files.

### 💡 Hard-Learned Pitfalls (2026-01-30)
- **Secret Drifts**: Development secrets do *not* automatically copy to production. Always push secrets to the `--env production` namespace.
- **Git Blockers**: If `npm run deploy:prod` fails on the "dirty state" check, commit your verified dev code first.
- **CLI Context**: Scripts running in production mode (like `register:prod`) must explicitly load `.env` if they rely on localized secrets.
