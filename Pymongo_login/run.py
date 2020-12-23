from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
title = "Dashboard"
heading = "Map"

    #mongodb
cluster=MongoClient("mongodb+srv://rishabh:maamaamaa@cluster0.9d4xg.mongodb.net/Dialect?authSource=admin&replicaSet=atlas-vbp7zo-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true")
db=cluster["Dialect"]
mongo= db["Users"]


@app.route('/')
def index():
    if 'username' in session:
            # here add the normal map page
            return "user is in the session" + session["username"]
    # here the normal page should go
    return render_template('index.html')
    

@app.route('/login', methods=['POST'])
def login():
    users = mongo
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            if login_user['superuser']== 'null':
                # here the normal page should go
                return redirect(url_for('index'))
            else:
                # here the the html with admin page should go
                return "Hello"

    return 'Invalid username or password'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name':request.form['username'], 'password': hashpass,'superuser': 'null'})
            session['username'] =  request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    # here the register page should go
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))


print(mongo.find_one())

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)