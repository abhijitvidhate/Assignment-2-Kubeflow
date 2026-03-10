# Kubeflow Pipelines Implementation

## Current Status

### ✅ Completed
- **Minikube Cluster**: Running with 4 CPUs, 8GB RAM
- **KFP Components**: All services running
  - ✅ MySQL database
  - ✅ MinIO object storage (fixed with Docker Hub image)
  - ✅ Workflow controller
  - ✅ Cache server
  - ✅ Metadata services
  - ✅ API server
- **Local Development**: Python environment set up with KFP SDK
- **Pipeline Development**: Created working pipeline code
- **Local Execution**: Pipeline runs successfully locally
- **Web UI**: Custom interface with full API connectivity


## How to Access the UI

### ✅ **Connection Issue FIXED!**

The UI connection issue has been resolved! The problem was that the MinIO object storage service couldn't start due to image pulling issues, which caused the KFP API to crash.

**What was fixed:**
- Updated MinIO to use `minio/minio:RELEASE.2023-03-20T20-16-18Z` from Docker Hub
- MinIO service is now running
- KFP API pod is now stable and running
- Port-forward is working

### 🚀 **How to Access the UI:**

1. **Start the Port Forward:**
```bash
kubectl port-forward -n kubeflow svc/ml-pipeline 8881:8888
```

2. **Start the Simple UI:**
```bash
cd kfp
source .kfp/bin/activate
python simple_ui.py
```

3. **Open in Browser:**
**http://localhost:5001**

### ✨ **UI Features:**
- ✅ **Dashboard**: View pipelines, experiments, and runs
- ✅ **Upload Pipelines**: Upload YAML pipeline files
- ✅ **Run Pipelines**: Start pipeline executions
- ✅ **Monitor Status**: Track run progress and status
- ✅ **Simple Interface**: Clean, easy-to-use web interface

### 🔧 **Official UI (Still Has Image Issues)**
The official UI pod cannot pull `gcr.io/ml-pipeline/frontend:2.3.0`. Try these solutions:

1. **Use Docker Hub image**:
```bash
kubectl set image deployment/ml-pipeline-ui ml-pipeline-ui=docker.io/kubeflow/pipelines/frontend:2.3.0 -n kubeflow
```

2. **Use alternative registry**:
```bash
kubectl set image deployment/ml-pipeline-ui ml-pipeline-ui=quay.io/kubeflow/pipelines/frontend:2.3.0 -n kubeflow
```

3. **Use older version**:
```bash
kubectl set image deployment/ml-pipeline-ui ml-pipeline-ui=gcr.io/ml-pipeline/frontend:2.0.0 -n kubeflow
```

**Access (if working):**
```bash
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
# Open: http://localhost:8080
```

### 📱 **API-Only Access**
Use the KFP Python client directly:

```bash
kubectl port-forward -n kubeflow svc/ml-pipeline 8881:8888
python kfp_client.py
```

### Option 3: Access via API (When services are stable)
```bash
# Port forward the API
kubectl port-forward -n kubeflow svc/ml-pipeline 8081:8888

# Use the Python client
python kfp_client.py
```

## Pipeline Files

- `hello_world_pipeline.py` - KFP pipeline definition (compiles to YAML)
- `local_pipeline.py` - Local execution version
- `kfp_client.py` - API client for cluster interaction
- `simple_ui.py` - Simple web interface for pipeline management
- `demo_ui.py` - Demo guide and instructions
- `start_demo.sh` - One-click demo launcher
- `hello_world_pipeline.yaml` - Compiled pipeline for cluster deployment


## 🚀 Quick Demo

## 🚀 Quick Demo

### 🛠️ Useful kubectl Commands (with sample output)

Reviewers can run these in another terminal to verify cluster state.

```bash
# List all Kubeflow pods
kubectl get pods -n kubeflow
```
Sample output:
```
NAME                                               READY   STATUS    RESTARTS   AGE
cache-deployer-deployment-76b5f6dfb9-msvsw         1/1     Running   0          25m
cache-server-5c9cbc6c9b-bfhp8                      1/1     Running   0          25m
metadata-envoy-deployment-6ff5567745-gdt82         1/1     Running   0          25m
minio-77cc99749c-2bfxg                             1/1     Running   0          25m
ml-pipeline-78b99d9f4f-6c7zq                       1/1     Running   0          5m
ml-pipeline-ui-6975c875f8-p689c                    0/1     ImagePullBackOff   0   12m
...
```

```bash
# Describe a specific pod for debugging
kubectl describe pod ml-pipeline-78b99d9f4f-6c7zq -n kubeflow
```

```bash
# View logs from a pod
kubectl logs ml-pipeline-78b99d9f4f-6c7zq -n kubeflow
```

```bash
# Delete and restart a misbehaving pod
kubectl delete pod ml-pipeline-ui-6975c875f8-p689c -n kubeflow
```

```bash
# Check service endpoints
kubectl get svc -n kubeflow
```

These commands help verify that services are running, logs are healthy, and port-forward can be established.

```bash
cd kfp && ./start_demo.sh
```

### Manual Demo Steps:
```bash
# Terminal 1: Start API access
kubectl port-forward -n kubeflow svc/ml-pipeline 8881:8888

# Terminal 2: Start UI
cd kfp && source .kfp/bin/activate && python simple_ui.py
```

**Open:** http://localhost:5001

### Demo Script:
```bash
cd kfp && source .kfp/bin/activate && python demo_ui.py
```

**Demo Flow:**
1. Upload `hello_world_pipeline.yaml`
2. Run pipeline with custom parameters
3. Monitor execution in real-time
4. View results and logs