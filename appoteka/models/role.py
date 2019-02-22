from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship
from appoteka import db

class Role(db.Model):
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"Role('{self.name}')"