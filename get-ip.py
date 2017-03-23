
from flask import Flask, request
from flask_restful import Resource, Api
import git

app = Flask(__name__)
api = Api(app)

class PullRequest(Resource):
    def get(self):
        return {'ip': request.remote_addr}
api.add_resource(PullRequest, '/')

if __name__ == '__main__':
#    app.run(host='0.0.0.0')
    app.run(debug=True)
