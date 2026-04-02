#!/bin/bash

# Build script for the application
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
npm run build

echo "📊 Analyzing bundle size..."
npm run analyze:bundle

echo "🔒 Running security audit..."
npm audit --audit-level high

echo "✅ Build completed successfully!"

# Create build info file
cat > dist/build-info.json << EOF
{
  "buildTime": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "gitCommit": "$(git rev-parse HEAD)",
  "gitBranch": "$(git rev-parse --abbrev-ref HEAD)",
  "nodeVersion": "$(node --version)",
  "npmVersion": "$(npm --version)"
}
EOF

echo "📝 Build info saved to dist/build-info.json"