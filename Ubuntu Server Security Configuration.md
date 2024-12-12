# Ubuntu Server Security Best Practices

## User Management
```bash
# Create dedicated service user
sudo adduser --system --no-create-home email-registration

# Disable root login
sudo passwd -l root

# Configure SSH
sudo nano /etc/ssh/sshd_config
# Set: 
# PermitRootLogin no
# PasswordAuthentication no
# AllowUsers your_username

sudo systemctl restart sshd
```

## Additional Security Layers
1. SSH Key Authentication
```bash
# Generate SSH key pair
ssh-keygen -t ed25519

# Copy public key to server
ssh-copy-id your_username@server_ip
```

2. Fail2Ban Installation
```bash
# Install Fail2Ban
sudo apt install -y fail2ban

# Configure for SSH protection
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
# Customize ban settings

sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

3. Regular Updates
```bash
# Automatic security updates
sudo dpkg-reconfigure --priority=low unattended-upgrades

# Enable automatic updates
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
# Uncomment and configure update settings
```

## Environment Hardening
```bash
# Set restrictive umask
echo "umask 027" >> ~/.bashrc

# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable cups
```

## Backup Strategy
```bash
# Install rsync for backups
sudo apt install -y rsync

# Create backup script
nano /opt/backup.sh
#!/bin/bash
BACKUP_DIR="/backup/email-registration"
mkdir -p $BACKUP_DIR
rsync -av /opt/email-registration $BACKUP_DIR/$(date +"%Y%m%d")

