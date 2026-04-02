module.exports = {
  apps: [{
    name: 'user-auth-system',
    script: './dist/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development',
      PORT: 3000
    },
    env_staging: {
      NODE_ENV: 'staging',
      PORT: 3000
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
    
    // Restart policy
    restart_delay: 4000,
    max_restarts: 10,
    min_uptime: '10s',
    
    // Memory management
    max_memory_restart: '1G',
    
    // Monitoring
    monitoring: false,
    
    // Advanced features
    watch: false,
    ignore_watch: ['node_modules', 'logs', 'uploads'],
    
    // Health check
    health_check_grace_period: 3000,
    
    // Graceful shutdown
    kill_timeout: 5000,
    listen_timeout: 3000,
    
    // Source map support
    source_map_support: true,
    
    // Instance variables
    instance_var: 'INSTANCE_ID',
    
    // Merge logs
    merge_logs: true,
    
    // Time zone
    time: true
  }],
  
  deploy: {
    staging: {
      user: 'deploy',
      host: ['staging.yourapp.com'],
      ref: 'origin/develop',
      repo: 'git@github.com:yourorg/user-auth-system.git',
      path: '/opt/app',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && npm run build:staging && pm2 reload ecosystem.config.js --env staging',
      'pre-setup': '',
      'ssh_options': 'StrictHostKeyChecking=no'
    },
    
    production: {
      user: 'deploy',
      host: ['production.yourapp.com'],
      ref: 'origin/main',
      repo: 'git@github.com:yourorg/user-auth-system.git',
      path: '/opt/app',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && npm run build:production && pm2 reload ecosystem.config.js --env production',
      'pre-setup': '',
      'ssh_options': 'StrictHostKeyChecking=no'
    }
  }
};