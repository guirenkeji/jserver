import logging

from flask import request
from flask_restplus import Resource
from flask import Module,render_template,jsonify, redirect, request, session, g
from src.services.postsserver import delete_post
# from rest_api_demo.api.blog.serializers import blog_post, page_of_blog_posts
# from rest_api_demo.api.blog.parsers import pagination_arguments
from src.controllers.common.restplus import api
from src.models.post import *

log = logging.getLogger(__name__)


ns = api.namespace('blog/posts', description='Operations related to blog posts')



@ns.route('/<int:id>')
@api.response(404, 'Post not found.')
class PostItem(Resource):


    @api.response(204, 'Post successfully deleted.')
    def delete(self, id):
        """
        Deletes blog post.
        """
        delete_post(id)
        return None, 204



