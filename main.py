import os, sys, json, random
from getpass import getpass
import auth
import blockchain

# Assurer que le répertoire des données existe
if not os.path.isdir("data"):
    os.makedirs("data")

def simulate_risk():
    # Simulation aléatoire d'une connexion suspecte (30% de chance)
    return random.random() < 0.3

def biometric_check():
    # Simulation d'une vérification biométrique par code PIN
    print("⚠ Connexion inhabituelle détectée (nouvelle IP ou appareil inconnu).")
    print("Vérification biométrique requise (simulation : code PIN).")
    pin = getpass("Veuillez entrer votre code PIN à 4 chiffres : ")
    return pin == "1234"  # Code PIN de test (à remplacer si besoin)

def main():
    print("=== Système de Vote Électronique - Prototype CLI ===")
    
    # Authentification de l'utilisateur
    username = input("Nom d'utilisateur : ")
    password = getpass("Mot de passe : ")
    
    # Vérification du mot de passe avec maximum 3 tentatives
    attempts = 1
    max_attempts = 3
    while not auth.verify_password(username, password):
        print("Identifiants incorrects.")
        attempts += 1
        if attempts > max_attempts:
            print("Échec de l'authentification après plusieurs tentatives.")
            sys.exit(1)
        username = input("Nom d'utilisateur : ")
        password = getpass("Mot de passe : ")
    
    # MFA : Générer un code OTP
    otp_code = auth.generate_otp(username)
    print(f"Code OTP envoyé (simulation) : {otp_code}")
    user_otp = input("Veuillez saisir le code OTP reçu : ")
    if user_otp != otp_code:
        print("Code OTP incorrect. Authentification échouée.")
        sys.exit(1)

    # Détection de risque de connexion inhabituelle
    if simulate_risk():
        if not biometric_check():
            print("Échec de la vérification biométrique. Connexion refusée.")
            sys.exit(1)

    print("Authentification réussie. Bienvenue,", username)

    # Charger les candidats
    try:
        with open("data/candidates.json", "r") as f:
            candidates = json.load(f)
    except FileNotFoundError:
        candidates = ["Candidat 1", "Candidat 2", "Candidat 3"]

    while True:
        print("\nListe des candidats :")
        for idx, cand in enumerate(candidates, start=1):
            print(f"  {idx}. {cand}")
        choice = input("Entrez le numéro du candidat choisi : ")
        try:
            choice_idx = int(choice)
        except ValueError:
            print("Entrée invalide.")
            continue
        if choice_idx < 1 or choice_idx > len(candidates):
            print("Numéro de candidat invalide.")
            continue

        selected_candidate = candidates[choice_idx - 1]
        receipt_hash = blockchain.add_block(username, selected_candidate)
        print(f"Vote enregistré pour \"{selected_candidate}\".")
        print(f"Hachage de suivi : {receipt_hash}")
        
        again = input("Souhaitez-vous revoter ? (o/n) : ")
        if again.strip().lower() != 'o':
            break
        else:
            print("Votre ancien vote reste chiffré, seul le dernier sera compté.")

    print("Merci d’avoir voté. Fin de la session.")

if __name__ == "__main__":
    main()

