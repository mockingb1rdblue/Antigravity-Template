# Cloudflare Architect Skill

This skill encompasses specialized knowledge for building and scaling the CarPiggy backend on Cloudflare.

## Core Competencies

### 1. Durable Object (DO) Design
- **Single Source of Truth**: Identify which entities need DOs (e.g., `WorldManagerDO`, `TurnCoordinatorDO`) to ensure strict consistency.
- **State Management**: Use `storage.get` and `storage.put` efficiently. Minimize the size of stored values.
- **Concurrency**: Understand the transactional nature of DO storage.

### 2. D1 Database Strategy
- **Relational Integrity**: Design schemas (`schema.sql`) that support efficient joins and historical queries.
- **Migrations**: Handle database changes using `wrangler d1 migrations` patterns.
- **Query Optimization**: Use indexes for frequently searched columns like `guild_id` or `world_id`.

### 3. Serverless Best Practices
- **Scale to Zero**: Optimize imports and bundle size to minimize cold start times.
- **Secrets Management**: Always use `wrangler secret put` for sensitive keys (Discord, Gemini, DeepSeek).
- **Environment Variables**: Use `vars` in `wrangler.toml` for non-sensitive config.

## Implementation Guidelines

- **Worker Verification**: Always include Discord signature verification (`discord-interactions` library).
- **Graceful Error Handling**: Return appropriate JSON responses for Discord interactions.
- **Logging**: Use `console.info` and `console.error` for visibility during development and production.

## Troubleshooting
- If deployment fails, check `wrangler.toml` bindings first.
- If DOs are not persisting state, verify the `new_sqlite_classes` or migrations tag.
- If D1 queries are slow, check for missing indexes.
