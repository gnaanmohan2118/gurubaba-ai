
# GuruBaba – Scalable FastAPI Chat & GROQ-powered Content App 🕉️

> GuruBaba is a production-oriented real-time web application built on **FastAPI** with content powered by a **GROQ** (Sanity) API.  
> Designed for high availability and security — containerized, deployed on **AWS EC2**, served by **NGINX** as a reverse proxy with **Certbot** SSL, and optionally managed infrastructure via **Terraform**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![AWS](https://img.shields.io/badge/AWS-EC2-orange)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---
🔗 **Live Demo:** [View GuruBaba-AI](http://gurubaba-ai.guru/)

---

##  Highlights (What makes it production-grade)
- **FastAPI** backend (async first) for powering blazing-fast REST + WebSocket APIs.  
- **GROQ API** integration to fetch and render CMS-managed spiritual content (Sanity/GROQ).  
- **Redis Pub/Sub** ready for scalable real-time messaging (placeholder client present).  
- **Dockerized** services for consistent deployments.  
- **NGINX reverse proxy + Certbot** for TLS termination and HTTP/2 support.  
- **Systemd / Supervisor** or container orchestration (ECS/EKS) friendly.  
- **Runs on AWS** (EC2 + optional RDS/ElastiCache) with IaC examples for Terraform.  
- **Ready for observability** with placeholders for Prometheus & Grafana.

---

##  Project Structure

```

.
├── README.md
└── backend
├── **init**.py
├── client.py          # GROQ & external API client + Redis client hooks
├── config.py          # Config loader (env / .env)
├── main.py            # FastAPI app (HTTP + WebSocket endpoints)
├── requirements.txt
├── static/
│   ├── guru.png
│   ├── script.js
│   └── style.css
└── templates/
└── index.html

````

---

##  Tech Stack (Quiet Simple)
- **Framework:** FastAPI (uvicorn, gunicorn workers optional)  
- **Content API:** GROQ (Sanity) — using GROQ queries to fetch CMS content  
- **Real-time:** WebSockets + Redis Pub/Sub  
- **Database:** Postgres (optional) / RDS on AWS  
- **Container:** Docker, docker-compose (local), registry (ECR / Docker Hub)  
- **Reverse Proxy & SSL:** NGINX + Certbot (Let's Encrypt)  
- **Cloud:** AWS EC2 (AMI) + optional EKS/ECS; Terraform for infra-as-code  
- **CI/CD:** GitHub Actions (build, test, push image, deploy)  
- **Monitoring:** Prometheus + Grafana (optional)

---

##  Features (current + planned)
- Async REST API endpoints (FastAPI)  
- WebSocket chat endpoints (scalable via Redis Pub/Sub)  
- GROQ-driven content endpoints (fetch content authored in Sanity)  
- Docker-ready with `Dockerfile` & `docker-compose` templates  
- Deployment-ready NGINX config & Certbot instructions  
- Infrastructure IaC (Terraform) templates (examples included)  
- Background cron-as-a-service module (for scheduled tasks)

---

##  Environment Variables (example `.env`)
```env
# App
APP_ENV=production
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=info

# GROQ / Sanity
SANITY_PROJECT_ID=your_project_id
SANITY_DATASET=production
SANITY_TOKEN=your_sanity_read_token

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=

# Database (optional)
DATABASE_URL=postgresql://user:password@host:5432/gurubaba

# JWT Auth (planned)
JWT_SECRET=supersecretkey
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=60

# Deployment
S3_BUCKET_STATIC=your-static-bucket
````

---

## Local Quick Start (development)

```bash
# 1. clone
git clone https://github.com/your-username/gurubaba.git
cd gurubaba/backend

# 2. create venv & install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. set env (example)
cp .env.example .env
# edit .env and add SANITY_TOKEN, etc.

# 4. run local redis (if not present)
# Linux:
sudo apt-get install redis-server
sudo systemctl start redis-server

# 5. start FastAPI dev server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://127.0.0.1:8000`.

---

##  Docker (local)

`Dockerfile` (example)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

`docker-compose.yml` (example)

```yaml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - redis
  redis:
    image: redis:7
    ports:
      - "6379:6379"
```

Run:

```bash
docker-compose up --build
```

---

##  Production Deployment (AWS EC2 + NGINX + Certbot) — High level

### 1) Provision EC2

* Launch an EC2 instance (Ubuntu 22.04 LTS recommended).
* Install Docker & docker-compose (or use systemd + uvicorn/gunicorn).
* Open ports: 22 (ssh), 80 (http), 443 (https).

### 2) Pull and run Docker image on EC2

* Build/push image to ECR/DockerHub from CI.
* Pull on EC2 and run `docker-compose` or run container via ECS/EKS.

### 3) NGINX reverse proxy

* Install NGINX on EC2 (or run an NGINX container).
* Configure NGINX to proxy to your app (internal port 8000).

Sample `/etc/nginx/sites-available/gurubaba`:

```nginx
server {
    listen 80;
    server_name your.domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    location /static/ {
        alias /var/www/gurubaba/static/;
    }
}
```

Enable and reload:

```bash
sudo ln -s /etc/nginx/sites-available/gurubaba /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 4) Certbot (Let's Encrypt)

Install certbot and get certificates:

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your.domain.com --non-interactive --agree-tos -m your-email@example.com
```

Certbot will automatically update your NGINX config to enable TLS. Verify renewal:

```bash
sudo certbot renew --dry-run
```

### 5) Systemd service (if running uvicorn without docker)

Create `/etc/systemd/system/gurubaba.service`:

```ini
[Unit]
Description=GuruBaba FastAPI
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/gurubaba/backend
EnvironmentFile=/home/ubuntu/gurubaba/backend/.env
ExecStart=/home/ubuntu/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker main:app -b 127.0.0.1:8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gurubaba
sudo systemctl start gurubaba
```

---

##  Security & Best Practices

* Never commit `.env` or secrets to GitHub. Use AWS Secrets Manager or Parameter Store.
* Limit SANITY\_TOKEN scope to read-only.
* Use AWS Security Groups to limit access to internal services (e.g., Redis, Postgres).
* Use HTTPS everywhere (Certbot or managed certificates).
* Run containers as non-root where possible.

---

##  Infrastructure as Code (Terraform) — minimal idea

* `main.tf` to provision VPC, EC2, Security Groups, and optionally ECR/ECS.
* Use outputs to pass instance public IP for DNS config.
* Use `user_data` to bootstrap Docker + pull image and `docker-compose up`.

---

##  Testing & CI/CD

* GitHub Actions pipeline:

  * Lint (flake8/ruff)
  * Unit tests (pytest)
  * Build Docker image
  * Push image to ECR/ DockerHub
  * SSH or SSM deploy step to EC2 (or trigger ECS/EKS deploy)

---

##  Architecture Diagram (brief)

```
[User] --HTTPS--> [NGINX (EC2)] --HTTP--> [FastAPI App Container (127.0.0.1:8000)]
                          |
                          +--> [Static files] (served by NGINX)
App <--> Redis (ElastiCache) for Pub/Sub
App <--> Postgres (RDS) for persistence
App <--> Sanity GROQ API (external)
```


---

##  Author

**Gnana Ganesh** – Backend & Cloud focused engineer
[LinkedIn](https://www.linkedin.com/in/gnana-ganesh-m/)

---





