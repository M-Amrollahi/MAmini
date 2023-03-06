import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from collect_data import f_prepTrackHash


st.markdown("<h1 style='text-align: center;'>Twitter Dashboard for Trends</h1>", unsafe_allow_html=True)

#with st.spinner('Updating...'):
#    res = f_prepTrackHash()
#    if res == None:
#        st.write("Error during updating")
#        st.stop()



df1 = pd.read_csv("./data/data_counts/df_counts_last24h_sharif_uni_with_rt_.csv")
df2 = pd.read_csv("./data/data_counts/df_counts_last24h_etesabat_sarasari_with_rt_.csv")

df1 = df1.drop(columns=["Unnamed: 0"])
df2 = df2.drop(columns=["Unnamed: 0"])

center_format = "<h4 style='text-align: center;'>{}</h4>"


## Last update
#dt_lastup = datetime.strptime(dataj["last_update"],"%Y-%m-%d %H:%M")
#str_lastupdate = dt_lastup.strftime("%Y-%m-%d %H:%M")
#st.markdown("__Last update: {} UTC__".format(str_lastupdate))



## Chart Last 24 hours
st.markdown(center_format.format("Number of tweets in last 24-hours (UTC) for #دانشگاه_شریف"),unsafe_allow_html=True)
fig = px.line(df1,x="date",y="cums",labels={"date":"Date(Last 24 hours)","cums":"Cumulative"})
st.plotly_chart(fig)


## Chart Last 24 hours
st.markdown(center_format.format("Number of tweets in last 24-hours (UTC) for #اعتصابات_سراسری"),unsafe_allow_html=True)
fig = px.line(df2,x="date",y="cums",labels={"date":"Date(Last 24 hours)","cums":"Cumulative"})
st.plotly_chart(fig)
