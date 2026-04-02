#!/bin/bash

# Test script for the application
set -e

echo "🧪 Starting test suite..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi

echo "📦 Installing dependencies..."
npm ci

echo "🔍 Running linting..."
npm run lint

echo "📝 Running type checking..."
npm run type-check

echo "🧪 Running unit tests..."
npm run test:unit -- --coverage

echo "🔗 Running integration tests..."
npm run test:integration

echo "♿ Running accessibility tests..."
npm run test:a11y

echo "🔒 Running security tests..."
npm audit --audit-level high

echo "📊 Generating test reports..."
mkdir -p reports

# Generate coverage report
if [ -d "coverage" ]; then
    cp -r coverage reports/
    echo "📈 Coverage report available at reports/coverage/index.html"
fi

# Generate test results summary
cat > reports/test-summary.md << EOF
# Test Results Summary

## Test Execution
- **Date**: $(date)
- **Node Version**: $(node --version)
- **npm Version**: $(npm --version)
- **Git Commit**: $(git rev-parse HEAD)

## Test Status
✅ All tests passed successfully!

## Coverage
See detailed coverage report in the coverage directory.

## Security Audit
No high-severity vulnerabilities found.
EOF

echo "✅ All tests completed successfully!"
echo "📊 Test reports available in the reports/ directory"