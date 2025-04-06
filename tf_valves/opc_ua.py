from opcua import Client, ua
import base64
import time

OPCUA_SERVER_URL = "opc.tcp://192.168.1.17:4840"

# Décode la chaîne base64 (le contenu après b=)
bytes_id = base64.b64decode("AQAAAKbhKnGK9zM6o+Y1NI3mYGeQ7iJ7heYzOovcCHuE6i5ztsZA")

# Crée un NodeId de type ByteString (identificateur = bytes, namespace = 5)
node = ua.NodeId(bytes_id, 5, ua.NodeIdType.ByteString)

client = Client(OPCUA_SERVER_URL)

try:
    client.connect()
    print("Connecté au serveur OPC UA")

    while True:
        print("Lecture de la valeur du noeud...")
        b_Homing_E = client.get_node(node).get_value()
        print(f"b_Homing_E : {b_Homing_E}")
        time.sleep(0.1)

except Exception as e:
    print(f"Erreur : {e}")

finally:
    client.disconnect()
    print("Déconnecté du serveur OPC UA")
