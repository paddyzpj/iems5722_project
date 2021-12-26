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
    query = "INSERT INTO user (username, password) VALUES ('" + username + "' , '" + password + "')"
    print("QUERY: ", query)
    cursor.execute(query)
    mydb.commit()
    mydb.close()
    return json.dumps({'status': 'ok'})


# 用户登入
@app.route("/api/project/login", methods=["POST"])
def login():
    print("-----ACTION: login-----")
    username = request.form.get("username")
    password = request.form.get("password")
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "SELECT user_id AS id FROM user WHERE username='" + username + "' and password='" + password + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    print("QUERY: ", query)
    print("RESULT: ", result)
    mydb.commit()
    mydb.close()
    if len(result) == 0:
        return json.dumps({'status': 'login failed'})
    else:
        return json.dumps({'status': 'ok', 'id': str(result[0])})


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
# @app.route('/api/a3/get_chatrooms', methods=['GET'])
# def get_chatrooms():
#     if request.method == 'GET':
#         # opendb
#         mydb = getDBInfo()
#         cursor = mydb.cursor()
#         cursor.execute("SELECT * FROM chatrooms")
#         result = cursor.fetchall()
#         mydb.close()
#         data = []
#         if result is not None:
#             for x in range(0, len(result)):
#                 res = result[x]
#                 temp = {'id': res[0], 'name': res[1]}
#                 data.append(temp)
#         response = {'status': "OK", 'data': data}
#         return json.dumps(response)


# /api/a3/get_messages
# @app.route('/api/a3/get_messages', methods=['GET'])
# def get_messages():
#     if request.method == 'GET':
#         args = request.args
#         print(args)
#         chatroom_id = request.args.get('chatroom_id')
#         page = request.args.get('page')
#         if chatroom_id is None or page is None:
#             return json.dumps({'status': 'ERROR', 'message': 'bad parameter'})
#         else:
#             chatroom_id = int(chatroom_id)
#             page = int(page)
#             # opendb
#             mydb = getDBInfo()
#             cursor = mydb.cursor()
#             cursor.execute(
#                 "SELECT * FROM messages WHERE chatroom_id=" + str(chatroom_id) + " ORDER BY message_time DESC")
#             result = cursor.fetchall()
#             mydb.close()
#             count = len(result)
#             total_pages = int(math.ceil(float(count) / 5))
#             if total_pages * 5 < count:
#                 total_pages = total_pages + 1
#             index = (page - 1) * 5
#             lastIndex = min(count, index + 5)
#             messages = []
#             for x in range(index, lastIndex):
#                 res = result[x]
#                 dt = res[5]
#                 dtStr = dt.strftime("%Y-%m-%d %H:%M:%S")
#                 messages.append(
#                     {'id': res[0], 'chatroom_id': res[1], 'user_id': res[2], 'name': res[3], 'message': res[4],
#                      'message_time': dtStr})
#             data = {'current_page': page, 'messages': messages, "total_pages": total_pages}
#             response = {'status': 'OK', 'data': data}
#             return json.dumps(response)


# /api/a3/send_message
# @app.route('/api/a3/send_message', methods=['POST'])
# def send_message():
#     if request.method == 'POST':
#         chatroom_id = int(request.form.get('chatroom_id'))
#         name = request.form.get('name')
#         message = request.form.get('message')
#         user_id = request.form.get('user_id')
#         if chatroom_id is None or chatroom_id == '' or \
#                 name is None or name == '' or \
#                 message is None or message == '' or \
#                 user_id is None or user_id == '':
#             return json.dumps({'status': 'ERROR', 'message': 'bad parameter'})
#         else:
#             if len(name) > 20:
#                 return json.dumps({'status': 'ERROR', 'message': 'The name is more than 20 characters'})
#             if len(message) > 200:
#                 return json.dumps({'status': 'ERROR', 'message': 'The message is more than 200 characters'})
#             # query chat room
#             # opendb
#             mydb = getDBInfo()
#             cursor = mydb.cursor()
#             cursor.execute("SELECT * FROM chatrooms WHERE id=" + str(chatroom_id))
#             result = cursor.fetchone()
#             if result is None:
#                 return json.dumps({'status': 'ERROR', 'message': 'chatroom_id not exsit'})
#             # insert message to db
#             cursor = mydb.cursor()
#             sql = "INSERT INTO messages (chatroom_id, user_id, name, message) VALUES (" + str(chatroom_id) + "," + str(
#                 user_id) + ",\'" + str(name) + "\',\'" + str(message) + "\')"
#             cursor.execute(sql)
#             mydb.commit()
#             mydb.close()
#             return json.dumps({'status': 'OK'})


# 获取通讯录上的所有人
@app.route("/api/project/rooms", methods=["GET"])
def get_rooms():
    print("-----ACTION: get_rooms-----")
    user_id = request.args.get("user_id")
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "SELECT username,user_id FROM user WHERE user_id in (" \
            "SELECT user_id_2 FROM friends WHERE user_id_1=" + user_id + ")"
    cursor.execute(query)
    result = cursor.fetchall()
    print("QUERY: ", query)
    print("RESULT: ", result)
    mydb.commit()
    mydb.close()
    rooms_data = []
    for user in result:
        rooms_data.append({'username': user[0], 'user_id': user[1]})
    return json.dumps({'status': 'ok', 'data': rooms_data})


# 获得对应好友的聊天消息
@app.route("/api/project/messages", methods=["GET"])
def get_messages():
    print("-----ACTION: get_messages-----")
    curr_user = request.args.get("curr_user")
    target_user = request.args.get("target_user")
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "SELECT message_id,sender,receiver,message,DATE_FORMAT(message_time,'%Y-%m-%d %H:%i') as message_time FROM messages WHERE (sender=" + curr_user + " and receiver=" + target_user + \
            ") OR (sender=" + target_user + " and receiver=" + curr_user + ") ORDER BY message_time DESC"
    print("QUERY: ", query)
    cursor.execute(query)
    result = cursor.fetchall()
    print("RESULT: ", result)
    mydb.commit()
    mydb.close()
    messages_detail = []
    for message in result:
        messages_detail.append(
            {'sender': message[1], 'receiver': message[2], 'message': message[3], 'message_time': message[4]})
    return json.dumps({'status': 'ok', 'data': messages_detail})


# 发送消息
@app.route("/api/project/messages", methods=["POST"])
def post_message():
    print("-----ACTION: post_messages-----")
    send_user = request.form.get("send_user")
    receive_user = request.form.get("receive_user")
    message = request.form.get("message")

    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "INSERT INTO messages (sender,receiver,message) VALUES " \
            "(" + send_user + "," + receive_user + ",'" + message + "')"
    print("QUERY: ", query)
    cursor.execute(query)
    result = cursor.fetchone()
    print("RESULT: ", result)
    mydb.commit()
    mydb.close()
    return json.dumps({'status': 'ok'})


# 添加朋友
@app.route("/api/project/add_friend", methods=["POST"])
def add_friend():
    print("-----ACTION: add_friend-----")
    sender_id = request.form.get("sender_id")
    receiver_name = request.form.get("receiver_name")
    print("--REQUEST CONTENT: request id: ", sender_id, ", receive name: ", receiver_name)
    mydb = getDBInfo()
    cursor = mydb.cursor()

    # 根据nickname 查看是否存在
    query = "select user_id FROM user where username='" + receiver_name + "'"
    cursor.execute(query)
    receiver_id = cursor.fetchone()

    if receiver_id is None:
        return json.dumps({'status': '0'})  # 没有该用户
    print("QUERY: ", query)
    print("RESULT: ", receiver_id)
    print("receiver id: ", receiver_id[0])

    query = "select count(*) as count FROM friends where user_id_1='" + sender_id + "' and user_id_2='" + str(
        receiver_id[0]) + "'"
    cursor.execute(query)
    is_friend = cursor.fetchone()
    print("QUERY: ", query)
    print("RESULT: ", is_friend)
    if is_friend[0] != 0:
        return json.dumps({'status': '2'})  # 已经添加了
    else:
        # print(receive_id['user_id'])
        query = "INSERT INTO request_list (sender, receiver) values(" + sender_id + ", " + str(
            receiver_id[0]) + ")"
        print("QUERY: ", query)
        cursor.execute(query)
        mydb.commit()
        return json.dumps({'status': '1'})  # 已发送请求

    mydb.close()


# 获得添加列表
@app.route("/api/project/get_friend_requests", methods=["GET"])
def get_friend_request():
    print("-----ACTION: get_friend_request-----")
    user_id = request.args.get("user_id")
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "select username from user where user_id in " \
            "(select sender from request_list where receiver=" + user_id + " and status=0)"
    cursor.execute(query)
    result = cursor.fetchall()
    print("QUERY: ", query)
    print("RESULT: ", result)
    mydb.close()
    request_users = []
    for user in result:
        request_users.append({'username': user[0]})
    return json.dumps({'status': 'ok', 'data': request_users})  # 已经添加了


# 获得联系人列表
@app.route("/api/project/get_friends", methods=["GET"])
def get_friends():
    print("-----ACTION: get_friends-----")
    user_id = request.args.get("user_id")
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "select username FROM user where user_id in (select user_id_2 from friends where user_id_1=" + user_id + ")"
    cursor.execute(query)
    result = cursor.fetchall()
    print("QUERY: ", query)
    print("RESULT: ", result)
    mydb.close()
    all_friends = []
    for user in result:
        all_friends.append({'username': user[0]})

    return json.dumps({'status': 'ok', 'data': all_friends})  # 已经添加了


# 添加好友操作（接受或拒绝 接受1 拒绝0）    CHECK
@app.route("/api/project/accept_or_refuse", methods=["GET"])
def accpet_or_refuse():
    print("-----ACTION: accept_or_refuse-----")
    operation = request.args.get("operation")
    request_name = request.args.get("request_name")
    receiver_id = request.args.get("receiver_id")

    print("operation: ", operation)
    print("request name: ", request_name)
    print("receive id: ", receiver_id)

    mydb = getDBInfo()
    cursor = mydb.cursor()
    # 先找出该用户名对应的id
    query = "SELECT user_id FROM user WHERE username=" + request_name
    cursor.execute(query)
    result = cursor.fetchone()
    print("QUERY: ", query)
    print("RESULT: ", result)
    request_id = result[0]
    print("request id: ", request_id)

    # waiting_list 删除该记录
    query = "delete FROM request_list WHERE receiver=" + str(receiver_id) + \
            " and sender=" + str(request_id)
    print("QUERY: ", query)
    cursor.execute(query)
    query = "delete FROM request_list WHERE receiver=" + str(request_id) + \
            " and sender=" + str(receiver_id)
    print("QUERY: ", query)
    cursor.execute(query)
    mydb.commit()

    if operation == '1':
        print("--Accept--")
        query = "INSERT INTO friends values(" + str(request_id) + "," + str(receiver_id) + ")"
        print("QUERY: ", query)
        cursor.execute(query)
        query = "INSERT INTO friends values(" + str(receiver_id) + "," + str(request_id) + ")"
        print("QUERY: ", query)
        cursor.execute(query)
        mydb.commit()

    else:
        print("--Refuse--")

    # query = "select nickname FROM relationship,user where user_id1=" + str(user_id) +" and user_id=user_id2"
    # print(query)
    # cursor.execute(query)
    # all_friends = cursor.fetchall()

    mydb.close()

    return json.dumps({'status': 'ok'})  # 已经添加了


# 发朋友圈
@app.route("/api/project/posts", methods=["POST"])
def new_posts():
    print("-----ACTION: new posts-----")
    user_id = request.form.get("user_id")
    content = request.form.get("posts_content")

    # 点赞数 默认为0
    # 评论数 默认为0
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = 'INSERT INTO posts (user_id, content) values(' + user_id + ",'" + content + "')"
    print("QUERY: ", query)
    cursor.execute(query)
    mydb.commit()
    mydb.close()
    return json.dumps({'status': 'ok'})  # 发送朋友圈成功


# 获取朋友圈列表
@app.route("/api/project/posts", methods=["GET"])
def get_posts():
    print("-----ACTION: get posts-----")
    user_id = request.args.get("user_id")
    # 点赞数 默认为0
    # 评论数 默认为0
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "SELECT m.*,n.is_like FROM(" \
            "SELECT posts.*,username FROM posts,user WHERE posts.user_id IN (" \
            "select DISTINCT(user_id_2) AS user_id FROM friends where " \
            "user_id_1 = " + user_id + " OR user_id_2=" + user_id + ") AND posts.user_id = user.user_id) as m " \
                                                                    "left join (SELECT * FROM likes_info WHERE user_id=" + user_id + ") AS n ON m.post_id=n.post_id ORDER BY post_time DESC"
    print("QUERY: ", query)
    cursor.execute(query)
    result = cursor.fetchall()
    print("RESULT: ", result)
    mydb.close()
    info = []
    for post in result:
        info.append(
            {'post_id': post[0], 'user_id': post[1], 'post_content': post[2], 'post_time': post[3], 'likes': post[4],
             'is_like': post[5]})
    return json.dumps({'status': 'ok', 'data': info})  # 发送朋友圈成功


# 点赞
@app.route("/api/project/like", methods=["POST"])
def give_like():
    print("-----ACTION: like-----")
    user_id = request.form.get("user_id")
    post_id = request.form.get("post_id")
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "REPLACE INTO likes_info VALUES(" + post_id + "," + user_id + ",1)"
    print("QUERY: ", query)
    # 将表中的值+1
    query = "UPDATE posts SET likes=likes+1 WHERE post_id = " + post_id
    print("QUERY: ", query)
    cursor.execute(query)
    mydb.commit()
    mydb.close()

    return json.dumps({'status': 'ok'})


# 取消点赞
@app.route("/api/project/dislike", methods=["POST"])
def cancel_like():
    print("-----ACTION: dislike-----")
    user_id = request.form.get("user_id")
    post_id = request.form.get("post_id")
    mydb = getDBInfo()
    cursor = mydb.cursor()
    query = "DELETE FROM likes_info WHERE post_id=" + post_id + " AND user_id=" + user_id
    print("QUERY: ", query)
    cursor.execute(query)
    query = "UPDATE posts SET likes=likes-1 WHERE post_id = " + post_id
    print("QUERY: ", query)
    cursor.execute(query)
    mydb.commit()
    mydb.close()

    return json.dumps({'status': 'ok'})


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
