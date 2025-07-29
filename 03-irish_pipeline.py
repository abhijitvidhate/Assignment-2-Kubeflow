import kfp
from kfp import dsl
from typing import NamedTuple

# Step 1: Load dataset
@dsl.component
def load_data() -> NamedTuple('Output', [('features_path', str), ('labels_path', str)]):
    import pandas as pd
    from sklearn.datasets import load_iris
    import os

    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    labels = pd.Series(iris.target)

    os.makedirs('/tmp/data', exist_ok=True)
    features_path = '/tmp/data/features.csv'
    labels_path = '/tmp/data/labels.csv'

    df.to_csv(features_path, index=False)
    labels.to_csv(labels_path, index=False)

    return (features_path, labels_path)

# Step 2: Train model
@dsl.component
def train_model(features_path: str, labels_path: str) -> NamedTuple('Output', [('accuracy', float)]):
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    X = pd.read_csv(features_path)
    y = pd.read_csv(labels_path).squeeze()
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"Model accuracy: {acc}")
    return (acc,)

# Step 3: Define pipeline
@dsl.pipeline(
    name="iris-classifier-pipeline",
    description="A simple ML pipeline with Iris dataset"
)
def iris_pipeline():
    data = load_data()
    model = train_model(features_path=data.outputs['features_path'],
                        labels_path=data.outputs['labels_path'])

# Step 4: Compile pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        pipeline_func=iris_pipeline,
        package_path='iris_pipeline.yaml'
    )