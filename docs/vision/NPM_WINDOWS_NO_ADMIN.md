# Setting up Node.js and npm on Windows without Admin Rights

Here are multiple options for using Node.js on Windows without admin rights:

## Option 1: Portable Node.js Binary (Simplest)

**Download and extract** the Windows binary `.zip` file from nodejs.org: [stackoverflow](https://stackoverflow.com/questions/37029089/how-to-install-nodejs-lts-on-windows-as-a-local-user-without-admin-rights)

1. Go to https://nodejs.org/en/download/ → "Windows Binary (.zip)" [gkarthiks.github](https://gkarthiks.github.io/quick-commands-cheat-sheet/nodeJS-in-windows.html)
2. Download the appropriate version (x64 or x86)
3. Extract to a user-writable location like `C:\Users\YourName\nodejs` or `%USERPROFILE%\bin\nodejs` [zwbetz](https://zwbetz.com/install-nodejs-on-windows-without-admin-access/)

**Add to user PATH** (no admin required):

Method 1 - Command line:
```cmd
setx NODEJS_HOME "%USERPROFILE%\nodejs\node-v20.11.0-win-x64"
setx PATH "%NODEJS_HOME%;%PATH%"
```


Method 2 - GUI:
1. Press `Win+R` and run: `rundll32 sysdm.cpl,EditEnvironmentVariables` [stackoverflow](https://stackoverflow.com/questions/37029089/how-to-install-nodejs-lts-on-windows-as-a-local-user-without-admin-rights)
2. In the **User variables** section (top window), find `Path` and click Edit [stackoverflow](https://stackoverflow.com/questions/37029089/how-to-install-nodejs-lts-on-windows-as-a-local-user-without-admin-rights)
3. Click New and add your Node.js folder path [stackoverflow](https://stackoverflow.com/questions/37029089/how-to-install-nodejs-lts-on-windows-as-a-local-user-without-admin-rights)
4. Click OK

**Verify installation** (restart cmd first):
```cmd
node -v
npm -v
npx -v
```

The `.zip` download includes node.exe, npm, and npx. [stackoverflow](https://stackoverflow.com/questions/37029089/how-to-install-nodejs-lts-on-windows-as-a-local-user-without-admin-rights)

## Option 2: Batch File Launcher (No PATH changes)

Create a batch file in your Node.js folder: [youtube](https://www.youtube.com/watch?v=BLnbtsDIW_E)

**nodeenv.bat:**
```batch
@echo off
PATH %~dp0;%PATH%;
cmd
```

Double-click this file to open a command prompt with Node.js available. You can then run npm/npx commands from that window, or launch VS Code from there. [youtube](https://www.youtube.com/watch?v=BLnbtsDIW_E)

## Option 3: NVM for Windows (User-level)

**PowerShell install script** (no admin): [gist.github](https://gist.github.com/rajeshkumaravel/285625f028b5a909b545a53f53c38239)

```powershell
cd $Env:USERPROFILE;
Invoke-WebRequest https://raw.githubusercontent.com/jchip/nvm/v1.5.4/install.ps1 -OutFile install.ps1;
.\install.ps1 -nvmhome $Env:USERPROFILE\nvm;
del install.ps1
```

This installs NVM (Node Version Manager) to your user profile, allowing you to manage multiple Node.js versions. [gist.github](https://gist.github.com/rajeshkumaravel/285625f028b5a909b545a53f53c38239)

**Usage:**
```cmd
nvm install lts
nvm use lts
```

**Note**: Some NVM implementations require admin for the `nvm use` command. The script above uses a version designed for user-level access. [dev](https://dev.to/yougotwill/portable-nodejs-without-administrator-access-1elk)

## Option 4: Node Portable (Pre-configured)

**Clone and run** this GitHub repository: [github](https://github.com/corentindesfarges/node-portable)

```cmd
git clone https://github.com/corentindesfarges/node-portable.git
cd node-portable
run.bat
```

This script automatically downloads and configures portable Node.js. You can specify versions: `run.bat 20.11.0`. [github](https://github.com/corentindesfarges/node-portable)

## Option 5: Python pip Method

If you have Python installed as a user (no admin):

```bash
pip install 'nodejs-bin[cmd]' --user
```

This installs Node.js binaries to your Python user directory and creates `node`, `npm`, and `npx` commands. [pypi](https://pypi.org/project/nodejs-bin/)

## For MCP Configuration

Since you're using this for Linear MCP, after installing with any option above:

**If npx still isn't found by MCP**, use absolute paths in your config:

1. Find npx location:
```cmd
where npx
```

2. Use full path in MCP config:
```json
{
  "linear": {
    "command": "C:\\Users\\YourName\\nodejs\\node-v20.11.0-win-x64\\npx.cmd",
    "args": ["-y", "@modelcontextprotocol/server-linear"],
    "env": {
      "LINEAR_API_KEY": "your_api_key"
    }
  }
}
```

## Recommended Approach for Your Setup

Given your technical background and likely constraints on the antigravity machine:

1. **Download the portable .zip** from nodejs.org (requires no installation)
2. **Extract to** `%USERPROFILE%\bin\nodejs` or similar user-writable location
3. **Use the batch file method** for immediate access without PATH changes
4. **Configure MCP with absolute paths** to avoid PATH inheritance issues

This gives you full control without admin rights and works reliably with MCP servers that have PATH issues. [zwbetz](https://zwbetz.com/install-nodejs-on-windows-without-admin-access/)
