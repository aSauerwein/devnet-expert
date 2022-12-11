## Flask Rest

### Exam Objectives
```
2.2	Build, manage, and operate a Python-based REST API with a web application framework (endpoints, HTTP request, and response)
```
### Version on CWS
```
(main) expert@expert-cws:~$ pip list | grep -i flask
Flask                        1.1.4
flask-restx                  0.5.1
types-Flask                  1.1.6
```

## starting with flask 1.1 tutorial
https://flask.palletsprojects.com/en/1.1.x/tutorial/
## now look at flask-restx
https://flask-restx.readthedocs.io/en/latest/


### Howto
* create api.py with blueprint

```python
flaskr/api.py

from flask import Blueprint
from flask_restx import Resource, Api

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
```
* install app in __init__.py

```python
flaskr/__init__.py

def create_app():
    app = ...
    # existing code omitted

    from . import api
    app.register_blueprint(api.bp)

    return app
```
* test http://127.0.0.1:5000/api/hello should return hello:world as json

* now something more advanced, create an API for the previos posts application
```python
api.py

@api.route("/post/<int:post_id>")

class Post(Resource):
    def get(self, post_id):
        db = get_db()
        post = db.execute(
            "SELECT id, title, body, created, author_id"
            " FROM post"
            " WHERE id = ?"
        ,(post_id, )).fetchone()
        return {
            "id": post["id"],
            "title": post["title"],
            "body": post["body"],
            "created": post["created"].timestamp(),
            "author_id": post["author_id"],
        }
    api.abort(404, f"Post id{post_id} doesn't exist.") 
```
  * in restx we can create CRUD applications by defining a class of "Resource". a HTTP GEST request is automatically forwarded to our "get()" function and therefore returning the selected post. http://127.0.0.1:8000/api/post/1 should return our first post, or returns `404` if the post does not exist

  * create post method to create new posts
