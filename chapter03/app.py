from flask import Flask

app = Flask(__name__)


# route 데코레이터를 사용하여 엔드포인트 등록
@app.route("/ping", methods=['GET'])
def ping():
    return "pong"
