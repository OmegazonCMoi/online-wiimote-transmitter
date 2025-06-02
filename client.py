import socket
import json
import time
import pygame
import sys

# Adresse du PC hôte (celui qui reçoit les données et contrôle vJoy)
HOST = '192.168.1.86'  # Remplace par l'IP de ton PC hôte
PORT = 5555

# Mode de fonctionnement (sera déterminé automatiquement)
USE_WIIMOTE = False
USE_KEYBOARD = False

# Initialisation de pygame
try:
    pygame.init()
    pygame.joystick.init()
    print("🎮 Pygame initialisé avec succès")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de pygame: {e}")
    sys.exit(1)

# Tentative de détection d'une manette (Wiimote)
joystick_count = pygame.joystick.get_count()
wiimote = None

if joystick_count > 0:
    try:
        # Essai de connexion à la première manette
        wiimote = pygame.joystick.Joystick(0)
        wiimote.init()
        
        print(f"✅ Manette détectée: {wiimote.get_name()}")
        print(f"   - Nombre d'axes: {wiimote.get_numaxes()}")
        print(f"   - Nombre de boutons: {wiimote.get_numbuttons()}")
        print(f"   - Nombre de chapeaux: {wiimote.get_numhats()}")
        
        # Vérifier si c'est bien une Wiimote (ou compatible)
        device_name = wiimote.get_name().lower()
        if any(keyword in device_name for keyword in ['nintendo', 'wiimote', 'wii', 'rvl']):
            USE_WIIMOTE = True
            print("🎯 Mode WIIMOTE activé")
        else:
            print(f"⚠️  Manette détectée mais ne semble pas être une Wiimote: {wiimote.get_name()}")
            print("🔄 Basculement vers le mode clavier...")
            USE_KEYBOARD = True
    except Exception as e:
        print(f"⚠️  Erreur lors de l'initialisation de la manette: {e}")
        print("🔄 Basculement vers le mode clavier...")
        USE_KEYBOARD = True
else:
    print("⚠️  Aucune manette détectée")
    print("🔄 Basculement vers le mode clavier...")
    USE_KEYBOARD = True

# Si aucun mode n'est activé, utiliser le clavier par défaut
if not USE_WIIMOTE and not USE_KEYBOARD:
    USE_KEYBOARD = True

# Importation du module keyboard si nécessaire
if USE_KEYBOARD:
    try:
        import keyboard
        print("⌨️  Module clavier importé avec succès")
    except ImportError:
        print("❌ Module 'keyboard' non installé. Installation...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard"])
        import keyboard
        print("✅ Module 'keyboard' installé et importé")

# Création du socket UDP
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"🌐 Socket UDP créé avec succès")
    print(f"📡 Cible: {HOST}:{PORT}")
except Exception as e:
    print(f"❌ Erreur lors de la création du socket: {e}")
    sys.exit(1)

# Affichage des instructions selon le mode
if USE_WIIMOTE:
    print("\n=== 🎮 MODE WIIMOTE ACTIVÉ ===")
    print("🎯 Contrôles Wiimote:")
    print("  - Bouton A/1: Bouton 1")
    print("  - Bouton B/2: Bouton 2") 
    print("  - Mouvements: Accéléromètre")
    print("  - Bouton HOME: Quitter")
else:
    print("\n=== ⌨️  MODE CLAVIER ACTIVÉ ===")
    print("🎯 Contrôles clavier (simulation Wiimote):")
    print("  - Touche '1': Bouton 1 Wiimote")
    print("  - Touche '2': Bouton 2 Wiimote")
    print("  - Flèches: Simulation mouvement")
    print("  - Échap: Quitter")
    print("\n📋 Instructions pour connecter une vraie Wiimote:")
    print("1. Paramètres Windows → Bluetooth → Ajouter un appareil")
    print("2. Maintenir boutons 1+2 sur la Wiimote pendant 3 sec")
    print("3. Sélectionner 'Nintendo RVL-CNT-01'")
    print("4. Redémarrer ce script")

print("📡 Démarrage de l'envoi des données...\n")

# Variables pour le fonctionnement
clock = pygame.time.Clock()
packet_count = 0
last_display_time = time.time()

# Variables pour simulation clavier
simulated_accel = [0, 0, 1000]  # Position neutre

def read_wiimote_data():
    """Lecture des données depuis la Wiimote"""
    global wiimote
    
    try:
        button_count = wiimote.get_numbuttons()
        button_states = {}
        
        # Lecture de tous les boutons
        for i in range(min(button_count, 12)):
            button_states[f'btn_{i}'] = wiimote.get_button(i)
        
        # Lecture des axes d'accélération
        accel_x, accel_y, accel_z = 0, 0, 1000
        axes_count = wiimote.get_numaxes()
        
        if axes_count >= 3:
            accel_x = int(wiimote.get_axis(0) * 1000)
            accel_y = int(wiimote.get_axis(1) * 1000) 
            accel_z = int(wiimote.get_axis(2) * 1000)
        
        # Mapping des boutons principaux (peut varier selon la Wiimote)
        button_1_pressed = button_states.get('btn_0', False) or button_states.get('btn_1', False)
        button_2_pressed = button_states.get('btn_1', False) or button_states.get('btn_2', False)
        
        # Détection du bouton HOME pour quitter
        quit_requested = False
        for i in range(button_count):
            if wiimote.get_button(i) and i >= 8:  # Bouton HOME généralement en fin
                quit_requested = True
                break
        
        return {
            'buttons': {
                '1': button_1_pressed,
                '2': button_2_pressed,
            },
            'accel': [accel_x, accel_y, accel_z],
            'all_buttons': button_states,
            'axes_count': axes_count,
            'button_count': button_count,
            'source': 'wiimote'
        }, quit_requested
        
    except Exception as e:
        print(f"❌ Erreur lecture Wiimote: {e}")
        return None, False

def read_keyboard_data():
    """Lecture des données depuis le clavier (simulation Wiimote)"""
    global simulated_accel
    
    try:
        # Lecture des boutons
        button_1_pressed = keyboard.is_pressed('1')
        button_2_pressed = keyboard.is_pressed('2')
        
        # Simulation de l'accéléromètre avec les flèches
        accel_x, accel_y, accel_z = simulated_accel
        
        # Flèches pour simuler le mouvement
        if keyboard.is_pressed('left'):
            accel_x = max(accel_x - 50, -1000)
        elif keyboard.is_pressed('right'):
            accel_x = min(accel_x + 50, 1000)
        else:
            accel_x = int(accel_x * 0.9)  # Retour progressif au centre
            
        if keyboard.is_pressed('up'):
            accel_y = min(accel_y + 50, 1000)
        elif keyboard.is_pressed('down'):
            accel_y = max(accel_y - 50, -1000)
        else:
            accel_y = int(accel_y * 0.9)  # Retour progressif au centre
        
        simulated_accel = [accel_x, accel_y, accel_z]
        
        # Détection de la touche Échap pour quitter
        quit_requested = keyboard.is_pressed('esc')
        
        return {
            'buttons': {
                '1': button_1_pressed,
                '2': button_2_pressed,
            },
            'accel': simulated_accel,
            'source': 'keyboard'
        }, quit_requested
        
    except Exception as e:
        print(f"❌ Erreur lecture clavier: {e}")
        return None, False

try:
    running = True
    while running:
        # Traitement des événements pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Lecture des données selon le mode
        if USE_WIIMOTE:
            input_data, quit_requested = read_wiimote_data()
        else:
            input_data, quit_requested = read_keyboard_data()
        
        if quit_requested:
            print("🛑 Arrêt demandé")
            running = False
            break
            
        if input_data is None:
            time.sleep(0.1)
            continue
        
        # Envoi des données via UDP
        try:
            message = json.dumps(input_data).encode()
            sock.sendto(message, (HOST, PORT))
            packet_count += 1
            
            # Affichage périodique (toutes les secondes ou lors d'actions)
            current_time = time.time()
            show_info = (current_time - last_display_time > 1.0 or 
                        input_data['buttons']['1'] or 
                        input_data['buttons']['2'])
            
            if show_info:
                source_icon = "🎮" if USE_WIIMOTE else "⌨️"
                buttons_pressed = []
                if input_data['buttons']['1']:
                    buttons_pressed.append("1")
                if input_data['buttons']['2']:
                    buttons_pressed.append("2")
                
                buttons_str = f"[{', '.join(buttons_pressed)}]" if buttons_pressed else "[aucun]"
                accel = input_data['accel']
                
                print(f"{source_icon} Paquet #{packet_count:04d} | Boutons: {buttons_str} | Accel: ({accel[0]:4d}, {accel[1]:4d}, {accel[2]:4d})")
                last_display_time = current_time
                
        except Exception as send_error:
            print(f"❌ Erreur lors de l'envoi: {send_error}")
        
        # Limitation à ~50 FPS
        clock.tick(50)
        time.sleep(0.02)

except KeyboardInterrupt:
    print("\n🛑 Arrêt du client (Ctrl+C)...")
except Exception as e:
    print(f"❌ Erreur générale: {e}")
finally:
    # Nettoyage des ressources
    try:
        if wiimote:
            wiimote.quit()
    except:
        pass
    
    try:
        pygame.quit()
    except:
        pass
        
    try:
        sock.close()
    except:
        pass
        
    print("🔌 Ressources libérées - Client fermé.")
