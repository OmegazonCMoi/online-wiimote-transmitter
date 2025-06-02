import socket
import json
import time

# IP du PC hôte (où se trouve Dolphin)
HOST = '192.168.1.86'  # ← Mets l'adresse locale ici
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Simule l'appui sur A pendant 1s toutes les 5s
    input_data = {
        'buttons': {
            'A': True,
            'B': False,
        },
        'accel': [0, 0, 0]  # pas utilisé pour l'instant
    }

    sock.sendto(json.dumps(input_data).encode(), (HOST, PORT))
    print("Données envoyées")
    time.sleep(1)

    # relâcher le bouton
    input_data['buttons']['A'] = False
    sock.sendto(json.dumps(input_data).encode(), (HOST, PORT))
    time.sleep(4)
