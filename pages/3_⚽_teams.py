import streamlit as st
import requests
from io import BytesIO

import base64


@st.cache_data
def image_to_base64(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    encoded = base64.b64encode(r.content).decode()
    return f"data:image/png;base64,{encoded}"



st.set_page_config(
    page_title = "Players",
    page_icon = "🏃‍♂️",
    layout = "wide"
)

df_data = st.session_state["data"]


@st.cache_data
def load_image(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    return BytesIO(r.content)

clubes = df_data["Club"].value_counts().index 
club = st.sidebar.selectbox("Clube", clubes) 

df_filtered = df_data[(df_data["Club"] == club)].set_index("Name")

logo_url = df_filtered.iloc[0]["Club Logo"]
st.image(load_image(logo_url), width=40)
st.markdown(f"## {club}")

columns = ["Age", "Photo", "Flag", "Overall", 'Value(£)', 'Wage(£)', 'Joined',
           'Height(cm.)', 'Weight(lbs.)',
           'Contract Valid Until', 'Release Clause(£)']


df_filtered = df_filtered.copy()

df_filtered["Photo"] = df_filtered["Photo"].apply(image_to_base64)
df_filtered["Flag"] = df_filtered["Flag"].apply(image_to_base64)

st.dataframe(df_filtered[columns],
             column_config={
                 "Overall": st.column_config.ProgressColumn(
                     "Overall", format="%d",min_value=0, max_value=100
                 ),
                 "Wage(£)": st.column_config.ProgressColumn("Weekly Wage", format="£%f",
                                                            min_value=0, max_value=df_filtered["Wage(£)"].max()),
                 "Photo": st.column_config.ImageColumn(),  
                 "Flag": st.column_config.ImageColumn("Country"),                                         
             },

              height=600
)