import socket
import json
import pyvjoy

HOST = '0.0.0.0'
PORT = 5555

try:
    j = pyvjoy.VJoyDevice(1)  # Assure-toi que vJoy fonctionne
    print("✅ vJoy device initialized successfully")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de vJoy: {e}")
    print("\n📋 Instructions vJoy:")
    print("1. Télécharge et installe vJoy depuis: http://vjoystick.sourceforge.net/")
    print("2. Configure au moins un device vJoy via 'Configure vJoy'")
    print("3. Assure-toi que le device 1 est activé")
    exit(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

# Mapping Wiimote → vJoy (peut être ajusté selon tes besoins)
BUTTON_MAPPING = {
    '1': 1,  # Bouton 1 Wiimote → Bouton 1 vJoy
    '2': 2   # Bouton 2 Wiimote → Bouton 2 vJoy
}

print(f"🌐 Serveur en écoute sur {HOST}:{PORT}...")
print("⏳ En attente de données Wiimote...")

# Variables pour les statistiques
packet_count = 0
last_accel = [0, 0, 0]

while True:
    try:
        data, addr = sock.recvfrom(1024)
        received_data = json.loads(data.decode())
        packet_count += 1
        
        # Accéder correctement aux données des boutons
        if 'buttons' in received_data:
            buttons_data = received_data['buttons']
            
            # Mise à jour des boutons vJoy
            for wiibtn, vjoy_btn in BUTTON_MAPPING.items():
                state = buttons_data.get(wiibtn, False)
                try:
                    j.set_button(vjoy_btn, state)
                except Exception as button_error:
                    print(f"❌ Erreur lors de la mise à jour du bouton {vjoy_btn}: {button_error}")
            
            # Affichage des informations de debug
            buttons_status = []
            for btn, pressed in buttons_data.items():
                if pressed:
                    buttons_status.append(f"{btn}")
            
            buttons_str = f"[{', '.join(buttons_status)}]" if buttons_status else "[aucun]"
            
            print(f"📦 Paquet #{packet_count:04d} de {addr[0]}:{addr[1]}")
            print(f"   🎮 Boutons pressés: {buttons_str}")
            
            # Afficher les données d'accélération si disponibles
            if 'accel' in received_data:
                accel = received_data['accel']
                last_accel = accel
                # Afficher seulement si l'accélération change significativement
                accel_change = any(abs(accel[i] - last_accel[i]) > 50 for i in range(3))
                if accel_change or any(buttons_data.values()):
                    print(f"   📊 Accélération: X={accel[0]:4d}, Y={accel[1]:4d}, Z={accel[2]:4d} (mG)")
            
            # Affichage d'informations de debug supplémentaires
            if 'all_buttons' in received_data:
                all_buttons = received_data['all_buttons']
                pressed_debug_buttons = [f"btn_{i}" for i, pressed in all_buttons.items() if pressed]
                if pressed_debug_buttons:
                    print(f"   🔍 Debug boutons: {pressed_debug_buttons}")
            
            if 'button_count' in received_data and 'axes_count' in received_data:
                print(f"   ℹ️  Wiimote info: {received_data['button_count']} boutons, {received_data['axes_count']} axes")
            
            print()  # Ligne vide pour la lisibilité
            
        else:
            print(f"⚠️  Données reçues invalides (pas de clé 'buttons'): {received_data}")

    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage JSON: {e}")
        print(f"   Données brutes reçues: {data}")
    except ConnectionResetError:
        print(f"⚠️  Connexion fermée par le client {addr}")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        print(f"   Type d'erreur: {type(e).__name__}")
