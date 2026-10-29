# TP05 — Déploiement d’un modèle AutoML

Projet local construit à partir de l’énoncé TP05 et des scripts TP04. Tous les chemins ci-dessous sont relatifs à la racine de ce dépôt. Les services et l’interface MLflow sont locaux.

## Préparation (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
New-Item -ItemType Directory -Force data, src, models, reports | Out-Null
Copy-Item ..\tp4\donnees.py .
python donnees.py
```

## Démarrage

Dans un premier terminal activé :

```powershell
mlflow server --host 127.0.0.1 --port 5000 --workers 1 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts
```

Dans un second terminal activé :

```powershell
python src/automl_deploy.py
python src/modele_manuel.py
python src/promouvoir.py fraude-automl
python src/promouvoir.py fraude-manuel
```

Deux terminaux de service activés, chacun avec `$env:MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"` :

```powershell
mlflow models serve -m "models:/fraude-automl@production" -p 8100 --env-manager local
mlflow models serve -m "models:/fraude-manuel@production" -p 8101 --env-manager local
```

Dans le terminal de travail, lancez `python src/client.py 8100` et `python src/client.py 8101`. Après les captures demandées, arrêtez les services et le serveur avec `Ctrl+C`.

## Comparaison et rendu

Compléter `reports/tp5_comparaison.md` avec les valeurs observées. Ne versionner ni données, ni modèles sérialisés, ni base MLflow ou artefacts locaux. Le parcours Vertex AI est facultatif selon l’énoncé.
