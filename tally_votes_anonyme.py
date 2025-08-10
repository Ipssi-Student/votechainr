import json
import os
from cryptography.fernet import Fernet
from collections import Counter
import hashlib

CHAIN_FILE = "data/blockchain.json"
KEY_FILE = "data/key.key"

def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def load_chain():
    with open(CHAIN_FILE, "r") as f:
        return json.load(f)

def get_last_votes(chain):
    """
    Retourne le dernier vote par utilisateur :
    { utilisateur: (encrypted_vote, vote_hash) }
    """
    last_votes = {}
    for block in chain:
        user = block["user"]
        last_votes[user] = (block["encrypted_vote"], block["vote_hash"])
    return last_votes

def decrypt_vote(encrypted_vote, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_vote.encode()).decode()

def pseudonymize(username):
    """
    Génère un pseudonyme anonyme et stable à partir du nom utilisateur.
    Utilise un hash SHA-256 tronqué à 8 caractères.
    """
    return hashlib.sha256(username.encode()).hexdigest()[:8]

if __name__ == "__main__":
    if not os.path.exists(CHAIN_FILE):
        print("Aucun vote enregistré.")
        exit()

    key = load_key()
    chain = load_chain()
    last_votes = get_last_votes(chain)

    results = Counter()

    print("\n=== Vérification des bulletins comptés (anonymes) ===")
    for user, (enc_vote, vote_hash) in last_votes.items():
        candidate = decrypt_vote(enc_vote, key)
        pseudo = pseudonymize(user)
        results[candidate] += 1
        print(f"Pseudonyme: {pseudo} | Candidat: {candidate} | Hash de suivi: {vote_hash}")

    print("\n=== Résultats finaux ===")
    for candidate, count in results.items():
        print(f"{candidate} : {count} vote(s)")
