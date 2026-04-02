#!/bin/bash

# Deployment script for CI/CD pipeline
set -e

# Configuration
ENVIRONMENT=${1:-staging}
APP_NAME="user-auth-system"
DOCKER_IMAGE="${DOCKER_REGISTRY}/${APP_NAME}:${GITHUB_SHA:-latest}"

echo "🚀 Starting deployment to ${ENVIRONMENT}..."

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo "❌ Invalid environment: $ENVIRONMENT"
    echo "Valid environments: staging, production"
    exit 1
fi

# Check required environment variables
required_vars=("DOCKER_REGISTRY" "DEPLOY_HOST" "DEPLOY_USER")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Required environment variable $var is not set"
        exit 1
    fi
done

echo "🐳 Building Docker image..."
docker build -f Dockerfile.production -t "$DOCKER_IMAGE" .

echo "📤 Pushing Docker image to registry..."
docker push "$DOCKER_IMAGE"

echo "🔄 Deploying to ${ENVIRONMENT} server..."
ssh -o StrictHostKeyChecking=no "${DEPLOY_USER}@${DEPLOY_HOST}" << EOF
    set -e
    
    echo "📥 Pulling latest image..."
    docker pull "$DOCKER_IMAGE"
    
    echo "🛑 Stopping existing containers..."
    docker-compose -f docker-compose.${ENVIRONMENT}.yml down || true
    
    echo "🔄 Starting new containers..."
    export DOCKER_IMAGE="$DOCKER_IMAGE"
    docker-compose -f docker-compose.${ENVIRONMENT}.yml up -d
    
    echo "🧹 Cleaning up old images..."
    docker system prune -f
    
    echo "✅ Deployment completed!"
EOF

# Health check
echo "🏥 Performing health check..."
sleep 30

if [ "$ENVIRONMENT" = "production" ]; then
    HEALTH_URL="$PRODUCTION_URL/health"
else
    HEALTH_URL="$STAGING_URL/health"
fi

if curl -f "$HEALTH_URL" > /dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "❌ Health check failed!"
    exit 1
fi

echo "🎉 Deployment to ${ENVIRONMENT} completed successfully!"