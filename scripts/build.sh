#!/bin/bash

# Build script for CI/CD pipeline
set -e

echo "🚀 Starting build process..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "📦 Installing dependencies..."
npm ci

echo "🔍 Running linting..."
npm run lint

echo "🧪 Running tests..."
npm run test

echo "🏗️ Building application..."
if [ "$NODE_ENV" = "production" ]; then
    npm run build:production
elif [ "$NODE_ENV" = "staging" ]; then
    npm run build:staging
else
    npm run build
fi

echo "📊 Generating build report..."
npm run analyze:bundle

echo "✅ Build completed successfully!"

# Create build info
cat > dist/build-info.json << EOF
{
  "buildTime": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "gitCommit": "${GITHUB_SHA:-$(git rev-parse HEAD)}",
  "gitBranch": "${GITHUB_REF_NAME:-$(git branch --show-current)}",
  "nodeVersion": "$(node --version)",
  "npmVersion": "$(npm --version)",
  "environment": "${NODE_ENV:-development}"
}
EOF

echo "📄 Build info created at dist/build-info.json"