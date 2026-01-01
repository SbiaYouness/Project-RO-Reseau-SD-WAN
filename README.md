# Projet Recherche Opérationnelle - Plus Court Chemin

Application de calcul du plus court chemin entre les villes marocaines avec simulation de pannes.

## Structure du Projet

### Fichiers Principaux
- **app.py** - Application Streamlit (interface web)
- **graph_algorithms.py** - Implémentation des algorithmes (Dijkstra et Bellman-Ford)
- **djikstra.py** - Version standalone de l'algorithme de Dijkstra
- **bellman_ford.py** - Version standalone de l'algorithme de Bellman-Ford
- **MatriceAdj.py** - Représentation du graphe en matrice d'adjacence

### Réseau de Villes
- **C** : Casablanca (Siège et Datacenter principal)
- **R** : Rabat (Direction régionale et Datacenter de secours)
- **T** : Tanger
- **F** : Fès
- **M** : Marrakech
- **A** : Agadir
- **O** : Oujda
- **B** : Béni Mellal
- **S** : Safi
- **H** : Hoceima

## Installation

```powershell
# Activer l'environnement virtuel
.venv\Scripts\activate

# Installer les dépendances (si nécessaire)
pip install -r requirements.txt
```

## Lancement

```powershell
streamlit run app.py
```

L'application sera accessible sur http://localhost:8501

## Fonctionnalités

✅ **Calcul du Plus Court Chemin** - Algorithme de Dijkstra
✅ **Visualisation Graphique** - Réseau interactif avec positions fixes
✅ **Simulation de Pannes** - Désactivation de villes et liaisons
✅ **Interface Bilingue** - Labels en français
✅ **Graphe Bidirectionnel** - Toutes les liaisons fonctionnent dans les deux sens

## Tests de Validation

Les algorithmes ont été testés et validés:
- Dijkstra et Bellman-Ford donnent des résultats identiques
- Tous les chemins sont bidirectionnels (A→B = B→A)
- Toutes les villes sont accessibles depuis n'importe quel point
- Les distances calculées sont les plus courtes possibles
