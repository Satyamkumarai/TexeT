from flask import Flask
from texet.extensions import mongo
from .settings import SECRET_KEY,admin_access_key,dbname,username,password
from .main.routes import bp
def create_app(testing:bool = True):
    #init app
    app = Flask(__name__)
    #config app
    # app.config['MONGO_URI'] = f"mongodb+srv://{username}:{password}@cluster0.70rhn.mongodb.net/{dbname}?retryWrites=true&w=majority"
    # app.config['SECRET_KEY'] = SECRET_KEY
    # app.config['ADMIN_ACCESS_KEY'] = admin_access_key
    #config Extensions
    # mongo.init_app(app)
    app.config['MONGO_URI'] = f"mongodb+srv://{username}:{password}@cluster0.70rhn.mongodb.net/{dbname}?retryWrites=true&w=majority"
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['ADMIN_ACCESS_KEY'] = admin_access_key

    mongo.init_app(app)
    app.register_blueprint(bp)
    return app    