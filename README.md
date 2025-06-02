# 🎮 Online Wiimote Transmitter

Un système Python pour utiliser une Nintendo Wiimote comme contrôleur sur PC via UDP, avec support de vJoy pour la simulation de manette.

**🆕 Mode automatique** : Détecte automatiquement si une Wiimote est connectée, sinon bascule vers le clavier !

## 📋 Fonctionnalités

- ✅ **Détection automatique** Wiimote vs Clavier
- ✅ **Connexion Bluetooth** avec la Wiimote
- ✅ **Mode fallback clavier** si pas de Wiimote
- ✅ **Lecture des boutons** (1, 2, A, B, etc.)
- ✅ **Accéléromètre** pour détecter les mouvements
- ✅ **Transmission UDP** en temps réel
- ✅ **Simulation de manette vJoy** côté host
- ✅ **Interface de debug** complète
- ✅ **Script de test** pour diagnostiquer les problèmes

## 🛠️ Prérequis

### Sur le PC Host (celui qui reçoit les données)
- **Windows 10/11** avec Bluetooth
- **vJoy** installé et configuré
- **Python 3.7+**

### Sur le PC Client (celui avec la Wiimote)
- **Windows 10/11** avec Bluetooth
- **Wiimote** (Nintendo Wii Remote) - optionnel
- **Python 3.7+**

## 📦 Installation

### 1. Installation des dépendances Python

```bash
pip install -r requirements.txt
```

### 2. Installation et configuration de vJoy (PC Host uniquement)

1. **Télécharger vJoy** : http://vjoystick.sourceforge.net/
2. **Installer vJoy** avec les paramètres par défaut
3. **Configurer vJoy** :
   - Ouvrir "Configure vJoy" depuis le menu Démarrer
   - Activer le Device #1
   - Configurer au moins 2 boutons
   - Cliquer "Apply"

### 3. Test de détection de la Wiimote (Optionnel)

**Avant de connecter une Wiimote, testez d'abord :**

```bash
python test_wiimote.py
```

Ce script vous dira si une Wiimote est détectée et comment la connecter si nécessaire.

### 4. Connexion de la Wiimote (PC Client) - Optionnel

1. **Activer le Bluetooth** sur votre PC
2. **Mettre la Wiimote en mode découverte** :
   - Méthode 1 : Retirer les piles, les remettre, puis appuyer sur le bouton rouge dans le compartiment
   - Méthode 2 : Appuyer simultanément sur les boutons "1" et "2" pendant 3 secondes
3. **Ajouter l'appareil Bluetooth** :
   - Paramètres Windows → Bluetooth et appareils → Ajouter un appareil
   - Sélectionner "Nintendo RVL-CNT-01" ou "Nintendo RVL-CNT-01-TR"
   - Laisser Windows installer les pilotes

## 🚀 Utilisation

### 1. Configurer l'adresse IP

Dans `client.py`, modifiez la ligne 7 :
```python
HOST = '192.168.1.86'  # Remplace par l'IP de ton PC host
```

Pour trouver l'IP du PC host :
```bash
ipconfig
```

### 2. Lancer le système

**Sur le PC Host :**
```bash
python host.py
```

**Sur le PC Client :**
```bash
python client.py
```

Le script détectera automatiquement le mode à utiliser !

### 3. Modes de fonctionnement

#### 🎮 Mode Wiimote (Automatique si détectée)
- **Bouton A/1** → Bouton 1 vJoy
- **Bouton B/2** → Bouton 2 vJoy  
- **Mouvements** → Données d'accéléromètre
- **Bouton HOME** → Quitter le client

#### ⌨️ Mode Clavier (Fallback automatique)
- **Touche '1'** → Bouton 1 Wiimote
- **Touche '2'** → Bouton 2 Wiimote
- **Flèches** → Simulation mouvement/accéléromètre
- **Échap** → Quitter le client

## 🔧 Dépannage

### 🔍 Première étape : Script de test
```bash
python test_wiimote.py
```

Ce script vous montrera exactement ce qui est détecté et comment résoudre les problèmes.

### ❌ "Aucune manette détectée" → Mode clavier automatique
- ✅ **Normal** : Le script basculera automatiquement vers le clavier
- 🎮 **Pour utiliser la Wiimote** : Suivez les instructions du script de test

### ❌ "Erreur lors de l'initialisation de vJoy"
1. Vérifiez que vJoy est installé
2. Ouvrez "Configure vJoy" et activez le Device #1
3. Redémarrez votre PC si nécessaire

### ❌ "Erreur de connexion UDP"
1. Vérifiez que l'adresse IP dans `client.py` est correcte
2. Assurez-vous que le firewall n'est pas en cause
3. Vérifiez que le port 5555 n'est pas utilisé par une autre application

### 🔍 Mode Debug

Le système affiche automatiquement :
- Mode utilisé (🎮 Wiimote ou ⌨️ Clavier)
- Nombre de paquets envoyés
- État des boutons pressés
- Données d'accélération en temps réel
- Informations sur la Wiimote détectée

## 📁 Structure du projet

```
online-wiimote-transmitter/
├── client.py          # Script client (auto Wiimote/Clavier)
├── host.py            # Script host (avec vJoy)
├── test_wiimote.py    # Script de test Wiimote
├── requirements.txt   # Dépendances Python
└── README.md         # Ce fichier
```

## ⚙️ Configuration avancée

### Mapping des boutons

Dans `host.py`, vous pouvez modifier le mapping :
```python
BUTTON_MAPPING = {
    '1': 1,  # Bouton 1 Wiimote → Bouton 1 vJoy
    '2': 2,  # Bouton 2 Wiimote → Bouton 2 vJoy
    # Ajoutez d'autres boutons si nécessaire
}
```

### Fréquence d'envoi

Dans `client.py`, ligne ~200+ :
```python
clock.tick(50)  # 50 FPS
time.sleep(0.02)  # 20ms
```

### Sensibilité simulation clavier

Dans `client.py`, fonction `read_keyboard_data()` :
```python
accel_x = max(accel_x - 50, -1000)  # Changez 50 pour modifier la sensibilité
```

## 🚀 Démarrage rapide

1. **Installation** : `pip install -r requirements.txt`
2. **Test** : `python test_wiimote.py` (optionnel)
3. **Host** : `python host.py` (PC avec vJoy)
4. **Client** : `python client.py` (PC avec/sans Wiimote)

Le système s'adapte automatiquement ! 🎉

## 🤝 Contribution

N'hésitez pas à contribuer en :
- Signalant des bugs
- Proposant des améliorations
- Ajoutant le support pour d'autres boutons/capteurs
- Testant avec différents modèles de Wiimote

## 📝 Licence

Ce projet est libre d'utilisation pour des fins personnelles et éducatives.

## 🙏 Remerciements

- Nintendo pour la Wiimote
- Équipe vJoy pour l'excellent simulateur de manette
- Communauté pygame pour les bindings de contrôleurs 