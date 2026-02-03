# Node.js and npm on Windows (No Admin)

For setup instructions on installing Node.js and npm on Windows without administrator privileges, see [NPM_WINDOWS_NO_ADMIN.md](file:///c:/Users/ad9840724/OneDrive%20-%20Nutrien/Documents/My%20Role/01_DEVELOPMENT_LAB/MCP_Foundation/NPM_WINDOWS_NO_ADMIN.md).

---

Here are multiple options for installing Node.js on Mac without sudo/admin rights:

## Option 1: NVM (Node Version Manager) - Recommended

**Install NVM** (no sudo required): [stackoverflow](https://stackoverflow.com/questions/55939943/how-do-you-download-node-js-on-mac-without-admin)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

Or using wget:
```bash
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

**Configure shell** (NVM auto-adds to `~/.bashrc`, but Mac uses zsh by default): [blog.stackademic](https://blog.stackademic.com/how-to-use-nvm-install-and-switch-specific-node-js-version-on-macos-909169fd7dcb)

For zsh (default on modern macOS):
```bash
vi ~/.zshrc
```

Add these lines:
```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

**Reload shell:**
```bash
source ~/.zshrc
```

**Verify NVM:**
```bash
nvm --version
```

**Install Node.js:**
```bash
nvm install --lts
nvm use --lts
nvm alias default lts/*
```

**Verify Node installation:**
```bash
node -v
npm -v
npx -v
```

### NVM Troubleshooting

**Issue**: Permission denied during NVM install [4geeks](https://4geeks.com/how-to/install-node-nvm-mac-osx)

**Solution**: Check `.nvm` directory permissions:
```bash
ls -la ~/.nvm
chmod -R u+w ~/.nvm
```

**Issue**: Command not found after install [blog.stackademic](https://blog.stackademic.com/how-to-use-nvm-install-and-switch-specific-node-js-version-on-macos-909169fd7dcb)

**Solution**: Ensure you're editing the correct shell config (`.zshrc` for zsh, `.bash_profile` for bash):
```bash
echo $SHELL
```

## Option 2: Direct Binary Download (Portable)

**Download and extract** Node.js binary: [groups.google](https://groups.google.com/g/nodejs/c/cUPqPV8x_KU)

1. Download `.tar.gz` from https://nodejs.org/en/download/
2. Extract to user directory:

```bash
cd ~/
mkdir nodejs
cd nodejs
curl -O https://nodejs.org/dist/v20.11.0/node-v20.11.0-darwin-x64.tar.gz
tar -xzf node-v20.11.0-darwin-x64.tar.gz
```

**Add to PATH** in `~/.zshrc` or `~/.bash_profile`:
```bash
export PATH="$HOME/nodejs/node-v20.11.0-darwin-x64/bin:$PATH"
```

**Reload shell:**
```bash
source ~/.zshrc
```

## Option 3: Compile from Source (User Directory)

**Download and compile** to `~/local`: [groups.google](https://groups.google.com/g/nodejs/c/cUPqPV8x_KU)

```bash
cd ~/Downloads
curl -O https://nodejs.org/dist/v20.11.0/node-v20.11.0.tar.gz
tar -xzf node-v20.11.0.tar.gz
cd node-v20.11.0

./configure --prefix=$HOME/local
make
make install
```

**Add to PATH** in `~/.zshrc`:
```bash
export PATH="$HOME/local/bin:$PATH"
```

**Reload:**
```bash
source ~/.zshrc
```

This requires Xcode Command Line Tools (installable without admin): `xcode-select --install` [stackoverflow](https://stackoverflow.com/questions/55939943/how-do-you-download-node-js-on-mac-without-admin)

## Option 4: Configure npm for User-Level Global Packages

If you have Node.js installed but npm requires sudo, reconfigure npm: [johnpapa](https://www.johnpapa.net/how-to-use-npm-global-without-sudo-on-osx/)

**Create user npm directory:**
```bash
mkdir "${HOME}/.npm-packages"
```

**Configure npm to use it:**
```bash
npm config set prefix "${HOME}/.npm-packages"
```

**Add to PATH** in `~/.zshrc`:
```bash
export NPM_PACKAGES="${HOME}/.npm-packages"
export PATH="$NPM_PACKAGES/bin:$PATH"
```

**Reload:**
```bash
source ~/.zshrc
```

Now `npm install -g` commands won't require sudo. [codestaff](https://www.codestaff.io/blog/how-to-use-install-npm-packages-without-sudo-on-linux-and-macos/)

## Option 5: Homebrew in User Directory (Advanced)

**Install Homebrew without sudo**: [scivision](https://www.scivision.dev/macos-homebrew-non-sudo/)

```bash
mkdir ~/homebrew
curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C ~/homebrew
```

**Add to PATH** in `~/.zshrc`:
```bash
export PATH="$HOME/homebrew/bin:$PATH"
```

**Install Node.js:**
```bash
brew install node
```

**Note**: Standard Homebrew installation requires initial sudo, but this user-directory method doesn't. However, NVM is simpler for most use cases. [scivision](https://www.scivision.dev/macos-homebrew-non-sudo/)

## For MCP Configuration on Mac

After installing with any method above, if MCP can't find npx:

**Find npx location:**
```bash
which npx
```

**Use absolute path in MCP config:**
```json
{
  "linear": {
    "command": "/Users/yourusername/.nvm/versions/node/v20.11.0/bin/npx",
    "args": ["-y", "@modelcontextprotocol/server-linear"],
    "env": {
      "LINEAR_API_KEY": "your_api_key"
    }
  }
}
```

Or add PATH explicitly:
```json
{
  "linear": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-linear"],
    "env": {
      "LINEAR_API_KEY": "your_api_key",
      "PATH": "/Users/yourusername/.nvm/versions/node/v20.11.0/bin:$PATH"
    }
  }
}
```

## Recommended Approach for Mac

**Use NVM** - it's the most flexible, requires no sudo, and allows easy version switching: [4geeks](https://4geeks.com/how-to/install-node-nvm-mac-osx)

1. Install NVM via curl command
2. Add NVM config to `~/.zshrc`
3. Install Node.js LTS with `nvm install --lts`
4. Set as default with `nvm alias default lts/*`
5. Use absolute path in MCP config if needed

This gives you full Node.js control in your user directory without any admin permissions required.

---

Here are comprehensive installation options for Mac when you have admin/sudo access:

## Option 1: Homebrew (Simplest for Admin Users)

**Install Homebrew** (if not already installed): [treehouse.github](https://treehouse.github.io/installation-guides/mac/node-mac.html)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Install Node.js:**

Latest version:
```bash
brew install node
```

LTS version (recommended):
```bash
brew install node@20
```

If installing an LTS version, you need to link it: [youtube](https://www.youtube.com/watch?v=O6MKC5TgQao)
```bash
brew link --force node@20
```

Or add to PATH in `~/.zshrc`:
```bash
export PATH="/usr/local/opt/node@20/bin:$PATH"
```

**Verify installation:**
```bash
node -v
npm -v
npx -v
```

**Update Node.js later:**
```bash
brew upgrade node
```

**Uninstall if needed:**
```bash
brew uninstall node
brew autoremove
```

## Option 2: NVM via Homebrew (Best for Version Management)

**Install NVM with Homebrew**: [youtube](https://www.youtube.com/watch?v=0LWJ3gmScUY)
```bash
brew install nvm
```

**Create NVM directory:**
```bash
mkdir ~/.nvm
```

**Add to shell config** (`~/.zshrc`):
```bash
export NVM_DIR="$HOME/.nvm"
[ -s "/usr/local/opt/nvm/nvm.sh" ] && \. "/usr/local/opt/nvm/nvm.sh"
[ -s "/usr/local/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/usr/local/opt/nvm/etc/bash_completion.d/nvm"
```

**Reload shell:**
```bash
source ~/.zshrc
```

**Install Node.js:**
```bash
nvm install --lts
nvm use --lts
nvm alias default lts/*
```

**Verify:**
```bash
node -v
npm -v
npx -v
```

## Option 3: NVM Direct Install (Recommended by Most Developers)

**Install NVM** (doesn't require sudo despite having it): [stackoverflow](https://stackoverflow.com/questions/55939943/how-do-you-download-node-js-on-mac-without-admin)
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

**Add to `~/.zshrc`:**
```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

**Install Node.js:**
```bash
nvm install --lts
nvm use --lts
nvm alias default lts/*
```

## Option 4: Official .pkg Installer

**Download from nodejs.org**: [youtube](https://www.youtube.com/watch?v=0LWJ3gmScUY)
1. Visit https://nodejs.org
2. Download LTS version `.pkg` file
3. Run installer with admin privileges
4. Follow installation prompts

**Verify:**
```bash
node -v
npm -v
npx -v
```

## Option 5: n (Node Version Manager via npm)

**Install n with Homebrew**: [youtube](https://www.youtube.com/watch?v=O6MKC5TgQao)
```bash
brew install n
```

Or with npm after installing Node via any method:
```bash
sudo npm install -g n
```

**Fix permissions** (if needed): [youtube](https://www.youtube.com/watch?v=O6MKC5TgQao)
```bash
sudo mkdir -p /usr/local/n && sudo chown -R $(whoami) /usr/local/n
```

**Install Node.js versions:**
```bash
sudo n lts
sudo n latest
sudo n 18.17.0
```

**Switch versions interactively:**
```bash
n
```
Use arrow keys to select, Enter to activate, `d` to delete, `q` to quit. [youtube](https://www.youtube.com/watch?v=O6MKC5TgQao)

**List remote versions:**
```bash
n ls-remote lts
n ls-remote latest
```

## Homebrew vs NVM Comparison

| Feature | Homebrew | NVM |
|---------|----------|-----|
| Version switching | Single version installed at a time | Multiple versions, easy switching  [reddit](https://www.reddit.com/r/webdev/comments/12hq3ol/nvm_or_homebrew_for_node_install/) |
| Installation | System-wide via `/usr/local` | User-specific in `~/.nvm`  [stackshare](https://stackshare.io/stackups/homebrew-vs-nvm) |
| Updates | `brew upgrade node` | `nvm install <version>` per version |
| Cross-platform | macOS only  [stackshare](https://stackshare.io/stackups/homebrew-vs-nvm) | macOS, Linux, Windows  [stackshare](https://stackshare.io/stackups/homebrew-vs-nvm) |
| Integration | Deep macOS ecosystem integration  [stackshare](https://stackshare.io/stackups/homebrew-vs-nvm) | Node.js focused workflow  [stackshare](https://stackshare.io/stackups/homebrew-vs-nvm) |
| Best for | Single version, system consistency | Multiple projects with different Node versions  [reddit](https://www.reddit.com/r/webdev/comments/12hq3ol/nvm_or_homebrew_for_node_install/) |

## Recommended Approach with Admin Access

**For most developers**: Use NVM (Option 2 or 3) [reddit](https://www.reddit.com/r/webdev/comments/12hq3ol/nvm_or_homebrew_for_node_install/)
- Allows multiple Node.js versions for different projects
- No sudo required for installing global packages
- Easy version switching
- Works consistently across platforms

**For simple single-version needs**: Use Homebrew (Option 1) [treehouse.github](https://treehouse.github.io/installation-guides/mac/node-mac.html)
- Fast, simple installation
- Integrates well with other Homebrew packages
- Easy updates with `brew upgrade`

**Avoid mixing**: Don't install Node via both Homebrew and NVM simultaneously - it causes PATH conflicts [stackoverflow](https://stackoverflow.com/questions/28017374/what-is-the-recommended-way-to-install-node-js-nvm-and-npm-on-macos-x)

## Configure npm to Avoid Sudo for Global Packages

Even with admin access, you should configure npm to install global packages without sudo: [johnpapa](https://www.johnpapa.net/how-to-use-npm-global-without-sudo-on-osx/)

```bash
mkdir "${HOME}/.npm-packages"
npm config set prefix "${HOME}/.npm-packages"
```

Add to `~/.zshrc`:
```bash
export NPM_PACKAGES="${HOME}/.npm-packages"
export PATH="$NPM_PACKAGES/bin:$PATH"
```

## For MCP Configuration

After installation, find npx location:
```bash
which npx
```

Use in MCP config (example paths):
```json
{
  "linear": {
    "command": "/usr/local/bin/npx",
    "args": ["-y", "@modelcontextprotocol/server-linear"],
    "env": {
      "LINEAR_API_KEY": "your_api_key"
    }
  }
}
```

Or for NVM installation:
```json
{
  "linear": {
    "command": "/Users/yourusername/.nvm/versions/node/v20.11.0/bin/npx",
    "args": ["-y", "@modelcontextprotocol/server-linear"],
    "env": {
      "LINEAR_API_KEY": "your_api_key"
    }
  }
}
```

---
Here's a thin-sliced, logical sequence for creating an MCP server foundation on Cloudflare:

## Step 1: Install Wrangler CLI

Wrangler is Cloudflare's CLI tool for Workers: [natoma](https://natoma.ai/blog/how-to-deploy-mcp-server-to-cloudflare-workers)

```bash
npm install -g wrangler
```

**Verify installation:**
```bash
wrangler --version
```

### Troubleshooting Step 1:
- **Permission errors**: Use `npm install -g wrangler --prefix=$HOME/.npm-packages` (Mac/Linux) or install without `-g` flag
- **Command not found**: Ensure npm global bin is in PATH (`npm config get prefix` to check location)

## Step 2: Authenticate with Cloudflare

Login to your Cloudflare account: [speakeasy](https://www.speakeasy.com/docs/standalone-mcp/cloudflare-deployment)

```bash
wrangler login
```

This opens a browser window for OAuth authentication. [speakeasy](https://www.speakeasy.com/docs/standalone-mcp/cloudflare-deployment)

**Alternative - API Token method:**
```bash
wrangler login --api-token YOUR_API_TOKEN
```

### Troubleshooting Step 2:
- **Browser doesn't open**: Manually visit the URL shown in terminal
- **Account selection**: Ensure you're logging into the correct Cloudflare account
- **Token issues**: Generate new API token at https://dash.cloudflare.com/profile/api-tokens

## Step 3: Create MCP Project from Template

**Option A - Use Cloudflare's official template** (easiest): [developers.cloudflare](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)

```bash
npm create cloudflare@latest -- my-mcp-server --template=cloudflare/ai/demos/remote-mcp-authless
```

This creates a project with:
- Pre-configured MCP server
- Streamable HTTP transport setup
- Basic wrangler configuration
- No authentication (add later if needed)

**Option B - Start from scratch**: [natoma](https://natoma.ai/blog/how-to-deploy-mcp-server-to-cloudflare-workers)

```bash
mkdir my-mcp-server
cd my-mcp-server
npm init -y
```

### Troubleshooting Step 3:
- **Template download fails**: Check internet connection, try option B
- **npm create errors**: Update npm with `npm install -g npm@latest`
- **Permission denied**: Use `sudo` or run from user-writable directory

## Step 4: Install Required Dependencies

Navigate into your project:
```bash
cd my-mcp-server
```

**Install core MCP and Cloudflare packages**: [natoma](https://natoma.ai/blog/how-to-deploy-mcp-server-to-cloudflare-workers)

```bash
npm install @modelcontextprotocol/sdk
npm install @cloudflare/workers-types --save-dev
npm install agents
```

### Troubleshooting Step 4:
- **Package not found**: Verify package names and versions on npm
- **Dependency conflicts**: Use `npm install --legacy-peer-deps`
- **Network errors**: Check firewall/proxy settings

## Step 5: Create Worker Script

Create `src/index.ts` (or appropriate location): [blog.cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // Create MCP server instance
    const server = new McpServer({
      name: "my-mcp-server",
      version: "1.0.0",
    });

    // Add a simple tool
    server.tool(
      "hello",
      "Say hello",
      { name: z.string().optional() },
      async (params) => {
        return {
          content: [{
            type: "text",
            text: `Hello ${params.name || "World"}!`
          }]
        };
      }
    );

    // Handle MCP requests at /sse endpoint
    if (url.pathname === "/sse") {
      return server.handleRequest(request);
    }

    // Default response
    return new Response("MCP Server Running", { status: 200 });
  }
};
```

### Troubleshooting Step 5:
- **TypeScript errors**: Install `typescript` with `npm install typescript --save-dev`
- **Import errors**: Check package installation, verify import paths
- **Syntax errors**: Use editor with TypeScript support (VS Code, Cursor)

## Step 6: Create Wrangler Configuration

Create `wrangler.jsonc` in project root: [speakeasy](https://www.speakeasy.com/docs/standalone-mcp/cloudflare-deployment)

```jsonc
{
  "name": "my-mcp-server",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-01",
  "node_compat": true,
  "workers_dev": true
}
```

### Troubleshooting Step 6:
- **Invalid JSON**: Ensure no trailing commas, proper quotes
- **Name conflicts**: Choose unique worker name
- **Compatibility date**: Use recent date in YYYY-MM-DD format

## Step 7: Test Locally

Start local development server: [wanglong](https://wanglong.cv/articles/deploying-remote-mcp-server-cloudflare/)

```bash
npm start
```

Or:
```bash
wrangler dev
```

Server runs at `http://localhost:8787/sse`. [wanglong](https://wanglong.cv/articles/deploying-remote-mcp-server-cloudflare/)

**Test with MCP Inspector**: [developers.cloudflare](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)

```bash
npx @modelcontextprotocol/inspector
```

Connect to `http://localhost:8787/sse` in the inspector. [developers.cloudflare](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)

### Troubleshooting Step 7:
- **Port already in use**: Kill process on port 8787 or use `wrangler dev --port 8788`
- **Server won't start**: Check syntax errors in code, review wrangler logs
- **MCP Inspector connection fails**: Verify endpoint URL, check CORS if needed

## Step 8: Deploy to Cloudflare

Deploy your MCP server: [natoma](https://natoma.ai/blog/how-to-deploy-mcp-server-to-cloudflare-workers)

```bash
npx wrangler deploy
```

This builds and deploys to Cloudflare's network. [speakeasy](https://www.speakeasy.com/mcp/deploying-mcp-servers)

**Note the deployment URL** (example: `https://my-mcp-server.your-account.workers.dev`). [speakeasy](https://www.speakeasy.com/docs/standalone-mcp/cloudflare-deployment)

### Troubleshooting Step 8:
- **Authentication failed**: Re-run `wrangler login`
- **Build errors**: Fix TypeScript/code errors, check build logs
- **Deployment timeout**: Check network, try again
- **Worker name conflict**: Change name in `wrangler.jsonc`

## Step 9: Configure MCP Client

**For Claude Desktop, Cursor, or similar**: [youtube](https://www.youtube.com/watch?v=PgSoTSg6bhY)

Add to your MCP client config (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "my-cloudflare-mcp": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://my-mcp-server.your-account.workers.dev/sse"
      ]
    }
  }
}
```

The `mcp-remote` package acts as an adapter for clients that don't natively support remote MCP servers. [blog.cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)

### Troubleshooting Step 9:
- **Client doesn't recognize server**: Restart MCP client completely
- **Connection errors**: Verify deployment URL is correct and accessible
- **npx not found**: Use absolute path to npx from earlier setup

## Step 10: Test Remote Connection

Restart your MCP client and verify:
- Server appears in available tools
- Can execute tools (like the "hello" example)
- Check Cloudflare dashboard logs for requests [youtube](https://www.youtube.com/watch?v=PgSoTSg6bhY)

**View logs:**
```bash
wrangler tail
```

Or visit Cloudflare dashboard → Workers & Pages → Your worker → Logs. [youtube](https://www.youtube.com/watch?v=PgSoTSg6bhY)

### Troubleshooting Step 10:
- **Server not appearing**: Check client config syntax, verify server is deployed
- **Tool execution fails**: Review server logs with `wrangler tail`
- **Authentication errors**: Add auth later (see Step 11)

## Optional Step 11: Add Authentication

For production, add OAuth authentication: [blog.cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)

```bash
npm install @cloudflare/workers-oauth-provider
```

Update your worker to use OAuth Provider wrapper: [blog.cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)

```typescript
import { OAuthProvider } from "@cloudflare/workers-oauth-provider";
import MyMCPServer from "./my-mcp-server";
import MyAuthHandler from "./auth-handler";

export default new OAuthProvider({
  apiRoute: "/sse",
  apiHandler: MyMCPServer.mount('/sse'),
  defaultHandler: MyAuthHandler,
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/token",
  clientRegistrationEndpoint: "/register",
});
```

Follow the full authentication guide at. [developers.cloudflare](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)

## Next Steps

- Add more tools and resources to your MCP server
- Configure KV namespace for state storage [developers.cloudflare](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)
- Set up environment variables in Cloudflare dashboard
- Implement proper error handling and logging
- Add rate limiting and security measures

This foundation gives you a working remote MCP server that can scale globally on Cloudflare's edge network. [blog.cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)