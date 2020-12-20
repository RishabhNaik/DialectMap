from flask import Flask, render_template, redirect, url_for, request
from bson import ObjectId
from pymongo import MongoClient
import os
from bson.json_util import dumps
import json



app = Flask(__name__)
title = "Dashboard"
heading = "Map"

    #mongodb
cluster=MongoClient("mongodb+srv://rishabh:maamaamaa@cluster0.9d4xg.mongodb.net/Dialect?retryWrites=true&w=majority")
db=cluster["Dialect"]
todos= db["geojson"]



def geocode ():
    todos.find({})
    cursor = todos.find()
    print("helo---------------------------------------------------------------------------")
    listin=[]
    for obj in cursor:
        name=obj['properties']['Name']
        age=obj['properties']['Age']
        gender=obj['properties']['gender']
        dialect=obj['properties']['dailectgroup']
        locate=obj['geometry']['coordinates']
        
        # locates = list(map(float, locate))
        y = ' '.join(map(str, locate))  
        x=y.split(",")
        tl = list(map(float, x)) 

        c={
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": tl
            },
            "properties": {
                "Name": name,
                "Age": age,
                "gender": gender,
                "dailectgroup": dialect,
                "recording":"" },
            }
        
        listin.append(c)
    diction=listin       
    print(diction)

    json_list=json.dumps(listin)


        # print(json_data)
    return json_list
        # return jsonify(full)




if __name__ == "__main__":
    app.run()

