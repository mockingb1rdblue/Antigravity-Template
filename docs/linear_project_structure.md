## Linear Project Structure: MCP Workflow Management System

### Project Setup

**Project Name**: `MCP Workflow Sync System`

**Project Description**: Cloudflare Workers-based MCP servers for centralized management and provisioning of modular scripts, skills, workflows, and rules across Antigravity and Perplexity-ask projects. Eliminates tech debt through single source of truth architecture with intelligent, context-aware workflow selection.

**Target Date**: 8 weeks from start

**Teams**: Engineering (you + AI agents)

**Cycle Length**: 1 week sprints [morgen](https://www.morgen.so/blog-posts/linear-project-management)

### Labels System

**Type Labels**: [onehorizon](https://onehorizon.ai/blog/linear-app-review)
- `type:infrastructure` - Cloudflare Workers setup, deployment configs
- `type:feature` - MCP tools, resources, authentication
- `type:documentation` - User guides, API docs, architecture diagrams
- `type:testing` - Validation, integration tests

**Priority Labels**: [everhour](https://everhour.com/blog/how-to-use-linear/)
- `priority:critical` - Blocking issues, core functionality
- `priority:high` - Essential for milestone completion
- `priority:medium` - Important but not blocking
- `priority:low` - Nice-to-have enhancements

**Status Labels**:
- `status:ready-for-agent` - Issue fully specified, agent can execute
- `status:needs-spec` - Requires additional detail before work
- `status:blocked` - Waiting on dependency or decision

**Component Labels**:
- `component:worker` - Cloudflare Worker entry point code
- `component:durable-object` - State management layer
- `component:storage` - KV, R2, D1 implementations
- `component:auth` - OAuth and authentication
- `component:workflows` - Workflow definition files

### Milestones

**Milestone 1: Foundation** (Weeks 1-2)
- Repository structure created
- Basic Cloudflare Worker deployed
- MCP protocol handler implemented
- Development workflow established

**Milestone 2: Core MCP Server** (Weeks 3-4)
- Workflow Registry Server operational
- KV-backed workflow catalog
- Basic MCP tools functional (list, get, search)
- Authentication implemented

**Milestone 3: Provisioning System** (Weeks 5-6)
- Project Provisioning Server deployed
- Durable Objects state management
- Project analysis and workflow selection logic
- Antigravity integration tested

**Milestone 4: Lifecycle Management** (Weeks 7-8)
- CI/CD pipeline for workflow updates
- Version tracking and rollback
- User documentation complete
- Production deployment

### Issue Template Structure

Every issue follows this format for agent compatibility: [linear](https://linear.app/method)

**Title**: `[Component] Action - Specific Outcome`

**Description Template**:
```
## Context
[1-2 sentences: why this matters, what it enables]

## Files to Modify/Create
- `path/to/file1.ts` - [brief purpose]
- `path/to/file2.ts` - [brief purpose]

## Acceptance Criteria
- [ ] Specific testable outcome 1
- [ ] Specific testable outcome 2
- [ ] Documentation updated in [file]

## Implementation Steps
1. Step with exact file and function name
2. Step with specific code location
3. Step with validation command

## Dependencies
- Blocks: #[issue-number]
- Requires: #[issue-number]

## Documentation Impact
[Which docs need updates, where to add them]

## Testing Instructions
[Exact commands to verify completion]
```

### Phase 1: Foundation Issues

**Issue 1.1**: `[infrastructure] Initialize Cloudflare Workers project structure`
- **Priority**: Critical
- **Labels**: type:infrastructure, component:worker, status:ready-for-agent
- **Files**: 
  - Create `wrangler.toml` with project config
  - Create `src/index.ts` with basic Worker handler
  - Create `package.json` with MCP SDK dependency
  - Create `.github/workflows/deploy.yml` for CI/CD
- **Acceptance Criteria**:
  - [ ] `wrangler dev` runs locally
  - [ ] `wrangler deploy` succeeds to staging
  - [ ] Worker responds to HTTP requests
- **Documentation**: Create `docs/setup.md` with installation steps

**Issue 1.2**: `[infrastructure] Create workflow repository structure`
- **Priority**: Critical
- **Labels**: type:infrastructure, component:workflows
- **Files**:
  - Create `workflows/core/` directory
  - Create `workflows/language/` directory
  - Create `workflows/domain/` directory
  - Create `workflows/manifest.yaml` schema
  - Create `workflows/README.md` template
- **Acceptance Criteria**:
  - [ ] Directory structure matches architecture plan
  - [ ] manifest.yaml validates against schema
  - [ ] README explains contribution process
- **Documentation**: Create `docs/workflow-structure.md`

**Issue 1.3**: `[component:worker] Implement MCP protocol handler`
- **Priority**: Critical
- **Labels**: type:feature, component:worker, status:ready-for-agent
- **Files**:
  - Modify `src/index.ts` - Add MCP request router
  - Create `src/mcp/handler.ts` - Protocol parsing logic
  - Create `src/mcp/types.ts` - TypeScript types for MCP messages
- **Steps**:
  1. Install `@modelcontextprotocol/sdk` in package.json
  2. Import `Server` class in index.ts line 1
  3. Instantiate Server with name "workflow-registry" and version "1.0.0"
  4. Add POST route `/mcp` that calls server.handleRequest()
  5. Add error handling for invalid JSON-RPC messages
- **Acceptance Criteria**:
  - [ ] POST /mcp returns valid MCP capabilities response
  - [ ] Invalid requests return proper error structure
  - [ ] Logs show request/response flow
- **Testing**: `curl -X POST https://localhost:8787/mcp -d '{"jsonrpc":"2.0","method":"initialize"}'`
- **Documentation**: Update `docs/api.md` with protocol details

### Phase 2: Core MCP Server Issues

**Issue 2.1**: `[component:storage] Setup Cloudflare KV for workflow catalog`
- **Priority**: High
- **Labels**: type:infrastructure, component:storage
- **Files**:
  - Modify `wrangler.toml` - Add KV namespace bindings
  - Create `src/storage/kv.ts` - KV abstraction layer
  - Create `scripts/seed-workflows.ts` - Initial data loader
- **Steps**:
  1. Run `wrangler kv:namespace create WORKFLOW_CATALOG`
  2. Add binding in wrangler.toml under `[[kv_namespaces]]`
  3. Create KV wrapper class in src/storage/kv.ts
  4. Implement get(), put(), list() methods with error handling
  5. Create seed script that loads workflows/ directory to KV
- **Acceptance Criteria**:
  - [ ] KV namespace created in Cloudflare dashboard
  - [ ] Wrapper class type-safe and tested
  - [ ] Seed script populates 5+ test workflows
- **Documentation**: Add KV operations to `docs/architecture.md`

**Issue 2.2**: `[component:worker] Implement list_workflows MCP tool`
- **Priority**: High
- **Labels**: type:feature, component:worker, status:ready-for-agent
- **Depends On**: #2.1
- **Files**:
  - Create `src/tools/list-workflows.ts` - Tool implementation
  - Modify `src/index.ts` - Register tool handler
- **Steps**:
  1. Import Server and CallToolRequestSchema from MCP SDK
  2. Create async function listWorkflows(filters) in list-workflows.ts
  3. Query KV using env.WORKFLOW_CATALOG.list({ prefix: filters.category })
  4. Map results to workflow metadata objects
  5. Register handler in index.ts: server.setRequestHandler(CallToolRequestSchema, ...)
  6. Add "list_workflows" case in switch statement
  7. Return content array with workflow list as JSON text
- **Acceptance Criteria**:
  - [ ] Tool returns all workflows when no filters
  - [ ] Filtering by category works correctly
  - [ ] Response matches MCP tool response schema
  - [ ] Error handling for missing KV data
- **Testing**: Use MCP client to call `list_workflows` with `{"category": "core"}`
- **Documentation**: Add tool to `docs/tools-reference.md` with examples

**Issue 2.3**: `[component:worker] Implement get_workflow_metadata MCP tool`
- **Priority**: High
- **Labels**: type:feature, component:worker, status:ready-for-agent
- **Depends On**: #2.1
- **Files**:
  - Create `src/tools/get-workflow.ts`
  - Modify `src/index.ts` - Add tool handler
- **Steps**:
  1. Create getWorkflowMetadata(workflowId) function
  2. Call env.WORKFLOW_CATALOG.get(workflowId, "json")
  3. Parse frontmatter from workflow markdown
  4. Return metadata object with name, tags, dependencies, scope
  5. Handle 404 when workflow not found
- **Acceptance Criteria**:
  - [ ] Returns complete metadata for valid workflow ID
  - [ ] Returns error for non-existent workflow
  - [ ] Parses YAML frontmatter correctly
- **Documentation**: Update `docs/tools-reference.md`

**Issue 2.4**: `[component:auth] Implement OAuth authentication`
- **Priority**: High
- **Labels**: type:feature, component:auth
- **Files**:
  - Create `src/auth/oauth.ts` - OAuth provider setup
  - Modify `src/index.ts` - Add auth middleware
  - Create `src/auth/middleware.ts` - Token validation
- **Steps**:
  1. Install `workers-oauth-provider` package
  2. Initialize OAuth provider with client credentials in env vars
  3. Create middleware that checks Authorization header
  4. Extract and validate Bearer token
  5. Attach user context to request object
  6. Add middleware to /mcp route before handler
- **Acceptance Criteria**:
  - [ ] Unauthenticated requests return 401
  - [ ] Valid OAuth tokens allow access
  - [ ] User ID extracted and logged
- **Documentation**: Create `docs/authentication.md` with setup guide

### Phase 3: Provisioning System Issues

**Issue 3.1**: `[component:durable-object] Create Provisioning Session Durable Object`
- **Priority**: Critical
- **Labels**: type:infrastructure, component:durable-object
- **Files**:
  - Create `src/durable-objects/provisioning-session.ts`
  - Modify `wrangler.toml` - Add Durable Object binding
  - Create `src/durable-objects/types.ts` - State interfaces
- **Steps**:
  1. Export class ProvisioningSession extends DurableObject
  2. Implement constructor with state and env parameters
  3. Add fetch() method to handle session requests
  4. Implement setState(), getState() using this.ctx.storage
  5. Add session expiry with this.ctx.storage.setAlarm()
  6. Register in wrangler.toml under [[durable_objects.bindings]]
- **Acceptance Criteria**:
  - [ ] Durable Object instantiates successfully
  - [ ] State persists across requests
  - [ ] Session expires after timeout
- **Documentation**: Add to `docs/architecture.md` under state management

**Issue 3.2**: `[component:worker] Implement analyze_project MCP tool`
- **Priority**: High
- **Labels**: type:feature, component:worker, status:ready-for-agent
- **Files**:
  - Create `src/tools/analyze-project.ts`
  - Create `src/analysis/scope-detector.ts` - Detection logic
  - Modify `src/index.ts` - Register tool
- **Steps**:
  1. Create analyzeProject(projectPath) function
  2. Instantiate Durable Object session for this project
  3. Implement scope detection: read package.json, pyproject.toml, .agent.md
  4. Extract languages, frameworks, domains from project files
  5. Store detected scope in Durable Object state
  6. Return scope summary with confidence scores
- **Acceptance Criteria**:
  - [ ] Detects Python projects from pyproject.toml
  - [ ] Detects TypeScript projects from package.json
  - [ ] Extracts domain hints from .agent.md
  - [ ] Stores state in Durable Object
- **Testing**: Provide sample project structures as test fixtures
- **Documentation**: Update `docs/tools-reference.md` with scope detection rules

**Issue 3.3**: `[component:worker] Implement provision_workflows MCP tool`
- **Priority**: Critical
- **Labels**: type:feature, component:worker, status:ready-for-agent
- **Depends On**: #3.2
- **Files**:
  - Create `src/tools/provision-workflows.ts`
  - Create `src/provisioning/selector.ts` - Selection algorithm
  - Create `src/provisioning/installer.ts` - File operations
- **Steps**:
  1. Create provisionWorkflows(projectPath, strategy) function
  2. Retrieve project scope from Durable Object session
  3. Query workflow manifest for matching workflows using scope tags
  4. Implement dependency resolution for required workflows
  5. For core workflows: return symlink instructions to global directory
  6. For project workflows: return copy instructions with content
  7. Update Durable Object with provisioning status
  8. Return provisioning plan as structured JSON
- **Acceptance Criteria**:
  - [ ] Selects all applicable workflows based on scope
  - [ ] Resolves dependencies correctly
  - [ ] Distinguishes core vs project-specific workflows
  - [ ] Provides actionable installation instructions
- **Documentation**: Create `docs/provisioning-guide.md` with examples

**Issue 3.4**: `[component:worker] Implement sync_core_workflows MCP tool`
- **Priority**: High  
- **Labels**: type:feature, component:worker, status:ready-for-agent
- **Files**:
  - Create `src/tools/sync-core.ts`
  - Create `src/sync/global-manager.ts` - Global directory operations
- **Steps**:
  1. Create syncCoreWorkflows() function
  2. Query KV for all workflows with category "core"
  3. Generate sync plan for ~/.gemini/antigravity/global_workflows/
  4. Return list of files to create/update with content
  5. Include checksums for verification
- **Acceptance Criteria**:
  - [ ] Returns all core workflows from catalog
  - [ ] Includes file paths relative to global directory
  - [ ] Provides workflow content ready to write
- **Documentation**: Update `docs/tools-reference.md`

### Phase 4: Lifecycle Management Issues

**Issue 4.1**: `[component:storage] Setup R2 bucket for workflow content`
- **Priority**: Medium
- **Labels**: type:infrastructure, component:storage
- **Files**:
  - Modify `wrangler.toml` - Add R2 bucket binding
  - Create `src/storage/r2.ts` - R2 abstraction layer
- **Steps**:
  1. Run `wrangler r2 bucket create workflow-content`
  2. Add binding in wrangler.toml under [[r2_buckets]]
  3. Create R2 wrapper with put(), get() methods
  4. Migrate large workflow files from KV to R2
  5. Keep metadata in KV, content in R2
- **Acceptance Criteria**:
  - [ ] R2 bucket created and accessible
  - [ ] Workflows over 10KB stored in R2
  - [ ] Metadata retrieval still fast from KV
- **Documentation**: Update `docs/architecture.md` storage section

**Issue 4.2**: `[infrastructure] Create CI/CD pipeline for workflow updates`
- **Priority**: High
- **Labels**: type:infrastructure, component:workflows
- **Files**:
  - Create `.github/workflows/sync-workflows.yml`
  - Create `scripts/validate-workflow.ts` - Validation script
  - Create `scripts/sync-to-kv.ts` - KV upload script
- **Steps**:
  1. Create GitHub Actions workflow triggered on push to workflows/
  2. Add step to validate workflow YAML frontmatter
  3. Add step to check for duplicate IDs or naming conflicts
  4. Add step to run workflow syntax validation
  5. Add step to sync validated workflows to KV using Wrangler API
  6. Add notification on success/failure
- **Acceptance Criteria**:
  - [ ] Pipeline runs on workflow file changes
  - [ ] Invalid workflows fail the build
  - [ ] Valid workflows sync to staging KV
  - [ ] Manual approval required for production
- **Documentation**: Create `docs/contributing-workflows.md`

**Issue 4.3**: `[component:worker] Implement workflow version tracking`
- **Priority**: Medium
- **Labels**: type:feature, component:durable-object
- **Files**:
  - Modify `src/durable-objects/provisioning-session.ts` - Add version ledger
  - Create `src/tools/get-workflow-versions.ts`
  - Create `src/tools/revert-workflow.ts`
- **Steps**:
  1. Extend Durable Object state to include version history array
  2. On provision, record workflow ID + version + timestamp
  3. Implement getWorkflowVersions(projectPath) tool
  4. Implement revertWorkflow(projectPath, workflowId, targetVersion) tool
  5. Add version comparison logic
- **Acceptance Criteria**:
  - [ ] Version history persists in Durable Object
  - [ ] Can query installed versions per project
  - [ ] Revert restores previous workflow version
- **Documentation**: Update `docs/tools-reference.md` with versioning

**Issue 4.4**: `[type:documentation] Create user documentation suite`
- **Priority**: High
- **Labels**: type:documentation
- **Files**:
  - Create `docs/getting-started.md` - Quickstart guide
  - Create `docs/user-guide.md` - Comprehensive usage
  - Create `docs/workflow-authoring.md` - Writing workflows
  - Create `docs/troubleshooting.md` - Common issues
  - Create `docs/api-reference.md` - All tools documented
- **Steps**:
  1. Write getting-started with 5-minute setup instructions
  2. Add user-guide with common workflows (provision new project, update existing, rollback)
  3. Document workflow authoring with frontmatter schema and examples
  4. Collect common errors and solutions for troubleshooting
  5. Generate API reference from tool implementations with examples
  6. Add screenshots/diagrams using ASCII art or Mermaid
- **Acceptance Criteria**:
  - [ ] Non-technical user can follow getting-started successfully
  - [ ] All MCP tools documented with examples
  - [ ] Workflow authoring guide includes 3+ complete examples
  - [ ] Troubleshooting covers 10+ common scenarios
- **Documentation**: Create `README.md` linking to all docs

**Issue 4.5**: `[component:worker] Implement usage analytics tools`
- **Priority**: Low
- **Labels**: type:feature, component:worker
- **Files**:
  - Create `src/tools/analyze-usage.ts`
  - Create `src/tools/find-drift.ts`
  - Setup Workers Analytics Engine binding
- **Steps**:
  1. Add Analytics Engine binding in wrangler.toml
  2. Log tool invocations to Analytics Engine
  3. Implement analyzeUsage() - query most used workflows
  4. Implement findDrift() - compare project workflows to catalog
  5. Return actionable insights
- **Acceptance Criteria**:
  - [ ] Analytics capture tool usage
  - [ ] Usage analysis returns top 10 workflows
  - [ ] Drift detection identifies outdated projects
- **Documentation**: Update `docs/tools-reference.md`

### Documentation Standards

Every completed issue must include: [reddit](https://www.reddit.com/r/technicalwriting/comments/113mh5p/technical_documentation_templatessamplesexamples/)

**Code Documentation**:
- Inline comments for complex logic only
- JSDoc for all exported functions with params and return types
- README.md in each src/ subdirectory explaining purpose

**User Documentation** (`docs/` directory):
- **Setup guides**: Step-by-step with exact commands, no assumptions
- **Usage guides**: Real-world examples with expected outputs
- **API reference**: Tool signatures, parameters, return types, examples
- **Architecture docs**: Diagrams (Mermaid), decision rationale, trade-offs
- **Troubleshooting**: Error messages → solutions, debug steps

**Documentation Structure**:
```
docs/
├── README.md                    # Doc index
├── getting-started.md           # 5-min quickstart
├── architecture.md              # System design
├── setup.md                     # Installation
├── user-guide.md                # Common workflows
├── tools-reference.md           # All MCP tools
├── workflow-structure.md        # Workflow format
├── workflow-authoring.md        # Writing workflows
├── contributing-workflows.md    # CI/CD process
├── authentication.md            # OAuth setup
├── provisioning-guide.md        # Detailed provisioning
├── troubleshooting.md           # Common issues
└── api-reference.md             # Complete API
```

### Issue Assignment Strategy

**For AI Agents**: [linear](https://linear.app/method)
- Only assign issues with `status:ready-for-agent` label
- Ensure Files, Steps, and Testing sections are complete
- Provide exact file paths and line numbers where possible
- Include validation commands that return pass/fail clearly

**Review Checklist Before Assignment**:
- [ ] Acceptance criteria are testable
- [ ] Files to modify are explicitly listed
- [ ] Steps include exact locations (file, function, line)
- [ ] Testing instructions are copy-paste executable
- [ ] Dependencies are clearly marked
- [ ] Documentation updates are specified

### Progress Tracking

**Daily**: Review issues marked `In Progress`, check for blockers

**Weekly** (end of cycle): [build.plumhq](https://build.plumhq.com/how-we-use-linear/)
- Sprint review: completed vs planned issues
- Update roadmap timeline based on velocity
- Adjust priorities for next cycle
- Update project README with current status

**Per Milestone**:
- Demo functional capabilities
- Deploy to staging environment
- Collect feedback and file improvement issues
- Update documentation with lessons learned

This Linear project structure provides forward momentum through clear dependencies, minimal token requirements via explicit file/step specifications, continuous documentation, and agent-friendly issue formatting that eliminates ambiguity. [linear](https://linear.app/method/introduction)