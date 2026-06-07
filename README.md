# 🛒 StockManager

Mini-ERP de gestion de vente et de stock développé en Python/Flask + SQLite.  
Projet réalisé en 1 jour pour démonstration technique.

---

## ✨ Fonctionnalités

| Module | Fonctionnalité |
|--------|---------------|
| 📊 Dashboard | CA du jour, alertes stock faible, graphique 7 jours |
| 📦 Produits | Ajouter / Modifier / Supprimer / Rechercher |
| 💰 Caisse | Panier interactif, encaissement, reçu automatique |
| 🧾 Historique | Toutes les ventes avec détail des articles |

---

## 🛠️ Stack technique

- **Backend** : Python 3.12 + Flask
- **Base de données** : SQLite (via module sqlite3 natif)
- **Frontend** : HTML/CSS vanilla + Chart.js
- **Architecture** : MVC simplifié (routes → BDD → templates)

---

## 🚀 Installation & Lancement

```bash
# 1. Cloner le repo
git clone https://github.com/rayan-toukap-dev/Stock-manager
cd Stock-manager

# 2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install flask

# 4. Lancer
python app.py
# → http://127.0.0.1:5000
```

---

## 📁 Structure du projet