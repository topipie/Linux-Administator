from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    # Connect to MySQL/MariaDB
    conn = mysql.connector.connect(
        host="localhost",
        user="ö",
        password="ö,
        database="öööö"
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

    # 3. Personoitu tarina
    story = (
        "Tervetuloa LEMP-applikaatioon! "
        "Täällä MySQL-palvelin kertoo ajankohtaisen kellonajan, "
        "ja voit aloittaa oman seikkailusi tietokantojen maailmassa."
    )

    # 4. Palauta kaikki selaimelle HTML:nä, mukana kuva
    return f"""
        <html>
            <head>
                <title>Melkein ku lauta</title>
            </head>
            <body>
                <h1>{result[0]}</h1>
                <p>{story}</p>
                <p>SQL-serverin kellonaika: {time_result[0]}</p>


                <!-- Tässä yksinkertainen linkki Streamlit-sivulle -->
                <p><a href="http://86.50.20.133/data-analysis/">Siirry Data Analysis -sivulle</a></p>

                <!-- Esimerkkikuva netistä -->
                <img src="https://images.cdn.yle.fi/image/upload/c_crop,h_506,w_900,x_0,y_96/ar_1.7777777777777777,c_fill,g_faces,h_431,w_767/dpr_2.0/q_auto:eco/f_auto/fl_lossy/v1518599673/17-24171552cebf18649c"
                     alt="Database" width="200">

                <p>Nauttikaa SQL-seikkailusta!</p>
            </body>
        </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


