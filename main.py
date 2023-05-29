import dns.resolver
import subprocess
import safety
import os

os.system('clear')

#Fonction qui va laisser le choix à l'utilisateur entre 3 modes
def choisir_programme():
    question = '\n'"Indiquer le programme que vous souhaitez utiliser (1, 2 ou 3): "
    print("1. Lancer un scan de vulnérabilitées locales (BLUE TEAM)")
    print("2. Lancer un scan offensif vers un domaine")
    print("3. Récuperer les 15 dernières CVE up-to-date")

    choix = input(question)
    
    if choix == "1":
        safety_check()
    elif choix == "2":
        scan_offensif()
    elif choix == "3":
        cve_recente("15")
    else:
        print("Choix invalide. Veuillez sélectionner 1, 2 ou 3.")
        choisir_programme()



# Fonction qui va résoudre un domaine avec la librairie pip "dnspython"
def resolve_domain(domain_name):
    try:
        answers = dns.resolver.resolve(domain_name, 'A')
        ips = [str(rdata) for rdata in answers]
        return ips
    except dns.resolver.NoAnswer:
        print("Pas d'enregistrement A trouvé pour le domaine.")
    except dns.resolver.NXDOMAIN:
        print("Le domaine n'existe pas.")
    except dns.exception.DNSException as e:
        print("Une erreur DNS s'est produite:", e)



#Fonction qui va ajouter https pour le besoin de wapiti
def add_https(url):
    if not url.startswith("https://"):
        url = "https://" + url
    return url


#Fonction qui va faire un scan NMAP de manière anonyme avec TOR (torify) et si une erreur suivient lance le NMAP de façons traditionnelles
#La fonction va enregistrer le résultat du scan lancer en arrière plan du script dans un fichier appelé "result_nmap.txt"
def nmap():
    print("\n"+"Scan NMAP sur "+ domain)
    try:
        #Lancemeent du scan avec TOR pour anonymiser l'IP
        commande = ["torify","nmap", "-sV","-sC" , domain]
        with open('resultat_nmap.txt', 'w') as f:
            f.write('\n'+"Scan NMAP sur ", domain,'\n')
            resultat_nmap = subprocess.run(commande, text=True, check=True, stdout=f)
        tor_ip = subprocess.run(['torify','curl', 'ifconfig.io'], capture_output=True, text=True)
        print("Le scan a été fait à partir d'une IP anonymisé (tor) : " + tor_ip)
        print("OK")
    except:
        commande = ["nmap", "-sV","-sC" , domain]
        with open('resultat_nmap.txt', 'w') as f:
            f.write('\n'+"Scan NMAP sur "+ domain + '\n')
            resultat_nmap = subprocess.run(commande, text=True, check=True, stdout=f)
            print("OK")

#Fonction qui va faire un scan web avec l'outils WAPITI
#La fonction va enregistrer le résultat du scan lancer en arrière plan du script dans un fichier appelé "resultats-wapiti.txt"
def wapiti():
    print("\n"+"Scan Wapiti sur "+ domain)
    target = add_https(domain)
    try:
        commande = ["wapiti", "-u", target,'-f','txt','-o', 'resultats-wapiti.txt']
        resultat_wapiti = subprocess.run(commande, text=True, check=True)
        print("OK")
    except:
        print("Une erreur avec le scan WAPITI est survenue")
   

#Fonction qui va regrouper les actions à faire dans le mode offensif à savoir les deux scans et l'envoie par mail des rapports sur le domaine victime
def scan_offensif():
    # Utilisation de la fonction pour résoudre le domaine en adresse IP
    global domain, ips
    domain = input('\n'+ "Renseigner le domaine que vous souhaitez scanner : " + '\n')
    ips = resolve_domain(domain)
    if ips:
        print(f"L'adresse IP associée à {domain} est :")
    for ip in ips:
        print(ip)   
    with open('resultats.txt', 'w') as f:
        f.write("Voici le rapport du scan offensif concernant les résultats trouvés sur :  " + domain + '\n')
    nmap()
    wapiti()

    print("'\n' Voulez-vous envoyer ce rapport par mail ? \n' ")
    print("1. Oui")
    print("2. Non"'\n')
    choix = input()
    

    if choix == "1":
        try : 
            mail(["resultats-wapiti.txt","resultat_nmap.txt"])
            print("OK")
        except:
            print("Une erreur avec l'envoie du mail")
            pass
    elif choix == "2":
        pass


#Fonciton qui va faire un scan de vulnérabilité en local orienté sur les dépendances python principalement
def safety_check():

    commande = "safety check --output text > resultat_safety.txt"
    os.system(commande)
    
    with open("resultat_safety.txt", "r") as fichier:
        print(fichier.read())

    print("'\n' Voulez-vous envoyer ce rapport par mail ? \n' ")
    print("1. Oui")
    print("2. Non"'\n')
    choix = input()
    

    if choix == "1":
        try : 
            mail(["resultat_safety.txt"])
        except:
            print("Une erreur avec l'envoie du mail")
            pass
    elif choix == "2":
        pass


#Fonction qui va envoyer par mail à l'adresse renseigné par l'utilisateur les pièces jointes des rapports demandés précedemment (local ou externe)
def mail(piecejointes):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    fromaddr = "hackingtoolsdv@gmail.com"
    fromaddr_psswd = "ivvgucatjaglcojd"

    toaddr = input("Renseigner l'adresse à laquelle vous souhaitez envoyer le rapport (PDF) : ")

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Script Liasse Ali Yalaoui "

    body = "Bonjour, vous trouverez le rapport du scan en pièce jointe"
    msg.attach(MIMEText(body, 'plain'))

    for piecejointe in piecejointes:
        with open(piecejointe, "rb") as file:
            part = MIMEApplication(file.read(), Name=piecejointe)
            part['Content-Disposition'] = f'attachment; filename="{piecejointe}"'
            msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, fromaddr_psswd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)


# La fonction va récuperer les 15 dernières CVE up-to-date et les affiché dans un format claire et concis, avec l'ID, la date, le sommaire de la CVE
def cve_recente(cve_count):
    import requests
    api_url = f"https://cve.circl.lu/api/last/{cve_count}"
    api_response = requests.get(api_url)
    
    if api_response.status_code != 200:
        print(f"Une erreur dans l'API est survenue: {api_response.status_code}")
        return

    cve_entries = api_response.json()

    for index in range(0, len(cve_entries)):
        entry = cve_entries[index]
        entry_info = f"ID: {entry['id']}, Publié le: {entry['Published']}"
        summary_info = f"Sommaire: {entry['summary']}"

        print("=== CVE Trouvés ===")
        print(entry_info)
        print(summary_info)
        print("=================\n")


#Lancement de la fonction qui initialise le script
choisir_programme()


