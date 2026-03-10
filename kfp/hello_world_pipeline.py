import kfp
from kfp import dsl

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

if __name__ == "__main__":
    # Compile the pipeline for cluster deployment
    kfp.compiler.Compiler().compile(
        pipeline_func=hello_world_pipeline,
        package_path="hello_world_pipeline.yaml"
    )
    print("Pipeline compiled to hello_world_pipeline.yaml")