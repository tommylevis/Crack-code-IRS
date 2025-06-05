import re
import pandas as pd
import matplotlib.pyplot as plt

# 1. Fonction de parsing adaptée à TON format de log
def parse_log_line(line):
    pattern = (
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s-\s-\s'                         # IP
        r'\[(?P<datetime>[^\]]+)\]\s'                                # Date
        r'"(?P<method>[A-Z]+)\s(?P<url>\S+)\sHTTP/[\d.]+"\s'         # Méthode + URL
        r'(?P<status>\d{3})\s'                                       # Code HTTP
        r'"(?P<user_agent>.+)"'                                      # User-Agent
    )
    match = re.search(pattern, line)
    if match:
        data = match.groupdict()
        data['status'] = int(data['status'])
        return data
    return None

# 2. Chargement du fichier log
def load_logs(filepath):
    parsed_lines = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        for i, line in enumerate(file):
            data = parse_log_line(line)
            if data:
                parsed_lines.append(data)
            else:
                print(f"[WARN] Ligne ignorée ({i}) : {line.strip()[:80]}")
    df = pd.DataFrame(parsed_lines)
    print(f"[INFO] Total lignes chargées : {len(df)}")
    return df

# 3. Filtrage des erreurs 404
def filter_404_errors(df):
    df_404 = df[df['status'] == 404]
    print(f"[INFO] Total erreurs 404 : {len(df_404)}")
    return df_404

# 4. Top 5 IPs fautives
def top_5_ips(df_404):
    top_ips = df_404['ip'].value_counts().head(5)
    print("[INFO] Top 5 IPs fautives :")
    print(top_ips)
    return top_ips

# 5. Visualisation graphique
def plot_404_ips(top_ips):
    plt.figure(figsize=(10, 6))
    top_ips.plot(kind='bar', color='tomato')
    plt.title("Top 5 IPs générant des erreurs 404")
    plt.xlabel("Adresse IP")
    plt.ylabel("Nombre d'erreurs 404")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# 6. Détection de bots
def detect_bots(df_404):
    bot_keywords = ['bot', 'crawler', 'spider']
    mask_bots = df_404['user_agent'].str.lower().str.contains('|'.join(bot_keywords))
    df_bots = df_404[mask_bots]
    pourcentage = (len(df_bots) / len(df_404)) * 100 if len(df_404) > 0 else 0
    print(f"[INFO] Pourcentage d’erreurs 404 causées par des bots : {pourcentage:.2f}%")
    print("[INFO] IPs suspectes (bots) :")
    print(df_bots['ip'].value_counts().head())
    return df_bots

# 7. Programme principal
if __name__ == "__main__":
    df = load_logs("/Users/hugo/Desktop/Python/Ecole/analy/access.log")  # Remplace par "access.log" si tu veux
    if df.empty:
        print("[ERREUR] Aucun log valide trouvé.")
    else:
        df_404 = filter_404_errors(df)
        if not df_404.empty:
            top_ips = top_5_ips(df_404)
            plot_404_ips(top_ips)
            df_bots = detect_bots(df_404)

            print("\n=== DISCUSSION ===")
            print("Les IPs ci-dessus génèrent beaucoup d’erreurs 404.")
            print("Des bots comme Googlebot, Bingbot ou YandexBot sont présents.")
            print("➡️ Actions possibles : bloquer certaines IPs, surveiller les comportements ou automatiser cette analyse.")
        else:
            print("[INFO] Aucune erreur 404 détectée.")
