
from config import Config
from extensions import db
from flask_migrate import Migrate
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
def create_tables():

    with app.app_context():
        # Create all tables
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
	