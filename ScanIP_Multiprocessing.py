import socket
import subprocess
import multiprocessing

class VotreClasse:
    def __init__(self):
        self.__ip = []

    def monAdresseIP(self):
        return socket.gethostbyname(socket.gethostname())

    def ping_ip(self, ip_ping):
        result = subprocess.run(["ping", "-n", "1", ip_ping], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "TTL=" in result.stdout:
            self.__ip.append(ip_ping)
            return f"Réponse reçue de {ip_ping}"
        else:
            return f"Adresse IP inaccessible : {ip_ping}"

    def scanIP(self, plageIP1: int, plageIP2: int) -> str:
        start_ip = ["192", "168", "", ""]
        ip_list = []
        results = []  # Stocke les résultats des pings
        for j in range(plageIP1 + 1):
            start_ip[2] = str(j)
            for i in range(plageIP2 + 1):
                start_ip[3] = str(i)
                ip_ping = ".".join(start_ip)
                ip_list.append(ip_ping)

        # Utilisation du multiprocessing pour lancer les pings en parallèle
        with multiprocessing.Pool() as pool:
            results = pool.map(self.ping_ip, ip_list)

        # Affiche les résultats
        result_str = "\n".join(results)
        if self.monAdresseIP() in self.__ip:
            self.__ip.remove(self.monAdresseIP())
        return result_str

# Exemple d'utilisation :
if __name__ == "__main__":
    your_instance = VotreClasse()
    result_str = your_instance.scanIP(5, 30)
    print(result_str)
