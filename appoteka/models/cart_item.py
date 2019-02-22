from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Boolean
from sqlalchemy.orm import backref, relationship
from appoteka import db
from appoteka.models.product import Product
from appoteka.models.user import User
from datetime import datetime


class Cart_Item(db.Model):
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship(
        Product,
        backref=backref('product',
                        uselist=True,
                        cascade='delete,all'))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(
        User,
        backref=backref('user',
                        uselist=True,
                        cascade='delete,all'))
    is_active = Column(Boolean, default = True)
    quantity = db.Column(db.Integer,nullable=True , default = 1)
    make_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Cart_Item('{self.product_id}','{self.user_id}','{self.quantity}','{self.make_date}')"



