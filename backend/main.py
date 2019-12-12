from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pydrill.client import PyDrill
from datetime import datetime
from time import mktime
import json
import os
from pandas import pandas as pd
import pymongo

# Initiate Flask App
app = Flask(__name__)
CORS(app)

# Initiate Connection with MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client['fighter_details']
mongo_coll = mongo_db['fighters']

# Initiate Connection with Drill
drill = PyDrill(host='localhost', port=8047)

list_name = []

def get_detail_fighter(name):
    try:
        find_fighter = mongo_coll.find({"fighter_name": name})
        height = ''
        weight = ''
        stance = ''
        reach = ''
        fighter_detail = {}
        for fighter in find_fighter:
            height = fighter['Height']
            weight = fighter['Weight']
            stance = fighter['Stance']
            reach = fighter['Reach']
            fighter_detail = {
                'height': height,
                'weight' : weight,
                'stance' : stance,
                'reach' : reach
            }
            break
        return json.dumps(fighter_detail)
    except:
        pass

def get_query_result():    
    try:
        result = drill.query('''
            SELECT * FROM
            dfs.`/home/syafiq/Downloads/Compressed/data.csv`
        ''')
        side = 'Red'
        df = result.to_dataframe()
        df_winner = df[df['Winner'] == side ]
        df_grouped = df_winner.groupby(['Referee']).size().reset_index(name="Count")
        df_sorted = df_grouped.sort_values(by=['Count'], ascending=False)
        return str(df_sorted.head(10))
    except():
        pass

def get_avg_performance():
    try:
        result = drill.query('''
            SELECT * FROM
            dfs.`/home/syafiq/Downloads/Compressed/data.csv`
        ''')
        df = result.to_dataframe()
        total = str(len(df.index))
        df_winner_red = df[df['Winner'] == 'Red' ]
        df_grouped_red = df_winner_red.groupby(['R_fighter']).size().reset_index(name="Count") #group by red menang 
        
        df_winner_blue = df[df['Winner'] == 'Blue' ]
        df_grouped_blue = df_winner_blue.groupby(['B_fighter']).size().reset_index(name="Count") #group by blue menang 
        #df_sorted = df_grouped.sort_values(by=['Count'], ascending=False)

        return str(total) + '\n' + str(df_grouped_red.head()) + '\n' + str(df_grouped_blue.head())
    except():
        pass

def get_unique_name():
    try:
        result = drill.query('''
            SELECT * FROM
            dfs.`/home/syafiq/Downloads/Compressed/data.csv`
        ''')
        df = result.to_dataframe()
        df_name_blue = df['B_fighter'].unique()
        df_name_red = df['R_fighter'].unique()

        for name in df_name_blue:
            if name not in list_name:
                list_name.append(name)

        for name in df_name_red:
            if name not in list_name:
                list_name.append(name)

        return "Hola"
    except():
        pass

@app.route('/fighter-name', methods=['GET'])
@cross_origin()
def all_name():
    return json.dumps(list_name)

@app.route('/fighter-detail/<name>', methods=['GET'])
@cross_origin()
def fighter_detail(name):
    return get_detail_fighter(name)

def get_performance(saya, lawan):
    result = drill.query('''
            SELECT * FROM
            dfs.`/home/syafiq/Downloads/Compressed/data.csv`
        ''')
    df = result.to_dataframe()
    # number of row
    number_of_row = len(df.index)
    # avg body landed
    blue_max_body_landed = pd.to_numeric(df['B_avg_BODY_landed']).sum()
    red_max_body_landed = pd.to_numeric(df['R_avg_BODY_landed']).sum()
    avg_body_landed = int((blue_max_body_landed + red_max_body_landed)/number_of_row)
    # avg distance landed
    blue_max_distance_landed = pd.to_numeric(df['B_avg_DISTANCE_landed']).sum()
    red_max_distance_landed = pd.to_numeric(df['R_avg_DISTANCE_landed']).sum()
    avg_distance_landed = int((blue_max_distance_landed + red_max_distance_landed)/number_of_row)
    # avg head landed
    blue_max_head_landed = pd.to_numeric(df['B_avg_HEAD_landed']).sum()
    red_max_head_landed = pd.to_numeric(df['R_avg_HEAD_landed']).sum()
    avg_head_landed = int((blue_max_head_landed + red_max_head_landed)/number_of_row)
    # avg ground landed
    blue_max_ground_landed = pd.to_numeric(df['B_avg_GROUND_landed']).sum()
    red_max_ground_landed = pd.to_numeric(df['R_avg_GROUND_landed']).sum()
    avg_ground_landed = int((blue_max_ground_landed + red_max_ground_landed)/number_of_row)
    # avg leg landed
    blue_max_leg_landed = pd.to_numeric(df['B_avg_LEG_landed']).sum()
    red_max_leg_landed = pd.to_numeric(df['R_avg_LEG_landed']).sum()
    avg_leg_landed = int((blue_max_leg_landed + red_max_leg_landed)/number_of_row)
    # data
    data_average = {
        'body': avg_body_landed,
        'distance': avg_distance_landed,
        'head': avg_head_landed,
        'ground': avg_ground_landed,
        'leg': avg_leg_landed
    }
    #--------------------------------------------------------------------------------------------
    # saya 
    df_saya = df[(df['B_fighter'] == saya) | (df['R_fighter'] == saya)]
    number_saya = len(df_saya.index)
    # avg body landed
    blue_saya_body_landed = pd.to_numeric(df_saya['B_avg_BODY_landed']).sum()
    red_saya_body_landed = pd.to_numeric(df_saya['R_avg_BODY_landed']).sum()
    saya_body_landed = int((blue_saya_body_landed + red_saya_body_landed)/number_saya)
    # avg distance landed
    blue_saya_distance_landed = pd.to_numeric(df_saya['B_avg_DISTANCE_landed']).sum()
    red_saya_distance_landed = pd.to_numeric(df_saya['R_avg_DISTANCE_landed']).sum()
    saya_distance_landed = int((blue_saya_distance_landed + red_saya_distance_landed)/number_saya)
    # avg head landed
    blue_saya_head_landed = pd.to_numeric(df_saya['B_avg_HEAD_landed']).sum()
    red_saya_head_landed = pd.to_numeric(df_saya['R_avg_HEAD_landed']).sum()
    saya_head_landed = int((blue_saya_head_landed + red_saya_head_landed)/number_saya)
    # avg ground landed
    blue_saya_ground_landed = pd.to_numeric(df_saya['B_avg_GROUND_landed']).sum()
    red_saya_ground_landed = pd.to_numeric(df_saya['R_avg_GROUND_landed']).sum()
    saya_ground_landed = int((blue_saya_ground_landed + red_saya_ground_landed)/number_saya)
    # avg leg landed
    blue_saya_leg_landed = pd.to_numeric(df_saya['B_avg_LEG_landed']).sum()
    red_saya_leg_landed = pd.to_numeric(df_saya['R_avg_LEG_landed']).sum()
    saya_leg_landed = int((blue_saya_leg_landed + red_saya_leg_landed)/number_saya)
    data_saya = {
        'body': saya_body_landed,
        'distance': saya_distance_landed,
        'head': saya_head_landed,
        'ground': saya_ground_landed,
        'leg': saya_leg_landed
    }
    #-------------------------------------------------------------------------------------------
    # lawan 
    df_lawan = df[(df['B_fighter'] == lawan) | (df['R_fighter'] == lawan)]
    number_lawan = len(df_lawan.index)
    # avg body landed
    blue_lawan_body_landed = pd.to_numeric(df_lawan['B_avg_BODY_landed']).sum()
    red_lawan_body_landed = pd.to_numeric(df_lawan['R_avg_BODY_landed']).sum()
    lawan_body_landed = int((blue_lawan_body_landed + red_lawan_body_landed)/number_lawan)
    # avg distance landed
    blue_lawan_distance_landed = pd.to_numeric(df_lawan['B_avg_DISTANCE_landed']).sum()
    red_lawan_distance_landed = pd.to_numeric(df_lawan['R_avg_DISTANCE_landed']).sum()
    lawan_distance_landed = int((blue_lawan_distance_landed + red_lawan_distance_landed)/number_lawan)
    # avg head landed
    blue_lawan_head_landed = pd.to_numeric(df_lawan['B_avg_HEAD_landed']).sum()
    red_lawan_head_landed = pd.to_numeric(df_lawan['R_avg_HEAD_landed']).sum()
    lawan_head_landed = int((blue_lawan_head_landed + red_lawan_head_landed)/number_lawan)
    # avg ground landed
    blue_lawan_ground_landed = pd.to_numeric(df_lawan['B_avg_GROUND_landed']).sum()
    red_lawan_ground_landed = pd.to_numeric(df_lawan['R_avg_GROUND_landed']).sum()
    lawan_ground_landed = int((blue_lawan_ground_landed + red_lawan_ground_landed)/number_lawan)
    # avg leg landed
    blue_lawan_leg_landed = pd.to_numeric(df_lawan['B_avg_LEG_landed']).sum()
    red_lawan_leg_landed = pd.to_numeric(df_lawan['R_avg_LEG_landed']).sum()
    lawan_leg_landed = int((blue_lawan_leg_landed + red_lawan_leg_landed)/number_lawan)
    data_lawan = {
        'body': lawan_body_landed,
        'distance': lawan_distance_landed,
        'head': lawan_head_landed,
        'ground': lawan_ground_landed,
        'leg': lawan_leg_landed
    }
    return {
        'average': data_average,
        'saya': data_saya,
        'lawan': data_lawan
    }

@app.route('/', methods=['GET'])
def hello():
    return "hello"

@app.route('/compare/<saya>/<lawan>', methods=['GET'])
@cross_origin()
def bandingkan(saya, lawan):
    try:
        result = drill.query('''
            SELECT * FROM
            dfs.`/home/syafiq/Downloads/Compressed/data.csv`
        ''')
        df = result.to_dataframe()

        # Pie Chart
        saya_blue_win = df[(df['B_fighter'] == saya) & (df['Winner'] == 'Blue')]
        saya_blue_win_jumlah = len(saya_blue_win.index)
        saya_red_win = df[(df['R_fighter'] == saya) & (df['Winner'] == 'Red')]
        saya_red_win_jumlah = len(saya_red_win.index)
        print(str(saya_blue_win_jumlah) + ' ' + str(saya_red_win_jumlah))        
        lawan_blue_win = df[(df['B_fighter'] == lawan) & (df['Winner'] == 'Blue')]
        lawan_blue_win_jumlah = len(lawan_blue_win.index)
        lawan_red_win = df[(df['R_fighter'] == lawan) & (df['Winner'] == 'Red')]
        lawan_red_win_jumlah = len(lawan_red_win.index)
        print(str(lawan_blue_win_jumlah) + ' ' + str(lawan_red_win_jumlah))

        # Radar Chart
        data_chart = get_performance(saya, lawan)

        return json.dumps({
            'pie':{
                'saya':{
                    'red':saya_red_win_jumlah,
                    'blue': saya_blue_win_jumlah
                },
                'lawan':{
                    'red': lawan_red_win_jumlah,
                    'blue': lawan_blue_win_jumlah
                }
            },
            'radar': data_chart
        })
    except():
        pass

@app.route('/analisa/<mulai>/<selesai>', methods=['GET'])
@cross_origin()
def analisa(mulai, selesai):
    result = drill.query('''
        SELECT * FROM
        dfs.`/home/syafiq/Downloads/Compressed/data.csv`
    ''')
    df = result.to_dataframe()
    df = df[(mulai < df['date']) & (df['date'] < selesai)]
    red_win = df[(df['Winner'] == 'Red')]
    blue_win = df[(df['Winner'] == 'Blue')]
    red = len(red_win.index)
    blue = len(blue_win.index)
    data = {
        'pie':{
            'mulai': mulai,
            'selesai': selesai,
            'red': red,
            'blue': blue,
        }
    }
    return json.dumps(data)

if __name__ == '__main__':
    get_unique_name()
    app.run(debug=True)



