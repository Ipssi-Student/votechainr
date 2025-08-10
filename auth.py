import json, hashlib, secrets
from datetime import datetime

USERS_FILE = "data/users.json"
OTP_LOG_FILE = "data/otp.log"

def load_users():
    """Charge les utilisateurs depuis le fichier JSON."""
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    return users

def verify_password(username, password):
    """
    Vérifie le mot de passe d'un utilisateur.
    Retourne True si les identifiants sont corrects, False sinon.
    """
    users = load_users()
    if username not in users:
        return False
    # Récupère le sel et le hash du mot de passe stockés
    salt = users[username]["salt"]
    stored_hash = users[username]["password_hash"]
    # Calcule le hash du mot de passe fourni avec le même sel
    hash_val = hashlib.sha256((password + salt).encode()).hexdigest()
    # Compare avec le hash stocké
    return hash_val == stored_hash

def generate_otp(username):
    """
    Génère un code OTP (One-Time Password) à 6 chiffres.
    Enregistre le code généré dans le journal OTP et le retourne.
    """
    # Génération d'un code OTP à 6 chiffres (zéros initiaux si besoin)
    code = str(secrets.randbelow(1000000)).zfill(6)
    # Enregistre le code OTP généré dans un fichier de log (horodaté)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - OTP généré pour {username}: {code}\n"
    try:
        with open(OTP_LOG_FILE, "a") as f:
            f.write(log_entry)
    except FileNotFoundError:
        # Créer le fichier s'il n'existe pas encore
        with open(OTP_LOG_FILE, "w") as f:
            f.write(log_entry)
    return code

