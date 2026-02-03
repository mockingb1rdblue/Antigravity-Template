const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function estimateTokens(text) {
    // Rough heuristic: 4 characters per token
    return Math.ceil(text.length / 4);
}

function getTrackedFiles() {
    try {
        // -c: cached (tracked)
        // -o: others (untracked)
        // --exclude-standard: apply .gitignore rules to -o
        // This combination gets all files that git knows about OR that are present and not ignored.
        const output = execSync('git ls-files -c -o --exclude-standard', { maxBuffer: 10 * 1024 * 1024, encoding: 'utf-8' });
        return output.split('\n').filter(line => line.trim().length > 0);
    } catch (error) {
        console.error("Error executing git command:", error);
        process.exit(1);
    }
}

function aggregateFiles() {
    console.log("Gathering file list...");
    const allFiles = getTrackedFiles();

    const mdFiles = [];
    const tsFiles = [];

    // Filter files
    allFiles.forEach(file => {
        // Normalize path separators
        const normalizedPath = file.split(path.sep).join('/');

        // Exclusion check
        if (normalizedPath.startsWith('docs/brain')) {
            return;
        }

        if (normalizedPath.endsWith('.md')) {
            mdFiles.push(file);
        } else if (normalizedPath.endsWith('.ts')) {
            tsFiles.push(file);
        }
    });

    console.log(`Found ${mdFiles.length} Markdown files.`);
    console.log(`Found ${tsFiles.length} TypeScript files.`);

    // Process MD files
    processBatch(mdFiles, 'MD_MASS.md');

    // Process TS files
    processBatch(tsFiles, 'TS_MASS.md');
}

function processBatch(files, outputFilename) {
    let combinedContent = "";
    let fileCount = 0;

    files.sort(); // Sort for deterministic output

    for (const filePath of files) {
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            const fileHeader = `\n\n================================================================================\n=== File: ${filePath} ===\n================================================================================\n\n`;
            combinedContent += fileHeader + content;
            fileCount++;
        } catch (err) {
            console.error(`Warning: Could not read file ${filePath}: ${err.message}`);
        }
    }

    const totalTokens = estimateTokens(combinedContent);
    const header = `# MASS AGGREGATION FILE: ${outputFilename}
# Generated: ${new Date().toISOString()}
# Total Files: ${fileCount}
# Approximate Token Count: ${totalTokens.toLocaleString()} (based on char_count / 4)
# --------------------------------------------------------------------------------\n`;

    const finalOutput = header + combinedContent;

    fs.writeFileSync(outputFilename, finalOutput, 'utf-8');
    console.log(`Successfully wrote ${outputFilename} (${totalTokens.toLocaleString()} estimated tokens).`);
}

aggregateFiles();
