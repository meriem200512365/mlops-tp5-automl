# Modèle manuel ou modèle AutoML ? (TP05)

Les valeurs ci-dessous doivent être complétées avec les mesures de cette exécution. Le jeu de test commun utilise `test_size=0.25` et `random_state=42`.

| Critère | Manuel (RF 500/16) | AutoML (FLAML 90 s) |
|---|---:|---:|
| Famille de modèle | Forêt aléatoire | XGBoost |
| F1 sur le jeu de test | 0,8669 | 0,8561 |
| Temps de recherche machine | Entraînement : 0,9 s | Recherche : 90,2 s |
| Temps humain (estimation) | Environ 1 h pour essais et réglages TP2 (à confirmer par le groupe) | Environ 15 min de préparation, puis 90 s de recherche (à confirmer par le groupe) |
| Latence médiane (ms) | 32,6 (deux mesures : 32,2 et 32,9) | 30,8 (deux mesures : 30,9 et 30,7) |
| Latence p95 (ms) | 48,5 (deux mesures : 47,8 et 49,2) | 31,8 (deux mesures : 31,8 et 31,7) |
| Taille du fichier (Mo) | 13,37 | 0,28 |
| Explicabilité | Importance des variables, 500 arbres, profondeur maximale 16 | Importance des variables XGBoost et configuration retenue visible dans le run MLflow |

## Décision (5 lignes)

Nous recommandons le modèle AutoML XGBoost pour ce déploiement local : il atteint F1 = 0,8561, contre 0,8669 pour la forêt manuelle.
L’écart de F1 est de 0,0108 ; il reste à vérifier que cette baisse respecte le seuil métier de détection des fraudes.
Le fichier AutoML pèse 0,28 Mo, contre 13,37 Mo pour le modèle manuel.
Sa latence médiane mesurée est de 30,8 ms et son p95 de 31,8 ms, contre 32,6 ms et 48,5 ms pour la forêt.
Nous le mettrions en production après validation du coût des faux négatifs, avec surveillance du F1 et retour possible au modèle manuel.

## Réponses aux questions

1. **Choix de production :** décider à partir des F1 mesurés et des contraintes de latence, taille, explicabilité et coût de maintenance. Le meilleur F1 seul ne suffit pas.
2. **Coût mensuel d’un endpoint Vertex AI :** hypothèse au 29 octobre 2026, un n1-standard-4 en us-central1 pendant 30 jours, au tarif public de 0,2279988 USD/heure : 0,2279988 × 24 × 30 = **164,16 USD/mois**. Le tarif AutoML tabulaire en inférence suit celui des modèles personnalisés ; le coût court pendant que le nœud est prêt, même sans requêtes. Estimation hors stockage, réseau, taxes et éventuelles remises. [Tarifs Google Cloud](https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing) ; [facturation des nœuds prêts](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/tabular-data/tabular-workflows/e2e-automl-online-predictions).
3. **Latence locale et cloud :** le cloud ajoute le délai réseau, le routage, le traitement du service distant et parfois le démarrage/chargement du modèle. Comparer ces facteurs aux médianes et p95 locaux mesurés au bloc D.
4. **Changement du moteur cloud :** une mise à jour peut modifier les prédictions, les performances ou le comportement d’exécution. Le risque est une régression ou une perte de reproductibilité sans versionnage et validation.
5. **Réversibilité :** conserver les données et leur schéma, le code, les paramètres, les versions de dépendances, les métriques et un artefact exportable ; tester régulièrement le ré-entraînement ou le déploiement hors plateforme.
6. **skops ou cloudpickle :** le modèle AutoML peut être une classe issue de différentes bibliothèques et requérir une sérialisation Python plus générale, d’où cloudpickle. Les formats pickle peuvent exécuter du code au chargement ; cela reste acceptable ici pour un artefact généré et chargé localement dans un environnement de confiance, jamais pour un fichier non fiable.

## Captures à insérer dans le rapport final

- Capture 1 : run `automl-90s` et fichier MLmodel dans l’interface MLflow.
- Capture 2 : services AutoML (8100) et manuel (8101) démarrés.
- Capture 3 : sorties client pour les deux ports et réponse à une requête invalide.
