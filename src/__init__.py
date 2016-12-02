# -*- coding: UTF-8 -*- 
from flask import Flask
from src.controllers import *
def create_agent_app ():
    app = Flask(__name__)
    app.jinja_env.variable_start_string = '(('
    app.jinja_env.variable_end_string = '))'
    app.config.from_pyfile('agentconfig.py')
#     app.register_module(svn_repo_info)
    app.register_module(zentao)
    app.register_module(nexusServer)
    app.register_module(nexus)
    return app