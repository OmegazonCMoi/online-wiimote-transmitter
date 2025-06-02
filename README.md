# online-wiimote-transmitter

**Contrôlez Dolphin à distance avec une vraie Wiimote connectée à un PC client, en transmettant les commandes via le réseau vers un PC hôte qui émule la Wiimote avec vJoy.**

---

## Description

Ce projet permet de lire les données d’une Wiimote connectée à un PC client, de transmettre les inputs (boutons, mouvements) via le réseau (UDP), et de les convertir en commandes sur un PC hôte grâce à un périphérique manette virtuelle vJoy. L’objectif est de pouvoir jouer à des jeux Wii à distance avec Parsec ou un autre logiciel de streaming.

---

## Fonctionnalités

* Lecture des boutons et capteurs de la Wiimote (simulation possible).
* Transmission réseau en temps réel des données Wiimote (UDP).
* Serveur sur PC hôte pour recevoir les données.
* Injection des commandes dans un joystick virtuel via vJoy.
* Compatible avec Dolphin configuré en Wiimote émulée par manette.

---

## Prérequis

* Windows (pour vJoy et pyvjoy)
* Python 3.x
* [vJoy](https://github.com/shauleiz/vJoy/releases) installé et configuré
* Bibliothèque Python `pyvjoy`
* (Optionnel) Bibliothèque Python pour Wiimote (`cwiid` sous Linux, autres sur Windows)

---

## Installation

1. Installe [vJoy](https://github.com/shauleiz/vJoy/releases) (version 2.1.9.1 recommandée).
2. Configure vJoy : active au moins un device (Device 1).
3. Installe Python 3.x depuis [python.org](https://www.python.org/downloads/).
4. Installe les dépendances Python :

```bash
pip install pyvjoy
```

---

## Usage

### Sur le PC client (avec la Wiimote)

Lance le script client pour lire les données Wiimote et les envoyer :

```bash
python client.py
```

*Note : le script actuel simule des inputs, à remplacer par une lecture réelle Wiimote.*

---

### Sur le PC hôte (Dolphin)

Lance le serveur pour recevoir et injecter les commandes dans vJoy :

```bash
python host.py
```

Configure Dolphin pour utiliser une Wiimote émulée par manette vJoy.

---

## Personnalisation

* Ajouter la prise en charge réelle des capteurs Wiimote (accéléromètre, gyro).
* Optimiser la latence réseau.
* Ajouter interface graphique.
* Support multi-Wiimote.

---

## Licence

Demerdez vous et faites ce que vous voulez.

---

## Auteurs

Omega 

---

Si tu veux, je peux te générer aussi un fichier README.md prêt à l’emploi avec tout ça dedans.
