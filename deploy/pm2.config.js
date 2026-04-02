module.exports = {
  apps: [{
    name: 'user-auth-system',
    script: 'server.js',
    instances: 'max',
    exec_mode: 'cluster',
    
    // Environment variables
    env: {
      NODE_ENV: 'development',
      PORT: 3000
    },
    
    env_staging: {
      NODE_ENV: 'staging',
      PORT: 3001
    },
    
    env_production: {
      NODE_ENV: 'production',
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
    
    // Memory management
    max_memory_restart: '1G',
    
    // Monitoring
    monitoring: false,
    
    // Advanced features
    source_map_support: true,
    instance_var: 'INSTANCE_ID',
    
    // Health check
    health_check_grace_period: 3000,
    
    // Graceful shutdown
    kill_timeout: 5000,
    listen_timeout: 3000,
    
    // Watch and restart
    watch: false,
    ignore_watch: [
      'node_modules',
      'logs',
      '*.log'
    ],
    
    // Cron restart
    cron_restart: '0 2 * * *',
    
    // Merge logs
    merge_logs: true,
    
    // Time zone
    time: true
  }],
  
  deploy: {
    staging: {
      user: 'deploy',
      host: 'staging.example.com',
      ref: 'origin/develop',
      repo: 'git@github.com:username/user-auth-system.git',
      path: '/var/www/staging',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && npm run build && pm2 reload ecosystem.config.js --env staging',
      'pre-setup': ''
    },
    
    production: {
      user: 'deploy',
      host: 'production.example.com',
      ref: 'origin/main',
      repo: 'git@github.com:username/user-auth-system.git',
      path: '/var/www/production',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && npm run build && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
};

// Additional PM2 configuration for monitoring
if (process.env.NODE_ENV === 'production') {
  module.exports.apps[0].monitoring = true;
  module.exports.apps[0].pmx = true;
}