#!/bin/bash
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

echo "🔍 Running code quality checks..."
npm run lint
npm run type-check

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

echo "📊 Analyzing bundle..."
npm run analyze:bundle

echo "🔒 Running security audit..."
npm audit --audit-level moderate

echo "✅ Build completed successfully!"

# Generate build info
cat > dist/build-info.json << EOF
{
  "buildTime": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "gitCommit": "$(git rev-parse HEAD)",
  "gitBranch": "$(git rev-parse --abbrev-ref HEAD)",
  "nodeVersion": "$(node --version)",
  "npmVersion": "$(npm --version)",
  "environment": "${NODE_ENV:-development}"
}
EOF

echo "📄 Build info generated at dist/build-info.json"