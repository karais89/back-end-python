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