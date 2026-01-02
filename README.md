**Démo vidéo de l’interface**

https://github.com/user-attachments/assets/9c7f7198-baed-4b94-ac30-2e674a6a6313

---

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
