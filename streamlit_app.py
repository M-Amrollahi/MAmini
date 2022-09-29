import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px


st.markdown("<h1 style='text-align: center;'>Twitter Dashboard <br> #MahsaAmini #مهسا_امینی</h1>", unsafe_allow_html=True)

## load the last-update file
try:
    with open("./data/data_counts/dataj.json","r+") as fconf:
        dataj = json.load(fconf)
        dt_lastup = datetime.strptime(dataj["last_update"],"%Y-%m-%d %H:%M")
        str_lastupdate = dt_lastup.strftime("%Y-%m-%d %H:%M")
        st.markdown("##### Last update: {} UTC".format(str_lastupdate))
except:
    st.markdown("__No data__")
    quit()

## load dataframes for both series
df1 = pd.read_csv("./data/data_counts/df_counts_by_day_with_retweet.csv")
df2 = pd.read_csv("./data/data_counts/df_counts_by_day_no_retweet.csv")

df1 = df1.drop(columns=["Unnamed: 0"])
df2 = df2.drop(columns=["Unnamed: 0"])

center_format = "<h2 style='text-align: center;'>{}</h1>"

st.markdown(center_format.format("Number of tweets including Re-Tweets"),unsafe_allow_html=True)
fig = px.bar(df1,x="date",y="count",labels={"date":"Date","count":"Count"})
st.plotly_chart(fig)

st.markdown(center_format.format("Cumulative sum of tweets including Re-Tweets"),unsafe_allow_html=True)
fig = px.bar(df1,x="date",y="cums",labels={"date":"Date","cums":"Cumulative"} )
st.plotly_chart(fig)    

st.markdown(center_format.format("Number of unique tweets"),unsafe_allow_html=True)
fig = px.bar(df2,x="date",y="count",labels={"date":"Date","count":"Count"} )
st.plotly_chart(fig)

st.markdown(center_format.format("Cumulative sum of unique tweets"),unsafe_allow_html=True)
fig = px.bar(df2,x="date",y="cums",labels={"date":"Date","cums":"Cumulative"} )
st.plotly_chart(fig)


