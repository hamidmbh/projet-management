# 💼 Gestion de Clients – Actualisation avec Flask & MySQL

Ce projet est une application web construite avec **Flask** et **MySQL** (via XAMPP), permettant de :
- Gérer une liste de clients.
- Calculer la **valeur actualisée** selon la formule :  
  `Valeur = (1 + taux)^(-années)`
- Enregistrer chaque opération dans un **historique**, même après suppression d’un client.

---

## ⚙️ Technologies utilisées

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- MySQL (via XAMPP)
- HTML / CSS

---

## 🔧 Installation et Lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/nom-du-repo.git
cd nom-du-repo
```

Créer un environnement virtuel
```
python -m venv .venv
# Sous Windows
.venv\Scripts\activate
# Sous Mac/Linux
source .venv/bin/activate
```

Installer les dépendances
```
pip install flask flask_sqlalchemy pymysql
pip install pymysql
```
Créer une base de données
```
CREATE DATABASE gestion_clients;
```
Créer les tables
```
USE gestion_clients;

CREATE TABLE client (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  taux FLOAT NOT NULL,
  annees INT NOT NULL,
  valeur FLOAT NOT NULL
);

CREATE TABLE historique (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  taux FLOAT NOT NULL,
  annees INT NOT NULL,
  valeur FLOAT NOT NULL,
  date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
  date_suppression DATETIME
);
```

Lancer l'application Flask
```
python app.py
```

Structure du projet
```
projet-management/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── delete-button.png
└── README.md
```
