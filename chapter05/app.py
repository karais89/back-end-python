from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = {}          # 새로 가입한 사용자 users란 변수에 정의 한다.
app.id_count = 1        # 회원 가입하는 사용자의 id 값을 저장


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json  # json -> dictionary
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1

    return jsonify(new_user)  # dictionary -> json

