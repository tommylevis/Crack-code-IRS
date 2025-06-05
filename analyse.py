import re
import csv
from collections import Counter
import matplotlib.pyplot as plt

def lire_log(fichier_path):
    try:
        with open(fichier_path, "r") as fichier:
            return fichier.readlines()
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier_path}' est introuvable.")
        exit()

def extraire_ips(lignes, mot_cle):
    pattern_ip = re.compile(r"from (\d+\.\d+\.\d+\.\d+)")
    lignes_filtrees = [ligne for ligne in lignes if mot_cle in ligne]
    return [pattern_ip.search(ligne).group(1) for ligne in lignes_filtrees if pattern_ip.search(ligne)]

def afficher_top_ips(counter, titre, top=5):
    print(f"\nTop {top} des IPs - {titre}")
    for ip, count in counter.most_common(top):
        print(f"{ip} : {count} tentatives")

def afficher_graphique(counter, titre, couleur="red", top=5):
    top_ips = counter.most_common(top)
    ips, counts = zip(*top_ips)
    plt.figure(figsize=(10, 6))
    plt.bar(ips, counts, color=couleur)
    plt.xlabel("Adresses IP")
    plt.ylabel("Nombre de tentatives")
    plt.title(titre)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def exporter_csv(echecs, succes, fichier_out="resultats_ips.csv"):
    with open(fichier_out, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "Échecs", "Succès"])
        all_ips = set(echecs.keys()) | set(succes.keys())
        for ip in all_ips:
            writer.writerow([ip, echecs.get(ip, 0), succes.get(ip, 0)])
    print(f"\nRésultats exportés vers {fichier_out}")

def interface_utilisateur(echecs, succes):
    while True:
        ip = input("\nEntrez une IP à analyser (ou 'exit' pour quitter) : ")
        if ip.lower() == "exit":
            break
        print(f"IP : {ip}")
        print(f"  ➤ Tentatives échouées : {echecs.get(ip, 0)}")
        print(f"  ➤ Tentatives réussies  : {succes.get(ip, 0)}")

def main():
    chemin_fichier = "/Users/hugo/Desktop/Python/Ecole/analyse/auth.log"  

    lignes = lire_log(chemin_fichier)
    
    ips_failed = extraire_ips(lignes, "Failed password")
    ips_accepted = extraire_ips(lignes, "Accepted password")

    compteur_failed = Counter(ips_failed)
    compteur_accepted = Counter(ips_accepted)

    afficher_top_ips(compteur_failed, "Connexions échouées")
    afficher_graphique(compteur_failed, "Top 5 IPs - Connexions échouées", couleur="red")

    print("\nIPs avec connexions échouées ET réussies :")
    for ip in set(compteur_failed) & set(compteur_accepted):
        print(f"{ip} ➤ Échecs : {compteur_failed[ip]} | Succès : {compteur_accepted[ip]}")

    exporter_csv(compteur_failed, compteur_accepted)

    interface_utilisateur(compteur_failed, compteur_accepted)

if __name__ == "__main__":
    main()
