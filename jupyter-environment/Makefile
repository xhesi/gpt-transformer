# ...existing code...

.PHONY: infra plan apply destroy ansible kubeconfig ansible-apps-simple reboot-servers status logs debug-pods check-dns resource-usage node-resources node-pressure resource-summary quick-setup health help helm-add-repo helm-install helm-status helm-uninstall jupyter-status jupyter-dns

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

jupyter-dns:
	@echo "=== JupyterHub DNS Status ==="
	@JUPYTER_IP=$$(kubectl get svc proxy-public -n jupyter -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "N/A"); \
	echo "JupyterHub LoadBalancer IP: $$JUPYTER_IP"; \
	echo ""; \
	echo "=== JupyterHub Service DNS Annotations ==="; \
	kubectl get svc proxy-public -n jupyter -o yaml 2>/dev/null | grep -A 5 "annotations:" || echo "No annotations found"; \
	echo ""; \
	echo "=== ExternalDNS Records for JupyterHub ==="; \
	kubectl logs -n external-dns-system deployment/external-dns --tail=20 2>/dev/null | grep -i jupyter || echo "No JupyterHub DNS records found in ExternalDNS logs"

# Combined JupyterHub deployment and status check
jupyter-deploy: helm-install
	@echo "=== Waiting for JupyterHub to be ready ==="
	kubectl wait --for=condition=ready pod -l app=jupyterhub -n jupyter --timeout=300s || echo "Timeout waiting for JupyterHub pods"
	@echo ""
	@make jupyter-status
	@echo ""
	@make jupyter-dns

# ...existing code...

# Help target
help:
	@echo "=== K3s Homelab Management ==="
	@echo ""
	@echo "Setup & Validation:"
	@echo "  setup			 - Initialize environment and validate configuration"
	@echo "  validate-env	  - Validate environment variables and SSH keys"
	@echo ""
	@echo "Infrastructure:"
	@echo "  plan			  - Show Terraform plan"
	@echo "  infra			 - Deploy infrastructure with Terraform"
	@echo "  destroy		   - Destroy infrastructure"
	@echo ""
	@echo "K3s Cluster:"
	@echo "  ansible		   - Deploy K3s cluster"
	@echo "  kubeconfig		- Get kubeconfig from cluster"
	@echo "  quick-setup	   - Infrastructure + K3s cluster"
	@echo ""
	@echo "Applications:"
	@echo "  ansible-apps-simple - Deploy MetalLB, bind9, ExternalDNS, Dashboard"
	@echo ""
	@echo "JupyterHub:"
	@echo "  helm-add-repo	 - Add JupyterHub Helm repository"
	@echo "  helm-install	  - Install JupyterHub via Helm"
	@echo "  helm-status	   - Show Helm deployment status"
	@echo "  helm-uninstall	- Uninstall JupyterHub"
	@echo "  jupyter-status	- Show JupyterHub pod and service status"
	@echo "  jupyter-dns	   - Check JupyterHub DNS configuration"
	@echo "  jupyter-deploy	- Deploy JupyterHub and show status"
	@echo ""
	@echo "Maintenance:"
	@echo "  reboot-servers	- Reboot all K3s servers"
	@echo ""
	@echo "Monitoring & Debugging:"
	@echo "  status			- Show cluster status"
	@echo "  health			- Comprehensive health check"
	@echo "  logs			  - Show logs from key components"
	@echo "  debug-pods		- Debug failed pods"
	@echo "  check-dns		 - Check DNS infrastructure status"
	@echo ""
	@echo "Resource Monitoring:"
	@echo "  resource-usage	- Show resource usage across all nodes"
	@echo "  node-resources	- Detailed resource breakdown per node"
	@echo "  node-pressure	 - Check nodes for resource pressure"
	@echo "  resource-summary  - Quick resource overview"
	@echo ""
	@echo "Examples:"
	@echo "  make quick-setup					# Deploy infrastructure and K3s"
	@echo "  make ansible-apps-simple		   # Deploy DNS infrastructure"
	@echo "  make jupyter-deploy				# Deploy JupyterHub"
	@echo "  make jupyter-status				# Check JupyterHub status"
	@echo "  make check-dns					 # Verify DNS is working"
	@echo "  make resource-summary			  # Check resource usage"
	@echo ""
	@echo "For help: make help"