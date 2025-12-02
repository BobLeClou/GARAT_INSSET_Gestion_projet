# GARAT_INSSET_Gestion_projet

Ce dépôt contient une API web Python (Flask) conteneurisée qui implémente les opérations CRUD pour la gestion d'utilisateurs. Le projet a été conçu comme base pédagogique pour apprendre l'intégration continue, le déploiement et le monitoring d'une application conteneurisée.

**But du projet**

- **API CRUD**: créer, lire, modifier et supprimer des utilisateurs.
- **Conteneurisation**: image Docker fournie pour exécuter l'application en local et en environnement cloud.
- **Observation**: configuration minimale pour la journalisation.

**Fonctionnalités principales**

- **Endpoints REST** pour la gestion des utilisateurs (voir `app/app.py`).
- **Accès base de données** encapsulé dans `app/database.py` et `app/crud.py`.
- **Templates HTML** pour des vues simples dans `app/templates/`.

**Déploiement / CI-CD (état actuel)**

J'ai tenté d'implémenter un pipeline CI/CD pour déployer l'image sur Google Cloud Platform (GCP), mais je n'ai pas réussi à finaliser cette partie à cause de nombreuses difficultés techniques, et d'un manque d'organisation de mon côté. Etant en congé la semaine du 1 décembre, j'ai naivement pensé qu'en travaillant dessus le weekend précédent, j'arriverai à fournir un livrable propre. J'ai grandement sous-estimé le temps que cela m'as demandé, et ai travaillé dessus non seulement le weekend, mais aussi une grande partie du lundi. Malheureusement le projet n'est fonctionnel que jusqu'au moment de déployer le fichier du cloud-run-service.


**Remarques finales**

Le code de l'API et les templates sont présents et utilisables en local. La partie CI/CD / déploiement GCP nécessite encore du travail et des vérifications de configuration (autorisations, secrets, registry).
