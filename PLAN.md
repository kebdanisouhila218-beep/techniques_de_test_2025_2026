# Plan de Test

## 1. Objectifs du plan de test
Définir l'ensemble des tests nécessaires pour valider :
- La **justesse** de l'algorithme de triangulation.
- La **conformité** du composant `Triangulator` avec l'API décrite dans `triangulator.yml`.
- La **bonne interaction** entre le `Triangulator` et le `PointSetManager`.
- La **robustesse**, la **performance** et la **qualité** du code produit.

Nous adoptons une démarche **Test-Driven Development (TDD)** autant que possible : rédaction des tests avant l’implémentation.


## 2. Stratégie générale

Nous suivrons les niveaux de test suivants :

| Niveau | Description | Boîte | Outils | Objectif |
|-------|-------------|------|--------|----------|
| Tests unitaires | Algorithme de triangulation et conversion binaire ↔ structures internes | Boîte blanche | `pytest` | Vérifier la justesse computationnelle |
| Tests d’intégration | Communication avec PointSetManager (mocké) | Boîte grise | `unittest.mock` | Vérifier les interactions |
| Tests API (end-to-end) | Appels HTTP sur le serveur Flask | Boîte noire | `pytest` + client Flask | Vérifier le comportement global |
| Tests de performance | Mesure du temps de triangulation & conversions | — | `pytest` (marqué) | Mesurer temps / coûts mémoire |


## 3. Jeux de données (partitions d’équivalence)

### Pour les `PointSet` :

| Cas | Description | Exemple |
|-----|-------------|---------|
| P0 | Ensemble vide | 0 point |
| P1 | 1 seul point | trivial |
| P2 | 2 points | pas de triangle possible |
| P3 | 3 points formant un triangle simple | cas nominal minimal |
| Pn | Plusieurs points aléatoires | tests réalistes |
| P_colinéaires | Tous les points sur une droite | doit renvoyer aucun triangle |
| P_dupliqués | Points identiques répétés | doit être géré proprement |


## 4. Tests unitaires (niveau composant)

### 4.1. Conversion binaire → structure interne (`parse_point_set`)
- Lecture du nombre de points
- Conversion float correcte
- Gestion des cas limites (P0, P_colinéaires, P_dupliqués, données invalides)

### 4.2. Conversion structure interne → représentation `Triangles`
- Vérifier :
  - Nombre de sommets identique à l’entrée
  - Indices des sommets corrects
  - Ordre des triangles cohérent ou stable

### 4.3. Algorithme de triangulation
- Au minimum : Triangulation naïve (ex. Delaunay simplifiée ou ear-clipping)
- Tests attendus :
  - `3` points → 1 triangle
  - Points colinéaires → 0 triangle
  - Carré → 2 triangles


## 5. Tests d’intégration (avec mocks)

Comme le `Triangulator` dépend du `PointSetManager`, nous utiliserons des **mocks**.

| Test | Description | Mock attendu |
|------|-------------|--------------|
| Récupération OK | GET /pointset/{id} renvoie un set | Stub renvoyant un PointSet valide |
| PointSet inexistant | 404 renvoyé par PSM | Triangulator doit renvoyer 404 |
| Erreur réseau | Timeout simulé | Triangulator doit renvoyer 503 |


## 6. Tests API (end-to-end Flask)

Utilisation du client Flask (`app.test_client()`).

| Endpoint | Cas testés | Résultat attendu |
|---------|------------|----------------|
| POST /triangulate | PointSet valide | Retourne `Triangles` binaires |
| POST /triangulate | ID inconnu | 404 |
| POST /triangulate | Format binaire invalide | 400 |


## 7. Tests de performance

### Objectifs
- Mesurer les temps d’exécution pour différentes tailles d’ensembles :
  - 100 points
  - 1 000 points
  - 10 000 points
- Mesurer le coût CPU/mémoire de la conversion binaire

### Mise en place
- Tests marqués `@pytest.mark.performance`
- Exclu des tests standards → exécutable avec :  
  ```bash
  make perf_test
