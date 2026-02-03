import { GoogleGenerativeAI } from '@google/generative-ai';

/**
 * Script to verify and list available Gemini models.
 * Usage: GEMINI_API_KEY=your_key npx ts-node scripts/verify-models.ts
 */
async function listModels() {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        console.error('❌ Error: GEMINI_API_KEY environment variable is not set.');
        process.exit(1);
    }

    try {
        console.log('📡 Fetching available models for your API key...');
        // Note: The Node.js SDK doesn't have a direct listModels method, 
        // so we use a fetch to the REST endpoint.
        const url = `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`;
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`API returned ${response.status}: ${response.statusText}`);
        }

        const data = await response.json() as any;
        console.log('\n✅ Available Models:');
        console.log('--------------------------------------------------');

        data.models.forEach((model: any) => {
            const isDeprecated = model.name.includes('1.0') || model.name.includes('vision');
            const status = isDeprecated ? '🚫 DEPRECATED' : '🟢 ACTIVE';

            console.log(`- ${model.name.padEnd(30)} | ${status}`);
            console.log(`  Description: ${model.description}`);
            console.log(`  Capabilities: ${model.supportedGenerationMethods.join(', ')}`);
            console.log('--------------------------------------------------');
        });

    } catch (error: any) {
        console.error('❌ Error fetching models:', error.message);
    }
}

listModels();
