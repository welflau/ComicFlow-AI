module.exports = {
  apps: [{
    name: 'user-auth-app',
    script: './dist/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    env_staging: {
      NODE_ENV: 'staging',
      PORT: 3000
    },
    // Logging
    log_file: './logs/combined.log',
    out_file: './logs/out.log',
    error_file: './logs/error.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    
    // Process management
    min_uptime: '10s',
    max_restarts: 10,
    autorestart: true,
    watch: false,
    
    // Memory management
    max_memory_restart: '1G',
    
    // Health monitoring
    health_check_grace_period: 3000,
    health_check_fatal_exceptions: true,
    
    // Advanced features
    source_map_support: true,
    instance_var: 'INSTANCE_ID',
    
    // Environment variables
    env_file: '.env.production',
    
    // Graceful shutdown
    kill_timeout: 5000,
    listen_timeout: 3000,
    
    // Monitoring
    pmx: true,
    
    // Cluster settings
    wait_ready: true,
    
    // Custom settings
    node_args: '--max-old-space-size=2048',
    
    // Cron restart
    cron_restart: '0 2 * * *', // Restart every day at 2 AM
    
    // Ignore watch
    ignore_watch: [
      'node_modules',
      'logs',
      '*.log',
      '.git'
    ],
    
    // Merge logs
    merge_logs: true,
    
    // Time zone
    time: true
  }],
  
  deploy: {
    production: {
      user: 'deploy',
      host: ['production.example.com'],
      ref: 'origin/main',
      repo: 'git@github.com:username/user-auth-app.git',
      path: '/opt/app',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && npm run build && pm2 reload ecosystem.config.js --env production',
      'pre-setup': 'apt-get install git -y'
    },
    
    staging: {
      user: 'deploy',
      host: ['staging.example.com'],
      ref: 'origin/develop',
      repo: 'git@github.com:username/user-auth-app.git',
      path: '/opt/app-staging',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && npm run build:staging && pm2 reload ecosystem.config.js --env staging',
      'pre-setup': 'apt-get install git -y'
    }
  }
};