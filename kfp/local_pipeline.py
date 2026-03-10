#!/usr/bin/env python3
"""
Simple Local Implementation of Kubeflow Pipeline
This script demonstrates a basic pipeline execution locally without Kubernetes.
"""

def hello_world_component(text: str) -> str:
    """A simple component that prints a message."""
    print(f"Hello, {text}!")
    return f"Hello, {text}!"

def hello_world_pipeline(text: str = "World"):
    """Simulate the pipeline execution."""
    print("Starting Hello World Pipeline...")
    result = hello_world_component(text=text)
    print("Pipeline completed.")
    return result

if __name__ == "__main__":
    # Run the pipeline locally
    result = hello_world_pipeline(text="Kubeflow User")
    print("Final result:", result)