# PLAN.md - Plan de tests pour le Triangulator

## 1. Objectifs généraux
- Vérifier la **justesse** de l’algorithme de triangulation (ex: Delaunay ?)
- Valider la **conformité de l’API HTTP** (triangulator.yml)
- Tester la **robustesse** face à des erreurs (ex: ID invalide, PointSet vide…)
- Mesurer la **performance** pour différents volumes de points
- Assurer la **qualité du code** (ruff) et **documenter** (pdoc3)

## 2. Tests unitaires (boîte blanche)

### 2.1 Triangulation algorithmique
- Fonction `triangulate(points: List[Tuple[float, float]]) -> List[Triangle]`
- Cas à tester :
  - Ensemble vide → retourne liste vide
  - 1 ou 2 points → pas de triangle possible
  - 3 points non alignés → 1 triangle
  - Points alignés → aucun triangle
  - Cas complexes (10+ points, formes irrégulières)
  - Tests avec valeurs limites (très petits/grands float)

### 2.2 Sérialisation binaire
- `encode_pointset(points)` / `decode_pointset(data)`
- `encode_triangles(triangles)` / `decode_triangles(data)`
- Vérifier round-trip : `decode(encode(x)) == x`
- Tester données corrompues → doivent lever des exceptions

## 3. Tests d’intégration / API (boîte noire)

### 3.1 Endpoint `/triangulate/<pointset_id>`
- Mock du **PointSetManager** (cf. CM2 → mocks avec `unittest.mock`)
- Simuler :
  - Réponse 200 avec PointSet valide → retourne triangles encodés
  - Réponse 404 (ID inconnu) → API renvoie 404
  - Réponse 500 (PointSetManager down) → API renvoie 502/503
  - PointSet vide ou invalide → logique gère proprement

### 3.2 Format de réponse
- Vérifier que la réponse est bien en **binaire brut** (pas JSON)
- Vérifier le `Content-Type` (peut être `application/octet-stream`)

## 4. Tests de robustesse
- ID non numérique → 400 Bad Request
- Envoi de données binaires corrompues au decodeur → exception gérée
- PointSet avec 1 million de points → pas de crash (mais test perf séparé)

## 5. Tests de performance (`perf_test`)
- Mesurer le temps de triangulation pour :
  - 10, 100, 1 000, 10 000 points
- Utiliser `pytest` avec marqueur `@pytest.mark.slow`
- Isoler ces tests → `make perf_test` ≠ `make unit_test`

## 6. Outils et organisation
- **Framework** : `pytest`
- **Mocks** : `unittest.mock` pour simuler `PointSetManager`
- **Couverture** : `coverage` → cible : ≥90%
- **Qualité** : `ruff check` → 0 warning
- **Doc** : `pdoc3` sur les fonctions principales
- **Makefile** avec les 6 commandes demandées