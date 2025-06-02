import socket
import json
import pyvjoy  # Nécessite vJoy installé et activé

PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', PORT))

vjoy = pyvjoy.VJoyDevice(1)

print("Serveur démarré...")

def map_button_state(data):
    # Exemple : bouton A = bouton 1 de la manette
    buttons = data.get("buttons", {})
    vjoy.set_button(1, int(buttons.get('A', False)))
    vjoy.set_button(2, int(buttons.get('B', False)))

while True:
    data, _ = sock.recvfrom(1024)
    try:
        input_data = json.loads(data.decode())
        map_button_state(input_data)
    except Exception as e:
        print("Erreur:", e)