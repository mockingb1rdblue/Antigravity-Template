import fs from 'fs';
import path from 'path';

const BANNED_PATTERNS = [
    { pattern: /gemini-2\.0/i, message: "❌ DEPRECATED: Gemini 2.0 is deprecated. Use 2.5-flash." },
    { pattern: /gemini-1\.5/i, message: "❌ DEPRECATED: Gemini 1.5 is legacy. Use 2.5-flash." },
    { pattern: /gemini-1\.0/i, message: "❌ DEPRECATED: Gemini 1.0 is legacy. Use 2.5-flash." },
    { pattern: /gemini-pro/i, message: "⚠️  WARNING: Generic 'gemini-pro' is ambiguous. Specify version." }
];

const ALLOWED_FILES = [
    'guard-models.mjs', // Self
    'README.md',       // Historical context acceptable
    'CHANGELOG.md',    // Historical context acceptable
    'history'          // Architecture decision records
];

function scanDirectory(dir) {
    let hasError = false;
    const files = fs.readdirSync(dir);

    for (const file of files) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
            if (file !== 'node_modules' && file !== '.git' && file !== 'dist') {
                if (scanDirectory(fullPath)) hasError = true;
            }
        } else {
            // Check allowed files
            if (ALLOWED_FILES.some(allowed => fullPath.includes(allowed))) continue;

            // Only scan source code and config, mostly
            if (!fullPath.match(/\.(ts|js|mjs|json|toml|md)$/)) continue;

            const content = fs.readFileSync(fullPath, 'utf-8');

            for (const { pattern, message } of BANNED_PATTERNS) {
                if (pattern.test(content)) {
                    console.error(`${message}\n    File: ${fullPath}`);
                    hasError = true;
                }
            }
        }
    }
    return hasError;
}

console.log("🛡️  Guarding against deprecated AI models...");
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');
const failed = scanDirectory(path.join(projectRoot, 'src')); // Primarily scan src

if (failed) {
    console.error("\n💥 Build Failed: Deprecated models detected in source code.\n   You must migrate to 'gemini-2.5-flash'.");
    process.exit(1);
} else {
    console.log("✅ Model hygiene passed.");
    process.exit(0);
}
