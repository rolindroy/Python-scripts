from flask import Flask, request
from flask_restful import Resource, Api
import git

app = Flask(__name__)
api = Api(app)

root_dir = "/webadmin/"

class PullRequest(Resource):
    def get(self, resource_id):
        dest_path = root_dir + resource_id
        repo = git.Repo(dest_path)
        repo_data = repo.remotes.origin
        sync = repo_data.pull();
        return {'Message': 'Done'}
api.add_resource(PullRequest, '/<string:resource_id>')

if __name__ == '__main__':
#    app.run(host='0.0.0.0')
    app.run(debug=True)

