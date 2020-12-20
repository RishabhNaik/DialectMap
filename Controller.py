from flask import Flask, render_template, redirect, url_for, request
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
import service
# import requests
import pyrebase
import sounddevice as sd
from scipy.io.wavfile import write


app = Flask(__name__)
title = "Dashboard"
heading = "Map"

    #mongodb
cluster=MongoClient("mongodb+srv://rishabh:maamaamaa@cluster0.9d4xg.mongodb.net/Dialect?retryWrites=true&w=majority")
db=cluster["Dialect"]
todos= db["geojson"]

firebaseConfig = {
  'apiKey': "AIzaSyAD2CE7gNCg7lUsTFQ-yNPy17lgbcA-lW8",
  'authDomain': "autobot-974fa.firebaseapp.com",
  'databaseURL': "https://autobot-974fa.firebaseio.com",
  'projectId': "autobot-974fa",
  'storageBucket': "autobot-974fa.appspot.com",
  'messagingSenderId': "395258880218",
  'appId': "1:395258880218:web:44a788d399296e47d245e3"
}

firebase=pyrebase.initialize_app(firebaseConfig)

db=firebase.database()
auth=firebase.auth()
storage=firebase.storage()

 


def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/")
def main():
    # requests.get("http://localhost:5000/getdata")
    return render_template('dialectproject.html')


@app.route("/AdminDashboard")
# def log ():
#    return redirect(url_for('login'))
def lists ():
	#Display the all Tasks
  todos_l=todos.find()
  a1="active"
  return render_template('dashboard.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/forms")
def forms ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('Form.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route('/record')
def record():
    

    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    audi=write('output.wav', fs, myrecording)  # Save as WAV file 
    filename='output.wav'
    cloudfilename='audio/1234'
    storage.child(cloudfilename).put(filename)

    Url=storage.child(cloudfilename).get_url(None)

    aud=Url

    return aud



@app.route("/action", methods=['GET','POST'])
def action ():
	#Adding a Task
  name=request.values.get("name")
  Age=request.values.get("age")
  gender=request.values.get("gender")
  dialect=request.values.get("dialect")
  loc=request.values.get("location")
  recording=request.values.get("audiourl")
  # service.insertRecord(name,Age,...)
  todos.insert_one({
          "type": "Feature",
          "properties": {
              "Name": name,
              "Age": Age,
              "gender": gender,
              "dailectgroup": dialect,
              "recording":recording },
          "geometry": {
            "type": "Point",
            "coordinates": [
              loc
            ]
          }
        })

  return redirect("/")



@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/AdminDashboard")

# @app.route("/update")
# def update ():
# 	id=request.values.get("_id")
# 	task=todos.find({"_id":ObjectId(id)})
# 	return render_template('update.html',tasks=task,h=heading,t=title)
 
@app.route("/getdata", methods=['GET'])
def geocode():
  response=service.geocode()
  return response




if __name__ == "__main__":
    app.run(debug=True)

