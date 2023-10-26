from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from werkzeug.utils import secure_filename

db = SQLAlchemy()
admin = Admin()
DB_NAME = 'database.db'
UPLOAD_FOLDER = '/website/static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def create_app():
    app = Flask(__name__)
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

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    from .models import User, Product
    from .models import PostView, UserView

    admin.add_view(UserView(User, db.session))
    admin.add_view(PostView(Product, db.session))

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


