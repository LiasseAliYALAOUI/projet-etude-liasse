
# Projet d'études - Liasse Ali YALAOUI

Voici la présentation de mon script pour le projet d'étude 2022-2023.

## Fonctions

### Scan de vulnérabilitées local (BLUE TEAM)

Le scan de vulnérabilitées local à été fait dans un but de répondre à des besoins BLUE TEAM, ce scan est orienté python et va en quelques secondes trouvés les vulnérabilitées locales de la machine comme des anciennes dépendances PIP par exmple.

Ce scan se base sur Safety DB, qui  est une base de données des vulnérabilités de sécurité connues dans les packages Python. Les données sont mises à disposition par pyup.io . 
La plupart des entrées sont trouvées en filtrant les CVEs (Common Vulnerabilities and Exposures) et les journaux des modifications à l'aide de certains mots clés, puis en les examinant manuellement.

### Scan offensif (RED TEAM)

Le scan offensif réponds à un besoin REDTEAM de trouver, identifier et analyser des domaines/ip/machines très rapidement de façons automatique et ergonomique.
Dans ce scan un premier scan machine (NMAP) va se réaliser à partir du domaine cible indiquer par l'utilisateur. Le script va d'abord tenter de lancer le scan NMAP à partir d'un proxy TOR avec torify pour continuer dans un but REDTEAM

Pour compléter le scan machine un scan web basé sur WAPITI va être réalisé afin d'identifier très rapidement les failles.
Les résultats de ces deux rapports seront envoyés par mail à l'utilisateur pour pouvoir lire plus clairement les résultats trouvés par le scan automatisé.

### CVE

Le mode CVE à pour but d'identifier très rapidement en un clique les 15 dernières CVE up-to-date afin de les exploiter dans un usage REDTEAM ou de s'en protéger dans un usage BLUE TEAM.

Pour récuperer les CVE j'ai choisi de me fier à [CIRCL](https://cve.circl.lu/) (Computer Incident Response Center Luxembourg), une organisation réputée dans le domaine de la sécurité informatique. CIRCL assure une mise à jour quasi instantannée de la base de données des CVE, ce qui permet de disposer d'informations actualisées sur les vulnérabilités connues.

Le Script va délivrer les CVE dans un format claire et concis, avec l'ID, la date, le sommaire de la CVE


## Installation

Pour télécharger le script :

```bash
  git clone https://github.com/LiasseAliYALAOUI/projet-etude-liasse
  cd projet-etude-liasse
```

Installation des dépendances 

```bash
  chmod +x setup.sh
  ./setup.sh
```

### Utilisation

```bash
  python3 main.py
```


## Ressources utilisées

 - [CIRCL](https://cve.circl.lu/)
 - [PIP](https://pypi.org/project/pip/)
 - [Wapiti](https://github.com/wapiti-scanner/wapiti)
 - [SMTPLIB]( https://docs.python.org/3/library/smtplib.html)
 - [Safety]( https://pypi.org/project/safety/)
