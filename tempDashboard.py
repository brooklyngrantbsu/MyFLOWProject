import streamlit as st
import numpy as np
import pandas as pd
import time # to simulate real time data
import plotly.express as px # interactive charts
import math
from beebotte import *



st.set_page_config(
    page_title = 'Temperature Dashboard',  # important pour le référencement sur Google quand on hébergera l'app
    page_icon = '✅',
    layout = 'wide'
)


st.title("Montpellier Travel Dashboard")
st.markdown("## Montpellier Travel Dashboard")


API_KEY = "NbQdAn7mUeLQANWweBUEvwnJ"
SECRET_KEY = "Is7TeBQKjGWEX5ox8NLIsOA1fGgbVUh9"

bclient = BBT(API_KEY, SECRET_KEY)

#clear site
placeholder = st.empty()


def getWeatherData():
    temp = bclient.read('Temperature', 'Temperature', limit=100)
    humidity = bclient.read('Temperature', 'Humidity', limit=100)
    tempAsList = [row['data'] for row in temp]
    humidityAsList = [row['data'] for row in humidity]

    ts = [pd.to_datetime(row['ts'], utc=True, unit='ms') for row in humidity]

    data = {"timestamp":ts, "temp":tempAsList, "humidity":humidityAsList}

    df = pd.DataFrame(data=data)

    return df


# read csv
@st.cache_data
def getStationData() -> pd.DataFrame:
    return pd.read_csv("BikeStations.csv")



stationDF = getStationData()


with st.form("coordForm"):
    st.write("Get the nearest bikes: ")
    userLong = int(st.number_input('Insert Longitude',format='%f',step=0.001))
    userLat = int(st.number_input('Insert Latitude',format='%f',step=0.001))


    # Every form must have a submit button.
    submitted = st.form_submit_button("Get nearest bike stations")
    if submitted:

        stationDF = stationDF.reset_index()  # make sure indexes pair with number of rows

        distanceDict = {}

        for index, row in stationDF.iterrows():
            distanceDict[stationDF["Street"][index]] = abs(math.dist([int(row['lon']), int(row['lat'])], [userLong, userLat]))

        # create two columns
        bikeFig, blank = st.columns(2)
        with bikeFig:
            st.markdown("### Bike Map")
            fig = st.map(stationDF)


while True:

    with placeholder.container():

        df = getWeatherData()

        # split the dashboard here in 2 columns
        kpi1, kpi2 = st.columns(2)
        # fill in those two columns with respective metrics 
        kpi1.metric(
            label="Current Temperature",
            value=int(df["temp"][len(df["temp"])-1]),
            delta=int(df["temp"][len(df["temp"])-1] - df["temp"][len(df["temp"])-2]),
        )

        kpi2.metric(
            label="Current Humidity",
            value=int(df["humidity"][len(df["humidity"])-1]),
            delta=int(df["humidity"][len(df["humidity"])-1] - df["humidity"][len(df["humidity"])-2]),
        )


        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("### Temperature")
            fig = px.line(data_frame=df, x="timestamp", y="temp")
            st.write(fig)
        
        with fig_col2:
            st.markdown("### Humidity")
            fig2 = px.line(data_frame=df, x="timestamp", y="humidity")
            st.write(fig2)

    time.sleep(60)
