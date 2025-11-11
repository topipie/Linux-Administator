import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

def main():
    st.title("Kemin lämpötiladata kuukausittain vuosilta 2020-2025 Tietokannasta haettuna")

    # Ota tiedot secrets.toml:sta
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

if __name__ == "__main__":
    main()

