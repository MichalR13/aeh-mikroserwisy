from flask import Flask

app = Flask(__name__)
app.secret_key='aeh'

def create_app():

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')



    return app