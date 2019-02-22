from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Boolean
from sqlalchemy.orm import backref, relationship
from appoteka import db
from appoteka.models.cart_item import Cart_Item
from appoteka.models.user import User
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    cart_item_id = Column(Integer, ForeignKey('cart_item.id'))
    cart_item = relationship(
        Cart_Item,
        backref=backref('cart_item',
                        uselist=True,
                        cascade='delete,all'))
   
    name = db.Column(db.String(20),  nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    address = db.Column(db.String(20),nullable=False)
    country = db.Column(db.String(120), nullable=False)
    zip_code = db.Column(db.String(7),  nullable=False)
    payment_method = db.Column(db.String(120),  nullable=False)
    name_on_card = db.Column(db.String(120),  nullable=False)
    credit_card_number = db.Column(db.String(20),  nullable=False)
    expiration = db.Column(db.String(120),  nullable=False)
    cvv = db.Column(db.String(20),  nullable=False)
    
    make_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Order('{self.product_id}','{self.user_id}','{self.quantity}','{self.make_date}')"



