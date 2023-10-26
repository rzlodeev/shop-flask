from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    product_in_cart = db.relationship("ProductInCart", backref='product')


class ProductInCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, db.ForeignKey('product.name'))
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates='products')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    products = db.relationship('ProductInCart', back_populates='user')

    def __str__(self):
        return self.first_name


class PostView(ModelView):
    can_delete = True
    form_columns = [Product.id, Product.name, Product.price]
    column_list = [Product.id, Product.name, Product.price]
    form_overrides = dict(pic=FileUploadField)


class UserView(ModelView):
    can_delete = False
    column_list = ['id', 'email', 'first_name']
