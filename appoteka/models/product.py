from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship
from appoteka import db
from appoteka.models.category import Category

class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    category = relationship(
        Category,
        backref=backref('category',
                        uselist=True,
                        cascade='delete,all'))
    description = db.Column(db.String(120))
    price = db.Column(db.Integer,nullable=True)
    image_file = db.Column(db.String(20),nullable=False, default='default_product.jpg')

    def __repr__(self):
        return f"Product('{self.name}','{self.description}','{self.price}','{self.image_file}')"

