#!/usr/bin/env python3
"""
KFP UI Demo Script - Quick demonstration of Kubeflow Pipelines UI functionality
"""

import time
import requests
import os

def demo_ui():
    """Demonstrate the KFP UI functionality"""

    print("🚀 KFP UI Demo - Quick Showcase")
    print("=" * 50)

    # Check if port-forward is running
    try:
        response = requests.get("http://localhost:8881/apis/v1beta1/healthz", timeout=5)
        if response.status_code == 200:
            print("✅ KFP API is accessible")
        else:
            print("❌ KFP API not accessible")
            print("💡 Start port-forward: kubectl port-forward -n kubeflow svc/ml-pipeline 8881:8888")
            return
    except:
        print("❌ Cannot connect to KFP API")
        print("💡 Start port-forward: kubectl port-forward -n kubeflow svc/ml-pipeline 8881:8888")
        return

    print("\n📋 Demo Steps:")
    print("1. Open browser to http://localhost:5001")
    print("2. Start the UI: python simple_ui.py")
    print("3. Follow these demo steps...")

    print("\n🎯 Demo Features:")

    # Check if pipeline file exists
    pipeline_file = "hello_world_pipeline.yaml"
    if os.path.exists(pipeline_file):
        print(f"✅ Pipeline file ready: {pipeline_file}")
    else:
        print(f"❌ Pipeline file missing: {pipeline_file}")
        print("   Run: python hello_world_pipeline.py")

    print("\n📤 Upload Pipeline:")
    print("   - Click 'Choose File' button")
    print(f"   - Select: {pipeline_file}")
    print("   - Enter pipeline name: 'demo-hello-world'")
    print("   - Click 'Upload Pipeline'")

    print("\n▶️  Run Pipeline:")
    print("   - Find 'demo-hello-world' in Pipelines list")
    print("   - Click 'Run' button")
    print("   - Enter run name: 'demo-run-1'")
    print("   - Click 'Run Pipeline'")

    print("\n📊 Monitor Execution:")
    print("   - Go to 'Recent Runs' section")
    print("   - Find your run in the list")
    print("   - Status should show: Running → Succeeded")
    print("   - Click run name for details")

    print("\n🎉 Demo Complete!")
    print("The UI provides full pipeline management:")
    print("   • Upload and manage pipelines")
    print("   • Create and monitor experiments")
    print("   • Run pipelines with parameters")
    print("   • View execution logs and artifacts")

    print("\n💡 Pro Tips:")
    print("   • Use the local execution for development: python local_pipeline.py")
    print("   • Check cluster status: kubectl get pods -n kubeflow")
    print("   • View logs: kubectl logs -n kubeflow <pod-name>")

if __name__ == "__main__":
    demo_ui()