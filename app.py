
from config import Config
from extensions import db
from flask_migrate import Migrate
# import mysql.connector
# from routes import main
# from models import models
from models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from routes import app
import sqlite3

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost/speed-interne'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
db.init_app(app)
migrate = Migrate(app, db)
def create_app():
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'base.db'
    # register_resources(app)
    register_extensions(app)  

    login_manager = LoginManager()
    login_manager.login_view = 'index'
    login_manager.init_app(app)
 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)


# def register_resources(app):
#     app.register_blueprint(main)
    

def create_tables():

    with app.app_context():
        # Create all tables
        db.create_all()

if __name__ == '__main__':
    create_tables()
    # app = create_app()
    app.run(debug=True)
	