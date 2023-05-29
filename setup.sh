#!/bin/bash


# Installation de NMAP
if ! command -v nmap &> /dev/null
then
    echo "Nmap n'est pas installé. Installation en cours..."
    # Installation de Nmap
    apt-get update
    apt-get install nmap -y
    if [ $? -eq 0 ]
    then
        echo "Nmap a été installé avec succès."
    else
        echo "Une erreur est survenue lors de l'installation de Nmap."
        exit
    fi
fi

# Installation de NMAP
if ! command -v wapiti &> /dev/null
then
    echo "Wapiti n'est pas installé. Installation en cours..."
    # Installation de Wapiti
    apt-get install wapiti -y
    if [ $? -eq 0 ]
    then
        echo "Nmap a été installé avec succès."
    else
        echo "Une erreur est survenue lors de l'installation de Nmap."
        exit
    fi
fi

# Installation de Python3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 n'est pas installé. Installation en cours..."
    # Installation de Python 3
    apt-get install python3 -y
    if [ $? -eq 0 ]
    then
        echo "Python 3 a été installé avec succès."
    else
        echo "Une erreur est survenue lors de l'installation de Python 3."
        exit
    fi
fi

# Installation de PIP pour Python3
if ! command -v pip &> /dev/null
then
    echo "pip n'est pas installé. Installation en cours..."
    # Installation de pip pour Python 3
    apt-get update
    apt-get install python3-pip -y
    if [ $? -eq 0 ]
    then
        echo "pip a été installé avec succès."
    else
        echo "Une erreur est survenue lors de l'installation de pip."
        exit
    fi
fi

#Installation PIP librairies
pip install smtplib
pip install safety
pip install requests
pip install dnspython


# Vérifier si l'installation a réussi
if [ $? -eq 0 ]
then
    echo "Les module ont étés installés avec succès."
else
    echo "Une erreur est survenue lors de l'installation des modules."
fi