# Aircraft Accident Map

Safety project with separate backend, database-service, frontend, and deploy artifacts.

## Commands

- Backend tests: `cd backend && poetry run pytest`
- Backend lint: `cd backend && poetry run ruff check .`
- Backend OpenAPI for GCP API Gateway: `cd backend && PYTHONPATH=src poetry run python -m safety_backend.openapi --backend-url https://BACKEND_URL --output openapi-gateway.json`
- Database-service tests: `cd database-service && poetry run pytest`
- Database-service lint: `cd database-service && poetry run ruff check .`
- Frontend tests: `cd frontend && npm test`
- Frontend coverage: `cd frontend && npm run test:coverage`
- Frontend lint: `cd frontend && npm run lint`
- Local app without Docker: `./scripts/run-local.sh`

## Backend FastAPI Lambda

Generate a GCP API Gateway OpenAPI document from the same FastAPI app routes:

```bash
cd backend
PYTHONPATH=src poetry run python -m safety_backend.openapi \
  --backend-url https://BACKEND_URL \
  --output openapi-gateway.json
```

Pre-commit regenerates and stages `backend/openapi-gateway.json` when staged files under `backend/` change.

## Docker Compose

Run:

```bash
docker compose up --build
```

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"version":"2.0","routeKey":"GET /health","rawPath":"/health","requestContext":{"http":{"method":"GET","path":"/health"}},"headers":{},"isBase64Encoded":false}'
```

## Kubernetes

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/redis.yaml
kubectl apply -f kubernetes/backend.yaml
kubectl apply -f kubernetes/frontend.yaml
kubectl apply -f kubernetes/ingress.yaml
```
