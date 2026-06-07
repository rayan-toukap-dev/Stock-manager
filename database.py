import sqlite3
import os

DB_PATH = "erp.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            categorie TEXT DEFAULT 'Général',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS ventes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL,
            date_vente TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS lignes_vente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vente_id INTEGER NOT NULL,
            produit_id INTEGER NOT NULL,
            produit_nom TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            prix_unitaire REAL NOT NULL,
            FOREIGN KEY (vente_id) REFERENCES ventes(id),
            FOREIGN KEY (produit_id) REFERENCES produits(id)
        );
    """)


    cursor.execute("SELECT COUNT(*) FROM produits")
    if cursor.fetchone()[0] == 0:
        produits_demo = [
                ("Riz (1kg)", 800, 50, "Alimentation"),
                ("Huile (1L)", 1200, 30, "Alimentation"),
                ("Savon Protex", 500, 80, "Hygiène"),
                ("Sucre (1kg)", 700, 40, "Alimentation"),
                ("Eau minérale", 300, 5, "Boissons"),
        ]
        cursor.executemany(
            "INSERT INTO produits (nom, prix, stock, categorie) VALUES (?, ?, ?, ?)",
            produits_demo
        )

    conn.commit()
    conn.close()