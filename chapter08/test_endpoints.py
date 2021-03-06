import pytest
import config
import json
import bcrypt

from sqlalchemy import create_engine, text
from app import create_app

database = create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow=0)


@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config["TEST"] = True
    api = app.test_client()
    return api


# pytest 에서 자동으로 실행된다 - 테스트가 실행 될때
def setup_function():
    # Create a test user
    hashed_password = bcrypt.hashpw(
        b"test password",
        bcrypt.gensalt()
    )
    new_user = [
        {
            'id': 1,
            'name': '송은우',
            'email': 'songew@gmail.com',
            'profile': 'test profile',
            'hashed_password': hashed_password
        },
        {
            'id': 2,
            'name': '김철수',
            'email': 'tet@gmail.com',
            'profile': 'test profile',
            'hashed_password': hashed_password
        }
    ]
    database.execute(text("""
        INSERT INTO users (
            id,
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :id,
            :name,
            :email,
            :profile,
            :hashed_password
        )
    """), new_user)

    # user 2 트윗 미리 생성
    database.execute(text("""
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUES (
            2,
            "Hello World!"
        )
    """))


# pytest 에서 자동으로 실행된다 - 테스트가 종료 될때
def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))  # 외부키가 걸여 있으면 데이터를 삭제할 수 없다. 임의로 비활성화 (테스트 용도)
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def test_ping(api):
    resp = api.get('/ping')
    assert b'pong' in resp.data


def test_login(api):
    resp = api.post(
        '/login',
        data=json.dumps({
            'email': 'songew@gmail.com',
            'password': 'test password'
        }),
        content_type='application/json'
    )
    assert b"access_token" in resp.data


def test_unauthorized(api):
    # access token이 없이는 401 응답을 리턴하는지 확인
    resp = api.post(
        '/tweet',
        data=json.dumps({'tweet': 'Hello World!'}),
        content_type='application/json',
    )
    assert resp.status_code == 401

    resp = api.post(
        '/follow',
        data=json.dumps({'follow': 2}),
        content_type='application/json',
    )
    assert resp.status_code == 401

    resp = api.post(
        '/unfollow',
        data=json.dumps({'unfollow': 2}),
        content_type='application/json',
    )
    assert resp.status_code == 401


def test_tweet(api):
    # 로그인
    resp = api.post(
        '/login',
        data=json.dumps({
            'email': 'songew@gmail.com',
            'password': 'test password'
        }),
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
    resp = api.get(f'/timeline/1')
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


def test_follow(api):
    # 로그인
    resp = api.post(
        '/login',
        data=json.dumps({
            'email': 'songew@gmail.com',
            'password': 'test password'
        }),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    # 먼저 사용자 1의 tweet 확인해서 tweet 리스트가 비어 있는 것을 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': []
    }

    # follow 사용자 아이디 = 2
    resp = api.post(
        '/follow',
        data=json.dumps({'follow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # 이제 사용자 1의 tweet 확인해서 사용자 2의 tweet이 리턴되는 것을 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 2,
                'tweet': 'Hello World!'
            }
        ]
    }


def test_unfollow(api):
    # 로그인
    resp = api.post(
        '/login',
        data=json.dumps({
            'email': 'songew@gmail.com',
            'password': 'test password'
        }),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    # follow 사용자 아이디 = 2
    resp = api.post(
        '/follow',
        data=json.dumps({'follow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # 이제 사용자 1의 tweet 확인해서 사용자 2의 tweet이 리턴되는 것을 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 2,
                'tweet': 'Hello World!'
            }
        ]
    }

    # unfollow 사용자 아이디 = 2
    resp = api.post(
        '/unfollow',
        data=json.dumps({'unfollow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # 이제 사용자 1의 tweet 확인해서 유저 2의 tweet이 더 이상 리턴되지 않는 것을 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': []
    }
