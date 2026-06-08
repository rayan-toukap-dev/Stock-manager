# 🛒 StockManager

Mini-ERP de gestion de vente et de stock développé en Python/Flask + SQLite.  
Projet réalisé en 1 jour pour démonstration technique.

---

##  Fonctionnalités

| Module | Fonctionnalité |
|--------|---------------|
| 📊 Dashboard | CA du jour, alertes stock faible, graphique 7 jours |
| 📦 Produits | Ajouter / Modifier / Supprimer / Rechercher |
| 💰 Caisse | Panier interactif, encaissement, reçu automatique |
| 🧾 Historique | Toutes les ventes avec détail des articles |

---

##  Stack technique

- **Backend** : Python 3.12 + Flask
- **Base de données** : SQLite (via module sqlite3 natif)
- **Frontend** : HTML/CSS vanilla + Chart.js
- **Architecture** : MVC simplifié (routes → BDD → templates)

---

##  Installation & Lancement

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

###  Structure du projet
mini-erp/
├── app.py          # Routes Flask + logique métier
├── database.py     # Connexion SQLite + initialisation
├── static/
│   └── style.css   # Styles globaux
└── templates/
├── base.html       # Layout commun (navbar)
├── dashboard.html  # KPIs + graphique
├── produits.html   # Liste produits
├── form_produit.html
├── caisse.html     # Interface caisse interactive
└── historique.html

---

##  Guide rapide (Formation personnel)

###  Ajouter un produit
1. Cliquer sur **Produits** dans la barre de navigation  
2. Cliquer sur **+ Ajouter**  
3. Remplir le nom, prix, stock et catégorie → **Ajouter**

###  Faire une vente
1. Cliquer sur **Caisse**  
2. Cliquer sur les produits à vendre (le panier se remplit à droite)  
3. Ajuster les quantités avec **+** / **−**  
4. Cliquer sur **✅ Encaisser** → le reçu s'affiche

###  Consulter les performances
1. Page **Dashboard** : chiffre du jour + alertes stock + graphique semaine  
2. Page **Historique** : toutes les ventes passées

---

##Auteur

**Rayan Ledoux Toukap Ngansop**  
Étudiant Master 1 Informatique — Université de Yaoundé 1  
📧 toukaprayan6@gmail.com | 📱 +237 6 76 13 54 97  
🔗 [github.com/rayan-toukap-dev](https://github.com/rayan-toukap-dev)