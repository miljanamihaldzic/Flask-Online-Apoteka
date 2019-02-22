from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship
from appoteka import db



class Category(db.Model):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    description = Column(String)
    name = Column(String)
    image_file = db.Column(db.String(100), nullable=False, default='category_default.png')
