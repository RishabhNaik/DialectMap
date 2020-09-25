from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os


app = Flask(__name__)
title = "Dashboard"
heading = "Map"

    #mongodb
cluster=MongoClient("mongodb+srv://rishabh:maamaamaa@cluster0.9d4xg.mongodb.net/Dialect?retryWrites=true&w=majority")
db=cluster["Dialect"]
todos= db["geojson"]

 
def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/")
def main():
    return render_template('dialectproject.html')


@app.route("/AdminDashboard")
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('dashboard.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/forms")
def forms ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('Form.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route('/getmethod/<geojson>')
def get_javascript_data(geojson):
    return geojson

@app.route("/accepted")
def tasks ():
	#Display the Uncompleted Tasks
	todos_l = todos.find({"accept":"yes"})
	a2="active"
	return render_template('accept.html',a2=a2,todos=todos_l,t=title,h=heading)

@app.route("/action", methods=['GET','POST'])
def action ():
	#Adding a Task
  name=request.values.get("name")
  Age=request.values.get("age")
  gender=request.values.get("gender")
  dialect=request.values.get("dialect")
  loc=request.values.get("location")
  todos.insert_one({
            "type": "Feature",
            "accept":"no",
            "properties": {
                "Name": name,
                "Age": Age,
                "gender": gender,
    "dailectgroup": dialect,
                "recording":"" },
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

@app.route("/accept")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["accept"]=="yes"):
		todos.update({"_id":ObjectId(id)}, {"$set": {"accept":"no"}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"accept":"yes"}})
	redir=redirect_url()	

	return redirect(redir)

# @app.route("/update")
# def update ():
# 	id=request.values.get("_id")
# 	task=todos.find({"_id":ObjectId(id)})
# 	return render_template('update.html',tasks=task,h=heading,t=title)
 
if __name__ == "__main__":
    app.run()
 