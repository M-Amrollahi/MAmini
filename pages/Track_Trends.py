import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
#from collect_data import f_prepTrackHash
from query import cls_qTrackHash


st.markdown("<h1 style='text-align: center;'>Twitter Dashboard for Trends</h1>", unsafe_allow_html=True)

#with st.spinner('Updating...'):
#    res = f_prepTrackHash()
#    if res == None:
#        st.write("Error during updating")
#        st.stop()

center_format = "<h4 style='text-align: center;'>{}</h4>"

obj_query = cls_qTrackHash()

for q in obj_query:
    
    filename = "./data/data_counts/df_counts_trends_{}.csv".format(q[0][0]+q[1][0])
    
    try:
        df1 = pd.read_csv(filename)
        df1 = df1.drop(columns=["Unnamed: 0"])

        st.markdown(center_format.format(f"Number of tweets for {q[0][1]}"),unsafe_allow_html=True)
        fig = px.bar(df1,x="date",y="tweet_count",labels={"date":"Date","tweet_count":"Count"})
        st.plotly_chart(fig)
    except:
        pass


