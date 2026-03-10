#!/usr/bin/env python3
"""
Simple KFP Web UI - Alternative interface for Kubeflow Pipelines
"""

from flask import Flask, render_template_string, request, jsonify
import kfp
import os
import json
from datetime import datetime

app = Flask(__name__)

# KFP API endpoint
KFP_HOST = os.getenv('KFP_HOST', 'http://localhost:8881')  # Use different port to avoid conflicts

def get_kfp_client():
    """Get KFP client with error handling"""
    try:
        client = kfp.Client(host=KFP_HOST)
        return client
    except Exception as e:
        print(f"Failed to connect to KFP: {e}")
        return None

@app.route('/')
def index():
    """Main dashboard page"""
    client = get_kfp_client()

    pipelines = []
    experiments = []
    runs = []

    if client:
        try:
            # Get pipelines
            pipelines = client.list_pipelines().pipelines or []
        except:
            pipelines = []

        try:
            # Get experiments
            experiments = client.list_experiments().experiments or []
        except:
            experiments = []

        try:
            # Get recent runs
            runs = client.list_runs().runs or []
            runs = runs[:10]  # Show only recent 10 runs
        except:
            runs = []

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kubeflow Pipelines - Simple UI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #4285f4; border-bottom: 2px solid #4285f4; padding-bottom: 10px; }
            .section { margin: 20px 0; }
            .section h2 { color: #34a853; margin-bottom: 10px; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f8f9fa; font-weight: bold; }
            tr:hover { background-color: #f8f9fa; }
            .status { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
            .status-Succeeded { background-color: #d4edda; color: #155724; }
            .status-Failed { background-color: #f8d7da; color: #721c24; }
            .status-Running { background-color: #d1ecf1; color: #0c5460; }
            .status-Pending { background-color: #fff3cd; color: #856404; }
            .btn { background-color: #4285f4; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }
            .btn:hover { background-color: #3367d6; }
            .upload-form { background-color: #f8f9fa; padding: 15px; border-radius: 4px; margin: 10px 0; }
            .alert { padding: 10px; margin: 10px 0; border-radius: 4px; }
            .alert-error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            .alert-success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Kubeflow Pipelines - Simple UI</h1>

            {% if not client %}
            <div class="alert alert-error">
                <strong>Connection Issue:</strong> Cannot connect to KFP API at {{ kfp_host }}.
                Make sure to port-forward the service: <code>kubectl port-forward -n kubeflow svc/ml-pipeline 8881:8888</code>
            </div>
            {% endif %}

            <div class="section">
                <h2>📤 Upload Pipeline</h2>
                <form class="upload-form" action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="pipeline_file" accept=".yaml,.yml" required>
                    <input type="text" name="pipeline_name" placeholder="Pipeline Name" required>
                    <button type="submit" class="btn">Upload Pipeline</button>
                </form>
            </div>

            <div class="section">
                <h2>🔬 Experiments</h2>
                {% if experiments %}
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                    {% for exp in experiments %}
                    <tr>
                        <td>{{ exp.name }}</td>
                        <td>{{ exp.description or 'No description' }}</td>
                        <td>{{ exp.created_at.strftime('%Y-%m-%d %H:%M') if exp.created_at else 'Unknown' }}</td>
                        <td>
                            <a href="/experiment/{{ exp.id }}" class="btn">View Runs</a>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
                {% else %}
                <p>No experiments found.</p>
                {% endif %}
            </div>

            <div class="section">
                <h2>⚙️ Pipelines</h2>
                {% if pipelines %}
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                    {% for pipeline in pipelines %}
                    <tr>
                        <td>{{ pipeline.name }}</td>
                        <td>{{ pipeline.description or 'No description' }}</td>
                        <td>{{ pipeline.created_at.strftime('%Y-%m-%d %H:%M') if pipeline.created_at else 'Unknown' }}</td>
                        <td>
                            <form action="/run_pipeline" method="post" style="display: inline;">
                                <input type="hidden" name="pipeline_id" value="{{ pipeline.id }}">
                                <input type="text" name="run_name" placeholder="Run name" required>
                                <button type="submit" class="btn">Run</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
                {% else %}
                <p>No pipelines found. Upload a pipeline to get started.</p>
                {% endif %}
            </div>

            <div class="section">
                <h2>🏃 Recent Runs</h2>
                {% if runs %}
                <table>
                    <tr>
                        <th>Run Name</th>
                        <th>Pipeline</th>
                        <th>Status</th>
                        <th>Started</th>
                        <th>Actions</th>
                    </tr>
                    {% for run in runs %}
                    <tr>
                        <td>{{ run.name }}</td>
                        <td>{{ run.pipeline_spec.pipeline_name or 'Unknown' }}</td>
                        <td><span class="status status-{{ run.status or 'Unknown' }}">{{ run.status or 'Unknown' }}</span></td>
                        <td>{{ run.created_at.strftime('%Y-%m-%d %H:%M') if run.created_at else 'Unknown' }}</td>
                        <td>
                            <a href="/run/{{ run.id }}" class="btn">View Details</a>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
                {% else %}
                <p>No runs found.</p>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    """

    return render_template_string(html,
                                client=client,
                                pipelines=pipelines,
                                experiments=experiments,
                                runs=runs,
                                kfp_host=KFP_HOST)

@app.route('/upload', methods=['POST'])
def upload_pipeline():
    """Upload a pipeline"""
    if 'pipeline_file' not in request.files:
        return "No file provided", 400

    file = request.files['pipeline_file']
    pipeline_name = request.form.get('pipeline_name')

    if not file or not pipeline_name:
        return "Missing file or pipeline name", 400

    # Save uploaded file temporarily
    temp_path = f"/tmp/{pipeline_name}.yaml"
    file.save(temp_path)

    client = get_kfp_client()
    if not client:
        return "Cannot connect to KFP API", 500

    try:
        pipeline = client.upload_pipeline(temp_path, pipeline_name)
        os.remove(temp_path)  # Clean up
        return f"✅ Pipeline '{pipeline_name}' uploaded successfully!", 200
    except Exception as e:
        os.remove(temp_path)  # Clean up
        return f"❌ Failed to upload pipeline: {str(e)}", 500

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    """Run a pipeline"""
    pipeline_id = request.form.get('pipeline_id')
    run_name = request.form.get('run_name')

    if not pipeline_id or not run_name:
        return "Missing pipeline ID or run name", 400

    client = get_kfp_client()
    if not client:
        return "Cannot connect to KFP API", 500

    try:
        run = client.run_pipeline(
            experiment_name="default",
            job_name=run_name,
            pipeline_id=pipeline_id
        )
        return f"✅ Pipeline run '{run_name}' started! Run ID: {run.id}", 200
    except Exception as e:
        return f"❌ Failed to start pipeline run: {str(e)}", 500

@app.route('/experiment/<experiment_id>')
def view_experiment(experiment_id):
    """View experiment details"""
    client = get_kfp_client()
    if not client:
        return "Cannot connect to KFP API", 500

    try:
        runs = client.list_runs(experiment_id=experiment_id).runs
        experiment = client.get_experiment(experiment_id)

        runs_html = ""
        for run in runs:
            runs_html += f"<li>{run.name} - {run.status}</li>"

        html = f"""
        <h1>Experiment: {experiment.name}</h1>
        <p>{experiment.description or 'No description'}</p>
        <h2>Runs</h2>
        <ul>
        {runs_html}
        </ul>
        <a href="/">Back to Dashboard</a>
        """
        return html
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/run/<run_id>')
def view_run(run_id):
    """View run details"""
    client = get_kfp_client()
    if not client:
        return "Cannot connect to KFP API", 500

    try:
        run = client.get_run(run_id)
        html = f"""
        <h1>Run: {run.name}</h1>
        <p>Status: {run.status}</p>
        <p>Pipeline: {run.pipeline_spec.pipeline_name}</p>
        <p>Started: {run.created_at}</p>
        <a href="/">Back to Dashboard</a>
        """
        return render_template_string(html, run=run)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    print(f"🚀 Starting Simple KFP UI on http://localhost:5001")
    print(f"📡 Connecting to KFP API at: {KFP_HOST}")
    print("💡 Make sure to port-forward: kubectl port-forward -n kubeflow svc/ml-pipeline 8881:8888")
    app.run(host='0.0.0.0', port=5001, debug=True)