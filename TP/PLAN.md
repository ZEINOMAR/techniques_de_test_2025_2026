# Plan d'action Tp technique de test

## objectif
L’objectif de ce TP est de concevoir, tester et valider le micro-service Triangulator, dont le rôle est de calculer la triangulation d’un ensemble de points 2D à partir d’un identifiant `pointSetId`.  

### test à réaliser
| Type de test | Objectif | Exemple de vérification |
|---------------|-----------|--------------------------|
| **Unitaire** | Vérifier le bon fonctionnement des fonctions internes | Tester l’encodage/décodage binaire et le calcul de triangulation |
| **API** | Vérifier la conformité de l’API avec la spec OpenAPI | Appel de `/triangulation/{pointSetId}` et contrôle des codes de retour (200, 400, 404, 500, 503) |
| **Intégration** | Tester les échanges entre Triangulator et PointSetManager | Simuler des réponses avec des mocks (succès, erreur, indisponibilité) |
| **Performance** | Mesurer la rapidité du service | Calcul de triangulation sur différents volumes de points |
| **Qualité** | Assurer un code propre et documenté | Vérification via `ruff`, `coverage` et `pdoc3` |
### structure du projet 
```
TECHNIQUES_DE_TEST_2025_2026/
│
├── TP/
│   ├── PLAN.md
│   ├── RETEX.md
│   ├── SUJET.md
│   ├── triangulation.png
│   ├── triangulator.yml
│   ├── point_set_manager.yml
│   ├── Makefile
│   │
│   ├── src/
│   │   └── triangulator/
│   │        (les fichier liés au triangulator)
│   ├── tests/
│   │   ├── unit/
│   │   │  (les differents tests unitaires envisagés)
│   │   │
│   │   ├── api/
│   │   │   └── test_api     
│   │   │
│   │   ├── integration/            
│   │   │   └── test_integration
│   │   │
│   │   └── perf/
│   │       └──  test_perf
│   └── docs/                             
├── pyproject.toml
├── requirements.txt
├── dev_requirements.txt
├── README.md
└── .gitignore                             

```
###  Exemple de test à faire
- **Tests unitaires**
  - Vérifier le bon encodage et décodage des données binaires.
  - Tester le calcul de triangulation sur différents ensembles de points.
  - Gérer les erreurs (points insuffisants, données invalides).

- **Tests API**
  - Tester la route `GET /triangulation/{pointSetId}` :
    - 200 → réponse binaire correcte.
    - 400 → ID invalide.
    - 404 → ID inconnu.
    - 500 → erreur interne.
    - 503 → service PointSetManager indisponible.

- **Tests d’intégration**
  - Simuler le comportement du PointSetManager avec des **mocks** pour tester les échanges entre services.

- **Tests de performance**
  - Mesurer le temps de traitement pour différents volumes de points.

- **Qualité**
  - Vérifier le code avec `ruff`.
  - Générer la couverture de test avec `coverage`.
### methodologie de travail
La méthode utilisée est le **TDD (Test Driven Development)**, ou développement guidé par les tests.  
Elle consiste à :

1. **Écrire les tests avant le code** : définir les comportements attendus avant d’implémenter les fonctions.  
2. **Faire échouer les tests** : vérifier que les tests détectent bien l’absence d’implémentation.  
3. **Coder la fonctionnalité minimale** pour faire passer les tests.  
4. **Relancer les tests** jusqu’à ce qu’ils soient tous réussis.  
5. **Améliorer et refactoriser le code** sans casser les tests existants.

Cette approche permet d’assurer la fiabilité du microservice **Triangulator**, de réduire les erreurs et de garantir que chaque fonction réponde exactement aux besoins spécifiés.