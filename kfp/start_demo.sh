#!/bin/bash
# Quick Start Demo Script for KFP UI

echo "🚀 Starting KFP UI Demo..."
echo "=========================="

# Check if port-forward is running
if ! pgrep -f "kubectl port-forward.*ml-pipeline" > /dev/null; then
    echo "📡 Starting port-forward..."
    kubectl port-forward -n kubeflow svc/ml-pipeline 8881:8888 &
    sleep 3
else
    echo "✅ Port-forward already running"
fi

# Check if UI is running
if ! pgrep -f "python simple_ui.py" > /dev/null; then
    echo "🌐 Starting UI..."
    cd /home/abhijit/ML-Ops-Assignement/Assignment-2/kubeflow/kfp
    source .kfp/bin/activate
    python simple_ui.py &
    sleep 3
else
    echo "✅ UI already running"
fi

echo ""
echo "🎯 Demo Ready!"
echo "=============="
echo "📱 Open browser: http://localhost:5001"
echo ""
echo "📋 Quick Demo Steps:"
echo "1. Upload 'hello_world_pipeline.yaml'"
echo "2. Run the pipeline"
echo "3. Monitor execution"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user input
trap 'echo ""; echo "🛑 Stopping services..."; pkill -f "kubectl port-forward.*ml-pipeline"; pkill -f "python simple_ui.py"; exit' INT
wait