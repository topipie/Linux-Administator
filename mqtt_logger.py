#!/usr/bin/env python3
import tomli
import mysql.connector
from mysql.connector import pooling
import paho.mqtt.client as mqtt
import json
import logging

# Lue secrets.toml
with open("secrets.toml", "rb") as f:
    secrets = tomli.load(f)

# Ota mqtt_chat-osio talteen
db_secrets = secrets["mqtt_chat"]

# Konfiguroi tietokanta
DB_CONFIG = {
    "host": db_secrets["host"],
    "user": db_secrets["user"],
    "password": db_secrets["password"],
    "database": db_secrets["database"]
}

# Lokitus
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Tietokantapooli
db_pool = pooling.MySQLConnectionPool(
    pool_name="mqtt_pool",
    pool_size=5,
    **DB_CONFIG
)

# MQTT-konfiguraatio
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "chat/messages"

def save_message(nickname, message, client_id):
    """Tallenna viesti tietokantaan."""
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        query = '''
        INSERT INTO messages (nickname, message, client_id)
        VALUES (%s, %s, %s)
        '''
        cursor.execute(query, (nickname, message, client_id))
        conn.commit()
        logger.info(f"Tallennettu: [{nickname}] {message[:50]}...")
    except mysql.connector.Error as err:
        logger.error(f"Tietokantavirhe: {err}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Yhdistetty MQTT-brokeriin")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"Yhteysvirhe, koodi: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        nickname = data.get("nickname", "Tuntematon")[:50]
        message = data.get("text", "")
        client_id = data.get("clientId", "")[:100]
        if message:
            save_message(nickname, message, client_id)
    except Exception as e:
        logger.error(f"Virhe viestin käsittelyssä: {e}")

def main():
    client = mqtt.Client(client_id="mqtt_logger")
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Sammutetaan...")
        client.disconnect()

if __name__ == "__main__":
    main()
