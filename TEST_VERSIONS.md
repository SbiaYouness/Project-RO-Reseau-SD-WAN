# 🧪 Test des Versions - Comparaison des Courbures

J'ai créé **3 versions différentes** pour résoudre les chevauchements de liens sur le côté gauche (C, R, M, A, S, B).

## 📦 Versions Disponibles

### Version 1: Courbures Agressives 🔵

**Fichier**: `app_version1.py`
**Stratégie**: Valeurs rad très élevées partout (0.4 à 0.6)
**Avantages**: Séparation maximale des liens
**Test**:

```powershell
streamlit run app_version1.py
```

### Version 2: Courbures Sélectives 🟢

**Fichier**: `app_version2.py`
**Stratégie**: Focus sur le côté gauche uniquement (rad 0.5-0.6 à gauche, modéré à droite)
**Avantages**: Balance entre lisibilité et séparation
**Test**:

```powershell
streamlit run app_version2.py
```

### Version 3: Approche Mixte 🟡

**Fichier**: `app_version3.py`
**Stratégie**: Alternance stratégique +/- pour éviter les conflits
**Avantages**: Courbes naturelles et séparation intelligente
**Test**:

```powershell
streamlit run app_version3.py
```

## 🎯 Comment Tester

1. **Ouvrez un terminal PowerShell**
2. **Activez l'environnement virtuel**:

   ```powershell
   cd "c:\Users\lampr\OneDrive\Documents\aa\ALL\RECHERCHE OPERATIONNELLE\AA project\Projet R.O"
   .\.venv\Scripts\Activate.ps1
   ```

3. **Testez chaque version** (une à la fois):

   ```powershell
   # Version 1
   streamlit run app_version1.py --server.port 8501

   # Arrêtez avec Ctrl+C, puis testez Version 2
   streamlit run app_version2.py --server.port 8502

   # Arrêtez avec Ctrl+C, puis testez Version 3
   streamlit run app_version3.py --server.port 8503
   ```

4. **Testez le chemin Casablanca → Marrakech** sur chaque version

## 📊 Points de Comparaison

Pour chaque version, vérifiez:

- ✅ Les liens C→M, C→R ne se chevauchent pas
- ✅ Les liens A→M, A→S, A→B sont séparés
- ✅ Les liens R→M, R→F sont visibles
- ✅ Les labels de latence sont lisibles
- ✅ L'apparence générale est esthétique

## 💡 Recommandations

- **Version 1**: Si vous voulez la séparation maximale (peut sembler "trop courbé")
- **Version 2**: Compromis équilibré (recommandé pour commencer)
- **Version 3**: Si vous préférez des courbes plus naturelles

## ⚡ Commande Rapide

Pour tester les 3 versions rapidement avec des ports différents:

```powershell
# Terminal 1
streamlit run app_version1.py --server.port 8501

# Terminal 2
streamlit run app_version2.py --server.port 8502

# Terminal 3
streamlit run app_version3.py --server.port 8503
```

Ensuite ouvrez:

- Version 1: http://localhost:8501
- Version 2: http://localhost:8502
- Version 3: http://localhost:8503

## 📝 Après le Test

Une fois que vous avez choisi la meilleure version:

1. Dites-moi laquelle vous préférez
2. Je remplacerai le fichier `app.py` principal avec celle-ci
3. L'application finale sera prête! 🎉
