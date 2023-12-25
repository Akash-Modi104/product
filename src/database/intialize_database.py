from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_table_not_exits(app):
  db.init_app(app)
  ma.init_app(app)
  from src.models import products
  # with app.app_context():
  #   db.create_all()
