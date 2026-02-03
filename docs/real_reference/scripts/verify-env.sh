#!/bin/bash
# scripts/verify-env.sh

ENV=$1
if [ -z "$ENV" ]; then
  ENV="development"
fi

echo "🔍 Verifying $ENV environment..."

# 1. Check for wrangler.toml
if [ ! -f "wrangler.toml" ]; then
  echo "❌ Error: wrangler.toml not found"
  exit 1
fi

# 2. Check for register-commands config match
# Note: This is a simple grep check, could be more robust
APP_ID_VAR="DISCORD_APP_ID"
if [ "$ENV" == "development" ]; then
    APP_ID_VAR="DEV_DISCORD_APP_ID"
fi

echo "✅ App ID Variable: $APP_ID_VAR"

# 2.1 Check for AI Keys
if [ -z "$GEMINI_API_KEY" ] && [ -z "$GOOGLE_GENAI_API_KEY" ]; then
    # Try loading from .env if not in shell
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi
fi

if [ -z "$GEMINI_API_KEY" ] && [ -z "$GOOGLE_GENAI_API_KEY" ]; then
    echo "⚠️  Warning: AI Key (GEMINI/GOOGLE) not found. 'verify-ai' might fail."
else
    echo "✅ AI Key Detected"
fi

# 3. Check for Production Lock
if [ "$ENV" == "production" ]; then
    if [ -f ".prod-lock" ]; then
        echo "🚫 ERROR: Production deployment is LOCKED."
        cat .prod-lock
        exit 1
    fi
fi

# 4. Check for uncommitted changes if production
if [ "$ENV" == "production" ]; then
    if ! git diff-index --quiet HEAD --; then
        echo "⚠️  Warning: You have uncommitted changes. Deploying to production from a dirty state is risky."
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

# 4. Success message
echo "✨ Environment check passed for $ENV."
echo "You are safe to proceed with:"
if [ "$ENV" == "production" ]; then
    echo "  wrangler deploy --env production"
else
    echo "  wrangler deploy"
fi
