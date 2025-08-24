# Makefile for Jupyter Helm deployment

# Variables
NAMESPACE = jupyter
RELEASE_NAME = jupyter
CHART_REPO = jupyterhub
CHART_NAME = jupyterhub/jupyterhub
VALUES_FILE = jupyter-values.yaml

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m # No Color

.PHONY: help repo-add repo-update install upgrade uninstall status logs port-forward clean

help: ## Show this help message
    @echo "Available targets:"
    @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

repo-add: ## Add JupyterHub Helm repository
    @echo "$(YELLOW)Adding JupyterHub Helm repository...$(NC)"
    helm repo add $(CHART_REPO) https://hub.jupyter.org/helm-chart/

repo-update: ## Update Helm repositories
    @echo "$(YELLOW)Updating Helm repositories...$(NC)"
    helm repo update

install: repo-add repo-update ## Install JupyterHub (first time deployment)
    @echo "$(YELLOW)Installing JupyterHub...$(NC)"
    helm upgrade --cleanup-on-fail \
        --install $(RELEASE_NAME) $(CHART_NAME) \
        --namespace $(NAMESPACE) \
        --create-namespace \
        --values $(VALUES_FILE)

upgrade: ## Upgrade existing JupyterHub deployment
    @echo "$(YELLOW)Upgrading JupyterHub...$(NC)"
    helm upgrade $(RELEASE_NAME) $(CHART_NAME) \
        --namespace $(NAMESPACE) \
        --values $(VALUES_FILE)

uninstall: ## Uninstall JupyterHub
    @echo "$(YELLOW)Uninstalling JupyterHub...$(NC)"
    helm uninstall $(RELEASE_NAME) --namespace $(NAMESPACE)
    kubectl delete namespace $(NAMESPACE)

status: ## Show deployment status
    @echo "$(YELLOW)Helm release status:$(NC)"
    helm status $(RELEASE_NAME) --namespace $(NAMESPACE)
    @echo "\n$(YELLOW)Kubernetes resources:$(NC)"
    kubectl get all --namespace $(NAMESPACE)

logs: ## Show hub logs
    @echo "$(YELLOW)Showing hub logs...$(NC)"
    kubectl logs --namespace $(NAMESPACE) -l component=hub --tail=50 -f

port-forward: ## Port forward to access locally (localhost:8080)
    @echo "$(YELLOW)Port forwarding to localhost:8080...$(NC)"
    @echo "Access JupyterHub at: http://localhost:8080"
    kubectl port-forward --namespace $(NAMESPACE) svc/proxy-public 8080:80

get-ip: ## Get external IP address
    @echo "$(YELLOW)Getting external IP address...$(NC)"
    kubectl get service --namespace $(NAMESPACE) proxy-public

clean: ## Clean up everything
    @echo "$(YELLOW)Cleaning up...$(NC)"
    make uninstall
    helm repo remove $(CHART_REPO)

# Quick setup target
setup: install status ## Quick setup: install and show status
    @echo "$(GREEN)JupyterHub setup complete!$(NC)"
    @echo "Run 'make get-ip' to get the external IP address"