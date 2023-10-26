from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import ProductInCart, Product
from . import db

cart = Blueprint('cart', __name__)


@cart.route('/cart', methods=['GET', 'POST'])
@login_required
def view_cart():
    cart_list = ProductInCart.query.filter_by(user=current_user)
    empty_cart_list = False

    product_list = Product.query

    if request.method == 'POST':
        delete_product_id = request.form.get('product_delete', '')
        if delete_product_id:
            product_to_delete = ProductInCart.query.filter_by(user=current_user, product_id=delete_product_id).first()
            db.session.delete(product_to_delete)
            flash('Product was removed from your cart', category='success')

        remove_one_product_id = request.form.get('product_remove_one', '')
        if remove_one_product_id:
            product_to_remove_one = ProductInCart.query.filter_by(user=current_user,
                                                                  product_id=remove_one_product_id).first()
            if product_to_remove_one.quantity == 1:
                db.session.delete(product_to_remove_one)
                flash('Product was removed from your cart', category='success')
            else:
                product_to_remove_one.quantity -= 1

        add_one_product_id = request.form.get('product_add_one', '')
        if add_one_product_id:
            product_to_add_one = ProductInCart.query.filter_by(user=current_user, product_id=add_one_product_id).first()
            product_to_add_one.quantity += 1

        db.session.commit()

    if not cart_list.count():
        empty_cart_list = True

    return render_template('cart.html', user=current_user, cart_list=cart_list, product_list=product_list,
                           is_empty=empty_cart_list)


@cart.route('/submit')
@login_required
# returns dictionary of current user cart with pairs: "Product id": "quantity"
def submit_cart():
    user_submit_list = ProductInCart.query.filter_by(user=current_user).all()
    user_order = {}
    for product in user_submit_list:
        user_order.update({product.product_id: product.quantity})
    return user_order
