import requests
from datetime import datetime, timedelta,timezone
import json
import os
import pandas as pd
import numpy as np
from query import cls_qMAmini, cls_qTrackHash
import streamlit as st

PATH_DATA_FOLDER = "./data/"


def f_getDataFrameFromRawJSON(str_path="./", fileTemplate=""):
    """ This function creates a dataframe out of json files provided by twitter """

    ls_js = []
    for filename in os.listdir(str_path):
        if filename.endswith(".json") and fileTemplate in filename :

            with open(str_path + filename) as fjson:

                #Load the json file by Twitter
                ls_js.append(json.load(fjson))
    
    ls_res = []
    for i in range(len(ls_js)):
        ls_res += ls_js[i]["data"]

    df_tmp = pd.DataFrame(ls_res)
    df_tmp = df_tmp.astype({"start": np.datetime64,"end":np.datetime64})
    df_tmp = df_tmp.sort_values(by=["start"],ascending=True).reset_index()
    df_tmp = df_tmp.drop(columns={"index"})
    
    return df_tmp


def f_getTwitterData( tup_query, path_saveFiles):

    configs = f_getConfigs("./config_counts.json")

    
    req_count = 0
    dict_reqParams = dict()

    str_nextToken = ""
    str_dtNow = datetime.now().strftime("%Y-%m-%d_%H-%M")

    while(True):
            
        #Set the params for creating http request
        str_qtotal = tup_query[0][1]
        if tup_query[1][1] == False:
            str_qtotal += " -is:retweet"
        dict_reqParams = {"query": str_qtotal ,
                        "start_time":configs["start_time"],#2017-01-01T00:00:01Z
                        #"end_time":str_endDatetime,
                        }
        #First index does not contain the next_token in params
        if str_nextToken != "": 
            dict_reqParams["next_token"] = str_nextToken


        #Get the http response from twitter API
        response = requests.get(configs["twitter_base_url"],
                                headers = {"Authorization": "Bearer " + st.secrets["twitter_bearer_key"]},
                                params = dict_reqParams)
        
        req_count += 1

        #Convert the response to json
        dict_respJSON = response.json()

        
        #If response includes error, then log it and stop sending requests. Sometimes we receive both error as well as data like the error with invalid palce_id
        if dict_respJSON.get("errors") != None and dict_respJSON.get("data") == None:
            
            print(dict_respJSON.get("errors"))    
            break
               

        #Save the json response to a separate file (using json.dump)
        try:
            
            str_filename = path_saveFiles + "ma_" + "counts_" + tup_query[0][0] + tup_query[1][0] + '_{:02d}'.format(req_count)+ ".json"
            with open(str_filename,"w") as fileJSON:
                json.dump(dict_respJSON, fileJSON)
            print(str_filename + " saved")
                
        except:
            print("---Error in saving JSON file: " + str_filename + "next_token: " + str_nextToken, exc_info=True)        

        
        #Set the next_token
        str_nextToken = dict_respJSON["meta"].get("next_token")
        if str_nextToken == None:
            print("***End of tweet responses***\n")
            break
        
        #time.sleep(configs["sleep_requests"])



def f_exportData(dict_data, str_path):

    try:
        with open(str_path, "w") as fconf:

            json.dump(dict_data, fconf)
    except Exception as er:
        print("Error in writing file.",er)


def f_getCountsPer1Day(df10):
    df159 = df10.groupby(pd.Grouper(key='start', freq='1D'))["tweet_count"].sum()
    df159 = pd.DataFrame({"date":df159.index.strftime("%Y-%m-%d"),"tweet_count":df159.values})
    
    return df159

def f_getCountsPer1Hour(df10):
    dtt = datetime.now(timezone.utc) - timedelta(days=1)
    dt_24h_before = datetime(dtt.year,dtt.month,dtt.day,dtt.hour,0,0,0)
    
    isLast24 = df10.start >= dt_24h_before
    
    df11 = df10.loc[isLast24].reset_index()
    df11 = df11.drop(columns={"index"})
    df11 = pd.DataFrame({"date":np.datetime_as_string(df11["start"],unit="m"),"tweet_count":df11["tweet_count"],"cums":df11["cums"]})
    
    return df11


def f_getConfigs(path_config):
    try:
        with open(path_config,"r") as fconf:
            configs = json.load(fconf)
    except:
        print("---Error reading the config file", exc_info=True)
        quit()

    return configs


def f_prepAmini():

    config = f_getConfigs("./config_amini.json")

    str_ftime = "%Y-%m-%d %H:%M:%S%Z:%z"
    dt_lastup = datetime.now(timezone.utc) - timedelta(seconds=15)
    
    if (dt_lastup - datetime.strptime(config["last_update_mamini"], str_ftime)).total_seconds() < 30 * 60:
        return 2

    str_endDatetime = dt_lastup.strftime(str_ftime)
    config["last_update_mamini"] = str_endDatetime
    

    path_dir = PATH_DATA_FOLDER + "tw_raw"+"/"

    obj_query = cls_qMAmini()

    ## This is to prevent users to update it at same time
    path_lockFile = "./.lock1"
    if os.path.exists(path_lockFile):
        print("Updating... Try it later")

        if  datetime.now().timestamp() - os.path.getmtime(path_lockFile) > 80:
            os.rmdir(path_lockFile)
        else:        
            return 3
    os.mkdir(path_lockFile)
    try:
        for q in obj_query:
            f_getTwitterData(q, path_dir )
    except:
        os.rmdir(path_lockFile)
        return
    os.rmdir(path_lockFile)

    dict_df = dict()
    for item in obj_query:
        fileKey = item[0][0]+item[1][0]
        dict_df[fileKey] = f_getDataFrameFromRawJSON(path_dir, fileKey)
    

    dict_data = dict()

    key_df = obj_query.f_getKey(cls_qMAmini.v_maminiAll,True)
    df1 = dict_df[key_df[0]+key_df[1]]
    dict_data["last_update"] = df1.loc[len(df1)-1,"start"].strftime("%Y-%m-%d %H:%M")


    key_df = obj_query.f_getKey(cls_qMAmini.v_maminiFA, True)
    df1 = dict_df[key_df[0]+key_df[1]];
    dict_data["sum_maminiFA_isRT"] = str(df1["tweet_count"].sum())

    key_df = obj_query.f_getKey(cls_qMAmini.v_maminiFA, False)
    df1 = dict_df[key_df[0]+key_df[1]]
    dict_data["sum_maminiFA_noRT"] = str(df1["tweet_count"].sum())

    key_df = obj_query.f_getKey(cls_qMAmini.v_maminiEN, True)
    df1 = dict_df[key_df[0]+key_df[1]]
    dict_data["sum_maminiEN_isRT"] = str(df1["tweet_count"].sum())

    key_df = obj_query.f_getKey(cls_qMAmini.v_maminiEN, False)
    df1 = dict_df[key_df[0]+key_df[1]]
    dict_data["sum_maminiEN_noRT"] = str(df1["tweet_count"].sum())

    key_df = obj_query.f_getKey(cls_qMAmini.v_maminiAll, True)
    df1 = dict_df[key_df[0]+key_df[1]]
    dict_data["sum_maminiALL_isRT"] = str(df1["tweet_count"].sum())

    key_df = obj_query.f_getKey(cls_qMAmini.v_maminiAll, False)
    df1 = dict_df[key_df[0]+key_df[1]]
    dict_data["sum_maminiALL_noRT"] = str(df1["tweet_count"].sum())

    print(dict_data)
    f_exportData(dict_data, "./data/data_counts/dataj.json")


    key_df = obj_query.f_getKey(cls_qMAmini.v_maminiAll,True)
    df1 = f_getCountsPer1Day(dict_df[key_df[0]+key_df[1]])
    df1["cums"] = df1["tweet_count"].cumsum()
    df1.to_csv("./data/data_counts/df_counts_by_day_with_retweet.csv")

    df1 = dict_df[key_df[0]+key_df[1]]
    df1["cums"] = df1["tweet_count"].cumsum()
    df1 = f_getCountsPer1Hour(df1)
    df1.to_csv("./data/data_counts/df_counts_last24h_with_retweet.csv")
    
    key_df = obj_query.f_getKey(cls_qMAmini.v_maminiAll,False)
    df2 = f_getCountsPer1Day(dict_df[key_df[0]+key_df[1]])
    df2["cums"] = df2["tweet_count"].cumsum()
    df2.to_csv("./data/data_counts/df_counts_by_day_no_retweet.csv")


    
    
    f_exportData(config , "./config_amini.json")


    for j in obj_query:
        key = j[0][0]+j[1][0]
        for i in os.listdir(path_dir):
            if i.endswith(".json") and key in i:
                os.remove(path_dir+ i)

    return 1


def f_prepTrackHash():

    config = f_getConfigs("./config_track.json")

    str_ftime = "%Y-%m-%d %H:%M:%S%Z:%z"
    dt_lastup = datetime.now(timezone.utc) - timedelta(seconds=15)
    
    if (dt_lastup - datetime.strptime(config["last_update_track_hash"], str_ftime)).total_seconds() < 30 * 60:
        return 2

    str_endDatetime = dt_lastup.strftime(str_ftime)
    config["last_update_track_hash"] = str_endDatetime
    

    path_dir = PATH_DATA_FOLDER + "tw_raw"+"/"

    obj_query = cls_qTrackHash()

    ## This is to prevent users to update it at same time
    path_lockFile = "./.lock2"
    if os.path.exists(path_lockFile):
        print("Updating... Try it later")

        if  datetime.now().timestamp() - os.path.getmtime(path_lockFile) > 80:
            os.rmdir(path_lockFile)
        else:        
            return 3
    os.mkdir(path_lockFile)
    try:
        for q in obj_query:
            f_getTwitterData(q, path_dir )
    except:
        os.rmdir(path_lockFile)
        return
    os.rmdir(path_lockFile)

    
    for item in obj_query:
        fileKey = item[0][0]+item[1][0]
        
        df1 = f_getDataFrameFromRawJSON(path_dir, fileKey)

        #key_df = obj_query.f_getKey(obj_query.m_queries[0][1],True)
        #df1 = dict_df[key_df[0]+key_df[1]]
        #df1["cums"] = df1["tweet_count"].cumsum()
        df1 = f_getCountsPer1Day(df1)
        df1.to_csv("./data/data_counts/df_counts_trends_{}.csv".format(fileKey))
        

    
    f_exportData(config , "./config_track.json")

    for j in obj_query:
        key = j[0][0]+j[1][0]
        for i in os.listdir(path_dir):
            if i.endswith(".json") and key in i:
                os.remove(path_dir+ i)

    return 1