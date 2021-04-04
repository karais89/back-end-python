# 챕터1. 파이썬 설치 및 개발 환경 구성

- 윈도우 이용자는 우분투를 설치하여 개발을 추천하고 있음
- 아나콘다를 이용한 파이썬 설치 (이책에서는 경량화된 미니콘다를 설치 한다)
- 깃, 깃허브 사용법
- 셀 설치 방법
- 에디터 소개 (vim 추천)

챕터1에서 엄청나게 다양한 것들에 대해 설명하고 있다. 다양한 부분에 대해 설명하고 있어서 좋았다.

우선 가상환경, 깃, 깃허브, 에디터 등은 모두 파이참 IDE를 사용하여 모두 해결 가능한 부분이라 파이참을 사용하여 개발 진행 예정.

# 챕터2. 현대 웹 시스템 구조 및 아키텍처

- 웹 시스템의 역사에 대한 이야기.
- 정적 → 자바스크립트 발전 → 동적 → 단일 페이지 앱
- 백엔드의 경우 처리 용량이나 속도가 크게 중요하지 않고, 개발의 속도와 편리함이 중요하다.
- 현대의 웹 시스템은 규모가 크고 처리해야하는 동시 요청 수와 데이터의 규모가 기하학적으로 증가하였다.
- 백엔드 개발에 입문했을 경우에는 API 개발부터 차근차근 학습
- 개발팀에 구성원에 대한 설명 (정리 생략)

# 챕터3. 첫 API 개발 시작

- Flask 소개 및 설치
- API 기초적인 기능 구현 (ping 엔드포인트 구현)
- API 실행

## Flask

- 파이썬 웹 프레임워크. 아주 가벼운 웹 프레임워크.
- 다른 프레임워크에 비해 비교적 쉽게 배울 수 있다. (API 입문 개발에 좋은 프레임워크)
- 파이썬 3.7 기준으로 작성됨.

```bash
pip install flask
```

## ping 엔드포인트 구현

- 단순히 pong이라는 텍스트를 리턴하는 엔드포인트.
    - 엔드포인트 = api 서버가 제공하는 통신 채널 혹은 접점
- 헬스 체크 엔드 포인트 (API의 정상 운행 여부 판단)

```python
from flask import Flask

app = Flask(__name__)

# route 데코레이터를 사용하여 엔드포인트 등록
@app.route("/ping", methods=['GET'])
def ping():
    return "pong"
```

- flask는 일반적으로 route 데코레이터를 사용해서 함수들을 엔드포인트로 등록하는 방식이 사용된다.

## API 실행하기

```python
FLASK_APP=app.py FLASK_DEBUG=1 flask run
```

- 실행의 경우도 파이참에서는 쉽게 실행할 수 있다.
- [http://127.0.0.1:5000/ping](http://127.0.0.1:5000/ping) 로 접속
- 책에서 접속 테스트를 httpie를 사용하여 진행함.

# 챕터4. HTTP의 구조 및 핵심 요소

- HTTP는 HTML을 주고 받을 수 있도록 만들어진 통신 규약이다.
- HTTP의 특징 2가지 (요청과 응답 방식, stateless)
    - 서버가 클라이언트로부터 요청을 받고 보냄
    - 각각의 HTTP 통신은 서로 독립적이며 그 전에 처리된 HTTP 통신에 대해 알지 못한다.
- 자주 사용되는 HTTP 메소드
    - GET: 어떠한 데이터를 서버로부터 요청할때 주로 사용됨
    - POST: 데이터를 생성하거나 수정 및 삭제 요청을 할 대 주로 사용됨
    - OPTIONS
    - PUT: 데이터를 새로 생성할 때 사용
    - DELETE: 데이터 삭제
- HTTP Status Code
    - 200 OK: 문제없을 때
    - 301 Moved Permanently: http 요청을 보낸 엔드포인트의 url 주소가 변경 됨.
    - 400 Bad Request: HTTP 요처이 잘모된 요청일때
    - 401 Unauthoried: 로그인이 필요한 경우
    - 403 Forbidden: 요청에 대한 권한이 없을때
    - 404 Not Found: uri가 존재하지 않을 경우
    - 500 Internal Server Error: 내부 서버 오류
- 엔드포인트 아키텍쳐 패턴
    - REST 방식
    - GraphQL
  
# 챕터 5. 본격적으로 API 개발하기

- 구현할 API 시스템은 미니 트위터 (회원가입, 로그인, 트윗, 다른 회원 팔로우, 언팔로우, 타임라인)

## 회원가입

- 회원 가입시 필요 정보 (id, name, email, password, profile)

```python
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
```

- postman을 사용한 정보 전송 or 파이참 기능 사용
- [https://www.jetbrains.com/help/pycharm/http-client-in-product-code-editor.html#composing-http-requests](https://www.jetbrains.com/help/pycharm/http-client-in-product-code-editor.html#composing-http-requests)
- 카운트 증가 해주는 부분은 문제 발생 소지 있음 (atomic 검색)

## 300자 제한 트윗 글 올리기

- 300자가 넘으면 400 Bad Request 응답
- 300자 이내면 사용자의 글을 저장

```python
app.tweets = []

@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return '사용자가 존재하지 않습니다', 400

    if len(tweet) > 300:
        return '300자를 초과했습니다', 400

    user_id = int(payload['id'])
    app.tweets.append({
        'user_id': user_id,
        'tweet': tweet
    })
    
    return '', 200
```

- 파이썬은 동적 타이핑 언어라 유연한 대신 코드의 실수 발생 가능성이 높다.
    - app.tweets 처럼 바로 클래스 안에 변수를 생성 할 수 있는데. 이 부분이 참 마음에 안드는 부분 이다.
- 우선 request 이후 200 응답이 온다면 OK.

## 팔로우와 언팔로우

```python
@app.route('/follow', methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return '사용자가 존재하지 않습니다', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)  # setdefault dictionary 기능

    return jsonify(user)
```

- setdefault는 파이썬에서 제공해주는 dictionary의 기능
- set 자료형을 사용하는데, 이 부분을 json 모듈이 json으로 변경하지 못해 에러가 발생하여 아래와 같이 처리해줘야 함.

```python
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder
```

- jsonEncoder 클래스의 default 메소드를 확장한다. set인 경우 list로 변경한다.
- 객체가 set이 아닌 경우는 기존 default 메소드를 호출한다.
- [https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.JSONEncoder](https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.JSONEncoder)

```python
@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['unfollow'])
    
    if user_id not in app.users or user_id_to_follow not in app.users:
        return '사용자가 존재하지 않습니다', 400
    
    user = app.users[user_id]
    user.setdefault('follow', set()).discard(user_id_to_follow)
    
    return jsonify(user)
```

- 언팔로우 구현 remove대신 discard를 사용하는 이유는 discard의 경우 없는 값을 삭제 해도 에러가 발생하지 않는다.

## 타임라인

- 해당 사용자의 트윗들 그리고 팔로우하는 사용자들의 트윗들을 리턴

```python
@app.route('/timeline/<int:user_id>', methods=['GET'])  # 엔드포인트 주소 <int:user_id> /timeline/1 같은 형태에서 1이 user_id에 저장됨
def timeline(user_id):
    if user_id not in app.users:
        return '사용자가 존재하지 않습니다', 400

    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        'user_id': user_id,
        'timeline': timeline
    })
```

- `<int:user_id>` 부분 확인
- `[tweet for tweet in app.tweets if tweet['user_id'] in follow_list]` 이건 파이썬 코드인데 가독성 최악 아닌가? 전체 트윗 중에 해당 사용자 그리고 해당 사용자가 팔로우하는 사용자들의 트윗들만 읽는다.
- [List comprehension (리스트 내포 for문 사용)](https://www.w3schools.com/python/python_lists_comprehension.asp)

    ```python
    # [표현식 for 항목 in 반복가능객체 if 조건문]

    a = [1,2,3,4]
    result = []
    for num in a:
        result.append(num*3)

    result = [num * 3 for num in a]
    result = [num * 3 for num in a if num % 2 == 0]  # 짝수만 담고 싶을때
    ```

    ```python
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    # 위와 같은 문장
    timeline = []
    for tweet in app.tweets:
        if tweet['user_id'] in follow_list:
            timeline.append(tweet)
    ```

## 5장 완료 느낀점

- DB를 사용하여 저장하지는 않지만, 메모리를 사용하여 유저 트윗 등을 저장하는 방식으로 구현하고, 대략적인 api 설계의 느낌을 볼 수 있어서 좋았다.
- post, get 방식으로 엔드 포인트 구현
- 파이참에서 제공해주는 [test restful web services](https://www.jetbrains.com/help/pycharm/testing-restful-web-services.html)가 편하다.
- 플라스크로 rest api 개발이 상당히 쉽다.

# 챕터 6. 데이터베이스

- 데이터를 영구적으로 보존하기 위해서는 데이터베이스 시스템을 사용해야 한다.
- 일반적으로 관계형 데이터베이스, 비관계형 데이터베이스로 구분 된다.
- 관계형 데이터베이스 (RDBMS)
    - MySQL, PostgreSQL 등
    - 2차원 테이블 형태
- 비관계형 데이터베이스
    - NoSQL 데이터베이스
    - 데이터가 들어오는 그대로 저장
- 관계형 데이터베이스 시스템은 주로 정형화된 데이터들 그리고 데이터의 완전성이 중요한 데이터들을 저장하는데 유리함. (전자상거래 정보, 은행 계좌 정보, 거래 정보 등)
- 비관계형 데이터베이스 시스템은 비정형화 데이터, 그리고 완전성이 상대적으로 덜 중요한 데이터를 저장하는데 유리함 (로그 데이터)
- SELECT, INSERT, UPDATE, DELETE에 대한 설명 생략
- join 구문은 여러 테이블을 연결할 때 사용

```sql
SELECT
	table.column1,
	table.column2,
FROM table1
JOIN table2 ON table1.id = table2.table1_id

# 사용자 이름을 user 테이블에서 읽어 들이고, 해당 사용자의 주소를 user_address라는 테이블에서 읽어 들인다
SELECT
	users.name
	user_address.address
FROM users
JOIN user_address ON users.id = user_address.user_id
```

- MySQL 설치 생략 (개인은 MariaDB 추천)

## API에 데이터베이스 연결하기

- 데이터베이스의 경우도 파이참에서 제공하는 내장된 데이터그립을 사용하면 쉽게 데이터베이스를 다룰 수 있다. (데이터 그립 프로그램을 별도로 설치해서 사용 가능)

```sql
CREATE DATABASE miniter;
USE miniter;
```

테이블 생성 구문

```sql
CREATE TABLE table_name (
	column1 data_type,
	column2 data_type,
	...
	PRIMARY KEY(column1),
	CONSTRAIT 1,
	CONSTRAIT 2
)
```

user 테이블 생성

```sql
CREATE TABLE users(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    profile VARCHAR(2000) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);
```

- NOT NULL은 해당 칼럼은 null이 될 수 없다
- AUTO_INCREMENT는 자동으로 1씩 증가된다.
- DEFAULT CURRENT_TIMESTAMP은 해당 칼럼이 없으면 디폴트 값을 현재 시간으로 사용
- ON UPDATE CURRENT_TIMESTAMP은 해당 로우가 수정되면 해당 컬럼의 값을 수정이 이루어진 시간으로 자동 생성해준다.
- PRIMARY KEY 고유키로 사용될 컬럼을 정해준다
- UNIQUE KEY는 해당 칼럼이 중복되는 로우가 없어야 된다.

```sql
CREATE TABLE users_follow_list(
    user_id INT NOT NULL,
    follow_user_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, follow_user_id),
    CONSTRAINT users_follow_list_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT users_follow_list_follow_user_id_fkey FOREIGN KEY (follow_user_id) REFERENCES users(id)
)
```

- CONSTRAINT... FOREIGN KEY ... REFERENCES ... 구문을 통해서 외부 키를 걸 수 있다.

```sql
CREATE TABLE tweets(
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    tweet VARCHAR(300) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT tweets_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)
);
```

테이블 전체 보기, 테이블 상세 보기

```sql
SHOW tables;
EXPLAIN users;
```

## SQLAlchemy

- SQLAlchemy는 파이썬에서 가장 널리 쓰이는 DB 라이브러리 중 하나이다. (ORM)
- 이 책에서는 ORM을 사용하지 않고 CORE 부분만 사용한다. (SQL을 더 익히기 위해 학습 목적)

```bash
pip install sqlalchemy
pip install mysql-connector-python
```

접속 예시

```python
from sqlalchemy import create_engine, text

db = {
    "user": "root",
    "password": "123456",
    "host": "localhost",
    "port": 3306,
    "database": "miniter"
}

db_url = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
db = create_engine(db_url, encoding='utf-8', max_overflow=0)

params = {'name': '송은우'}
rows = db.execute(text("SELECT * FROM users WHERE name = :name"), params).fetchall()

for row in rows:
    print(f"name: {row['name']}")
    print(f"email: {row['email']}")
```

- [f string 포맷](https://docs.python.org/3/tutorial/inputoutput.html)

## SQLAlchemy를 사용하여 API와 데이터베이스 연결

```python
db = {
    "user": "root",
    "password": "123456",
    "host": "localhost",
    "port": 3306,
    "database": "miniter"
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
```

```python
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

# create_app이라는 함수 정의. Flask가 create_app이라는 함수를 자동으로 팩토리 함수로 인식함
def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database

    return app
```

- config.py를 만들고, flask에서 config 파일을 자동으로 불러올 수 있는 함수등을 제공함.
- create_app함수는 flask에서 제공해주는 팩토리 함수. 자동으로 불러와짐.
- [https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/)

### 회원가입

```python
# 회원가입 엔드포인트
@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user_id = current_app.database.execute(text("""
    INSERT INTO users (
        name,
        email,
        profile,
        hashed_password
    ) VALUES (
        :name,
        :email,
        :profile,
        :password
    )
    """), new_user).lastrowid

    row = current_app.database.execute(text("""
        SELECT id, name, email, profile
        FROM users
        WHERE id = :user_id
    """), {
        'user_id': new_user_id
    }).fetchone()

    # 파이썬 식 3항 연산자.. (참인경우 값 if 조건 else 거짓인경우 값)
    created_user = {
        'id': row['id'],
        'name': row['name'],
        'email': row['email'],
        'profile': row['profile']
    } if row else None

    return jsonify(created_user)
```

- current_app은 create_app 함수로 생성한 플라스크 앱 app을 의미한다. current_app은 request와 마찬가지로 컨텍스트 구간에서 사용할 수 있는 플라스크가 자동으로 생성해 주는 객체이다.
- 책 소스가 좀 헷갈리게 되어 있다. app과 current_app을 번갈아가면서 사용하는데. current_app을 사용하는게 맞는거 같긴하다.
- g라는 변수도 따로 사용할 수 있나 보다.
- [current_app과 g의 차이](https://stackoverflow.com/questions/40881750/whats-the-difference-between-current-app-and-g-context-variable)
- 파이썬식 3항 연산자 가독성 개판.

### tweet

```python
@app.route('/tweet', methods=['POST'])
def tweet():
    user_tweet = request.json
    tweet = user_tweet['tweet']

    if len(tweet) > 300:
        return '300자를 초과했습니다', 400

    current_app.database.execute(text("""
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUES (
            :id,
            :tweet
        )
    """), user_tweet)

    return '', 200
```

### timeline

```python
@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    rows = current_app.database.execute(text("""
        SELECT 
            t.user_id,
            t.tweet
        FROM tweets t
        LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
        WHERE t.user_id = :user_id
        OR t.user_id = ufl.follow_user_id
    """), {
        'user_id': user_id
    }).fetchall()

    timeline = [{
        'user_id': row['user_id'],
        'tweet': row['tweet']
    } for row in rows]

    return jsonify({
        'user_id': user_id,
        'timeline': timeline
    })
```

- 데이터베이스에 있는 데이터들을 읽어 들여서 JSON 형태로 변환하여 HTTP 응답으로 보낸다.
- LEFT JOIN으로 해당 사용자가 팔로우하는 사용자가 없더라도 해당 사용자의 트윗만을 읽어 들이게 한다.
- 여기서도 리스트 내포 FOR문 사용됨

### 나머지 엔드포인트 구현

- ping, follow, unfollow

```python
@app.route('/follow', methods=['POST'])
def follow():
    payload = request.json
    rowcount = current_app.database.execute(text("""
            INSERT INTO users_follow_list (
                user_id,
                follow_user_id
            ) VALUES (
                :id,
                :follow
            )
            """), payload).rowcount

    return '', 200

@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload = request.json
    rowcount = current_app.database.execute(text("""
                    DELETE FROM users_follow_list WHERE user_id = :id AND follow_user_id = :unfollow
                    """), payload).rowcount

    return '', 200
```

### 리팩토링

```python
from flask import Flask, jsonify, request, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text

# Defalut JSON encoder는 set을 JSON으로 변환할 수 없다.
# 그러므로 커스텀 인코더를 작성하여 set을 list로 변환하여
# JSON으로 변환 가능하게 해주어야 한다.
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

def get_user(user_id):
    user = current_app.database.execute(text("""
            SELECT id, name, email, profile
            FROM users
            WHERE id = :user_id
        """), {
        'user_id': user_id
    }).fetchone()

    return {
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'profile': user['profile']
    } if user else None

def insert_user(user):
    return current_app.database.execute(text("""
    INSERT INTO users (
        name,
        email,
        profile,
        hashed_password
    ) VALUES (
        :name,
        :email,
        :profile,
        :password
    )
    """), user).lastrowid

def insert_tweet(user_tweet):
    return current_app.database.execute(text("""
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUES (
            :id,
            :tweet
        )
    """), user_tweet).rowcount

def insert_follow(user_follow):
    return current_app.database.execute(text("""
            INSERT INTO users_follow_list (
                user_id,
                follow_user_id
            ) VALUES (
                :id,
                :follow
            )
            """), user_follow).rowcount

def insert_unfollow(user_unfollow):
    return current_app.database.execute(text("""
                DELETE FROM users_follow_list 
                WHERE user_id = :id 
                AND follow_user_id = :unfollow
                """), user_unfollow).rowcount

def get_timeline(user_id):
    timeline = current_app.database.execute(text("""
        SELECT 
            t.user_id,
            t.tweet
        FROM tweets t
        LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
        WHERE t.user_id = :user_id
        OR t.user_id = ufl.follow_user_id
    """), {
        'user_id': user_id
    }).fetchall()

    return [{
        'user_id': tweet['user_id'],
        'tweet': tweet['tweet']
    } for tweet in timeline]

# create_app이라는 함수 정의. Flask가 create_app이라는 함수를 자동으로 팩토리 함수로 인식함
def create_app(test_config=None):
    app = Flask(__name__)

    app.json_encoder = CustomJSONEncoder

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database

    # ping
    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"

    # 회원가입 엔드포인트
    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user = request.json
        new_user_id = insert_user(new_user)
        new_user = get_user(new_user_id)

        return jsonify(new_user)
    

    @app.route('/tweet', methods=['POST'])
    def tweet():
        user_tweet = request.json
        tweet = user_tweet['tweet']

        if len(tweet) > 300:
            return '300자를 초과했습니다', 400

        insert_tweet(user_tweet)

        return '', 200

    @app.route('/timeline/<int:user_id>', methods=['GET'])
    def timeline(user_id):
        return jsonify({
            'user_id': user_id,
            'timeline': get_timeline(user_id)
        })

    @app.route('/follow', methods=['POST'])
    def follow():
        payload = request.json
        insert_follow(payload)
        
        return '', 200

    @app.route('/unfollow', methods=['POST'])
    def unfollow():
        payload = request.json
        insert_unfollow(payload)

        return '', 200

    return app
```

- 데이터베이스에 SQL을 실행하는 로직들을 따로 함수로 만들어 작성.

# Chapter7. 인증

API에서는 기본적인 인증을 요구한다.

## 인증

- 인증은 사용자의 신원을 확인하는 절차다.
- 로그인 기능을 구현하는 것이 인증 엔드포인트다.

로그인 기능의 일반적인 인증 절차

1. 사용자 가입 절차를 통해 아이디와 비밀번호 생성
2. 가입한 아이디와 비밀번호를 DB에 저장. 사용자 비밀번호는 암호화 필수
3. 사용자가 로그인할 때 본인의 아이디와 비밀번호를 입력
4. 사용자가 입력한 비밀번호를 암호화한 후, 그 값을 이미 암호화되어 DB에 저장된 비밀번호화 비교
5. 비밀번호 일치시 로그인 성공
6. 로그인 성공시 백엔드 api 서버는 access token을 프론트엔드 혹은 클라이언트에게 전송한다.
7. 프론트엔드 서버는 로그인 성공 후 다음부터 해당 사용자의 acces token을 첨부해서 request를 서버에 전송하여 사용한다.

## 사용자 비밀번호 암호화

암호화 이유

- 외부의 해킹에 의한 데이터베이스의 노출
- 내부 인력에 의한 데이터베이스의 노출

> 사용자 비밀번호 암호화 할때는 단방향 해시 함수를 일반적으로 사용한다.

단방향 해시 함수는 복호화를 할 수 없는 암호화 알고리즘이다.

```python
import hashlib
m = hashlib.sha256()
m.update(b"test password")
m.hexdigest()
```

## Bcrypt 암호 알고리즘

- 단방향 해시 알고리즘도 취약점이 존재한다.
- 일반적으로 2가지 보완점을 사용
    1. salting 이라는 방법
        - 실제 비밀번호 이외에 추가적으로 랜덤 데이터를 더해 해시 값을 계산
    2. key stretching 이라는 방법
        - 단방향 해시 알고리즘을 계산한 후 그 해시 값을 또 해시하고 여러번 반복하는 방법
- salting와 key stretching를 구현한 해시 함수 중 가장 널리 사용되는 것이 bcrypt이다.

```python
pip install bcrypt

import bcrypt
bcrypt.hashpw(b"secret password", bcrypt.gensalt())
bcrypt.hashpw(b"secret password", bcrypt.gensalt()).hex
```

- 확인해보니 bcrypt는 salt값을 bcrypt.hashpw로 생성시 앞에 이미 저장을 함.
    - salt 값이 해킹 당하면 어쩌지? 했는데 결국엔 외부에서는 rainbow attack 등으로 해킹하는 것이기때문에. DB 자체가 털리지 않는 이상은 괜찮은 것 같음.
    - 그런데 만약 DB가 털린다? 그러면 salt는 알고 있으니.. 다른 방법을 이용해야 될 것 같은데.. 모르겟네. DB가 털려도 안전하려면 다른 방법을 이용해야 될 것 같은데 잘 모르겠다.

## access token

- 사용자가 로그인 성공 이후 백엔드 api 서버는 access token 이라고 하는 데이터를 프론트엔드에게 전송한다.
- 그리고 프론트엔드에서는 해당 사용자의 access token을 http 요청에 첨부해서 서버에 전송한다.
- http는 stateless다. 현재의 http 통신에서 이전에 이미 인증이 진행됐는지 알지 못한다. http 통신을 할 때에는 해당 http 요청을 처리하기 위해 필요한 모든 데이터를 첨부해서 요청을 보내야 한다.

## JWT(JSON Web Token)

- access token을 생성하는 방법 중 가장 널리 사용되는 기술 중 하나가 JWT이다.
- JWT는 이름 그대로 JSON 데이터를 token으로 변환하는 방식이다.

```python
POST /auth HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
	"username": "joe",
	"password": "password"
}
```

- 사용자 아이디는 "joe"이고 비밀번호는 "password"이다
- HTTP Post 요청을 /auth 엔드포인트에 전송한다.

```python
{
	user_id = 1
}
```

- access token을 받은 프론트엔드가 쿠키 등에 access token을 저장하고 있다가 요청 시 access token을 첨부해 보낸다. 그러면 백엔드 api 서버는 access token을 복호화해서 json 데이터를 얻을 수 있다.
- 단순 json 데이터를 사용하면 해킹 가능성이 있다. jwt에는 단순 데이터 전송 기능 이외에 검증의 기능도 가지고 있다. 백엔드 api 서버는 자신이 생성한 jwt인지 아닌지 확인할 수 있는 기능을 제공한다.

### JWT 구조

- header
- payload
- signature

```python
xxxxx.yyyyy.zzzzz
```

- x 부분은 헤더이고 y 부분은 payoad이며 z 부분은 signature다. 각 부분은 . 으로 분리한다.

header

- 헤더는 두 부분으로 되어 있다. 토큰 타입, 해시 알고리즘

```python
{
	"alg": "HS256",
	"typ": "JWT"
}
```

payload

- jwt를 통해 실제로 서버 간에 전송하고자 하는 데이터 부분.

```python
{
	"user_id": 2
	"exp" : 1539517391
}
```

- 중요한 부분은 payload는 누구나 복원 가능하기 때문에 중요한 정보는 넣지 않아야 한다.

signature

- jwt가 원본 그대로라는 것을 확인하는데 사용하는 부분
- Base64URL 코드화된 header와 payload 그리고 jwt secret를 헤더에 지정된 암호화 알고리즘으로 암호화 하여 전송한다. (복호화 가능한 암호)

### PyJWT

```python
pip install PyJWT
```

```python
import jwt
data_to_encode = {'some':'payload'}
encryption_secret = 'secrete'
algorithm = 'HS256'
encoded = jwt.encode(data_to_encode, encryption_secret, algorithm=algorithm)
jwt.decode(encoded, encryption_secret, algorithms=[algorithm])
```

```python
@app.route('/tweet', methods=['POST'])
@login_required
def tweet():
    user_tweet = request.json
    user_tweet['id'] = g.user_id
    tweet = user_tweet['tweet']

    if len(tweet) > 300:
        return '300자를 초과했습니다', 400

    insert_tweet(user_tweet)

    return '', 200

@app.route('/follow', methods=['POST'])
@login_required
def follow():
    payload = request.json
    insert_follow(payload)
    
    return '', 200

@app.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
    payload = request.json
    insert_unfollow(payload)

    return '', 200
```

- tweet의 경우 jwt 토큰에서 받은 id를 넘겨 받는다.
- 이후 과정에서는 로그인 후 access token을 받고 해당 엔드포인트에서 access token을 같이 넘겨줘야 정상 동작한다.


# Chapter 8. unit test

- 개발한 시스템이 정상적으로 동작하는지 확인 하는 과정인 테스트에 대해 알아보자.
- 다양한 테스트 방법 중 단위 테스트에 대해서 알아볼 예정

## 테스트 자동화의 중요성

> 시스템 테스트에서 가장 중요한 것은 테스트의 자동화이다.

테스트를 최대한 자동화해서 테스트가 반복적으로, 그리고 자주 실행될 수 있도록 한다.

또한 항상 정확하게, 그리고 빠지는 부분이 없도록 테스트가 실행되도록 하는 것이 중요하다.

시스템 테스트 방법 3가지

- UI test / End-To-End test
- integration test
- unit test

## UI test / End-To-End Test

- 시스템의 UI를 통해서 테스트 하는 것
- 사용자가 실제로 시스템을 사용하는 방식과 가장 동일하게 테스트 할 수 있다.
- 시간이 많이 소모되는 테스트 이다. 자동화가 까다롭다.
- 일반적으로 비중 10%

## integration test

- 테스트 하고자 하는 서버를 실제로 실행시키고, 테스트 HTTP 요청등을 실행하여 테스트 해보는 방식
- 테스트 하고자 하는 해당 시스템만 실행시켜 테스트한다.
- UI test 보다 테스트 설정이나 실행 시간이 더 짧고 간단하다.
- 일반적으로 비중 20%

## unit test

- 코드를 직접 테스트 한다는 개념
- 코드를 테스트 하는 코드를 작성해서 테스트 한다.
- 코드로 코드를 테스트하므로 자동화는 100% 가능하다.
- 언제든지 반복적으로 실행시킬 수 있다. 실행 속도도 빠르다.
- 전체적인 부분을 테스트하는데는 제한적이다.
- 일반적으로 비중 70%

## pytest

```python
pip install pytest
```

- 파일 이름의 앞부분에 test_ 라고 되어 있는 파일들만 테스트 파일로 인식하고 실행한다.
- 함수 이름 앞부분에 test_ 라고 되어 있는 함수들만 실제 unit test 함수로 인식하고 실행한다.

```python
# test_multiply_by_two.py

def multiply_by_two(x):
	return x * 2

def test_multiply_by_two():
	assert multiply_by_two(4) == 7
```

- pytest 명령어 실행

- 파이참에서 따로 unit test 하는 방법이 있을 것 같은데 한번 리서치 필요할 것 같다.
    - 파이썬 3.x 부터는 unittests가 내장되어 있지만, 저자는 pytest 가 더 쉬워서 해당 모듈을 추천
    - 파이참에서 default test runner에서도 pytest 설정 가능
    - 우선 개별로 실행도 가능하고, 터미널에서 전체 실행해도 괜찮을 것 같긴하다. 편함

## 미니터 API unit test

- unit test는 일반적으로 함수를 테스트하는 코드이다.
- Flask 에서는 엔드포인트들 또한 함수로 구현되어 있다.
- 앞으로 구현할 unit test는 엔드포인트를 직접 테스트할 수 있다는 장점이 있다.
- 테스트 데이터베이스를 만들어야 된다.
    - 여기서 약간의 난관이 있음.
    - test 라는 유저를 만들어야 됨 (mysql 관리자)
    - DB 설정은 6장 참고

    ```sql
    create database test_db // 데이터베이스 생성
    create user 'test'@'%' identified by 'password'; //  사용자 생성
    grant all privileges on test_db.* to 'test'@'%'; //  특정 DB에 대한 모든 권한 부여.
    ```

- flask에서는 unit test에서 엔드포인트들을 테스트 할 수 있는 기능을 제공한다.

### ping 엔드포인트 유닛 테스트 하기

```python
import pytest
from app import create_app

@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config["TEST"] = True
    api = app.test_client()
    return api
```

- pytest.fixture 데코레이터 적용
    - pytest가 알아서 같은 이름의 함수의 리턴 값을 해당 인자에 넣어 준다.
- TEST 옵션을 true로 설정하여 flask가 에러가 났을 경우 http 요청 오류 부분은 핸들링하지 않게 한다.
- test_client 함수를 호출해서 테스트용 클라이언트를 생성한다. 테스트용 클라이언트를 사용하여 uri 기반으로 원하는 엔드포인트들 호출할 수 있게 된다.

```python
def test_ping(api):
    resp = api.get('/ping')
    assert b'pong' in resp.data
```

- app 인자는 pytest 커맨드를 실행할때 자동으로 넘겨준다 (pytest.fixture 설정한 함수 이름)
- test_client의 get 메소드를 통해서 get 요청을 /ping uri와 연결되어 있는 엔드포인트에 보낸다.
- b는 바이트로 변환한다는 의미이고 resp.data는 바이트 형태라 바이트로 변환해서 비교하는 것

### tweet 테스트 하기

- tweet를 생성하기 위해서는 먼저 사용자가 있어야 한다.
- 해당 사용자로 인증 절차를 거친 후 access token을 받은 후 tweet 엔드포인트를 호출해야 한다.

```python
def test_tweet(api):
    # 테스트 사용자 생성
    new_user = {
        'email': 'songew@gmail.com',
        'password': 'test password',
        'name': '송은우',
        'profile': 'test profile'
    }
    resp = api.post(
        '/sign-up',
        data=json.dumps(new_user),
        content_type='application/json'
    )
    assert resp.status_code == 200

    # Get the id of the new user
    resp_json = json.loads(resp.data.decode('utf-8'))
    new_user_id = resp_json['id']

    # 로그인
    resp = api.post(
        '/login',
        data=json.dumps({'email': 'songew@gmail.com', 'password': 'test password'}),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    # tweet
    resp = api.post(
        '/tweet',
        data=json.dumps({'tweet': 'Hello World!'}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # tweet 확인
    resp = api.get(f'/timeline/{new_user_id}')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 1,
                'tweet': 'Hello World!'
            }
        ]
    }
```

- tweet 엔드포인트를 호출하기 위해서는 사전에 다양한 엔드포인트 들을 호출해야 한다.
- pytest에서는 각 테스트 실행 전 바로 전, 그리고 바로 후에 실행할 코드를 지정해 놓아 자동으로 적용시킬 수 있게 해준다.
    - setup_function, teardown_function

```python
test_config = {
    'DB_URL': f"mysql+mysqlconnector://{test_db['user']}:{test_db['password']}@{test_db['host']}:{test_db['port']}/{test_db['database']}?charset=utf8",
    'JWT_SECRET_KEY': 'secret key'
}
```

- config 설정에 jwt_secret_key 추가

### unit test의 중요성

- unit test는 중요하다.
- test 코드를 구현하는 것이 실제 코드를 구현하는 것 만큼 혹은 그 이상 공수가 든다.
- 책의 저자는 개인적으로 같이 일하는 개발자들에게 항상 실제 개발하는데 총 10시간이 걸린다면 5시간은 실제 개발에 사용하고, 나머지 5시간은 unit test를 구현하는 데 사용하라고 한다.
- unit test는 개발자들의 방패이다.