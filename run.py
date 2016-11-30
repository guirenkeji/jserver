# -*- coding: UTF-8 -*- 

from src import create_agent_app
from src.agentconfig import *

app = create_agent_app()

if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host= HOST,port=PORT)
