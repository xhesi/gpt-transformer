# ...existing code...

.PHONY: infra plan apply destroy ansible kubeconfig ansible-apps-simple reboot-servers status logs debug-pods check-dns resource-usage node-resources node-pressure resource-summary quick-setup health help helm-add-repo helm-install helm-status helm-uninstall jupyter-status jupyter-dns jupyter-annotate jupyter-deploy jupyter-logs

# ...existing code...

# Helm and JupyterHub targets
helm-add-repo:
	@echo "=== Adding JupyterHub Helm repository ==="
	helm repo add jupyterhub https://hub.jupyter.org/helm-chart/
	helm repo update

helm-install: helm-add-repo
	@echo "=== Installing JupyterHub ==="
	kubectl create namespace jupyter --dry-run=client -o yaml | kubectl apply -f -
	helm upgrade --install my-hub jupyterhub/jupyterhub \
		--namespace jupyter \
		--values jupyter-values.yaml

helm-status:
	@echo "=== Helm Deployments ==="
	helm list -a
	@echo ""
	@echo "=== JupyterHub Helm Status ==="
	helm status my-hub -n jupyter || echo "JupyterHub not installed"

helm-uninstall:
	@echo "=== Uninstalling JupyterHub ==="
	helm uninstall my-hub -n jupyter || echo "JupyterHub not found"

jupyter-status:
	@echo "=== JupyterHub Status ==="
	@echo "Namespace: jupyter"
	kubectl get pods -n jupyter
	@echo ""
	@echo "=== JupyterHub Services ==="
	kubectl get svc -n jupyter
	@echo ""
	@echo "=== JupyterHub Ingress/LoadBalancer ==="
	kubectl get svc -n jupyter --field-selector spec.type=LoadBalancer -o wide
	@echo ""
	@echo "=== JupyterHub PVCs ==="
	kubectl get pvc -n jupyter

# Add External-DNS annotation to the proxy service
jupyter-annotate:
	@echo "=== Adding External-DNS annotation to proxy-public service ==="
	kubectl annotate svc proxy-public -n jupyter external-dns.alpha.kubernetes.io/hostname=jupyter.k3.galanxhi.com --overwrite
	@echo "Annotation added successfully!"

jupyter-dns:
	@echo "=== JupyterHub DNS Status ==="
	@JUPYTER_IP=$$(kubectl get svc proxy-public -n jupyter -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "N/A"); \
	echo "JupyterHub LoadBalancer IP: $$JUPYTER_IP"; \
	echo ""; \
	echo "=== Proxy-Public Service Full Details ==="; \
	kubectl get svc proxy-public -n jupyter -o yaml; \
	echo ""; \
	echo "=== External-DNS Pod Status ==="; \
	kubectl get pods -n external-dns-system; \
	echo ""; \
	echo "=== External-DNS Logs (last 20 lines) ==="; \
	kubectl logs -n external-dns-system deployment/external-dns --tail=20 2>/dev/null || echo "External-DNS logs not accessible"

# Combined JupyterHub deployment with annotation
jupyter-deploy: helm-install jupyter-annotate
	@echo "=== Waiting for JupyterHub to be ready ==="
	kubectl wait --for=condition=ready pod -l app=jupyterhub -n jupyter --timeout=300s || echo "Timeout waiting for JupyterHub pods"
	@echo ""
	@make jupyter-status
	@echo ""
	@make jupyter-dns

# ...existing code...

# Help target
help:
	@echo "=== JupyterHub Management ==="
	@echo ""
	@echo "JupyterHub:"
	@echo "  helm-add-repo	 - Add JupyterHub Helm repository"
	@echo "  helm-install	  - Install JupyterHub via Helm"
	@echo "  helm-status	   - Show Helm deployment status"
	@echo "  helm-uninstall	- Uninstall JupyterHub"
	@echo "  jupyter-status	- Show JupyterHub pod and service status"
	@echo "  jupyter-annotate  - Add External-DNS annotation to proxy service"
	@echo "  jupyter-dns	   - Check JupyterHub DNS configuration"
	@echo "  jupyter-logs	  - Show JupyterHub logs"
	@echo "  jupyter-deploy	- Deploy JupyterHub with DNS annotation"
	@echo ""
	@echo "Examples:"
	@echo "  make jupyter-deploy	# Deploy JupyterHub with DNS"
	@echo "  make jupyter-status	# Check JupyterHub status"
	@echo "  make jupyter-dns	# Check DNS configuration"
	@echo ""
	@echo "For help: make help"