/**
 * Script to register Discord slash commands
 * Run this whenever you update command schemas
 * 
 * Usage:
 *   node scripts/register-commands.mjs [environment]
 *   
 * Examples:
 *   node scripts/register-commands.mjs development
 *   node scripts/register-commands.mjs production
 */

import 'dotenv/config';

const environment = process.argv[2] || 'development';

const config = {
    development: {
        appId: process.env.DEV_DISCORD_APP_ID,
        token: process.env.DEV_DISCORD_BOT_TOKEN,
        guildId: process.env.DEV_GUILD_ID // Optional: for guild-specific commands (faster updates)
    },
    production: {
        appId: process.env.DISCORD_APP_ID,
        token: process.env.DISCORD_BOT_TOKEN,
        publicKey: process.env.DISCORD_PUBLIC_KEY,
        guildId: null // Global commands
    }
};

const { appId, token, guildId } = config[environment];

if (!appId || !token) {
    console.error(`Missing credentials for ${environment} environment`);
    console.error(`Required: ${environment === 'development' ? 'DEV_DISCORD_APP_ID and DEV_DISCORD_BOT_TOKEN' : 'DISCORD_APP_ID and DISCORD_BOT_TOKEN'}`);
    process.exit(1);
}

const commands = [
    {
        name: 'createworld',
        description: 'Create a new game world with dedicated channels',
        options: [
            {
                name: 'name',
                description: 'Name of the world',
                type: 3, // STRING
                required: true
            },
            {
                name: 'setting',
                description: 'World setting/lore (e.g., "A dark forest where ancient magic lingers")',
                type: 3, // STRING
                required: false
            }
        ]
    },
    {
        name: 'deleteworld',
        description: 'Delete a game world and its channels',
        options: [
            {
                name: 'world',
                description: 'Select the world to delete',
                type: 3, // STRING
                required: true,
                autocomplete: true
            }
        ]
    },
    {
        name: 'join',
        description: 'Join the current world',
        options: [
            {
                name: 'character_name',
                description: 'Your character name',
                type: 3, // STRING
                required: true
            }
        ]
    },
    {
        name: 'commit',
        description: 'Commit your action for the current turn',
        options: [
            {
                name: 'action',
                description: 'What does your character do?',
                type: 3, // STRING
                required: true
            }
        ]
    },
    {
        name: 'cleanupguild',
        description: 'Remove orphaned world channels (admin cleanup)'
    },
    {
        name: 'status',
        description: 'Check the current turn status'
    },
    {
        name: 'character',
        description: 'Set your GURPS character stats',
        options: [
            {
                name: 'manual',
                description: 'Open a modal for manual stat entry',
                type: 1 // SUB_COMMAND
            },
            {
                name: 'auto',
                description: 'Automatically generate stats from a description',
                type: 1, // SUB_COMMAND
                options: [
                    {
                        name: 'description',
                        description: 'A brief description of your character (e.g. "a nimble elf archer")',
                        type: 3, // STRING
                        required: true
                    }
                ]
            },
            {
                name: 'visualize',
                description: 'Generate a portrait of your character (Phase 3)',
                type: 1, // SUB_COMMAND
                options: [
                    {
                        name: 'prompt',
                        description: 'Optional style override (e.g. "cyberpunk style", "oil painting")',
                        type: 3,
                        required: false
                    }
                ]
            }
        ]
    },
    {
        name: 'listworlds',
        description: 'List all active worlds in this server'
    },
    {
        name: 'admin',
        description: 'Administrative tools',
        options: [
            {
                name: 'sync',
                description: 'Sync Persistent State from Database (Restore Memory)',
                type: 1 // SUB_COMMAND
            }
        ]
    },
    {
        name: 'help',
        description: 'Get help with game mechanics and commands',
        options: [
            {
                name: 'topic',
                description: 'The topic you need help with',
                type: 3, // STRING
                required: false,
                autocomplete: true
            }
        ]
    }
];

async function registerCommands() {
    // Guild-specific commands (instant updates for dev) or global commands (for prod)
    const url = guildId
        ? `https://discord.com/api/v10/applications/${appId}/guilds/${guildId}/commands`
        : `https://discord.com/api/v10/applications/${appId}/commands`;

    console.log(`Registering commands for ${environment} environment...`);
    if (guildId) {
        console.log(`Using guild-specific registration (guild: ${guildId}) for instant updates`);
    } else {
        console.log('Using global registration (may take up to 1 hour to propagate)');
    }

    if (config[environment].publicKey) {
        console.log(`Verifying against Public Key: ${config[environment].publicKey.substring(0, 8)}...`);
    }

    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Authorization': `Bot ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(commands)
    });

    if (!response.ok) {
        const error = await response.text();
        console.error('Failed to register commands:', error);
        process.exit(1);
    }

    const registered = await response.json();
    console.log(`✅ Successfully registered ${registered.length} commands!`);
    console.log('\nRegistered commands:');
    registered.forEach(cmd => {
        console.log(`  - /${cmd.name}: ${cmd.description}`);
        if (cmd.options) {
            cmd.options.forEach(opt => {
                const required = opt.required ? '(required)' : '(optional)';
                console.log(`    - ${opt.name} ${required}: ${opt.description}`);
            });
        }
    });
    console.log('\n⚠️  Note: Global commands may take up to 1 hour to propagate to all servers.');
    console.log('For instant updates during development, consider using guild-specific commands instead.');
}

registerCommands().catch(console.error);
