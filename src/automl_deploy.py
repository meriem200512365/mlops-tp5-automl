"""Train a FLAML classifier and register its export in the local MLflow registry."""
import sys
import time
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from flaml import AutoML
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BUDGET = 90
TRACKING_URI = "http://127.0.0.1:5000"


def main():
    df = pd.read_csv("data/transactions.csv")
    X, y = df.drop(columns="fraude"), df["fraude"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
    Path("reports").mkdir(exist_ok=True)
    Path("models").mkdir(exist_ok=True)

    automl = AutoML()
    start = time.time()
    automl.fit(Xtr, ytr, task="classification", metric="f1", time_budget=BUDGET,
               seed=42, verbose=0, log_file_name="reports/flaml_tp5.log")
    duration = round(time.time() - start, 1)
    model = automl.model.estimator
    f1_flaml = round(f1_score(yte, automl.predict(Xte)), 4)
    f1_model = round(f1_score(yte, model.predict(Xte)), 4)
    print("famille retenue    :", automl.best_estimator, "| classe :", type(model).__name__)
    print("F1 (objet FLAML)   :", f1_flaml)
    print("F1 (modele exporte):", f1_model, "<- doit etre identique")
    if f1_flaml != f1_model:
        raise RuntimeError("Le modèle extrait ne reproduit pas le F1 de FLAML")
    joblib.dump(model, "models/model_automl.pkl")

    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment("tp5-automl-deploiement")
    with mlflow.start_run(run_name=f"automl-{BUDGET}s"):
        mlflow.log_params({"outil": "flaml", "budget_s": BUDGET,
                           "famille": automl.best_estimator})
        mlflow.log_params({f"cfg_{k}": v for k, v in automl.best_config.items()})
        mlflow.log_metrics({"f1": f1_model, "duree_recherche_s": duration})
        mlflow.log_artifact("reports/flaml_tp5.log")
        info = mlflow.sklearn.log_model(
            model, name="model", input_example=Xte.head(3),
            registered_model_name="fraude-automl", serialization_format="cloudpickle")
    print("enregistre : fraude-automl, version", info.registered_model_version)


if __name__ == "__main__":
    main()
