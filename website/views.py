import sqlalchemy.sql
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import ProductInCart, Product, User
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    products_list = Product.query
    with_product = request.args.get('with_product', '')
    product_id = request.form.get('product_add', '') # Id of product from form

    def add_product_to_cart(add_product_id=product_id):
        current_product = ProductInCart.query.filter_by(product_id=add_product_id, user_id=current_user.id).first()
        if current_product:
            current_product.quantity += 1
        else:
            new_product = ProductInCart(product_id=add_product_id, user_id=current_user.id, quantity=1)
            db.session.add(new_product)
        db.session.commit()
        flash('Product added to your cart!', category='success')
        return redirect(url_for('views.home'))

    def clear_products_with_null_id():
        products_in_cart_list = ProductInCart.query
        for product in products_in_cart_list:
            if not product.product_id:
                print(product)
                db.session.delete(product)
        db.session.commit()

    if request.method == 'POST':
        if current_user.is_authenticated:
            add_product_to_cart()
            return redirect(url_for('views.home'))
        else:
            # passes id of product that user tried to add to cart, so it will be added after login
            return redirect(url_for('auth.login', with_product=True, product_id=product_id))

    if with_product:
        product_id_anon = request.args.get('product_id',
                                           '')  # Id of product that unauthenticated user tried to add to cart
        print(product_id_anon)
        add_product_to_cart(product_id_anon) # Adds product to cart that unauthenticated user added earlier

    clear_products_with_null_id()
    return render_template('home.html', user=current_user, products_list=products_list)


@views.route('/delete-product', methods=['POST'])
def delete_product():
    product = json.loads(request.data)
    productId = product['productId']
    product = ProductInCart.query.get(productId)
    if product:
        if product.user_id == current_user.id:
            db.session.delete(product)
            db.session.commit()

    return jsonify({})
