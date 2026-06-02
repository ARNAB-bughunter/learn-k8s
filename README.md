# learn-k8s — Todo App on Kubernetes

Deploys the [Todo App](todo_app/) (FastAPI + PostgreSQL) to a local Kubernetes cluster.

## Architecture

```
                        NodePort :30100
Browser ──────────────► webapp-service ──► webapp-deployment (arnabnaha/todo_app:v1)
                                                    │
                                                    ▼
                                         postgres-service :5432
                                                    │
                                                    ▼
                                         postgres-deployment (postgres:latest)
```

## Files

| File | Purpose |
|---|---|
| `webapp.yaml` | Webapp Deployment + NodePort Service (port 30100) |
| `postgres.yaml` | PostgreSQL Deployment + ClusterIP Service (port 5432) |
| `postgres-secret.yaml` | Base64-encoded DB credentials (user/password/db name) |
| `postgres-config.yaml` | ConfigMap with the postgres service hostname |

## Prerequisites

- A running Kubernetes cluster (e.g. Minikube, kind, or k3s)
- `kubectl` configured to talk to it

## Deploy

Apply in this order — secrets must exist before the pods that reference them:

```bash
kubectl apply -f postgres-secret.yaml
kubectl apply -f postgres-config.yaml
kubectl apply -f postgres.yaml
kubectl apply -f webapp.yaml
```

## Verify

```bash
kubectl get pods
kubectl get services
```

Both pods should reach `Running` status. The webapp pod will be healthy once PostgreSQL is ready (it runs `init_db` on startup).

## Access the app

```bash
# Minikube
minikube service webapp-service

# Or get the node IP and hit port 30100 directly
kubectl get nodes -o wide
# then open http://<NODE_IP>:30100
```

## Credentials

Stored in `postgres-secret.yaml` as base64-encoded values:

| Variable | Decoded value |
|---|---|
| `POSTGRES_USER` | `postgres` |
| `POSTGRES_PASSWORD` | `postgres` |
| `POSTGRES_DB` | `todos` |

To update credentials, re-encode and edit the secret:

```bash
echo -n 'newvalue' | base64
```

Then re-apply:

```bash
kubectl apply -f postgres-secret.yaml
kubectl rollout restart deployment postgres-deployment webapp-deployment
```

## Tear down

```bash
kubectl delete -f webapp.yaml
kubectl delete -f postgres.yaml
kubectl delete -f postgres-config.yaml
kubectl delete -f postgres-secret.yaml
```

## App source

See [todo_app/README.md](todo_app/README.md) for local/Docker Compose development instructions.
