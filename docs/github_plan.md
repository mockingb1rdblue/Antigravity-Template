## GitHub Branching Strategy: AI-Assisted Solo Development with MCP System

### Core Philosophy

Use **simplified trunk-based development** optimized for AI agent execution with strategic branching for isolation. Default to direct commits on `main` for single-session work, create branches only when you need parallelism, experimentation, or multi-day efforts. [buildwithmatija](https://www.buildwithmatija.com/blog/git-commits-vs-branches-solo-ai-developer)

### Branch Structure

**Protected Branches**:
- `main` - Production-ready code, always deployable
- `staging` - Pre-production testing environment

**Working Branches** (short-lived, issue-specific):
- `feature/[linear-issue-id]-brief-description` - New capabilities
- `refactor/[linear-issue-id]-brief-description` - Code improvements
- `fix/[linear-issue-id]-brief-description` - Bug fixes
- `docs/[linear-issue-id]-brief-description` - Documentation only
- `experiment/ai-[description]` - Uncertain AI-generated explorations [buildwithmatija](https://www.buildwithmatija.com/blog/git-commits-vs-branches-solo-ai-developer)

**Example**: `feature/MCP-1.3-mcp-protocol-handler`

### Branching Decision Framework

**Commit Directly to `main` When**: [buildwithmatija](https://www.buildwithmatija.com/blog/git-commits-vs-branches-solo-ai-developer)
- Single Linear issue completable in 1-2 hours
- AI agent can generate, test, and verify in one session
- Low risk (documentation, small utilities, config tweaks)
- No parallel work needed
- Already tested in isolation

**Create Branch When**: [buildwithmatija](https://www.buildwithmatija.com/blog/git-commits-vs-branches-solo-ai-developer)
- Issue spans multiple days or sessions
- Large-scope changes (entire MCP server implementation)
- Experimental/uncertain AI outputs that might be abandoned
- Need to pause mid-work to address production issues
- Multiple agents working on different features simultaneously
- Breaking changes requiring review before merge

**Examples**:
- ✅ Direct to `main`: Fix typo in docs, add single utility function, update package version
- 🌿 Branch: Implement entire Durable Objects layer, refactor authentication system, experimental workflow selection algorithm

### Git Worktrees for Parallel Development

When working on multiple Linear issues simultaneously (e.g., one AI agent per feature), use **Git worktrees** instead of switching branches: [nrmitchi](https://www.nrmitchi.com/2025/10/using-git-worktrees-for-multi-feature-development-with-ai-agents/)

```bash
# Setup worktrees for parallel development
git worktree add ../mcp-provisioning feature/MCP-3.2-analyze-project
git worktree add ../mcp-auth feature/MCP-2.4-oauth-auth

# Work in separate directories simultaneously
cd ../mcp-provisioning  # Agent 1 works here
cd ../mcp-auth          # Agent 2 works here

# When done, remove worktrees
git worktree remove ../mcp-provisioning
```

This prevents context switching overhead and allows multiple AI coding sessions in parallel without branch conflicts. [nrmitchi](https://www.nrmitchi.com/2025/10/using-git-worktrees-for-multi-feature-development-with-ai-agents/)

### Pull Request Workflow

**PR Requirements** (enforced via branch protection):
- CI/CD checks pass (tests, linting, build)
- At least 1 approval (self-review for solo, but forces review step)
- Linear issue linked in PR description
- Documentation updated (checked via GitHub Action)

**PR Template** (`.github/pull_request_template.md`):
```markdown
## Linear Issue
Closes MCP-[issue-number]

## Changes
- Bullet list of what changed
- Focus on WHY, not what (code shows what)

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Documentation updated

## AI Agent Notes
[If AI-generated, note which prompts/context were used for future reference]

## Deployment Notes
[Any special considerations for deployment]
```

**PR Size Guidelines**: [mergify](https://mergify.com/blog/pull-request-management-streamline-your-workflow-with-automation)
- Target: < 400 lines changed
- If larger: split into stacked PRs with dependencies
- Use draft PRs for work-in-progress visibility

### Automation with GitHub Actions

**On Every PR** (`.github/workflows/pr-checks.yml`): [pullchecklist](https://www.pullchecklist.com/posts/github-pull-request-automation)
```yaml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Code quality
      - name: Lint TypeScript
        run: npm run lint
      
      - name: Type check
        run: npm run type-check
      
      # Tests
      - name: Unit tests
        run: npm test
      
      - name: Integration tests
        run: npm run test:integration
      
      # Documentation
      - name: Check docs updated
        run: |
          if git diff --name-only origin/main | grep -q "^src/"; then
            if ! git diff --name-only origin/main | grep -q "^docs/"; then
              echo "Code changed but docs not updated"
              exit 1
            fi
          fi
      
      # Size check
      - name: PR size check
        run: |
          LINES_CHANGED=$(git diff --shortstat origin/main | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+')
          if [ "$LINES_CHANGED" -gt 400 ]; then
            echo "::warning::PR has $LINES_CHANGED lines. Consider splitting."
          fi
      
      # Linear issue link
      - name: Verify Linear link
        run: |
          if ! grep -q "MCP-[0-9]" PR_BODY.md; then
            echo "PR must link to Linear issue"
            exit 1
          fi
```

**Auto-label PRs** (`.github/workflows/label-pr.yml`): [mergify](https://mergify.com/blog/pull-request-management-streamline-your-workflow-with-automation)
```yaml
name: Auto Label

on:
  pull_request:
    types: [opened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Label by size
        uses: codelytv/pr-size-labeler@v1
        with:
          xs_label: 'size:xs'
          xs_max_size: 10
          s_label: 'size:s'
          s_max_size: 100
          m_label: 'size:m'
          m_max_size: 400
          l_label: 'size:l'
          l_max_size: 1000
          xl_label: 'size:xl'
      
      - name: Label by component
        run: |
          if git diff --name-only | grep -q "^src/tools/"; then
            gh pr edit ${{ github.event.pull_request.number }} --add-label "component:worker"
          fi
          if git diff --name-only | grep -q "^src/durable-objects/"; then
            gh pr edit ${{ github.event.pull_request.number }} --add-label "component:durable-object"
          fi
          if git diff --name-only | grep -q "^docs/"; then
            gh pr edit ${{ github.event.pull_request.number }} --add-label "type:documentation"
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Auto-merge for Dependabot/Docs** (`.github/workflows/auto-merge.yml`): [mergify](https://mergify.com/blog/pull-request-management-streamline-your-workflow-with-automation)
```yaml
name: Auto Merge

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  auto-merge:
    if: |
      github.actor == 'dependabot[bot]' || 
      contains(github.event.pull_request.labels.*.name, 'type:documentation')
    runs-on: ubuntu-latest
    steps:
      - name: Auto-approve
        run: gh pr review ${{ github.event.pull_request.number }} --approve
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Enable auto-merge
        if: contains(github.event.pull_request.labels.*.name, 'automerge')
        run: gh pr merge ${{ github.event.pull_request.number }} --auto --squash
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Deploy to Staging on Merge** (`.github/workflows/deploy-staging.yml`):
```yaml
name: Deploy Staging

on:
  push:
    branches: [staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          environment: staging
          command: deploy --env staging
      
      - name: Comment on PRs
        run: |
          echo "Deployed to staging: https://mcp-staging.your-domain.workers.dev"
```

### Merge Strategies

**Squash Merge** (default): [mergify](https://mergify.com/blog/pull-request-management-streamline-your-workflow-with-automation)
- Use for feature branches: collapses all commits into one clean commit
- Keeps `main` history linear and readable
- Format: `[MCP-123] Add workflow provisioning (#45)`

**Regular Merge**:
- Use only for `staging` → `main` to preserve deployment history
- Maintains complete audit trail

**Rebase**:
- Never use (causes confusion with AI-generated commit histories)

### Branch Protection Rules

**For `main` branch**:
- ✅ Require pull request before merging
- ✅ Require status checks to pass (CI, tests, lint)
- ✅ Require conversation resolution
- ✅ Require linear history (squash merges only)
- ❌ Do not require approvals (solo dev, but use self-review habit)
- ✅ Dismiss stale PR approvals when new commits pushed
- ✅ Allow force pushes: disabled
- ✅ Allow deletions: disabled

**For `staging` branch**:
- ✅ Require pull request
- ✅ Require status checks
- ✅ Allow force pushes from admins (for hotfix testing)

### Workflow for Each Linear Issue

**Starting Work**:
```bash
# Sync with remote
git checkout main && git pull origin main

# Create branch from Linear issue
git checkout -b feature/MCP-1.3-mcp-protocol-handler

# Set upstream
git push -u origin feature/MCP-1.3-mcp-protocol-handler
```

**During Development**:
```bash
# Commit frequently (AI generates in bursts)
git add src/mcp/handler.ts
git commit -m "Implement MCP request parser"

git add src/mcp/types.ts
git commit -m "Add TypeScript types for MCP messages"

# Push regularly to backup work
git push
```

**Creating PR**:
```bash
# Ensure clean state
npm run lint:fix
npm test
git add . && git commit -m "Fix lint issues"

# Push final changes
git push

# Create PR via CLI (faster than web UI)
gh pr create \
  --title "[MCP-1.3] Implement MCP protocol handler" \
  --body "Closes MCP-1.3

## Changes
- Added MCP request router in index.ts
- Implemented protocol parsing in handler.ts
- Added TypeScript types for JSON-RPC messages

## Testing
- [x] Unit tests added for parser
- [x] Integration test with mock MCP client
- [x] Manual testing with curl

## AI Agent Notes
Generated using Cursor with MCP SDK documentation context" \
  --label "type:feature,component:worker,priority:critical"
```

**Self-Review Process** (force good habits): [mergify](https://mergify.com/blog/pull-request-management-streamline-your-workflow-with-automation)
1. Review "Files changed" tab in GitHub PR
2. Add inline comments explaining complex logic
3. Verify all acceptance criteria from Linear issue met
4. Check documentation was updated
5. Approve your own PR (triggers auto-merge if checks pass)

**Merging**:
```bash
# If checks pass and self-approved
gh pr merge --squash --delete-branch

# Or wait for auto-merge if labeled 'automerge'
```

**After Merge**:
```bash
# Update local main
git checkout main && git pull

# Linear issue automatically moves to "Done" (via GitHub integration)
```

### Hotfix Workflow

**Critical Production Issue**:
```bash
# Create fix branch from main
git checkout main && git pull
git checkout -b fix/critical-auth-bypass

# Make minimal fix
# ... edit files ...

# Fast-track PR
gh pr create --title "🚨 [HOTFIX] Fix authentication bypass" \
  --label "priority:critical,automerge" \
  --body "Critical security fix. Auto-merging after CI."

# Deploys automatically to staging, then promote to production
```

### Stacked PRs for Large Features

When a milestone requires multiple dependent changes: [mergify](https://mergify.com/blog/pull-request-management-streamline-your-workflow-with-automation)

```bash
# Base feature
git checkout -b feature/MCP-3.0-provisioning-base
# ... implement base ...
gh pr create --base main

# Dependent feature 1
git checkout -b feature/MCP-3.1-durable-objects
# ... implement DO ...
gh pr create --base feature/MCP-3.0-provisioning-base

# Dependent feature 2  
git checkout -b feature/MCP-3.2-analyze-project
# ... implement analysis ...
gh pr create --base feature/MCP-3.1-durable-objects

# Merge order: base → DO → analysis (each triggers next)
```

### Git Commit Message Standards

**Format**: `[MCP-###] Imperative description`

**Examples**:
- ✅ `[MCP-1.3] Implement MCP protocol handler`
- ✅ `[MCP-2.1] Add KV storage abstraction layer`
- ✅ `[MCP-4.4] Update user documentation with examples`
- ❌ `Fixed stuff`
- ❌ `WIP`
- ❌ `Added some code that the AI generated`

**Multi-file commits**: Group by logical change, not by file
- ✅ One commit: "Implement OAuth authentication" (touches auth.ts, middleware.ts, types.ts)
- ❌ Three commits: "Add auth.ts", "Add middleware.ts", "Add types.ts"

### Repository Hygiene

**Daily**:
- Delete merged branches: `git branch -d feature/MCP-1.3-handler`
- Clean up worktrees: `git worktree prune`

**Weekly**:
- Review open PRs: merge or close stale ones
- Update dependencies: `npm update` → new PR if changes
- Check GitHub Actions usage (stay under free tier limits)

**Per Milestone**:
- Tag release: `git tag -a v1.0.0-milestone-1 -m "Milestone 1: Foundation"`
- Push tags: `git push --tags`
- Create GitHub Release with changelog

### GitHub Repository Settings

**Branch Configuration**:
- Default branch: `main`
- Auto-delete head branches after merge: ✅ Enabled

**Actions Permissions**:
- Allow all actions and reusable workflows
- Allow GitHub Actions to create PRs: ✅ (for automated updates)

**Integrations**:
- Linear: Sync issue status with PR state
- Cloudflare: Deploy on merge to staging/main
- Slack: Notify on PR ready for review (optional)

This branching strategy balances simplicity for AI agents (clear branch naming, minimal ceremony) with safety (PR checks, branch protection) while optimizing for solo development velocity. The automation reduces manual overhead while the structured PR process forces proper review even when working alone. [graphite](https://graphite.com/guides/trunk-vs-gitflow)