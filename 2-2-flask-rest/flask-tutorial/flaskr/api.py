from flask import Blueprint
from flask_restx import Resource, Api, fields
from flaskr.db import get_db

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)


@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


post_model = api.model(
    "Model",
    {
        "id": fields.String,
        "title": fields.String,
        "body": fields.String,
        "created": fields.DateTime(dt_format="rfc822"),
        "author_id": fields.Integer,
    },
)


@api.route(
    "/post/",
)
class Posts(Resource):
    @api.marshal_with(post_model, envelope="resource")
    def get(self, **kwargs):
        # get list of posts
        db = get_db()
        posts = db.execute(
            "SELECT id, title, body, created, author_id"
            " FROM post"
            " ORDER BY created DESC"
        ).fetchall()

        return posts

    def post(self):
        # create post
        if api.payload is not None:
            db = get_db()
            post = db.execute(
                "INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)",
                (api.payload["title"], api.payload["body"], 1),
            )
            db.commit()
            return None, 201

        api.abort(404, "no payload specified")
        pass


@api.route("/post/<int:post_id>")
class Post(Resource):
    @api.marshal_with(post_model, envelope="resource")
    def get(self, post_id):
        db = get_db()
        post = db.execute(
            "SELECT id, title, body, created, author_id" " FROM post" " WHERE id = ?",
            (post_id,),
        ).fetchone()
        if post != None:
            return post
        api.abort(404, f"Post id {post_id} doesn't exist.")

    def put(self, post_id):
        db = get_db()
        post = db.execute(
            "SELECT id, title, body, created, author_id" " FROM post" " WHERE id = ?",
            (post_id,),
        ).fetchone()
        if post != None:
            db.execute(
                "UPDATE post SET title = ?, body = ?" " WHERE id = ?",
                (api.payload["title"], api.payload["body"], post_id),
            )
            db.commit()
            return None, 200
        api.abort(404, f"Post id {post_id} doesn't exist.")
