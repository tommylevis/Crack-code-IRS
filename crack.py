import random

# --- Partie 1 : Chargement des mots de passe faibles ---
def charger_mots_de_passe(fichier=None):
    if fichier:
        try:
            with open(fichier, "r") as f:
                return [ligne.strip() for ligne in f if ligne.strip()]
        except FileNotFoundError:
            print("Fichier introuvable, utilisation de la liste par défaut.")
    return ["123456", "password", "admin", "123456789", "qwerty", 
            "abc123", "letmein", "welcome", "monkey", "football"]

# --- Partie 2 : Fonction principale du jeu ---
def crackme():
    mots_de_passe = charger_mots_de_passe("mots_de_passe.txt")  # Mettre None pour ignorer le fichier
    mot_secret = random.choice(mots_de_passe)

    historique = []
    nb_essais = 0

    print("Bienvenue dans le jeu CrackMe !")
    limite = input("Nombre maximum d'essais ? (laisser vide pour illimité) : ")
    triche_active = input("Mode triche ? (oui/non) : ").strip().lower() == "oui"

    if triche_active:
        print(f"[TRICHE] Le mot de passe est : {mot_secret}")

    try:
        limite = int(limite)
    except ValueError:
        limite = None

    while True:
        tentative = input("Entrez un mot de passe : ").strip()
        nb_essais += 1
        historique.append(tentative)

        if tentative == mot_secret:
            print(f"\nBravo ! Vous avez trouvé le mot de passe en {nb_essais} essai(s) !")
            break
        else:
            print("Incorrect.")
            # Donne des indices
            if len(tentative) > len(mot_secret):
                print("- Le mot de passe est plus court.")
            elif len(tentative) < len(mot_secret):
                print("- Le mot de passe est plus long.")
            if tentative and tentative[0] == mot_secret[0]:
                print("- Le mot commence par la même lettre.")
            lettres_communes = sum(1 for a, b in zip(tentative, mot_secret) if a == b)
            print(f"- Lettres communes à la même position : {lettres_communes}")

        # Vérifie si le nombre d’essais est dépassé
        if limite is not None and nb_essais >= limite:
            print(f"\nÉchec ! Vous avez atteint la limite de {limite} essais. Le mot était : {mot_secret}")
            break

    print("\nHistorique de vos tentatives :")
    for i, essai in enumerate(historique, 1):
        print(f"{i}. {essai}")

# --- Lancement du jeu ---
if __name__ == "__main__":
    crackme()
