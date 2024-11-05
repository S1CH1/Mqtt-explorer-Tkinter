import time
import json
import requests
import paho.mqtt.client as mqtt

# On définit deux variables, une pour la clé API et une autre pour l'URL de CoinMarketCap
API_KEY = "3883d3b5-8546-4cae-aa23-a6e1a37f2fe9"  # Remplace par ta clé API CoinMarketCap
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# On prépare l'entête de la requête, voir doc de l'API, code Python fourni
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY,
}

# On fixe les paramètres, on choisit de prendre les 10 premières cryptos de la liste et de les convertir en EUR
parameters = {
    "start": "1",
    "limit": "10",
    "convert": "EUR"
}

# Récupération des données de CoinMarketCap
def get_crypto_data():
    response = requests.get(URL, headers=headers, params=parameters)
    # Si le code de statut est 200
    if response.status_code == 200:
        data = response.json()
        sorted_data = []
        for crypto in data['data']:
            sorted_data.append({
                'name': crypto['name'],
                'symbol': crypto['symbol'],
                'price': crypto['quote']['EUR']['price'],
                'market_cap': crypto['quote']['EUR']['market_cap'],
                'percent_change_24h': crypto['quote']['EUR']['percent_change_24h']
            })
        return sorted_data
    else:
        print(f"Erreur lors de la récupération des données: {response.status_code}")
        return None

# Fonction de rappel pour la connexion
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au serveur MQTT")
    else:
        print(f"Échec de la connexion, code de retour: {rc}")

# Fonction de rappel pour la publication
def on_publish(client, userdata, mid):
    print("Message publié")

# Configuration du client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

# Connexion au serveur MQTT
client.connect("localhost", 1883, 60)

# Boucle principale pour publier des messages
try:
    while True:
        crypto_data = get_crypto_data()
        if crypto_data:
            for crypto in crypto_data:
                message = json.dumps(crypto)
                client.publish("crypto/data", message)
                print(f"Données publiées sur le topic 'crypto/data': {message}")
        time.sleep(10)  # Attendre 10 secondes avant de publier à nouveau
except KeyboardInterrupt:
    print("Interruption par l'utilisateur")
finally:
    client.disconnect()
    print("Déconnecté du serveur MQTT")