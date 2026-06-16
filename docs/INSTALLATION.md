# Installation Guide - Hospital Information System

## Prerequisites

### System Requirements
- Operating System: Windows, macOS, or Linux
- Python: 3.9 or higher
- PostgreSQL: 12 or higher
- RAM: Minimum 4GB (8GB recommended)
- Disk Space: Minimum 10GB for database

### Software Requirements
1. Python 3.9+
2. PostgreSQL Database Server
3. Git (for version control)
4. Virtual Environment Manager (venv)

## Step-by-Step Installation

### 1. Database Setup

#### On Windows:
```bash
# Download PostgreSQL from https://www.postgresql.org/download/windows/
# Run installer and remember the password for 'postgres' user

# Create database and user
psql -U postgres
CREATE DATABASE his_main;
CREATE USER his_user WITH PASSWORD 'secure_password';
ALTER ROLE his_user SET client_encoding TO 'utf8';
ALTER ROLE his_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE his_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE his_main TO his_user;
\q
```

#### On macOS:
```bash
# Install PostgreSQL using Homebrew
brew install postgresql@15
brew services start postgresql@15

# Create database and user
psql postgres
CREATE DATABASE his_main;
CREATE USER his_user WITH PASSWORD 'secure_password';
ALTER ROLE his_user SET client_encoding TO 'utf8';
ALTER ROLE his_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE his_main TO his_user;
\q
```

#### On Linux (Ubuntu):
```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE his_main;
CREATE USER his_user WITH PASSWORD 'secure_password';
ALTER ROLE his_user SET client_encoding TO 'utf8';
ALTER ROLE his_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE his_main TO his_user;
\q
```

### 2. Application Setup

```bash
# Clone repository
git clone https://github.com/ArunPrasad82/HIS.git
cd HIS

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
python -m alembic upgrade head

# Create super user (first time setup)
python scripts/create_superuser.py
```

### 3. Running the Application

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run Streamlit application
streamlit run app.py
```

The application will open at `http://localhost:8501`

## Troubleshooting

### Database Connection Issues

**Error: "could not connect to server"**
- Ensure PostgreSQL service is running
- Check database credentials in `.env` file
- Verify PostgreSQL is listening on correct port (default: 5432)

### Python Package Issues

**Error: "No module named 'streamlit'"**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

**Error: "Port 8501 is already in use"**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

## Production Deployment

### Server Configuration

1. **Install on Production Server**
   - Follow steps 1-2 from above on production server

2. **Environment Configuration**
   - Update `.env` with production database credentials
   - Set `APP_ENV=production`
   - Change `SECRET_KEY` to a strong random value

3. **Web Server Setup (Nginx)**

```nginx
upstream streamlit {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. **SSL Certificate (Let's Encrypt)**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot certonly --nginx -d your-domain.com
   ```

5. **Systemd Service**

Create `/etc/systemd/system/his.service`:
```ini
[Unit]
Description=Hospital Information System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/HIS
Environment="PATH=/opt/HIS/venv/bin"
ExecStart=/opt/HIS/venv/bin/streamlit run app.py --server.port 8501 --server.address 127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable his
sudo systemctl start his
```

## First Login

1. Open browser and go to `http://localhost:8501`
2. Login with super user credentials
3. Create hospital configuration
4. Create admin user for the hospital
5. Configure master data

## Next Steps

- Review User Manual (`docs/USER_MANUAL.md`)
- Configure system settings
- Set up users and roles
- Customize master data for your hospital
