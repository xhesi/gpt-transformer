# Jupyter on Kubernetes + Local Notebooks

Deploy a Jupyter environment to Kubernetes using Helm and run notebooks locally for development.

## Project layout
- jupyter-environment/
  - Makefile (Helm automation)
  - jupyter-values.yaml (JupyterHub config)
- notebooks/ (your notebooks)
- src/, data/, requirements.txt

## Prerequisites
- Python 3.8+
- Kubernetes cluster + kubectl
- Helm 3.x
- Make (macOS has it by default)

## Quick start

### Run notebooks locally
- Install deps:
  - pip install -r requirements.txt
- Start JupyterLab:
  - jupyter lab
- Work in notebooks/ and src/

### Deploy to Kubernetes (JupyterHub)
- Generate a strong proxy secret and update jupyter-values.yaml:
  - openssl rand -hex 32
  - Set the value under proxy.secretToken
- Install/upgrade via Makefile:
  - cd jupyter-environment
  - make install
- Check status:
  - make status
- Access:
  - If your cluster supports LoadBalancer: make get-ip
  - Otherwise: make port-forward (http://localhost:8080)

## Common Make targets
- make help — list targets
- make install — add repo/update and install JupyterHub
- make upgrade — upgrade release
- make status — Helm and k8s status
- make logs — hub logs
- make get-ip — external IP (if LoadBalancer)
- make port-forward — local access via 8080
- make uninstall — remove the release
- make clean — uninstall and remove Helm repo

## Configuration tips
Edit jupyter-environment/jupyter-values.yaml:
- Auth: DummyAuthenticator for dev (admin user: admin, password: jupyter). Do not use in prod.
- Image: jupyter/datascience-notebook:latest (change as needed)
- Storage: singleuser.storage.capacity default 10Gi
- Default URL: /lab (JupyterLab)

## Troubleshooting
- External IP pending: your cluster may not support LoadBalancer. Use make port-forward.
- Pods not starting: make logs, kubectl describe pod <pod> -n jupyter
- Auth errors: verify hub.config settings and restart:
  - helm upgrade jupyter jupyterhub/jupyterhub -n jupyter -f jupyter-values.yaml

## Next steps
- Add your notebooks under notebooks/ and commit (consider clearing outputs before commit).
- Add Python deps to requirements.txt.
- For production: replace DummyAuthenticator, configure a proper Authenticator, TLS/Ingress, and user storage class.
