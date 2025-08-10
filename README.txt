# VoteChainR – Système de Vote en ligne Sécurisé (minimaliste sans connexion internet pour le prototype)

VoteChainR est un prototype en ligne de commande de système de vote en ligne utilisant :
- **One-Time Password (OTP)**
- **Authentification multi-facteurs (MFA) Généré aléatoirement code PIN :1234**
- **Enregistrement des votes dans une blockchain locale**
- **Chiffrement Fernet** pour protéger les choix des électeurs
- **Dépouillement anonyme ou nominatif pour le mode Admin**

## Arborescennce du projet

votechainr/
│
├── main.py                     # Lancement principal du programme
├── auth.py                     # Authentification MFA (mot de passe, OTP, PIN Biométrique :1234)
├── blockchain.py               # Gestion de la "blockchain" locale
├── add_user.py                 # Ajout d’un nouvel utilisateur
├── tally_votes_anonyme.py      # Affichage pseudonymisé des résultats anonyme + hash
├── tally_votes.py              # Affichage non pseudonymisé des résultats (version administrateur)
│
├── data/
│   ├── users.json              # Fichier des utilisateurs (chiffré)
│   ├── candidates.json         # Fichier des candidats
│   ├── blockchain.json         # Fichier de la chaîne de blocs
│   └── key.key                 # Clé de chiffrement Fernet (Généré automatiquement par main.py)
│
└── README.txt		        # Guide d'utilisation rapide

## Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/Ipssi-Student/votechainr
   cd votechainr

2. **Créer un environnement virtuel et installer les dépendances**

   ```bash
python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows
pip install cryptography

3. **Préparer les données**

Créer le dossier data (dans le dossier votechainr) et déplacer les fichiers : users.json; candidates.json; blockchain.json (le fichier key.key est généré automatiquement lors du lancement du fichier main.py)

## Utilisation

1. **Ajouter un utilisateur**

  ```bash
  python add_user.py

Entrer un nom d’utilisateur et un mot de passe.
Le mot de passe est haché avec un sel avant stockage dans users.json.

2. **Voter**
    ```bash
    python main.py
    suivre les indications
 
Authentification par mot de passe
Génération et saisie d’un code OTP
Simulation d’une vérification biométrique en cas de connexion suspecte de façon aléatoire (code : 1234)
Sélection du candidat par numéro
Possibilité de revoter (De même si l'utilisateur se reconnecte le dernier vote sera comptabilisé)
Réception d’un hash de suivi pour preuve de vote


3. **Dépouiller les votes**

Mode anonyme :
    ```bash
    python tally_votes_anonyme.py

Affiche :
    Pseudonyme (hash SHA-256 tronqué)
    Candidat choisi
    Hash de suivi
    Résultats de la campagne de vote

Mode nominatif (administrateur) :
    ```bash
    python tally_votes.py

Affiche :
    Utilisateur
    Candidat choisi
    Hash de suivi
    Résultats de la campagne de vote


4. **Vérification de la blockchain**
Se déplacer dans le dossier data/
    ```bash
    cd data
    cat blockchian.json

Affiche :
    Index du vote
    Horodatage, Timestamp
    Utilisateur ayant voté
    Vote chiffré avec Fernet
    Vote chiffré 
    Hash du bloc précédent (chaînage)
    Hash du bloc lui-même (intégrité)

5. **Liste des utilisateurs inscrits**
Se déplacer dans le dossier data/
    ```bash
    cd data
    cat users.json

Affiche :
    Index du voteUn sel aléatoire
    Le mot de passe haché et le sel

6. **liste des candidats**
Se déplacer dans le dossier data/
    ```bash
    cd data
    cat candidates.json

Affiche :
    Chaque élément du tableau est un nom de candidat.
