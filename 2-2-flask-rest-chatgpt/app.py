from flask import Flask
from flask_restx import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, world!'}

parser = reqparse.RequestParser()
parser.add_argument('message', type=str)

@api.route('/echo')
class Echo(Resource):
    @api.expect(parser)
    def post(self):
        args = parser.parse_args()
        return {'message': args['message']}
    

if __name__ == '__main__':
    app.run(debug=True)