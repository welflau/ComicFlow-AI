#!/bin/bash

# Deployment script
set -e

ENVIRONMENT=${1:-staging}

echo "🚀 Starting deployment to $ENVIRONMENT..."

# Validate environment
if [[ "$ENVIRONMENT" != "staging" && "$ENVIRONMENT" != "production" ]]; then
    echo "❌ Invalid environment: $ENVIRONMENT"
    echo "Usage: $0 [staging|production]"
    exit 1
fi

# Load environment variables
if [ -f ".env.$ENVIRONMENT" ]; then
    echo "📋 Loading environment variables for $ENVIRONMENT"
    export $(cat .env.$ENVIRONMENT | xargs)
else
    echo "⚠️ No environment file found for $ENVIRONMENT"
fi

# Set deployment variables based on environment
if [ "$ENVIRONMENT" = "staging" ]; then
    DEPLOY_HOST=${STAGING_HOST}
    DEPLOY_USER=${STAGING_USER}
    DEPLOY_KEY=${STAGING_KEY}
    DEPLOY_PATH="/var/www/staging"
else
    DEPLOY_HOST=${PRODUCTION_HOST}
    DEPLOY_USER=${PRODUCTION_USER}
    DEPLOY_KEY=${PRODUCTION_KEY}
    DEPLOY_PATH="/var/www/production"
fi

echo "🏗️ Building application for $ENVIRONMENT..."
npm run build

echo "📦 Creating deployment package..."
tar -czf deploy-package.tar.gz -C dist .

echo "📤 Uploading to server..."
# Create temporary SSH key file
echo "$DEPLOY_KEY" > /tmp/deploy_key
chmod 600 /tmp/deploy_key

# Upload package
scp -i /tmp/deploy_key -o StrictHostKeyChecking=no deploy-package.tar.gz $DEPLOY_USER@$DEPLOY_HOST:/tmp/

# Deploy on server
ssh -i /tmp/deploy_key -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST << EOF
    set -e
    
    echo "🔄 Backing up current deployment..."
    if [ -d "$DEPLOY_PATH" ]; then
        sudo cp -r $DEPLOY_PATH $DEPLOY_PATH.backup.\$(date +%Y%m%d_%H%M%S)
    fi
    
    echo "📁 Creating deployment directory..."
    sudo mkdir -p $DEPLOY_PATH
    
    echo "📦 Extracting new deployment..."
    cd $DEPLOY_PATH
    sudo tar -xzf /tmp/deploy-package.tar.gz
    sudo chown -R www-data:www-data $DEPLOY_PATH
    
    echo "🔧 Updating nginx configuration..."
    sudo cp $DEPLOY_PATH/nginx.conf /etc/nginx/sites-available/user-auth-system
    sudo ln -sf /etc/nginx/sites-available/user-auth-system /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    
    echo "🔄 Restarting PM2 processes..."
    if command -v pm2 &> /dev/null; then
        pm2 reload $DEPLOY_PATH/pm2.config.js --env $ENVIRONMENT
    fi
    
    echo "🧹 Cleaning up..."
    rm -f /tmp/deploy-package.tar.gz
    
    echo "✅ Deployment completed successfully!"
EOF

# Cleanup
rm -f /tmp/deploy_key deploy-package.tar.gz

echo "🔍 Running post-deployment health checks..."
sleep 10

# Health check
if [ "$ENVIRONMENT" = "staging" ]; then
    HEALTH_URL="https://staging.example.com/health"
else
    HEALTH_URL="https://example.com/health"
fi

if curl -f "$HEALTH_URL" > /dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "❌ Health check failed!"
    exit 1
fi

echo "🎉 Deployment to $ENVIRONMENT completed successfully!"