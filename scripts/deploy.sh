#!/bin/bash
set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}

echo "🚀 Starting deployment to $ENVIRONMENT..."

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo "❌ Invalid environment. Use 'staging' or 'production'"
    exit 1
fi

# Load environment variables
if [ -f ".env.$ENVIRONMENT" ]; then
    source ".env.$ENVIRONMENT"
else
    echo "❌ Environment file .env.$ENVIRONMENT not found"
    exit 1
fi

echo "📦 Building Docker image..."
docker build -f Dockerfile.production -t "$APP_NAME:$VERSION" .

echo "🏷️ Tagging image..."
docker tag "$APP_NAME:$VERSION" "$DOCKER_REGISTRY/$APP_NAME:$ENVIRONMENT-$VERSION"
docker tag "$APP_NAME:$VERSION" "$DOCKER_REGISTRY/$APP_NAME:$ENVIRONMENT-latest"

echo "📤 Pushing to registry..."
docker push "$DOCKER_REGISTRY/$APP_NAME:$ENVIRONMENT-$VERSION"
docker push "$DOCKER_REGISTRY/$APP_NAME:$ENVIRONMENT-latest"

echo "🔄 Deploying to server..."
ssh -o StrictHostKeyChecking=no "$DEPLOY_USER@$DEPLOY_HOST" << EOF
    cd $DEPLOY_PATH
    
    # Backup current version
    if [ -f docker-compose.$ENVIRONMENT.yml ]; then
        docker-compose -f docker-compose.$ENVIRONMENT.yml down
    fi
    
    # Pull latest images
    docker pull $DOCKER_REGISTRY/$APP_NAME:$ENVIRONMENT-latest
    
    # Start new version
    docker-compose -f docker-compose.$ENVIRONMENT.yml up -d
    
    # Clean up old images
    docker system prune -f
EOF

echo "⏳ Waiting for deployment to stabilize..."
sleep 30

echo "🔍 Running health check..."
HEALTH_URL="$APP_URL/health"
for i in {1..10}; do
    if curl -f "$HEALTH_URL" > /dev/null 2>&1; then
        echo "✅ Health check passed"
        break
    else
        echo "⏳ Health check attempt $i/10 failed, retrying..."
        sleep 10
    fi
    
    if [ $i -eq 10 ]; then
        echo "❌ Health check failed after 10 attempts"
        exit 1
    fi
done

echo "📊 Deployment summary:"
echo "  Environment: $ENVIRONMENT"
echo "  Version: $VERSION"
echo "  URL: $APP_URL"
echo "  Deployed at: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "✅ Deployment completed successfully!"