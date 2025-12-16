# RETEX – Techniques de Test (Projet Triangulator)

## 1. Contexte et Objectifs

Ce projet avait pour but de développer un micro-service de triangulation 2D robuste, performant et conforme à une spécification binaire stricte. La contrainte majeure était l'absence de bibliothèques tierces pour la géométrie (comme `numpy` ou `scipy`), imposant une implémentation "from scratch".

L'objectif pédagogique principal était d'adopter une approche **"Test First"** : concevoir les tests et l'architecture avant l'implémentation finale pour garantir la fiabilité et prévenir les régressions.

---

## 2. Choix Techniques et Architecture

### Architecture Modulaire

J'ai opté pour une séparation stricte des responsabilités afin de maximiser la testabilité :

- **`core.py`** : Contient l'algorithme de **Bowyer-Watson**. Ce module est pur (sans entrées/sorties), ce qui le rend facile à tester avec des jeux de données statiques.
- **`binary.py`** : Gère la sérialisation bas niveau (`struct.pack/unpack`). Isoler cette partie a permis de valider le protocole binaire indépendamment de la logique métier.
- **`client_psm.py`** : Encapsule les appels réseaux via `urllib`. Cela a permis de mocker facilement les appels externes sans dépendre du serveur réel.

### Algorithme

Le choix s'est porté sur l'algorithme de **Bowyer-Watson** pour la triangulation de Delaunay. Bien que complexe à implémenter (gestion du "Super Triangle", nettoyage des triangles externes), c'est une méthode itérative qui s'intègre parfaitement dans un pipeline de traitement point par point.

---

## 3. Stratégie de Test (TDD et Qualité)

J'ai suivi une approche itérative en trois phases :

1. **Phase "Stub" (Bouchon)** : J'ai d'abord écrit des tests validant l'API et le binaire avec une fonction de triangulation factice. Cela a permis de valider la chaîne d'intégration continue (CI) très tôt.
2. **Phase Implémentation** : J'ai remplacé le bouchon par l'algorithme réel. Les tests existants ont servi de filet de sécurité pour vérifier que l'intégration restait fonctionnelle.
3. **Phase Couverture (100%)** : J'ai ajouté des tests spécifiques pour atteindre les cas limites (branches d'erreurs, exceptions réseau, fichiers corrompus).

### Types de tests implémentés :

- **Unitaires (`tests/unit`)** : Couverture exhaustive des modules `binary` et `core`. Utilisation intensive de `unittest.mock` et `monkeypatch` pour simuler les réponses HTTP (200, 404, 503) du client PSM.
- **Intégration (`tests/integration`)** : Validation du flux complet (API → Decode → Triangulate → Encode). J'ai pu vérifier que les erreurs de format binaire remontaient correctement sous forme d'erreurs HTTP 400.
- **Performance (`tests/perf`)** : Validation que l'algorithme traite 200 points en moins de 0.5 seconde.

---

## 4. Difficultés et Solutions

### Le Mocking des appels réseau

Simuler `urllib` pour atteindre **98% de couverture** dans `client_psm.py` a été l'un des défis majeurs.

- **Problème :** Tester les timeouts ou les erreurs protocolaires (418 I'm a teapot) sans accès internet réel.
- **Solution :** Utilisation de `patch` pour intercepter `urlopen` et lever manuellement des exceptions `URLError` ou `HTTPError` contrôlées.

### Rigueur du Linter (`ruff`)

L'outil de linting imposait des règles strictes (docstrings à l'impératif, longueur de ligne < 88 caractères).

- **Impact :** Cela a forcé une refactorisation du code, notamment le découpage des formules mathématiques complexes dans `core.py` pour les rendre plus lisibles.
- **Apprentissage :** J'ai compris que la qualité de code ne concerne pas que le fonctionnement, mais aussi la maintenabilité et la lisibilité.

---

## 5. Bilan et Améliorations Possibles

### Ce qui a bien fonctionné :

- **L'automatisation via le Makefile :** Avoir des commandes simples (`make test`, `make coverage`, `make lint`) a fluidifié le développement.
- **La robustesse :** La couverture à 100% m'a forcé à gérer des cas "impossibles" en temps normal (fichiers tronqués, octets en trop), rendant le code très solide.

### Pistes d'amélioration :

- **Précision des flottants :** L'algorithme actuel utilise des comparaisons strictes. Une approche avec une tolérance (epsilon) serait plus sûre pour gérer parfaitement les points colinéaires ou très proches.
- **Optimisation :** Pour de très grands jeux de données (>10 000 points), une structure spatiale comme un Quadtree serait nécessaire pour optimiser la recherche des triangles.

---

## 6. Retour d’expérience personnel

Ce projet a été particulièrement formateur car il m’a obligé à adopter une démarche rigoureuse, centrée sur les tests et la qualité logicielle, bien différente d’un développement classique orienté uniquement vers l’implémentation.

### Ce que j’estime avoir bien fait

Le principal point positif de mon travail est l’adoption réelle d’une démarche **Test First**. L’écriture des tests avant l’implémentation m’a permis de clarifier très tôt les responsabilités de chaque module, les formats de données attendus et les comportements en cas d’erreur. Cette approche a fortement limité le couplage entre les couches API, logique métier, sérialisation binaire et communication réseau.

La séparation claire des modules (`core`, `binary`, `client_psm`, `api`) s’est révélée être un excellent choix. Elle a facilité le mocking, les tests d’intégration et les refactorisations successives sans introduire de régressions. De plus, l’utilisation systématique du linter (`ruff`) m’a conduit à produire un code lisible, cohérent et bien documenté.

Enfin, la recherche d’une couverture de tests élevée m’a obligé à traiter de nombreux cas limites (buffers binaires corrompus, octets supplémentaires, erreurs réseau inattendues), ce qui a rendu le service final bien plus robuste qu’une implémentation minimale.

### Ce que j’ai mal anticipé ou sous-estimé

J’ai initialement sous-estimé le temps nécessaire pour satisfaire pleinement les contraintes de qualité imposées par le linting (docstrings à l’impératif, sections bien structurées, longueur de ligne). Ces règles se sont révélées centrales dans la validation finale du projet.

De plus, mon plan de tests initial pour l’algorithme de triangulation était trop optimiste. Certains comportements géométriques (points colinéaires, points internes) n’ont réellement été compris qu’au moment de l’implémentation, ce qui a nécessité une évolution des tests.

### Ce que je ferais autrement avec le recul

Si je devais refaire ce projet, je commencerais par des tests plus abstraits et plus simples pour l’algorithme de triangulation, quitte à les affiner progressivement. Cela permettrait d’obtenir plus rapidement une version fonctionnelle de bout en bout.

Je consacrerais également plus de temps dès le début à l’étude détaillée des règles de qualité, afin d’écrire directement des docstrings conformes et éviter de nombreuses corrections en fin de projet.

### Évaluation du plan initial

Avec le recul, le plan initial était pertinent sur le plan architectural, mais incomplet sur le plan des cas limites réels. L’évolution progressive des tests s’est cependant révélée positive, car elle reflète une démarche réaliste de développement logiciel.

### Conclusion personnelle

Ce projet m’a permis de comprendre que les tests ne sont pas uniquement un outil de validation, mais un véritable levier de conception. Ils influencent directement l’architecture, la maintenabilité et la capacité d’évolution d’un projet logiciel sans régression.