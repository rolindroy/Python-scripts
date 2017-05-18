#!/usr/bin/env python
import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class PullRequest(Resource):
    def get(self, user_name):
        variable_manager = VariableManager()
        loader = DataLoader()

        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='./hosts')
        playbook_path = './playbook.yml'
	remoteuser = 'ubuntu_user' # Modify for default user
	
	if user_name:
	    remoteuser = user_name 

        if not os.path.exists(playbook_path):
            print '[INFO] The playbook does not exist'
            sys.exit()

        Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
        options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, remote_user=remoteuser, private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=4, check=False)

        variable_manager.extra_vars = {'target_host': request.remote_addr} # This can accomodate various other command line arguments.`

        passwords = {}

        pbexecutor = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)

        results = pbexecutor.run()

        return {'Result': results}

api.add_resource(PullRequest, '/<string:user_name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run(debug=True)
