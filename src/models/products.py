from datetime import datetime

from src.database.intialize_database import db, ma



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.relationship('Stock', uselist=False, back_populates='product', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', back_populates='product', cascade='all, delete-orphan')


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), unique=True, nullable=False)
    product = db.relationship('Product', back_populates='stock')


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='transactions')
