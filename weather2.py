import time
import json
import random
import paho.mqtt.client as mqtt

# Configuration des données fictives
CITY = "Mont-de-Marsan"

# Fonction pour générer des données météo fictives
def get_fake_weather_data():
    weather_data = {
        "name": CITY,
        "main": {
            "temp": round(random.uniform(-10, 35), 2),
            "pressure": random.randint(980, 1050),
            "humidity": random.randint(10, 100)
        },
        "weather": [
            {
                "description": random.choice(["clear sky", "few clouds", "scattered clouds", "rain", "thunderstorm"]),
                "icon": "01d"
            }
        ]
    }
    return weather_data

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

# Connexion au serveur MQTT local
client.connect("localhost", 1883, 60)

# Boucle principale pour publier des messages
try:
    while True:
        weather_data = get_fake_weather_data()
        if weather_data:
            weather_json = json.dumps(weather_data)
            client.publish("weather/data", weather_json)
            print(f"Données publiées: {weather_json}")
        time.sleep(10)  # Publier toutes les 10 secondes
except KeyboardInterrupt:
    print("Arrêt du programme")
    client.disconnect()