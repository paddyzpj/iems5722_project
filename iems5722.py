# -*- coding: utf-8 -*-
from flask import Flask, request
import mysql.connector
import json
import time
import math

# init flash
app = Flask(__name__)

# config
app.config['DEBUG'] = True


# 用户注册
@app.route("/api/project/register", methods=["POST"])
def register():
    print("-----ACTION: register-----")
    username = request.form.get("username")
    password = request.form.get("password")
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "INSERT INTO user (username, password) VALUES ('%s', '%s')"
    print("QUERY: ", query)
    cursor.execute(query, [username, password])
    mydb.commit()
    mydb.close()
    return json.dumps({'status': 'register successfully'})


# 用户登入
@app.route("/api/project/login", methods=["POST"])
def login():
    print("-----ACTION: login-----")
    username = request.form.get("username")
    password = request.form.get("password")
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "SELECT user_id AS id FROM user WHERE username='%s' and password='%s'"
    cursor.execute(query, [username, password])
    result = cursor.fetchone()
    print("QUERY: ", query)
    print("RESULT: ", result)
    mydb.commit()
    mydb.close()
    if len(result) == 0:
        return json.dumps({'status': 'login failed'})
    else:
        return json.dumps({'status': 'ok', 'id': result["id"]})


# /api/a4/submit_push_token
@app.route('/api/a4/submit_push_token', methods=['POST'])
def submit_push_token():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        token = request.form.get('token')
        # opendb
        mydb = getDBInfo()
        # insert token to db
        cursor = mydb.cursor()
        sql = "INSERT INTO push_tokens (user_id, token) VALUES (" + int(user_id) + ",\'" + str(token) + "\')"
        cursor.execute(sql)
        mydb.commit()
        mydb.close()
        return json.dumps({'status': 'OK'})


# /api/a3/get_chatrooms
@app.route('/api/a3/get_chatrooms', methods=['GET'])
def get_chatrooms():
    if request.method == 'GET':
        # opendb
        mydb = getDBInfo()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM chatrooms")
        result = cursor.fetchall()
        mydb.close()
        data = []
        if result is not None:
            for x in range(0, len(result)):
                res = result[x]
                temp = {'id': res[0], 'name': res[1]}
                data.append(temp)
        response = {'status': "OK", 'data': data}
        return json.dumps(response)


# /api/a3/get_messages
@app.route('/api/a3/get_messages', methods=['GET'])
def get_messages():
    if request.method == 'GET':
        args = request.args
        print(args)
        chatroom_id = request.args.get('chatroom_id')
        page = request.args.get('page')
        if chatroom_id is None or page is None:
            return json.dumps({'status': 'ERROR', 'message': 'bad parameter'})
        else:
            chatroom_id = int(chatroom_id)
            page = int(page)
            # opendb
            mydb = getDBInfo()
            cursor = mydb.cursor()
            cursor.execute(
                "SELECT * FROM messages WHERE chatroom_id=" + str(chatroom_id) + " ORDER BY message_time DESC")
            result = cursor.fetchall()
            mydb.close()
            count = len(result)
            total_pages = int(math.ceil(float(count) / 5))
            if total_pages * 5 < count:
                total_pages = total_pages + 1
            index = (page - 1) * 5
            lastIndex = min(count, index + 5)
            messages = []
            for x in range(index, lastIndex):
                res = result[x]
                dt = res[5]
                dtStr = dt.strftime("%Y-%m-%d %H:%M:%S")
                messages.append(
                    {'id': res[0], 'chatroom_id': res[1], 'user_id': res[2], 'name': res[3], 'message': res[4],
                     'message_time': dtStr})
            data = {'current_page': page, 'messages': messages, "total_pages": total_pages}
            response = {'status': 'OK', 'data': data}
            return json.dumps(response)


# /api/a3/send_message
@app.route('/api/a3/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        chatroom_id = int(request.form.get('chatroom_id'))
        name = request.form.get('name')
        message = request.form.get('message')
        user_id = request.form.get('user_id')
        if chatroom_id is None or chatroom_id == '' or \
                name is None or name == '' or \
                message is None or message == '' or \
                user_id is None or user_id == '':
            return json.dumps({'status': 'ERROR', 'message': 'bad parameter'})
        else:
            if len(name) > 20:
                return json.dumps({'status': 'ERROR', 'message': 'The name is more than 20 characters'})
            if len(message) > 200:
                return json.dumps({'status': 'ERROR', 'message': 'The message is more than 200 characters'})
            # query chat room
            # opendb
            mydb = getDBInfo()
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM chatrooms WHERE id=" + str(chatroom_id))
            result = cursor.fetchone()
            if result is None:
                return json.dumps({'status': 'ERROR', 'message': 'chatroom_id not exsit'})
            # insert message to db
            cursor = mydb.cursor()
            sql = "INSERT INTO messages (chatroom_id, user_id, name, message) VALUES (" + str(chatroom_id) + "," + str(
                user_id) + ",\'" + str(name) + "\',\'" + str(message) + "\')"
            cursor.execute(sql)
            mydb.commit()
            mydb.close()
            return json.dumps({'status': 'OK'})


# get db connect
def getDBInfo():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="saxon",
        passwd="saxon1264",
        auth_plugin="mysql_native_password",
        database="iems5722"
    )
    return mydb


if __name__ == "__main__":
    app.run()
