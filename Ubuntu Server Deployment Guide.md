# Email Registration System - Ubuntu Server Deployment

## Prerequisite: System Update
```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y build-essential curl git wget software-properties-common
```

## Python Environment Setup
```bash
# Install Python and virtual environment
sudo apt install -y python3 python3-pip python3-venv

# Create project directory
mkdir -p /opt/email-registration
cd /opt/email-registration

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install flask flask-cors cryptography pandas gunicorn
```

## Node.js Installation
```bash
# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installations
node --version
npm --version
```

## Application Setup
```bash
# Clone repository (replace with your git repository)
git clone https://github.com/yourusername/email-registration.git .

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
npm run build
```

## Nginx Reverse Proxy
```bash
# Install Nginx
sudo apt install -y nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/email-registration

# Add following configuration:
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/email-registration /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Systemd Service Configuration
```bash
# Create backend service file
sudo nano /etc/systemd/system/email-registration-backend.service

# Add following configuration:
[Unit]
Description=Email Registration Backend
After=network.target

[Service]
User=your_username
WorkingDirectory=/opt/email-registration/backend
ExecStart=/opt/email-registration/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable email-registration-backend
sudo systemctl start email-registration-backend
```

## Firewall Configuration
```bash
# Install UFW (Uncomplicated Firewall)
sudo apt install -y ufw

# Allow SSH, HTTP, HTTPS
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'

# Enable firewall
sudo ufw enable
```

## SSL/TLS with Let's Encrypt
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL Certificate
sudo certbot --nginx -d your_domain.com
```

## Security Enhancements
```bash
# Set proper permissions
sudo chown -R your_username:your_username /opt/email-registration

# Restrict directory access
chmod 750 /opt/email-registration
chmod 640 /opt/email-registration/backend/company_email_accounts.db
```

## Monitoring and Logs
```bash
# Check service status
sudo systemctl status email-registration-backend

# View logs
journalctl -u email-registration-backend

