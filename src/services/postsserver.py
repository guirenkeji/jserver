# from rest_api_demo.database import db
from src.models.post import *
from src.models import database


def delete_post(post_id):
    session = database.get_session()

    post = Post()
    post_id = Post.query.filter(Post.id == post_id).one()
    session.delete(post_id)
    session.commit()



