
import json, hashlib
from datetime import datetime
from cryptography.fernet import Fernet

CHAIN_FILE = "data/blockchain.json"
KEY_FILE = "data/key.key"

# Charger ou générer la clé de chiffrement pour les votes
try:
    with open(KEY_FILE, "rb") as kf:
        key = kf.read()
except FileNotFoundError:
    # Génère une nouvelle clé si aucune n'existe et la sauvegarde
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as kf:
        kf.write(key)
fernet = Fernet(key)

def load_chain():
    """Charge la blockchain (liste des bulletins) depuis le fichier JSON."""
    try:
        with open(CHAIN_FILE, "r") as f:
            chain = json.load(f)
    except FileNotFoundError:
        # Si le fichier n'existe pas encore, on retourne une liste vide
        chain = []
    return chain

def add_block(username, candidate_name):
    """
    Ajoute un nouveau bulletin de vote (bloc) dans la blockchain simulée.
    Chiffre le choix du candidat et lie le bloc au précédent par un hachage.
    Retourne le hachage anonyme (empreinte) du bulletin pour vérification.
    """
    chain = load_chain()
    # Chiffrement du vote (nom du candidat)
    ciphertext = fernet.encrypt(candidate_name.encode())
    # Conversion du résultat chiffré en base64 pour le stockage
    encrypted_vote = ciphertext.decode()
    # Calcul du hachage anonyme du vote (empreinte du bulletin chiffré)
    vote_hash = hashlib.sha256(ciphertext).hexdigest()
    # Hachage du bloc précédent (pour lier dans la chaîne)
    if chain:
        prev_hash = chain[-1]["block_hash"]
    else:
        prev_hash = "0" * 64  # 64 zéros pour le bloc initial (genesis)
    # Préparation des données du nouveau bloc (sans le hachage du bloc)
    block = {
        "index": len(chain) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": username,
        "encrypted_vote": encrypted_vote,
        "vote_hash": vote_hash,
        "prev_hash": prev_hash
    }
    # Calcul du hachage du bloc (incluant toutes les données ci-dessus)
    block_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
    block["block_hash"] = block_hash
    # Ajout du bloc à la chaîne et sauvegarde dans le fichier
    chain.append(block)
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4, ensure_ascii=False)
    return vote_hash

