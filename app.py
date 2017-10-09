# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, request, json,redirect
import pymysql
import json
import urllib2
import re
import threading, time

app = Flask(__name__)

def ddmm_to_latlon(degree_minute):
	if not degree_minute or degree_minute == '0':
		return 0.
	d, m = re.match(r'^(\d+)(\d\d\.\d+)$', degree_minute).groups()
	return float(d) + float(m) / 60
global points
points = {
    "type": "FeatureCollection",
    "features": [

]
}

def select_DB():
    global points
    connection = pymysql.connect(host='localhost', user='root', password='1356789', db='example', charset='utf8')
    cursor = connection.cursor()
    sql = "Select * from locate4 order by date desc"
    cursor.execute(sql)
    i = 0
    # Using DB
    for row in cursor:
        i = i+1
        x = {"type": "Feature",
            "geometry": { "type": "Point", "coordinates": [row[6], row[5]] },
            "properties": { "prop0": "value0" }}
        points['features'].append(x)
        if i > 10:
            break
    """

    # USING API_URL
    response = urllib2.urlopen('')
    data_file = json.load(response)
    i = 0
    for x in data_file['data']:
        i = i + 1
        if x['value']['fixQ'] == 1:
            lat = ddmm_to_latlon(str(x['value']['latitude']))
            long = ddmm_to_latlon(str(x['value']['longtitude']))
            l = {"type": "Feature",
                 "geometry": {"type": "Point", "coordinates": [long, lat]},
                "properties": {"prop0": "value0"}}
            points['features'].append(l)
        if i > 10:
            break
    """


@app.route('/user')
def showUserName():
    return render_template('user.html', name=session['userName'])

@app.route('/post/<int:postId>')
def showPost(postId):
    return postId


@app.route('/index', methods=['GET','POST'])
def index():
    select_DB()
    return render_template("index.html", points=json.dumps(points))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session['userName'] = request.form['userName']
        return redirect(url_for('showUserName'))
    else:
        return 'login failed'

@app.route('/signUP')
def signUp():
    return render_template('signup.html')

@app.route('/signUpUser',methods =['POST'])
def signUpUser():
    #user = request.form['username']
    #password = request.form['password']
    return json.dumps({'status':'OK','user':'sd','pass':'123'})
# URL 생성
# 라우팅이 설정된 함수에 대해 URL을 얻어낼수 있다.

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)
