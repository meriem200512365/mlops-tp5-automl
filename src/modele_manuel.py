"""Train and register the TP2 random-forest reference model."""
import sys
import time
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main():
    df = pd.read_csv("data/transactions.csv")
    X, y = df.drop(columns="fraude"), df["fraude"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
    start = time.time()
    model = RandomForestClassifier(n_estimators=500, max_depth=16,
                                   random_state=42).fit(Xtr, ytr)
    duration = round(time.time() - start, 1)
    f1 = round(f1_score(yte, model.predict(Xte)), 4)
    Path("models").mkdir(exist_ok=True)
    joblib.dump(model, "models/model_manuel.pkl")
    print("modele manuel : F1 =", f1, "| entrainement", duration, "s")

    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("tp5-automl-deploiement")
    with mlflow.start_run(run_name="manuel-rf-500-16"):
        mlflow.log_params({"outil": "scikit-learn", "n_estimators": 500,
                           "max_depth": 16})
        mlflow.log_metrics({"f1": f1, "duree_entrainement_s": duration})
        info = mlflow.sklearn.log_model(
            model, name="model", input_example=Xte.head(3),
            registered_model_name="fraude-manuel",
            skops_trusted_types=["sklearn.tree._tree.Tree"])
    print("enregistre : fraude-manuel, version", info.registered_model_version)


if __name__ == "__main__":
    main()
