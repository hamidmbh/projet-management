from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re


app = Flask(__name__)

# Configuration pour MySQL via XAMPP (à adapter selon tes infos)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_clients'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    taux = db.Column(db.Float, nullable=False)
    annees = db.Column(db.Integer, nullable=False)
    valeur = db.Column(db.Float, nullable=False)

class Historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    taux = db.Column(db.Float, nullable=False)
    annees = db.Column(db.Integer, nullable=False)
    valeur = db.Column(db.Float, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_suppression = db.Column(db.DateTime, nullable=True)  # Null = pas supprimé

@app.route('/')
def index():
    clients = Client.query.all()  # Liste clients actifs
    return render_template('index.html', clients=clients)

@app.route('/add_client', methods=['POST'])
def add_client():
    nom = request.form['nom'].strip()
    try:
        taux = float(request.form['taux']) / 100  # Convertir % en décimal
        annees = int(request.form['annees'])
    except ValueError:
        return "Taux ou années invalides", 400

    if taux < 0 or annees < 0:
        return "Taux et années doivent être positifs", 400
    if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nom):
        return "Nom doit contenir seulement des lettres et des espaces", 400

    valeur = (1 + taux) ** (-annees)
    client = Client(nom=nom, taux=taux, annees=annees, valeur=valeur)
    db.session.add(client)
    db.session.commit()

    historique = Historique(
        nom=nom,
        taux=taux,
        annees=annees,
        valeur=valeur,
        date_creation=datetime.utcnow(),
        date_suppression=None
    )
    db.session.add(historique)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_client/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get(client_id)
    if client:
        historique_entry = Historique.query.filter_by(nom=client.nom, date_suppression=None).first()
        if historique_entry:
            historique_entry.date_suppression = datetime.utcnow()

        db.session.delete(client)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
