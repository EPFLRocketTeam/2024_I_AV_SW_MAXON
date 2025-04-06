from opcua import Client
import time

OPCUA_SERVER_URL = "opc.tcp://192.168.1.17:4840"
NODE_ID = "ns=5;b=AQAAAKbhKnGK9zM6o+Y1NI3mYGeQ7iJ7heYzOovcCHuE6i5ztsZA"

client = Client(OPCUA_SERVER_URL)

try:
    client.connect()
    print("Connecté au serveur OPC UA")

    while True:
        # On ne met pas :.2f ici car ce n’est pas forcément un float
        b_Homing_E = client.get_node(NODE_ID).get_value()
        print(f"b_Homing_E : {b_Homing_E}")

        time.sleep(0.1)

except Exception as e:
    print(f"Erreur : {e}")

finally:
    client.disconnect()
    print("Déconnecté du serveur OPC UA")
