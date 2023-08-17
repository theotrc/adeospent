from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import pandas as pd
import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY"),
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)




from .models_predictions import Base,engine
Base.metadata.create_all(bind=engine)

df = pd.read_csv("App/static/data/prdictions_0_ccdp.csv")

df_predictions = pd.read_csv("App/static/data/cost_predictions.csv")



db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app=Flask(__name__)
    app.config.from_object('config')
    
    # Create database connection object
    


    from .routes.account import account_blue
    from .routes.home import home_blue
    from .routes.auth import auth_blue
    from .routes.sentry_route import sentry_blue

    app.register_blueprint(sentry_blue)
    app.register_blueprint(account_blue)
    app.register_blueprint(home_blue)
    app.register_blueprint(auth_blue)


    return app

app = create_app()

with app.app_context():
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()






login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# logger = logging.getLogger("monlog")
# logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler('logs.log')
# fh.setLevel(logging.DEBUG)
# formatter =logging.Formatter("%(levelname)-8s %(asctime)s %(message)s")
# fh.setFormatter(formatter)
# logger.addHandler(fh)

from App import models
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return models.User.query.get(int(user_id))


@app.cli.command("init_db")
def init_db():
    models.init_db()

