#!/bin/bash

# Usage: ./scripts/apply-migration.sh <migration_file.sql> [environment]

FILE=$1
ENV=$2

if [ -z "$FILE" ]; then
  echo "Usage: ./scripts/apply-migration.sh <migration_file.sql> [environment]"
  exit 1
fi

DB_NAME="carpiggy-db-dev"
WRANGLER_FLAGS=""

if [ "$ENV" == "production" ]; then
  DB_NAME="carpiggy-db"
  WRANGLER_FLAGS="--remote"
  echo "🚀 Applying migration to PRODUCTION..."
else
  WRANGLER_FLAGS="--remote" # Default to remote dev for this project's setup
  echo "🧪 Applying migration to DEVELOPMENT..."
fi

npx wrangler d1 execute "$DB_NAME" --file="$FILE" $WRANGLER_FLAGS
