import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from datetime import datetime
import requests   # <-- Chuck Norris -vitsien hakua varten

# --- FUNKTIO KEMIN LÄMPÖTILADATAAN ---
def kemin_lampotilat_page():
    st.title("Kemin lämpötiladata kuukausittain vuosilta 2020-2025 Tietokannasta haettuna")

    conn = mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=st.secrets["mysql"]["port"]
    )

    query = "SELECT Vuosi, Kuukausi, Keskilampotila FROM kemin_lampotilat"
    df = pd.read_sql(query, conn)
    conn.close()

    fig = px.line(df, x="Kuukausi", y="Keskilampotila", color="Vuosi", title="Kuukausittaiset keskilämpötilat")
    st.plotly_chart(fig, use_container_width=True)

# --- FUNKTIO OPENWEATHERDATAAN ---
def weather_page():
    st.title("15 min välein päivittyvä säädata Helsingistä (OpenWeatherMap)")

    conn = mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=st.secrets["mysql"]["port"]
    )

    query = "SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50"
    df = pd.read_sql(query, conn)
    conn.close()

    st.dataframe(df)

    if not df.empty:
        fig = px.line(df, x="timestamp", y="temperature", color="city", title="Viimeisimmät lämpötilat")
        st.plotly_chart(fig, use_container_width=True)

# --- UUSI FUNKTIO: CHUCK NORRIS -VITSIT ---
def chuck_page():
    st.title("😂 Chuck Norris -vitsigeneraattori")

    # --- Kuvat vierekkäin ---
    col1, col2 = st.columns(2)

    with col1:
        st.image(
            "https://preview.redd.it/fun-question-what-was-captain-jack-sparrows-favorite-brand-v0-so89u8z9e8md1.jpeg?auto=webp&s=a4908f9f9f59634550ff99fe793cfde52013b801",
            width=250
        )

    with col2:
        st.image(
            "https://i.ytimg.com/vi/BfJKy8stdMo/maxresdefault.jpg",
            width=250
        )

    # Funktio vitsin hakemiseen
    def get_joke():
        url = "https://api.chucknorris.io/jokes/random"
        response = requests.get(url)
        return response.json()["value"]

    st.subheader("Päivän Chuck Norris -vitsi:")

    # Placeholder näyttää aina vain yhden vitsin
    joke_placeholder = st.empty()
    joke_placeholder.info(get_joke())

    if st.button("Hae uusi vitsi"):
        joke_placeholder.info(get_joke())  # korvaa vanhan vitsin, sama tyyli

# --- PÄÄSIVU JA VALIKKO ---
def main():
    st.sidebar.title("Valitse sivu")
    page = st.sidebar.radio("Sivut:", [
        "Kemin lämpötiladata",
        "Helsingin säädata",
        "Chuck Norris -vitsit"
    ])

    if page == "Kemin lämpötiladata":
        kemin_lampotilat_page()
    elif page == "Helsingin säädata":
        weather_page()
    elif page == "Chuck Norris -vitsit":
        chuck_page()

if __name__ == "__main__":
    main()
