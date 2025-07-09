# Microservices Configuration System

Modern Python microservices communicating via RabbitMQ with load balancing.

## Prerequisites
- Docker Engine
- Docker Compose
- Helm (for Kubernetes deployment)

## Build && push images

```bash
bash publish_images.bash
```


## Deployment Options

### Docker Compose Deployment
```bash
docker compose up --build
```

#### Scaling
Run 4 instances of web service with load balancing:
```bash
docker compose up --build --scale web_service=4 --scale worker_service=2
```

### Helm Chart Deployment
```bash
# Install Helm: https://helm.sh/docs/intro/install/
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install config-system ./helm/config-system
```

#### Scaling
```bash
helm upgrade config-system ./helm/config-system --set web_service.replicas=4 --set worker_service.replicas=2
```

## Accessing the Service
- **Docker Compose**: 
  ```bash
  curl http://localhost:8880/status
  ```
- **Helm Chart**:
  ```bash
  curl http://localhost/status  # Via LoadBalancer
  ```

## Project Structure
```
.
├── config_sender/      # Configuration provider service
├── web_service/        # Web interface service
├── nginx/              # Load balancer configuration
├── helm/               # Kubernetes Helm charts
└── docker-compose.yml  # Orchestration configuration
```

