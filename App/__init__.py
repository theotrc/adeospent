from flask import Flask
import pandas as pd
from flask_sqlalchemy import SQLAlchemy


df = pd.read_csv("App/static/data/dtpbilling_2023.csv")

df_predictions = pd.read_csv("App/static/data/cost_predictions.csv")


def create_app():
    app = Flask(__name__)
    
    app.config.from_object('config')

    from .routes.home import home_blue

    app.register_blueprint(home_blue)

    return app


app = create_app()

