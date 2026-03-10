#!/usr/bin/env python3
"""
Kubeflow Pipelines Client - Connect to KFP API and manage pipelines
"""

import kfp
from kfp import dsl
import requests
import time

# KFP API endpoint (when running locally with port-forward)
KFP_HOST = "http://localhost:8081"

def check_kfp_connection():
    """Check if KFP API is accessible"""
    try:
        # Try to connect to the pipeline service
        response = requests.get(f"{KFP_HOST}/apis/v1beta1/healthz", timeout=5)
        if response.status_code == 200:
            print("✅ KFP API is accessible")
            return True
        else:
            print(f"❌ KFP API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to KFP API: {e}")
        print("💡 Make sure to port-forward the KFP UI service:")
        print("   kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80")
        return False

def create_client():
    """Create KFP client"""
    try:
        client = kfp.Client(host=KFP_HOST)
        print("✅ KFP Client created successfully")
        return client
    except Exception as e:
        print(f"❌ Failed to create KFP client: {e}")
        return None

@dsl.component
def hello_world_component(text: str) -> str:
    """A simple component that prints a message."""
    print(f"Hello, {text}!")
    return f"Hello, {text}!"

@dsl.pipeline(
    name="Hello World Pipeline",
    description="A simple hello world pipeline"
)
def hello_world_pipeline(text: str = "World"):
    hello_task = hello_world_component(text=text)

def upload_and_run_pipeline():
    """Upload pipeline and create a run"""
    client = create_client()
    if not client:
        return

    try:
        # Upload the pipeline
        pipeline_file = "hello_world_pipeline.yaml"
        pipeline_name = "hello-world-pipeline"

        print(f"📤 Uploading pipeline from {pipeline_file}...")
        pipeline = client.upload_pipeline(pipeline_file, pipeline_name)
        print(f"✅ Pipeline uploaded successfully: {pipeline.name}")

        # Create a run
        print("🚀 Creating a pipeline run...")
        run = client.run_pipeline(
            experiment_name="default",  # Use default experiment
            job_name=f"hello-world-run-{int(time.time())}",
            pipeline_id=pipeline.id,
            params={"text": "Kubeflow User from API"}
        )
        print(f"✅ Pipeline run created: {run.name}")
        print(f"📊 Run ID: {run.id}")

        # Monitor the run
        print("📊 Monitoring pipeline run...")
        run_detail = client.get_run(run.id)
        print(f"Run status: {run_detail.run.status}")

    except Exception as e:
        print(f"❌ Failed to upload/run pipeline: {e}")

if __name__ == "__main__":
    print("🔗 Connecting to Kubeflow Pipelines...")

    if check_kfp_connection():
        upload_and_run_pipeline()
    else:
        print("\n💡 Since UI is not accessible, you can:")
        print("1. Fix the UI pod image issue")
        print("2. Use the local pipeline execution (local_pipeline.py)")
        print("3. Wait for the cluster to stabilize")