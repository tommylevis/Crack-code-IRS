import re

def is_valid_ipv4(ip):
    # Expression régulière pour une IPv4 classique
    pattern = r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'
    
    if not re.match(pattern, ip):
        return False

    # Vérifie que chaque octet est entre 0 et 255
    parts = ip.split('.')
    for part in parts:
        if not 0 <= int(part) <= 255:
            return False
    return True

# Test
ips_to_test = [
    "192.168.1.1",
    "10.0.0.255",
    "172.16.254.1",
    "adc.def.ghi.jkl",
    "256.256.256.256",
    "192.168.1.",  # souvent accepté, mais certains outils le refusent
    "192.168.1.01",
    "0.0.0.0"
]

for ip in ips_to_test:
    print(f"{ip} -> {'Valide' if is_valid_ipv4(ip) else 'Invalide'}")
