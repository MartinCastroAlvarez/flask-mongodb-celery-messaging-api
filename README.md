# Iguazu
Chat server using Flask, MongoDB, Redis and Celery.

![image-alt](./iguazu.jpg)

## References
- [Celery official documentation](https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html)
- [Class-based tasks with Celery](https://stackoverflow.com/questions/41788017/register-celery-class-based-task)
- [Redis with Flask](https://redis-py.readthedocs.io/en/latest/)
- [JWT with Flask](https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb)
- [Bcrypt with Python](https://blog.ruanbekker.com/blog/2018/07/04/salt-and-hash-example-using-python-with-bcrypt-on-alpine/)
- [Elasticsearch with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/6.1/docker.html)
- [Flask REST API](https://flask-restful.readthedocs.io/en/latest/)
- [Redis connector with Flask](https://pypi.org/project/flask-redis/)
- [Embedded documents with Mongo Engine](https://stackoverflow.com/questions/27846322)
- [DockerHub Celery](https://hub.docker.com/_/celery)
- [DockerHub MongoDB](https://hub.docker.com/_/mongo)
- [DockerHub Redis](https://hub.docker.com/_/redis)
- [Running MongoDB with Docker](https://www.thepolyglotdeveloper.com/2019/01/getting-started-mongodb-docker-container-deployment/)
- [Setting MongoDB credentials](https://forums.docker.com/t/create-new-database-in-mongodb-with-docker-compose/58306/2)
- [Requiring password in Redis with Docker](https://nickjanetakis.com/blog/docker-tip-27-setting-a-password-on-redis-without-a-custom-config)
- [Flask, Celery and Redis integration](https://github.com/mattkohl/docker-flask-celery-redis)
- [Mongo Engine with Flask](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/MONGODB_SETTINGS)
- [Indexing with Mongo Engine](https://scalegrid.io/blog/handling-index-creation-with-mongoengine-in-python/)
- [Pagination with MongoDB](https://www.codementor.io/arpitbhayani/fast-and-efficient-pagination-in-mongodb-9095flbqr)
- [MongoEngine Documentation](https://buildmedia.readthedocs.org/media/pdf/mongoengine-odm/latest/mongoengine-odm.pdf)
- [Authenticating to MongoDB with Docker](https://stackoverflow.com/questions/34559557)
- [MongoDB projection with MongoEngine](https://stackoverflow.com/questions/27021095/mongoengine-limiting-number-of-responses-from-dbref)

## API
| Method | Endpoint         | Action                |
| ------ | ---------------- | --------------------- |
| GET    | /check           | Health Check          |
| POST   | /check           | Health Check          |
| GET    | /users           | List Users            |
| POST   | /users           | Create User           |
| POST   | /login           | Do Login              |
| GET    | /messages        | List User Messages    |
| POST   | /messages        | Send a Message        |
| GET    | /notifications   | List Notifications    |

## Instructions

#### Installation
Install all the dependencies:
```bash
virtualenv -p python3 .env
source .env/bin/activate
pip install -r requirements.txt
```
Build the local Docker images:

#### Setup
Run all the services:
```bash
sudo docker-compose up \
    --detach \
    --build \
    --renew-anon-volumes
```

#### Health Checks
Validate MongoDB is running:
```bash
sudo docker logs iguazu_nosql-server_1
```
You should expect to see the following:
```bash
[...]
[...] waiting for connections on port 27017
[...]
```
Validate Redis is up and running:
```bash
sudo docker logs iguazu_cache-server_1
```
You should expect to see the following:
```bash
[...]
[...] Running mode=standalone, port=6379.
[...]
```
Validate the web service is up and running:
```bash
sudo docker logs iguazu_web-server_1
```
You should expect to see the following:
```bash
[...]
[...] INFO success: uwsgi entered RUNNING state
[...]
```
Validate that the app is up and running.
```bash
curl -i -d '' -XPOST http://localhost:8080/check
```
You should expect to see the following:
```bash
{
    "health": "ok"
}
```
Validate that Celery is up and running:
```bash
sudo docker logs iguazu_worker-1_1 --follow --tail 30
```
You should expect to see the following:
```bash
[...]
[...] mingle: searching for neighbors
[...] mingle: all alone
[...] celery@b0d4e3fc35bb ready.
[...]
```

#### Development
You may perform changes to the Flask app and then run:
```bash
sudo docker restart iguazu_web-server_1 iguazu_worker-1_1
```
You may tail the web server logs using this command:
```bash
sudo docker logs iguazu_web-server_1 --follow --tail 100
sudo docker logs iguazu_web-worker_1 --follow --tail 100
```

#### Unit Tests
Execute this command to run Unit Tests:
```bash
export PYTHONPATH="$PYTHONPATH:$(pwd)"
nosetests \
    --cover-min-percentage 20 \
    --logging-level=DEBUG \
    -a "unit_test=true" \
    --with-coverage \
    --cover-erase \
    --detailed-errors \
    --cover-package ./app \
    ./tests
```
You should expect something like this:
```bash
Name                               Stmts   Miss  Cover
------------------------------------------------------
app/__init__.py                       46      9    80%
app/api/__init__.py                   12      0   100%
app/api/auth.py                       19      0   100%
app/api/health.py                     15      0   100%
app/api/messages.py                   27      3    89%
app/api/notifications.py              17      0   100%
app/api/users.py                      27      3    89%
app/config.py                         34      0   100%
app/controllers/__init__.py           28     12    57%
app/controllers/health.py             31     16    48%
app/controllers/messages.py           65     38    42%
app/controllers/notifications.py      44     23    48%
app/controllers/users.py              68     44    35%
app/exceptions/__init__.py            20      0   100%
app/exceptions/auth.py                13      0   100%
app/exceptions/form.py                61      0   100%
app/exceptions/health.py               8      0   100%
app/exceptions/not_found.py            7      0   100%
app/main.py                            4      4     0%
app/models/__init__.py                 2      0   100%
app/models/message.py                 41      1    98%
app/models/notification.py            17      2    88%
app/models/user.py                    19      1    95%
app/security/__init__.py               0      0   100%
app/security/encryption.py            21      9    57%
app/security/login.py                 17      6    65%
app/validations/__init__.py            6      2    67%
app/validations/messages.py           61     31    49%
app/validations/notifications.py      28     13    54%
app/validations/pagination.py         11      5    55%
app/validations/users.py              27     12    56%
app/worker/__init__.py                 3      0   100%
app/worker/main.py                     3      3     0%
app/worker/messages.py                18      8    56%
app/worker/tasks.py                    5      0   100%
app/worker/users.py                   18      8    56%
------------------------------------------------------
TOTAL                                843    253    70%
----------------------------------------------------------------------
Ran 12 tests in 0.138s

OK
```

#### Tear Down
You can stop the services using this command:
```bash
sudo docker-compose down
```

## Deployment
This section is out of scope.

## Regression Tests

##### 1st test: Basic Health Check
Validate that the app is up and running.
```bash
curl -i -d '' -XPOST http://localhost:8080/check
```
Expect this response:
```bash
{
    "health": "ok"
}
```
In case of errors, you would get something like this:
```bash
{
    "code": 503,
    "subcode": 5002,
    "error": "App Not Healthy"
}
```

##### 2nd test: Unauthorized Access
Send an unauthorized request:
```bash
curl -i -d '{
    "sender": 0, "recipient": 1,
    "content": {"type": "video", 
        "source": "youtube",
        "url", "https://www.youtube.com/watch?v=wbZZy9yogg8"}}' \
    -H "Content-Type: application/json" \
    -XPOST http://localhost:8080/messages
```
Expect this response:
```bash
{
  "msg": "Missing Authorization Header"
}
```

##### 3nd test: Unauthorized Access
Send an unauthorized request:
```bash
curl -i -d '{
    "sender": 0, "recipient": 1,
    "content": {"type": "video", 
        "source": "youtube",
        "url", "https://www.youtube.com/watch?v=wbZZy9yogg8"}}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer lorem-ipsum" \
    -XPOST http://localhost:8080/messages
```
Expect this response:
```bash
{
  "msg": "Not enough segments"
}
```

##### 4th test: Login
Do login:
```bash
curl -i -d '{"username": "daikiri", "password": "tekila"}' \
    -H "Content-Type: application/json" \
    -XPOST http://localhost:8080/login
```
Expect this response:
```bash
{
    "id": "71c240bd63284b9ca5e69b5b7a6618e1",
    "timestamp": "2019-08-11 04:47:02.602000",
    "username": "daikiri",
    "password": "...',
    "token": "...",
    "refresh_token": "..."
}
```
You may then save the token to a variable this way:
```bash
TOKEN=$(curl -d '{"username": "daikiri", "password": "tekila"}' \ 
    -H "Content-Type: application/json" \
    -XPOST http://localhost:8080/login | jq -r '.token')
echo "Token: $TOKEN"
```

##### 5th test: User creation
Create a new user:
```bash
NEW_USERNAME="gin.$(date +%s)"
echo "New User: $NEW_USERNAME"
curl -i -d '{"username": "'$NEW_USERNAME'", "password": "tonic"}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XPOST http://localhost:8080/users
```
Expect this response:
```bash
{
    "job_id": "fd903510-3833-4668-bcf0-336e2cb533d4"
}
```
You may send the request in this test twice to get a conflict error.

##### 6th test: Notifications
List your notifications:
```bash
curl -i -d '{"limit": 2}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XGET http://localhost:8080/notifications
```
Expect this response:
```bash
{
    "notifications": [
        {
            "message": {
                "id": "5d506506e2ef969b83b36fdd",
                "timestamp": "2019-08-11 18:57:10.149127",
                "username": "gin.1565549830",
                "password": "..."
            },
            "is_error": false,
            "code": 10099,
            "title": "User Creation",
            "timestamp": "2019-08-11 18:57:10.379000"
        },
        {
            "message": {
                "code": 400,
                "subcode": 4004,
                "error": "Username Already Taken"
            },
            "is_error": true,
            "code": 10099,
            "title": "User Creation",
            "timestamp": "2019-08-11 18:57:20.029000"
        }
    ]
}
```

##### 7th test: List existing users
List users:
```bash
curl -i -d '{"limit": 2}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XGET http://localhost:8080/users
```
Expect this response:
```bash
{
    "users": [
        {
            "id": "5d5064ea5d65dc6eddb0d161",
            "timestamp": "2019-08-11 18:56:41.969000",
            "username": "daikiri",
            "password": ..."
        },
        {
            "id": "5d5064fdcb3bd9f18db36fdd",
            "timestamp": "2019-08-11 18:57:01.744000",
            "username": "gin.1565549821",
            "password": "..."
        }
    ]
}
```
You may then store the IDs in env variables:
```bash
USERS=$(curl -d '{"limit": 3}' -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" -XGET http://localhost:8080/users)
USER1=$(echo $USERS | jq -r '.users[0].id')
USER2=$(echo $USERS | jq -r '.users[1].id')
echo "User1: $USER1"
echo "User2: $USER2"
```

##### 8th test: Sending image messages
Send a new image message:
```bash
curl -i -d '{
    "sender_id": "'$USER1'",
    "recipient_id": "'$USER2'",
    "content": {
        "type": "image", 
        "height": 100,
        "width": 100,
        "url": "https://via.placeholder.com/150"
    }}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XPOST http://localhost:8080/messages
```
Expect this response:
```bash
{
    "job_id": "68e5369d-dcd1-4ea2-9f3d-56f2825771b1"
}
```

##### 9th test: Sending video messages
Send a new video message:
```bash
curl -i -d '{
    "sender_id": "'$USER1'",
    "recipient_id": "'$USER2'",
    "content": {
        "type": "video", 
        "source": "youtube",
        "url": "https://www.youtube.com/watch?v=wbZZy9yogg8"
    }}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XPOST http://localhost:8080/messages
```
Expect this response:
```bash
{
    "job_id": "68e5369d-dcd1-4ea2-9f3d-56f2825771b1"
}
```

##### 10th test: Sending text messages
Send a new text message:
```bash
curl -i -d '{
    "sender_id": "'$USER1'",
    "recipient_id": "'$USER2'",
    "content": {
        "type": "text",
        "text": "Lorem Ipsum Dolor Sit Amet"
    }}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XPOST http://localhost:8080/messages
```
Expect this response:
```bash
{
    "job_id": "68e5369d-dcd1-4ea2-9f3d-56f2825771b1"
}
```

##### 11th test: Notifications
List your notifications:
```bash
curl -i -d '{"limit": 3}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XGET http://localhost:8080/notifications
```
Expect this response:
```bash
{
    "notifications": [
        {
            "message": {
                "id": "5d5066fac18c26c62b30ae5a",
                "sender": "5d5064ea5d65dc6eddb0d161",
                "recipient": "5d5064fdcb3bd9f18db36fdd",
                "timestamp": "2019-08-11 19:05:30.012855",
                "content": {
                    "type": "image",
                    "url": "https://via.placeholder.com/150",
                    "width": 100,
                    "height": 100
                }
            },
            "is_error": false,
            "code": 10095,
            "title": "New Message",
            "timestamp": "2019-08-11 19:05:30.035000"
        },
        {
            "message": {
                "id": "5d5067093105de528230ae5a",
                "sender": "5d5064ea5d65dc6eddb0d161",
                "recipient": "5d5064fdcb3bd9f18db36fdd",
                "timestamp": "2019-08-11 19:05:45.605418",
                "content": {
                    "type": "video",
                    "url": "https://www.youtube.com/watch?v=wbZZy9yogg8",
                    "source": "youtube"
                }
            },
            "is_error": false,
            "code": 10095,
            "title": "New Message",
            "timestamp": "2019-08-11 19:05:45.620000"
        },
        {
            "message": {
                "id": "5d50671d86bf3b84f330ae5a",
                "sender": "5d5064ea5d65dc6eddb0d161",
                "recipient": "5d5064fdcb3bd9f18db36fdd",
                "timestamp": "2019-08-11 19:06:05.616069",
                "content": {
                    "type": "text",
                    "text": "Lorem Ipsum Dolor Sit Amet"
                }
            },
            "is_error": false,
            "code": 10095,
            "title": "New Message",
            "timestamp": "2019-08-11 19:06:05.637000"
        }
    ]
}
```

##### 12nd test: Sending text messages with errors
Send a new text message:
```bash
curl -i -d '{
    "sender_id": "'$USER1'",
    "recipient_id": "'$USER2'",
    "content": {
        "type": "text"
    }}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XPOST http://localhost:8080/messages
```
Expect this response:
```bash
{
    "job_id": "68e5369d-dcd1-4ea2-9f3d-56f2825771b1"
}
```

##### 13rd test: Notifications
List your notifications:
```bash
curl -i -d '{"limit": 1}' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XGET http://localhost:8080/notifications
```
Expect this response:
```bash
{
    "notifications": [
        {
            "message": {
                "code": 400,
                "subcode": 4010,
                "error": "Invalid Text"
            },
            "is_error": true,
            "code": 10095,
            "title": "New Message",
            "timestamp": "2019-08-11 19:08:48.781000"
        }
    ]
}
```

##### 14th test: Listing Messages
List messages:
```bash
curl -i -d '{
        "sender_id": "'$USER1'",
        "recipient_id": "'$USER2'",
        "limit": 3
    }' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XGET http://localhost:8080/messages
```
Expect this response:
```bash
{
    "messages": [
        {
            "id": "5d5066fac18c26c62b30ae5a",
            "sender": "5d5064ea5d65dc6eddb0d161",
            "recipient": "5d5064fdcb3bd9f18db36fdd",
            "timestamp": "2019-08-11 19:05:30.012000",
            "content": {
                "type": "image",
                "url": "https://via.placeholder.com/150",
                "width": 100,
                "height": 100
            }
        },
        {
            "id": "5d5067093105de528230ae5a",
            "sender": "5d5064ea5d65dc6eddb0d161",
            "recipient": "5d5064fdcb3bd9f18db36fdd",
            "timestamp": "2019-08-11 19:05:45.605000",
            "content": {
                "type": "video",
                "url": "https://www.youtube.com/watch?v=wbZZy9yogg8",
                "source": "youtube"
            }
        },
        {
            "id": "5d50671d86bf3b84f330ae5a",
            "sender": "5d5064ea5d65dc6eddb0d161",
            "recipient": "5d5064fdcb3bd9f18db36fdd",
            "timestamp": "2019-08-11 19:06:05.616000",
            "content": {
                "type": "text",
                "text": "Lorem Ipsum Dolor Sit Amet"
            }
        }
    ]
}
```

```bash
TOKEN=$(curl -d '{"username": "daikiri", "password": "tekila"}' \ 
    -H "Content-Type: application/json" \
    -XPOST http://localhost:8080/login | jq -r '.token')
```
##### 15th test: Messages pagination
List messages and record the last ID:
```bash
SEARCH=$(curl -d '{
        "sender_id": "'$USER1'",
        "recipient_id": "'$USER2'",
        "limit": 2
    }' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XGET http://localhost:8080/messages)
LAST_MESSAGE_ID=$(echo $SEARCH | jq -r '.messages[-1].id')
echo $SEARCH | jq -r '.messages[] | "\(.id) \(.timestamp)"'
```
Now recursively fetch more messages:
```bash
SEARCH=$(curl -d '{
        "sender_id": "'$USER1'",
        "recipient_id": "'$USER2'",
        "start": "'$LAST_MESSAGE_ID'",
        "limit": 2
    }' \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -XGET http://localhost:8080/messages)
LAST_MESSAGE_ID=$(echo $SEARCH | jq -r '.messages[-1].id')
echo $SEARCH | jq -r '.messages[] | "\(.id) \(.timestamp)"'
```
You should expect to see a reverse time series in your CLI:
```bash
5d50964307579d45c867dafd 2019-08-11 22:27:15.245000
5d509642deab8b5e9e67dafb 2019-08-11 22:27:14.147000
5d50964201405eb25b67dafd 2019-08-11 22:27:14.693000
5d5096405504dc87a467dafd 2019-08-11 22:27:12.878000
5d50964007579d45c867dafc 2019-08-11 22:27:12.518000
5d50964001405eb25b67dafc 2019-08-11 22:27:12.043000
```
