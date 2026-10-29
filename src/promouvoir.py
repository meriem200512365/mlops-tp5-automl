"""Set the production alias on the latest registered version of a model."""
import sys

import mlflow
from mlflow import MlflowClient


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"fraude-automl", "fraude-manuel"}:
        raise SystemExit("Usage: python src/promouvoir.py fraude-automl|fraude-manuel")
    name = sys.argv[1]
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    client = MlflowClient()
    versions = client.search_model_versions(f"name='{name}'")
    if not versions:
        raise SystemExit(f"Aucune version trouvée pour {name}")
    latest = max(int(v.version) for v in versions)
    client.set_registered_model_alias(name, "production", str(latest))
    print(f"{name} : version {latest} promue (alias production)")


if __name__ == "__main__":
    main()
