from opcua import Client
import time

# Adresse du serveur OPC UA sur l’automate Wago (remplacez l’IP par celle de votre automate)
OPCUA_SERVER_URL = "opc.tcp://192.168.0.10:4840"

# Noeud de la variable à lire (ce NodeId est un exemple, ajustez-le selon votre projet)
NODE_ID = "ns=2;s=TempConsigne"  # ns=2 : namespace, s=TempConsigne : nom de la variable

# Connexion au serveur OPC UA
client = Client(OPCUA_SERVER_URL)
try:
    client.connect()
    print("Connecté au serveur OPC UA")

    while True:
        # Lire la valeur de la variable
        temp_value = client.get_node(NODE_ID).get_value()
        print(f"Température consigne : {temp_value:.2f} °C")

        # Pause de 100 ms avant la prochaine lecture
        time.sleep(0.1)

except Exception as e:
    print(f"Erreur : {e}")

finally:
    client.disconnect()
    print("Déconnecté du serveur OPC UA")
