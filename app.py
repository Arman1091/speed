from flask import Flask, render_template
from config import Config
from extensions import db
from flask_migrate import Migrate
from routes import main
from models import models
from models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_resources(app)
    register_extensions(app)  

    login_manager = LoginManager()
    login_manager.login_view = 'main.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def register_resources(app):
    app.register_blueprint(main)
    


if __name__ == '__main__':
    app = create_app()
   
    app.run(debug = True)
	