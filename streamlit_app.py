from matplotlib import markers
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import templates


st.markdown("<h1 style='text-align: center;'>Twitter Dashboard for<br><a href='https://twitter.com/search?q=%23MahsaAmini'>#MahsaAmini</a>  <a href='https://twitter.com/search?q=%23%D9%85%D9%87%D8%B3%D8%A7_%D8%A7%D9%85%DB%8C%D9%86%DB%8C'>#مهسا_امینی</a></h1>", unsafe_allow_html=True)
## load the last-update file
try:
    with open("./data/data_counts/dataj.json","r+") as fconf:
        dataj = json.load(fconf)
        
except:
    st.markdown("__No data__")
    quit()

## load dataframes for both series
df1 = pd.read_csv("./data/data_counts/df_counts_by_day_with_retweet.csv")
df2 = pd.read_csv("./data/data_counts/df_counts_by_day_no_retweet.csv")
df3 = pd.read_csv("./data/data_counts/df_counts_last24h_with_retweet.csv")

df1 = df1.drop(columns=["Unnamed: 0"])
df2 = df2.drop(columns=["Unnamed: 0"])
df3 = df3.drop(columns=["Unnamed: 0"])

center_format = "<h4 style='text-align: center;'>{}</h4>"


## Last update
dt_lastup = datetime.strptime(dataj["last_update"],"%Y-%m-%d %H:%M")
str_lastupdate = dt_lastup.strftime("%Y-%m-%d %H:%M")
st.markdown("__Last update: {} UTC__".format(str_lastupdate))




## Table number of tweets on each hashtag
st.markdown(center_format.format("Number of tweets on each hashtag"),unsafe_allow_html=True)
tag_table = templates.f_getTableTemplate()
tag_table = tag_table.format(int(dataj["sum_maminiFA_isRT"]),int(dataj["sum_maminiFA_noRT"]),int(dataj["sum_maminiEN_isRT"]),int(dataj["sum_maminiEN_noRT"]),int(dataj["sum_maminiALL_isRT"]),int(dataj["sum_maminiALL_noRT"]))
st.markdown(tag_table,unsafe_allow_html=True)



## Chart Last 24 hours
st.markdown(center_format.format("1. Number of tweets(Any) in last 24-hours (UTC)"),unsafe_allow_html=True)
fig = px.line(df3,x="date",y="cums",labels={"date":"Date(Last 24 hours)","cums":"Cumulative"})
st.plotly_chart(fig)



## Chart number of tweets(Any) including Re-Tweets
st.markdown(center_format.format("2-1. Number of tweets(Any) including Re-Tweets"),unsafe_allow_html=True)
fig = px.bar(df1,x="date",y="tweet_count",labels={"date":"Date","tweet_count":"Count"})
st.plotly_chart(fig)

## Chart cumulative sum of tweets(Any) including Re-Tweets
st.markdown(center_format.format("2-2. Cumulative sum of tweets(Any) including Re-Tweets"),unsafe_allow_html=True)
fig = px.bar(df1,x="date",y="cums",labels={"date":"Date","cums":"Cumulative"} )
st.plotly_chart(fig)    

## Chart number of unique tweets(Any)
st.markdown(center_format.format("3-1. Number of unique tweets(Any)"),unsafe_allow_html=True)
fig = px.bar(df2,x="date",y="tweet_count",labels={"date":"Date","tweet_count":"Count"} )
st.plotly_chart(fig)

## Chart cumulative sum of unique tweets(Any)
st.markdown(center_format.format("3-2. Cumulative sum of unique tweets(Any)"),unsafe_allow_html=True)
fig = px.bar(df2,x="date",y="cums",labels={"date":"Date","cums":"Cumulative"})
st.plotly_chart(fig)


