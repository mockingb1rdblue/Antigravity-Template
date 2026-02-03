# MCP Foundation - Plan Outline

## Phase 1: Environment Setup
- [/] Repository initialization
- [/] Git configuration (user.name, user.email)
- [/] Essential files (.gitignore, README.md)

## Phase 2: Core Implementation
- [ ] Implement MCP Server foundation
- [ ] Define standard tool interfaces
- [ ] Setup documentation structure

## Phase 3: Slicing & Status Tracking
- [ ] Create STATUS.md as source of truth
- [ ] Thin-slice tasks from Plan Outline
- [ ] Establish sync workflow

Yes, Linear MCP can create projects. The Linear MCP server includes project management capabilities that allow AI assistants to create projects with associated issues, get project information, list and filter projects, and associate issues with existing projects. [linear](https://linear.app/docs/mcp)

## Project Management Features

The Linear MCP server provides several project-related tools:

- **Create projects** with associated issues [github](https://github.com/dvcrn/mcp-server-linear)
- **Get project information** including rich text descriptions [github](https://github.com/cline/linear-mcp)
- **Search and list projects** with optional filtering and rich text description support [github](https://github.com/cline/linear-mcp)
- **Associate issues with projects** to organize work [mcpservers](https://mcpservers.org/servers/timottowitz/linear-mcp)
- **Project milestone management** including creating, updating, and deleting milestones [github](https://github.com/dvcrn/mcp-server-linear)

## How It Works

The Linear MCP server bridges AI assistants and Linear's project management system through the Model Context Protocol. This allows you to interact with Linear programmatically through AI tools like Cursor, Cline, or other MCP-compatible clients. Instead of manually switching between your development environment and Linear's web interface, you can ask your AI assistant to create projects, update issue statuses, or query project data directly. [builder](https://www.builder.io/blog/linear-mcp-server)

The server uses Linear's GraphQL API and supports both legacy description fields and Linear's newer `documentContent` field for rich text descriptions. [github](https://github.com/cline/linear-mcp)

The error indicates that `npx` is not found in your system PATH. This is a common MCP server configuration issue on Windows where the Node.js executable paths aren't accessible to the MCP client. [github](https://github.com/smithery-ai/cli/issues/115)

## Quick Fixes

**Option 1: Install Node.js/npm**
If Node.js isn't installed, install it first. `npx` comes bundled with npm (Node Package Manager). [docs.qoder](https://docs.qoder.com/troubleshooting/mcp-common-issue)

**Option 2: Use absolute path to npx**
Instead of relying on PATH, specify the full path to `npx` in your MCP configuration: [ithy](https://ithy.com/article/npx-error-resolution-ybyttsd4)

1. Find where `npx` is installed by running in terminal:
   ```
   where npx
   ```
   This typically returns something like `C:\Program Files\nodejs\npx.cmd` [ithy](https://ithy.com/article/npx-error-resolution-ybyttsd4)

2. Update your MCP server configuration to use the full path instead of just `npx` [forum.cursor](https://forum.cursor.com/t/npx-command-is-not-working-on-mcp-windows-and-macos/53486)

**Option 3: Use node with npx-cli.js directly**
Replace the `npx` command with the full node path pointing to npx-cli.js: [github](https://github.com/cline/cline/issues/1247)
```
C:\Users\<username>\AppData\Roaming\npm\node_modules\npm\bin\npx-cli.js
```

## Windows-Specific Issues

Windows MCP servers often have PATH environment issues because GUI applications don't inherit terminal PATH configurations. The MCP client runs in a different environment than your shell, so even if `npx` works in your terminal, it may not be accessible to the MCP server process. [github](https://github.com/continuedev/continue/issues/4791)

You can verify `npx` works in your terminal by running `npx -v`. If it returns a version number but MCP still fails, you need to use the absolute path approach in your MCP configuration. [ithy](https://ithy.com/article/npx-error-resolution-ybyttsd4)

---

The error indicates that `npx` is not found in your system PATH. This is a common MCP server configuration issue on Windows where the Node.js executable paths aren't accessible to the MCP client. [github](https://github.com/smithery-ai/cli/issues/115)

## Quick Fixes

**Option 1: Install Node.js/npm**
If Node.js isn't installed, install it first. `npx` comes bundled with npm (Node Package Manager). [docs.qoder](https://docs.qoder.com/troubleshooting/mcp-common-issue)

**Option 2: Use absolute path to npx**
Instead of relying on PATH, specify the full path to `npx` in your MCP configuration: [ithy](https://ithy.com/article/npx-error-resolution-ybyttsd4)

1. Find where `npx` is installed by running in terminal:
   ```
   where npx
   ```
   This typically returns something like `C:\Program Files\nodejs\npx.cmd` [ithy](https://ithy.com/article/npx-error-resolution-ybyttsd4)

2. Update your MCP server configuration to use the full path instead of just `npx` [forum.cursor](https://forum.cursor.com/t/npx-command-is-not-working-on-mcp-windows-and-macos/53486)

**Option 3: Use node with npx-cli.js directly**
Replace the `npx` command with the full node path pointing to npx-cli.js: [github](https://github.com/cline/cline/issues/1247)
```
C:\Users\<username>\AppData\Roaming\npm\node_modules\npm\bin\npx-cli.js
```

## Windows-Specific Issues

Windows MCP servers often have PATH environment issues because GUI applications don't inherit terminal PATH configurations. The MCP client runs in a different environment than your shell, so even if `npx` works in your terminal, it may not be accessible to the MCP server process. [github](https://github.com/continuedev/continue/issues/4791)

You can verify `npx` works in your terminal by running `npx -v`. If it returns a version number but MCP still fails, you need to use the absolute path approach in your MCP configuration. [ithy](https://ithy.com/article/npx-error-resolution-ybyttsd4)

---

try normal full install options path first, if we stall within 10s i want to move to portable/manual install options

---

Yes! You have multiple options for installing Node.js locally on Windows:

## Winget (Recommended for Windows)

```bash
winget install OpenJS.NodeJS.LTS
```

This installs the Long Term Support version of Node.js along with npm and npx. You can also install the current release version with `winget install OpenJS.NodeJS`. After installation, verify with `node -v` and `npm -v`. [winget](https://winget.run/pkg/OpenJS/NodeJS)

## Python pip Install

You can install Node.js via Python's pip package manager: [pypi](https://pypi.org/project/nodejs-bin/)

```bash
pip install 'nodejs-bin[cmd]'
```

This installs Node.js and creates the `node`, `npm`, and `npx` command-line tools. Without the `[cmd]` option, you'd need to run them as: [pypi](https://pypi.org/project/nodejs-bin/)
```bash
python -m nodejs
python -m nodejs.npm
python -m nodejs.npx
```

You can specify a version with `pip install nodejs-bin==16.15.1`. [pypi](https://pypi.org/project/nodejs-bin/)

## Portable/Manual Install

If you want a fully portable version without system installation, you can download the Windows binaries directly from nodejs.org and extract them to any folder. Then either: [gist.github](https://gist.github.com/massahud/321a52f153e5d8f571be)
- Add that folder to your PATH
- Use the full path to `node.exe` and `npx` in your MCP configuration

Given your Windows environment and likely having winget available, the `winget install OpenJS.NodeJS.LTS` approach is cleanest and will ensure npx is properly in your PATH for the MCP server. [code-craft](https://code-craft.us/2025/05/13/winget-to-install-node-and-git/)