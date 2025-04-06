from opcua import Client
import time

# Adresse du serveur OPC UA sur l’automate Wago (remplacez l’IP par celle de votre automate)
OPCUA_SERVER_URL = "opc.tcp://192.168.1.17:4840"

# Noeud de la variable à lire (ce NodeId est un exemple, ajustez-le selon votre projet)
NODE_ID = "ns=5;s=b_Homing_E"  # ns=2 : namespace, s=TempConsigne : nom de la variable

# Connexion au serveur OPC UA
client = Client(OPCUA_SERVER_URL)
try:
    client.connect()
    print("Connecté au serveur OPC UA")

    while True:
        # Lire la valeur de la variable
        b_Homing_E = client.get_node(NODE_ID).get_value()
        print(f"b_Homing_E : {b_Homing_E:.2f}" )

        # Pause de 100 ms avant la prochaine lecture
        time.sleep(0.1)

except Exception as e:
    print(f"Erreur : {e}")

finally:
    client.disconnect()
    print("Déconnecté du serveur OPC UA")
