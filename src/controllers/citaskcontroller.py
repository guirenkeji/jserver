# -*- coding: UTF-8 -*- 
import os
from flask import Flask,request,url_for,jsonify
import jenkinsapi
from marathon import MarathonClient
import template
from jenkinsapi.jenkins import Jenkins 
import appinteration
import jconfig
from src.controllers import taskcicontroller
# import appclientcontroller
from src.services import citaskserver

import xml.etree.ElementTree
from src.controllers.common.restplus import api

ci_task = api.namespace('blog/posts', description='Operations related to blog posts')