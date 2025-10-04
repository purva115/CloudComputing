# Docker Multi-Container Microservice Application

## Project Overview
This project demonstrates a multi-container Docker application that combines a Python Flask web application with Redis caching and PostgreSQL database. The application tracks page visits using Redis as a cache and displays a hit counter.

## Architecture
- **Web Service**: Flask application running on Python 3.7-alpine
- **Cache Service**: Redis for storing hit counts
- **Database Service**: PostgreSQL for data persistence

## Prerequisites
- Docker Desktop installed and running
- Git for version control
- Web browser for testing

## Execution Steps

### 1. Install and Verify Docker
```bash
# Verify Docker installation
docker -v
```

### 2. Set Up PostgreSQL Container
```bash
# Pull PostgreSQL image
docker pull postgres

# Create and start PostgreSQL instance
docker run -d -p 5432:5432 --name postgres1 -e POSTGRES_PASSWORD=pass12345 postgres

# Access the container (optional)
docker exec -it postgres1 bash

# Connect to PostgreSQL (inside container)
psql -d postgres -U postgres
```

### 3. Create Project Files

#### requirements.txt
```
flask
redis
```

#### app.py
```python
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

#### Dockerfile
```dockerfile
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

#### compose.yaml
```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:5000"
    depends_on:
      - redis
  redis:
    image: "redis:alpine"
```

### 4. Build and Run the Application
```bash
# Build and start all services
docker compose up

# To run in background (detached mode)
docker compose up -d

# To stop services
docker compose down
```

### 5. Test the Application
Open your web browser and navigate to:
```
http://localhost:8000
```

You should see the message "Hello World! I have been seen X times." where X increments with each page refresh.

## What I Learned

### Docker Fundamentals
- **Containerization**: Understanding how to package applications with their dependencies into portable containers
- **Docker Images vs Containers**: Images are blueprints, containers are running instances
- **Port Mapping**: How to expose container ports to the host system using `-p` flag

### Multi-Container Orchestration
- **Docker Compose**: Learned to define and manage multi-container applications using YAML configuration
- **Service Dependencies**: Understanding how services depend on each other using `depends_on`
- **Container Networking**: How containers communicate with each other by service name (e.g., Flask app connecting to 'redis' host)

### Microservices Architecture
- **Service Separation**: Each service (web, cache, database) runs in its own container
- **Loose Coupling**: Services communicate through well-defined interfaces
- **Scalability**: Each service can be scaled independently

### Development Workflow
- **Environment Consistency**: Containers ensure the application runs the same way across different environments
- **Rapid Deployment**: Easy to start/stop entire application stack with single commands
- **Debugging**: Using container logs and exec commands to troubleshoot issues

### Technical Skills Gained
- Writing Dockerfiles with multi-stage instructions
- Managing environment variables in containers
- Using Redis as a caching layer
- Integrating multiple technologies in a containerized environment
- Version control with Git and GitHub integration

## Key Commands Used
```bash
# Container management
docker pull <image>
docker run [OPTIONS] <image>
docker exec -it <container> <command>

# Docker Compose
docker compose up
docker compose down
docker compose logs <service>

# Verification
docker ps
docker images
```

## Project Structure
```
my-docker-app/
├── app.py              # Flask web application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── compose.yaml       # Multi-container orchestration
├── README.md          # Project documentation
└── screenshots/       # Application screenshots
```

## Future Improvements
- Add persistent volume for PostgreSQL data
- Implement proper logging and monitoring
- Add health checks for services
- Configure production-ready settings
- Add unit tests and CI/CD pipeline