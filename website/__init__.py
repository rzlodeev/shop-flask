from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from turbo_flask import Turbo
import threading, time

db = SQLAlchemy()
admin = Admin()
DB_NAME = 'database.db'
UPLOAD_FOLDER = '/website/static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def create_app():
    app = Flask(__name__)
    turbo = Turbo(app)

    app.config['SECRET_KEY'] = '420promlg'
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    admin.init_app(app)

    from .views import views
    from .auth import auth
    from .cart import cart, submit_cart

    from . import models

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(cart, url_prefix='/')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from website.formulas_generator import generate_formula

    @app.errorhandler(404)
    def not_found(e):
        return redirect(url_for('error404')), 404

    create_app.error404_thread_is_alive = False

    @app.route('/page_not_found/')
    def error404():
        def update_load():
            create_app.error404_thread_is_alive = True
            with app.app_context():
                while True:
                    time.sleep(3)
                    if turbo.can_push():
                        turbo.push(turbo.replace(render_template('error404.html'), "formula"))
                    else:
                        print('cant push')
                        render_template('error404.html')

        with app.app_context():
            if not create_app.error404_thread_is_alive:
                threading.Thread(target=update_load).start()
        return render_template('error404.html')

    @app.context_processor
    def inject_load():
        d = {'formula': generate_formula()}
        print(d)
        return d

    from .models import User, Product
    from .models import PostView, UserView

    admin.add_view(UserView(User, db.session))
    admin.add_view(PostView(Product, db.session))

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


