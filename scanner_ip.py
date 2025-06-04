import socket
import argparse
import threading
from queue import Queue
import csv

# Timeout global pour les connexions
socket.setdefaulttimeout(1)

# File d'attente des ports à scanner
port_queue = Queue()

# Résultats
open_ports = []
closed_ports = []

# Fonction de scan d'un seul port
def scan_port(ip, port, verbose):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"[+] Port {port} ouvert")
                open_ports.append(port)
            elif verbose:
                print(f"[-] Port {port} fermé")
                closed_ports.append(port)
    except socket.gaierror:
        print(f"[!] Adresse IP invalide : {ip}")
        exit(1)
    except Exception as e:
        print(f"[!] Erreur : {e}")

# Thread worker
def worker(ip, verbose):
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(ip, port, verbose)
        port_queue.task_done()

# Fonction principale
def main():
    parser = argparse.ArgumentParser(description="Mini-scanner de ports TCP")
    parser.add_argument("--ip", required=True, help="Adresse IP à scanner")
    parser.add_argument("--start-port", type=int, required=True, help="Port de début")
    parser.add_argument("--end-port", type=int, required=True, help="Port de fin")
    parser.add_argument("--threads", type=int, default=100, help="Nombre de threads (par défaut : 100)")
    parser.add_argument("--verbose", action="store_true", help="Afficher aussi les ports fermés")
    parser.add_argument("--output", help="Fichier de sortie (txt ou csv)")

    args = parser.parse_args()

    # Remplir la queue avec les ports à scanner
    for port in range(args.start_port, args.end_port + 1):
        port_queue.put(port)

    # Lancer les threads
    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(args.ip, args.verbose))
        t.start()
        threads.append(t)

    # Attendre la fin du scan
    port_queue.join()

    # Sauvegarde des résultats
    if args.output:
        if args.output.endswith(".csv"):
            with open(args.output, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Port", "Status"])
                for port in open_ports:
                    writer.writerow([port, "open"])
                if args.verbose:
                    for port in closed_ports:
                        writer.writerow([port, "closed"])
        else:
            with open(args.output, "w") as f:
                f.write("Ports ouverts :\n")
                for port in open_ports:
                    f.write(f"{port}\n")
                if args.verbose:
                    f.write("\nPorts fermés :\n")
                    for port in closed_ports:
                        f.write(f"{port}\n")
        print(f"\n[+] Résultats sauvegardés dans {args.output}")

if __name__ == "__main__":
    main()
