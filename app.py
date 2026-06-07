from flask import Flask, render_template, request, redirect, url_for, jsonify,flash
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = "erp-supermarket-2025"

@app.before_request
def setup():
    pass


@app.route("/")
def dashboard():
    db = get_db()

    ca_jour = db.execute("""
        SELECT COALESCE(SUM(total), 0) as total
        FROM ventes
        WHERE DATE(date_vente) = DATE('now')
    """).fetchone()["total"]

    nb_ventes = db.execute("""
        SELECT COUNT(*) as nb FROM ventes
        WHERE DATE(date_vente) = DATE('now')
    """).fetchone()["nb"]

    stock_faible = db.execute("""
        SELECT * FROM produits WHERE stock < 10 ORDER BY stock ASC
    """).fetchall()

    top_produits = db.execute("""
        SELECT produit_nom, SUM(quantite) as total_vendu
        FROM lignes_vente
        GROUP BY produit_nom
        ORDER BY total_vendu DESC
        LIMIT 5
    """).fetchall()

    ventes_semaine =db.execute("""
        SELECT DATE(date_vente) as jour,
            COALESCE(SUM(total), 0) as ca,
            COUNT(*) as nb
        FROM ventes
        WHERE date_vente >= DATE('now', '-6 days')
        GROUP BY DATE(date_vente)
        ORDER BY jour ASC
    """).fetchall()

    from datetime import date, timedelta
    jours_complets = {}
    for i in range(6, -1, -1):
        jour = (date.today() - timedelta(days=i)).isoformat()
        jours_complets[jour] = {"ca": 0, "nb": 0}
    for v in ventes_semaine:
        jours_complets[v["jour"]] = {"ca": v["ca"], "nb": v["nb"]}

    labels = list(jours_complets.keys())
    data_ca = [jours_complets[j]["ca"] for j in labels]
    data_nb = [jours_complets[j]["nb"] for j in labels]

    from datetime import datetime
    jours_fr = ["Lun", "Mar", "Mer", "Jeu","Ven","Sam","Dim"]
    labels_fr=[]
    for j in labels:
        d = datetime.fromisoformat(j)
        labels_fr.append(f"{jours_fr[d.weekday()]}{d.day:02d}")

    db.close()
    return render_template("dashboard.html",
        ca_jour=ca_jour,
        nb_ventes=nb_ventes,
        stock_faible=stock_faible,
        top_produits=top_produits,
        labels = labels_fr,
        data_ca = data_ca,
        data_nb = data_nb,
    )


@app.route("/produits")
def produits():
    db = get_db()
    search = request.args.get("q","")
    if search:
        liste = db.execute(
            "SELECT * FROM produits WHERE nom LIKE ? ORDER BY nom",
            (f"%{search}%",)
        ).fetchall()
    else:
        liste = db.execute("SELECT * FROM produits ORDER BY nom").fetchall()
    db.close()
    return render_template("produits.html", produits=liste, search=search)

@app.route("/produits/ajouter", methods=["GET","POST"])
def ajouter_produit():
    if request.method == "POST":
        nom = request.form["nom"].strip()
        prix = float(request.form["prix"])
        stock = int(request.form["stock"])
        categorie = request.form.get("categorie","Général")

        if not nom or prix <= 0:
            flash("Nom et prix requis.","error")
            return redirect(url_for("ajouter_roduit"))

        db = get_db()
        db.execute(
            "INSERT INTO produits (nom, prix, stock, categorie) VALUES (?, ?, ?, ?)",
            (nom, prix, stock, categorie)
        )
        db.commit()
        db.close()
        flash(f"Produit '{nom}' ajouté ✓", "success")
        return redirect(url_for("produits"))
    
    return render_template("form_produit.html", produit=None, action="Ajouter")

@app.route("/produits/modifier/<int:id>", methods=["GET", "POST"])
def modifier_produit(id):
    db = get_db()
    produit = db.execute("SELECT * FROM produits WHERE id = ?",(id,)).fetchone()

    if request.method == "POST":
        nom = request.form["nom"].strip()
        prix = float(request.form["prix"])
        stock = int(request.form["stock"])
        categorie = request.form.get("categorie", "Général")

        db.execute(
            "UPDATE produits SET nom=?, prix=?, stock=?, categorie=? WHERE id=?",
            (nom, prix, stock, categorie, id)
        )
        db.commit()
        db.close()
        flash(f"Produit '{nom}' modifié ✓", "success")
        return redirect(url_for("produits"))

    db.close()
    return render_template("form_produit.html", produit=produit, action="Modifier")

@app.route("/produits/supprimer/<int:id>", methods=["POST"])
def supprimer_produit(id):
    db= get_db()
    produit = db.execute("SELECT nom FROM produits WHERE id=?", (id,)).fetchone()
    db.execute("DELETE FROM produits WHERE id=?", (id,))
    db.commit()
    db.close()
    flash(f"Produit '{produit['nom']}' supprimé", "info")
    return redirect(url_for("produits"))

@app.route("/caisse")
def caisse():
    db = get_db()
    produits = db.execute("SELECT * FROM produits WHERE stock > 0 ORDER BY nom").fetchall()
    db.close()
    return render_template("caisse.html", produits=produits)

@app.route("/api/produit/<int:id>")
def api_produit(id):
    db = get_db()
    p = db.execute("SELECT * FROM produits WHERE id=?", (id,)).fetchone()
    db.close
    if p:
        return jsonify({"id": p["id"], "nom": p["nom"], "prix": p["prix"], "stock": p["stock"]})
    return jsonify({"error":"Introuvable"}), 404

@app.route("/caisse/encaisser", methods=["POST"])
def encaisser():
    data = request.get_json()
    panier = data.get("panier", [])

    if not panier:
        return jsonify({"error":"Panier vide"}), 400

    db = get_db()
    total = sum(item["prix"] * item["quantite"] for item in panier)

    cursor = db.execute("INSERT INTO ventes (total) VALUES (?)", (total,))
    vente_id = cursor.lastrowid

    for item in panier:
        db.execute("""
            INSERT INTO lignes_vente (vente_id, produit_id, produit_nom, quantite, prix_unitaire)
            VALUES (?, ?, ?, ?, ?)
        """, (vente_id, item["id"], item["nom"], item["quantite"], item["prix"]))

        db.execute(
            "UPDATE produits SET stock = stock - ? WHERE id = ?",
            (item["quantite"], item["id"])
        )

    db.commit()
    db.close()
    return jsonify({"success":True, "vente_id":vente_id, "total":total})

@app.route("/historique")
def historique():
    db = get_db()
    ventes = db.execute("""
        SELECT v.id, v.total, v.date_vente,
                GROUP_CONCAT(lv.produit_nom || 'x' || lv.quantite, ', ') as details
        FROM ventes v
        LEFT JOIN lignes_vente lv ON v.id = lv.vente_id
        GROUP BY v.id 
        ORDER BY v.date_vente DESC
        LIMIT 100
    """).fetchall()
    db.close()
    return render_template("historique.html", ventes = ventes)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)