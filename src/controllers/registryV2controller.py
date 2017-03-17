# -*- coding: UTF-8 -*-
from flask import Module,render_template,jsonify, redirect, request, session, g
from src.agentconfig import *
import os
import logging
import json
from src.services.component import server
import httplib
import re
import operator
logging.basicConfig(level=logging.DEBUG)
registryV2Server = Module(__name__)
@registryV2Server.route('/')
def hello_registryV2Server():
    print dir(request)
    return 'Hello registryV2Server!'
@registryV2Server.route('/nexus/1.0/package/delete',methods=['DELETE'])
def imagesList():
    return 'Hello nexusServer_info!'