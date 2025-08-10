import json
import hashlib
import secrets
import os

USERS_FILE = "data/users.json"

def load_users():
    """Charge la liste des utilisateurs depuis le fichier JSON."""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Enregistre la liste des utilisateurs dans le fichier JSON."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def add_user(username, password):
    """Ajoute un utilisateur avec un mot de passe salé + haché."""
    users = load_users()

    if username in users:
        print(f"⚠️ L'utilisateur '{username}' existe déjà.")
        return

    salt = secrets.token_hex(8)  # sel aléatoire
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()

    users[username] = {
        "salt": salt,
        "password_hash": password_hash
    }

    save_users(users)
    print(f"Utilisateur '{username}' ajouté avec succès.")

if __name__ == "__main__":
    print("=== Ajout d'un nouvel utilisateur au système de vote ===")
    username = input("Nom d'utilisateur : ").strip()
    password = input("Mot de passe : ").strip()

    if username and password:
        add_user(username, password)
    else:
        print("Nom d'utilisateur et mot de passe obligatoires.")
