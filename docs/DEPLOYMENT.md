# Deployment Guide

## Production Setup

### 1. Server Requirements
- Ubuntu 20.04 LTS or later
- Docker and Docker Compose
- Nginx (for reverse proxy)
- SSL certificate (Let's Encrypt recommended)
- Minimum 2GB RAM, 20GB storage

### 2. Environment Configuration

**Backend Production Environment**
```env
DEBUG=False
SECRET_KEY=your-super-secure-production-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

# Database
DB_NAME=education_platform_prod
DB_USER=prod_user
DB_PASSWORD=super-secure-db-password
DB_HOST=postgres
DB_PORT=5432

# JWT
JWT_SECRET_KEY=your-jwt-production-secret

# Video Security
VIDEO_ENCRYPTION_KEY=your-video-encryption-key
VIDEO_SIGNED_URL_EXPIRY=3600

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email (SMTP)
EMAIL_HOST=smtp.yourmailprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

**Frontend Production Environment**
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_APP_NAME=Education Platform
NEXT_PUBLIC_UPLOAD_URL=https://api.yourdomain.com/media
```

### 3. Docker Production Setup

**docker-compose.prod.yml**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: education_postgres_prod
    environment:
      POSTGRES_DB: education_platform_prod
      POSTGRES_USER: prod_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: education_backend_prod
    volumes:
      - media_files:/app/media
      - static_files:/app/staticfiles
    environment:
      - DEBUG=False
      - DB_HOST=postgres
    depends_on:
      - postgres
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    container_name: education_frontend_prod
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: education_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - static_files:/var/www/static
      - media_files:/var/www/media
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
  media_files:
  static_files:
```

### 4. Nginx Configuration

**nginx.conf**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    # Frontend
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    # Backend API
    server {
        listen 443 ssl http2;
        server_name api.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        client_max_body_size 100M;

        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /admin/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        location /media/ {
            alias /var/www/media/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 5. SSL Certificate Setup

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Generate certificates
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 6. Deployment Commands

```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up --build -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

# Create superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

### 7. Monitoring and Maintenance

**Log Monitoring**
```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Log rotation
sudo logrotate -f /etc/logrotate.d/docker-containers
```

**Database Backup**
```bash
# Backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U prod_user education_platform_prod > backup.sql

# Restore
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U prod_user education_platform_prod < backup.sql
```

### 8. Security Checklist

- [ ] Change all default passwords
- [ ] Enable firewall (UFW)
- [ ] Configure fail2ban
- [ ] Set up automated backups
- [ ] Enable SSL/TLS
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure log aggregation
- [ ] Enable intrusion detection

### 9. Performance Optimization

- Use Redis for caching
- Implement CDN for static files
- Enable Gzip compression
- Optimize database queries
- Set up load balancing for high traffic
- Configure database connection pooling
- Implement proper caching strategies