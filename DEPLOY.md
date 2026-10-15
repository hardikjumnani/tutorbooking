# Deploy runbook — AWS (Terraform → Helm → Monitoring)

Follow these steps in one sitting, then **destroy everything** to avoid charges.
Everything here needs an AWS account with access keys.

> **Cost:** EKS + NAT gateway + 2 nodes ≈ $0.30–0.40 per hour. Plan for ~1–2 hours.

---

## 0. Install the tools (Windows, one time)

```powershell
winget install Hashicorp.Terraform
winget install Amazon.AWSCLI
winget install Kubernetes.kubectl
winget install Helm.Helm
```

Open a **new terminal** afterwards so the tools are on your PATH.

## 1. Give AWS your credentials

```powershell
aws configure
# Access key ID, Secret access key, region = ap-south-1, output = json
aws sts get-caller-identity          # confirms you are logged in
```

## 2. Create the infrastructure (Terraform)

```bash
cd terraform
terraform init
terraform plan          # screenshot this (Module 7)
terraform apply         # type: yes   (~15–20 minutes)
cd ..
```

Point kubectl at the new cluster, then check the nodes:

```bash
aws eks update-kubeconfig --region ap-south-1 --name tutorslot-eks
kubectl get nodes       # should show 2 nodes in Ready state
```

## 3. Let the cluster pull your images

Your GHCR images are private by default. Easiest option — **make them public**:
GitHub → your profile → Packages → `tutorslot-backend` → Package settings →
Change visibility → Public (repeat for `tutorslot-frontend`).

(Or keep them private and create a pull secret:)

```bash
kubectl create namespace tutorslot
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=hardikjumnani \
  --docker-password=<GITHUB_TOKEN_with_read:packages> \
  -n tutorslot
# then add:  --set imagePullSecrets[0].name=ghcr-secret  to the helm command below
```

## 4. Install the cluster add-ons

```bash
# Ingress controller (implements the Ingress resource)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx --create-namespace

# Metrics Server (required for the HPA to read CPU usage)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## 5. Deploy the app with Helm

```bash
SHA=$(git rev-parse HEAD)     # the image tag pushed by CI
helm upgrade --install tutorslot ./helm/tutorslot \
  -n tutorslot --create-namespace \
  -f helm/tutorslot/values-dev.yaml \
  --set backend.tag=$SHA --set frontend.tag=$SHA
```

Verify (screenshots for Module 8):

```bash
kubectl get pods -n tutorslot        # all Running (2 backend, 2 frontend, 1 postgres)
kubectl get svc -n tutorslot         # ClusterIP services
kubectl get ingress -n tutorslot
helm list -n tutorslot
```

## 6. Open the app through the Ingress

```bash
# Get the ingress load balancer address:
kubectl get svc -n ingress-nginx ingress-nginx-controller
# (gives an AWS ELB hostname, e.g. abc123.ap-south-1.elb.amazonaws.com)

# Quick check with the host header:
curl -H "Host: tutorslot.local" http://<ELB-hostname>/api/appointments
```

For a browser screenshot, map the hostname: find the ELB's IP
(`nslookup <ELB-hostname>`) and add `  <IP> tutorslot.local` to
`C:\Windows\System32\drivers\etc\hosts`, then open http://tutorslot.local

(Simplest fallback if the ELB is slow: `kubectl port-forward -n tutorslot svc/frontend 3000:80` → http://localhost:3000)

## 7. Show autoscaling (HPA)

```bash
kubectl get hpa -n tutorslot                 # shows targets and replica count
# In another terminal, generate load:
URL="http://<ELB-hostname>/api/appointments" WORKERS=30 DURATION=180 bash scripts/load-test.sh
# Watch it scale up:
kubectl get hpa -n tutorslot -w              # screenshot replicas increasing
```

## 8. Monitoring (Prometheus + Grafana)

Follow [`monitoring/README.md`](monitoring/README.md):

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace -f monitoring/prometheus-values.yaml

# Turn on our ServiceMonitor so Prometheus scrapes the app:
helm upgrade tutorslot ./helm/tutorslot -n tutorslot \
  --reuse-values --set monitoring.serviceMonitor.enabled=true

# Open the UIs:
kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3001:80
```

- Prometheus http://localhost:9090 → Status > Targets → `tutorslot-backend` UP (screenshot).
- Grafana http://localhost:3001 (admin / tutorslot-admin) → import
  `monitoring/grafana-dashboard.json` → panels show live data (screenshot).

## 9. TEAR DOWN (do not skip)

```bash
# Remove the load balancers FIRST, or the VPC refuses to delete:
helm uninstall tutorslot -n tutorslot
helm uninstall kube-prometheus-stack -n monitoring
helm uninstall ingress-nginx -n ingress-nginx
kubectl get svc -A | grep LoadBalancer      # make sure none remain

# Then destroy all AWS infrastructure:
cd terraform
terraform destroy       # type: yes  (screenshot the completion — Module 7)
```

> If `terraform destroy` hangs on the VPC, a leftover load balancer is usually
> the cause. Delete any remaining `LoadBalancer` services, then run it again.
