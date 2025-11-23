#!/usr/bin/env python3
import requests
import mysql.connector
from datetime import datetime
import toml
import os

# ------------------------------------------------------------------
# LUE SECRETS.TOML TARKASTA POLUSTA
# ------------------------------------------------------------------
SECRETS_PATH = "/home/ubuntu/myapp/.streamlit/secrets.toml"

if not os.path.exists(SECRETS_PATH):
    raise FileNotFoundError(f"Secrets file not found at {SECRETS_PATH}")

secrets = toml.load(SECRETS_PATH)

# OPENWEATHER API KEY
API_KEY = secrets["api_keys"]["openweather"]

# MYSQL TIETOKANTA SECRETSISTÄ
MYSQL_USER = secrets["mysql"]["user"]
MYSQL_PASS = secrets["mysql"]["password"]
MYSQL_DB   = secrets["mysql"]["database"]
MYSQL_HOST = secrets["mysql"]["host"]
MYSQL_PORT = secrets["mysql"]["port"]

# ------------------------------------------------------------------
# API KUTSU
# ------------------------------------------------------------------
CITY = "Helsinki"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

temp = data['main']['temp']
desc = data['weather'][0]['description']
timestamp = datetime.now()

# ------------------------------------------------------------------
# YHDISTÄ MYSQL TIETOKANTAAN
# ------------------------------------------------------------------
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    database=MYSQL_DB,
    port=MYSQL_PORT
)

cursor = conn.cursor()

# ------------------------------------------------------------------
# LUO TAULU JOS SITÄ EI OLE
# ------------------------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    description VARCHAR(100),
    timestamp DATETIME
)
""")

# ------------------------------------------------------------------
# TALLETA UUSIN DATA
# ------------------------------------------------------------------
cursor.execute(
    "INSERT INTO weather_data (city, temperature, description, timestamp) VALUES (%s, %s, %s, %s)",
    (CITY, temp, desc, timestamp)
)

conn.commit()
cursor.close()
conn.close()

# ------------------------------------------------------------------
# PRINT CRON-LOKKIIN
# ------------------------------------------------------------------
print(f"[OK] Tallennettu: {CITY} | {temp}°C | {desc} | {timestamp}")

