# Plan de Test

## 1. Objectifs du plan de test
Définir l'ensemble des tests nécessaires pour valider :
- La **justesse** de l'algorithme de triangulation.
- La **conformité** du composant `Triangulator` avec l'API décrite dans `triangulator.yml`.
- La **bonne interaction** entre le `Triangulator` et le `PointSetManager`.
- La **robustesse**, la **performance** et la **qualité** du code produit.

Nous adoptons une démarche **Test-Driven Development (TDD)** : les tests guident l’implémentation.


## 2. Stratégie générale

| Niveau | Description | Pourquoi ? | Comment ? | Outils | Type |
|-------|-------------|------------|-----------|--------|------|
| Tests unitaires | Tests de l’algorithme et de la conversion binaire | Garantir la justesse interne du traitement | Tester directement les fonctions internes avec des jeux de données connus | `pytest` | Boîte blanche |
| Tests d’intégration | Interaction Triangulator ↔ PointSetManager | Valider le dialogue entre services | Utilisation de **mocks** pour simuler l’API externe | `unittest.mock`, `pytest` | Boîte grise |
| Tests API (end-to-end) | Tests HTTP complets sur Flask | Vérifier le comportement réel du service | Utilisation du `test_client` Flask pour envoyer des requêtes | `pytest` + Flask client | Boîte noire |
| Tests de performance | Mesure temps / mémoire | Assurer que la triangulation reste utilisable à grande échelle | Génération de grands ensembles + mesure d’exécution | `pytest` (marquage) | — |


## 3. Jeux de données (partitions d’équivalence)

Ces jeux sont définis pour s’assurer que **chaque type de cas possible** est couvert.

| Cas | Pourquoi ? | Exemple | Attendu |
|-----|------------|---------|---------|
| P0 | Vérifier gestion du vide | `[]` | Aucun triangle |
| P1 | Cas limite trivial | `[1 point]` | Aucun triangle |
| P2 | Segments | 2 points | Aucun triangle |
| P3 | Cas minimal formant un triangle | 3 points non colinéaires | 1 triangle correct |
| Pn | Cas réaliste | 10+ points | Plusieurs triangles cohérents |
| P_colinéaires | Gestion des entrées dégénérées | points alignés | 0 triangle |
| P_dupliqués | Robustesse aux doublons | points répétés | Doit ignorer ou traiter correctement |


## 4. Tests unitaires (niveau composant)

### Pourquoi ?
Ces tests assurent la validité du cœur logique du service, indépendamment du réseau ou de l’API externe.

### Comment ?
- On crée des données binaires artificielles
- On les passe aux fonctions internes
- On compare avec les résultats attendus

### 4.1. `parse_point_set`
- Lecture correcte du nombre de points
- Conversion correcte `float ↔ binaire`
- Tests sur données invalides (bytes mal formés)

### 4.2. Génération de la structure `Triangles`
- Vérification du respect du format binaire attendu
- Correspondance correcte indices → sommets

### 4.3. Algorithme de triangulation
Cas testés :
| Entrée | Attendu |
|--------|---------|
| 3 points | 1 triangle |
| 4 points formant un carré | 2 triangles |
| Points colinéaires | 0 triangle |


## 5. Tests d’intégration (avec mocks)

### Pourquoi ?
Le `Triangulator` ne stocke rien : il **dépend** du `PointSetManager`.  
On doit donc vérifier l’interaction sans dépendre d’un vrai réseau.

### Comment ?
- Utilisation de `unittest.mock.Mock` pour simuler les réponses HTTP du PSM.
- Les tests vérifient :
  - Réponses correctes selon le statut du PSM.
  - Gestion des erreurs réseau.

| Test | Scénario simulé | Attendu |
|------|-----------------|---------|
| Récupération OK | Le PSM renvoie un set valide | Triangulateur renvoie Triangles |
| ID inconnu | PSM renvoie 404 | Triangulateur renvoie 404 |
| Timeout | PSM ne répond pas | Triangulateur renvoie 503 |


## 6. Tests API (end-to-end Flask)

### Pourquoi ?
Pour s'assurer que le service complet fonctionne **tel qu’un client l’utiliserait**.

### Comment ?
- Démarrer l'application Flask en mode test
- Appeler les endpoints en binaire via `test_client`

| Endpoint | Cas testés | Résultat attendu |
|---------|------------|----------------|
| POST /triangulate | ID valide | Response 200 + Triangles binaires |
| POST /triangulate | ID inconnu | Response 404 |
| POST /triangulate | Format binaire invalide | Response 400 |


## 7. Tests de performance

### Pourquoi ?
La triangulation peut être coûteuse → il faut garantir un temps raisonnable.

### Comment ?
- Génération automatique d’ensembles de tailles croissantes
- Mesure du temps via `time.perf_counter()`
- Tests marqués `@pytest.mark.performance` pour exclusion du run normal

Exécution :
```bash
make perf_test
