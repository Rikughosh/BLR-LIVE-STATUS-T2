import streamlit as st
import pandas as pd
from FlightRadar24 import FlightRadar24API
import pydeck as pdk

st.set_page_config(page_title="BLR Flight Command Center", layout="wide")

st.title("✈️ BLR Flight Command Center")
st.caption("Live International Flights • Terminal 2 • With Real-Time Map")

fr_api = FlightRadar24API()

@st.cache_data(ttl=60)
def get_flights():
    flights = fr_api.get_flights(airport='BLR')
    data = []
    for f in flights:
        try:
            data.append({
                "Flight": f.flight_number,
                "Airline": f.airline_name,
                "Latitude": f.latitude,
                "Longitude": f.longitude,
                "Altitude": f.altitude,
                "Speed": f.ground_speed
            })
        except:
            continue
    return pd.DataFrame(data)

df = get_flights()

st.metric("Flights Tracked", len(df))

if not df.empty:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[Longitude, Latitude]',
        get_radius=20000,
        get_fill_color='[255, 140, 0]',
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=13.1986,
        longitude=77.7066,
        zoom=4,
        pitch=40
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"html": "<b>Flight:</b> {Flight}<br/><b>Airline:</b> {Airline}"}
    )

    st.pydeck_chart(deck)

st.dataframe(df, use_container_width=True)

if st.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()
