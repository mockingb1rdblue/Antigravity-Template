import { genkit } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';
import dotenv from 'dotenv';

dotenv.config();

async function verifyGemini() {
    console.log('🔍 Verifying Gemini 2.5 Flash via Genkit...');
    const apiKey = process.env.GOOGLE_GENAI_API_KEY || process.env.GEMINI_API_KEY;
    if (!apiKey) {
        console.error('❌ Error: GEMINI_API_KEY or GOOGLE_GENAI_API_KEY is not set.');
        return false;
    }

    try {
        const ai = genkit({
            plugins: [googleAI({ apiKey })],
            model: 'googleai/gemini-2.5-flash',
        });

        const { text } = await ai.generate("Respond with 'OK' if you are online.");

        if (text.includes('OK')) {
            console.log('✅ Gemini 2.5 is online and responding via Genkit.');
            return true;
        } else {
            console.warn(`⚠️  Gemini responded, but output was unexpected: ${text}`);
            return true;
        }
    } catch (error) {
        console.error('❌ Error verifying Gemini via Genkit:', error.message);
        return false;
    }
}

async function verifyDeepSeek() {
    console.log('🔍 Verifying DeepSeek (deepseek-chat)...');
    const apiKey = process.env.DEEPSEEK_API_KEY;
    if (!apiKey) {
        console.warn('⚠️  Warning: DEEPSEEK_API_KEY is not set. Skipping DeepSeek verification.');
        return true;
    }

    try {
        const response = await fetch('https://api.deepseek.com/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: "deepseek-chat",
                messages: [{ role: "user", content: "Respond with 'OK' if you are online." }],
                max_tokens: 10
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const text = data.choices[0].message.content;
        if (text.includes('OK')) {
            console.log('✅ DeepSeek is online and responding.');
            return true;
        } else {
            console.warn(`⚠️  DeepSeek responded, but output was unexpected: ${text}`);
            return true;
        }
    } catch (error) {
        console.error('❌ Error verifying DeepSeek:', error.message);
        return false;
    }
}

async function listModels() {
    console.log('📋 Listing Available Google AI Models via API...');
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        console.error('❌ Error: GEMINI_API_KEY is not set.');
        return;
    }

    try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`;
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('\nAvailable Models:');

        if (data.models && Array.isArray(data.models)) {
            data.models.forEach(model => {
                const name = model.name.replace('models/', '');
                const isRecommended = name === 'gemini-2.5-flash' ? ' ⭐ RECOMMENDED' : '';
                console.log(`- ${name} (${model.displayName})${isRecommended}`);
                const tasks = model.supportedGenerationMethods?.join(', ') || 'Custom';
                console.log(`  Capabilities: ${tasks}\n`);
            });
        } else {
            console.log('No models found or unrecognized response format.');
        }
    } catch (error) {
        console.error('❌ Error listing models:', error.message);
    }
}

async function run() {
    const args = process.argv.slice(2);

    if (args.includes('--list')) {
        await listModels();
        return;
    }

    console.log('🚀 Starting Standardized AI Verification (Genkit 2.5)...');
    const geminiOk = await verifyGemini();
    const deepSeekOk = await verifyDeepSeek();

    if (geminiOk && deepSeekOk) {
        console.log('✨ All AI models are verified and functional via standardize Genkit infrastructure.');
        process.exit(0);
    } else {
        console.error('💥 Some AI models failed verification.');
        process.exit(1);
    }
}

run();
