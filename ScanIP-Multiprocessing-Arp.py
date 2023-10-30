# coding: utf-8

import socket
import subprocess
import multiprocessing

class Ip:
    @staticmethod
    def monAdresseIP():
        return socket.gethostbyname(socket.gethostname())

class VotreClasse:
    def __init__(self):
        self.__ip = []
        self.__mac = []

    def ping_ip(self, ip_ping):
        result = subprocess.run(["ping", "-n", "1", ip_ping], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "TTL=" in result.stdout:
            #self.__ip.append(ip_ping)  # Ajoutez l'adresse IP à la liste __ip
            return f"Réponse reçue: {ip_ping}"
        else:
            return f"Adresse IP inaccessible: {ip_ping}"

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
        temp = []
        for line in result_str.split("\n"):
            parts = line.split(":")
            if len(parts) > 1:
                if parts[0] == "Réponse reçue" :
                    temp.append(parts[1].strip())
        for i in range(len(temp)):
            self.__ip.append(temp[i])
        local_ip = Ip.monAdresseIP()  # Get the local IP address
        if local_ip in self.__ip:
            self.__ip.remove(local_ip)
        return result_str
    
    def arp(self) -> list:
        resultat = []
        temp = []
        print(self.__ip)
        for ip in self.__ip:
            result = subprocess.run(["arp", "-a", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                print(result.stdout) # Affiche la sortie standard (résultat de la commande arp)
                lines = result.stdout.splitlines() # Divise la sortie en lignes pour obtenir l'adresse MAC
                if len(lines) >= 4:
                    self.__mac.append(lines[3].split()[1])  # Assuming that the MAC address is the second item in the split result
            else:
                print(f"Erreur lors de l'exécution de la commande arp pour l'IP : {ip}")
                print(result.stderr)
        for i in range(len(self.__ip)):
            ip = self.__ip[i]
            mac = self.__mac[i]
            temp = [ip, mac]
            resultat.append(temp)
            
        return resultat #crée une liste dans une liste contenant l'ip et l'adresse mac d'un pc


# Exemple d'utilisation :
if __name__ == "__main__":
    reseau = VotreClasse()
    print("192.168.[*].[]")
    print("         ^")
    print("         |")
    val1 = int(input("> Choisissez un numéro : "))  # Choisissez au lieu de Choose
    print(f"192.168.[{val1}].[*]")
    print("              ^")
    print("              |")
    val2 = int(input("> Choisissez un numéro : "))  # Choisissez au lieu de Choose
    resultScanIP = reseau.scanIP(val1, val2)
    print(resultScanIP)
    input()
    resultARP:list = reseau.arp()
    print(resultARP)
    input()
