#!/usr/bin/env python3
"""
Script de test pour vérifier la détection de la Wiimote
Usage: python test_wiimote.py
"""

import pygame
import sys
import time

def test_wiimote_detection():
    """Test de détection des manettes/Wiimote"""
    
    print("🔍 === TEST DE DÉTECTION WIIMOTE ===\n")
    
    # Initialisation de pygame
    try:
        pygame.init()
        pygame.joystick.init()
        print("✅ Pygame initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de pygame: {e}")
        return False
    
    # Détection des manettes
    joystick_count = pygame.joystick.get_count()
    print(f"📊 Nombre de manettes détectées: {joystick_count}")
    
    if joystick_count == 0:
        print("\n❌ Aucune manette détectée!")
        print("\n📋 Instructions pour connecter une Wiimote:")
        print("1. ⚙️  Paramètres Windows → Bluetooth et appareils")
        print("2. 🔄 Cliquer sur 'Ajouter un appareil'")
        print("3. 🎮 Sur la Wiimote: maintenir boutons 1+2 pendant 3 secondes")
        print("4. 📱 Sélectionner 'Nintendo RVL-CNT-01' dans la liste")
        print("5. ⏳ Attendre la fin de l'installation des pilotes")
        print("6. 🔁 Relancer ce script\n")
        return False
    
    # Test de chaque manette détectée
    for i in range(joystick_count):
        print(f"\n🎮 === MANETTE #{i} ===")
        
        try:
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            
            name = joystick.get_name()
            print(f"📝 Nom: {name}")
            print(f"🔢 ID: {joystick.get_instance_id()}")
            print(f"🎚️  Axes: {joystick.get_numaxes()}")
            print(f"🔴 Boutons: {joystick.get_numbuttons()}")
            print(f"🧭 Chapeaux: {joystick.get_numhats()}")
            
            # Vérification si c'est une Wiimote
            name_lower = name.lower()
            is_wiimote = any(keyword in name_lower for keyword in ['nintendo', 'wiimote', 'wii', 'rvl'])
            
            if is_wiimote:
                print("🎯 ✅ WIIMOTE DÉTECTÉE!")
                print("🚀 Cette manette devrait fonctionner avec le script principal")
            else:
                print("⚠️  Pas une Wiimote Nintendo reconnue")
                print("🔍 Peut fonctionner, mais non garanti")
            
            # Test rapide des boutons et axes
            print("\n🧪 Test en temps réel (5 secondes)...")
            print("   Appuyez sur des boutons ou bougez la Wiimote...")
            
            clock = pygame.time.Clock()
            start_time = time.time()
            
            while time.time() - start_time < 5:
                pygame.event.pump()  # Mise à jour des événements
                
                # Test des boutons
                pressed_buttons = []
                for btn in range(joystick.get_numbuttons()):
                    if joystick.get_button(btn):
                        pressed_buttons.append(str(btn))
                
                # Test des axes
                axes_values = []
                for axis in range(min(joystick.get_numaxes(), 6)):  # Limite à 6 axes
                    value = joystick.get_axis(axis)
                    if abs(value) > 0.1:  # Seuil pour éviter le bruit
                        axes_values.append(f"A{axis}:{value:.2f}")
                
                # Affichage si activité détectée
                if pressed_buttons or axes_values:
                    activity = []
                    if pressed_buttons:
                        activity.append(f"Boutons:[{','.join(pressed_buttons)}]")
                    if axes_values:
                        activity.append(f"Axes:[{','.join(axes_values)}]")
                    
                    print(f"   🔴 {' | '.join(activity)}")
                
                clock.tick(20)  # 20 FPS
            
            joystick.quit()
            
        except Exception as e:
            print(f"❌ Erreur avec la manette #{i}: {e}")
    
    print("\n✅ Test terminé!")
    return True

def main():
    """Fonction principale"""
    
    try:
        success = test_wiimote_detection()
        
        if success:
            print("\n🎯 Pour utiliser le transmetteur:")
            print("   python client.py")
        else:
            print("\n💡 Une fois la Wiimote connectée, essayez:")
            print("   python test_wiimote.py")
            print("   puis: python client.py")
            
    except KeyboardInterrupt:
        print("\n🛑 Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
    finally:
        try:
            pygame.quit()
        except:
            pass
        print("\n🔌 Test fermé")

if __name__ == "__main__":
    main() 