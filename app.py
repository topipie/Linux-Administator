from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    # Connect to MySQL/MariaDB
    conn = mysql.connector.connect(
        host="localhost",
        user="exampleuser",
        password="change_this_strong_password",
        database="exampledb"
    )
    cursor = conn.cursor()

    # 1. Hae tervehdys
    cursor.execute("SELECT 'Hello from MySQL!'")
    result = cursor.fetchone()

    # 2. Hae SQL-palvelimen kellonaika
    cursor.execute("SELECT NOW()")
    time_result = cursor.fetchone()

    # Clean up
    cursor.close()
    conn.close()

    # 3. Palauta molemmat selaimelle
    return f"""
        <h1>{result[0]}</h1>
        <p>SQL-serverin kellonaika: {time_result[0]}</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
