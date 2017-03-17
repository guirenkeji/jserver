from datetime import datetime
from src.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText


from sqlalchemy.orm import relationship
class Post(BaseModel):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    title = Column(NVARCHAR(80))
    body = Column(UnicodeText)
    pub_date = Column(DateTime)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category')

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title
    
