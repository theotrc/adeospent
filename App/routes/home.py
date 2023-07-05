from flask import render_template,Blueprint, request
from App import df, df_predictions, db
from flask_login import login_required,current_user
from ..models import User, Product
from ..models_predictions import Prediction, engine, product_spend
from sqlalchemy.orm import Session
from datetime import datetime


home_blue = Blueprint("home", __name__, static_folder="../static", template_folder="../templates")


@home_blue.route("/")
@login_required
def home():

    user = User.query.filter_by(id=current_user.id).first()
    ids = [i.tangram_id for i in  user.product]
    
    id = ids[0]
    temp = df.loc[df.unique_id == str(id)].sort_values("ds")
    x = temp["ds"].values.tolist()
    y = temp["y"].fillna(0).values.tolist()

    liney = []
    linedata = temp.loc[temp.ds > "2022-12-01"][["y","ds","forecast_2023"]].dropna()
    liney=linedata.y.cumsum().values.tolist()
    linex=linedata.ds.values.tolist()
    plafond= linedata.forecast_2023.values.tolist()

    with Session(engine) as session:

        data = {}
        for spend in session.query(product_spend).filter_by(title=str(id)).all():

            temp_date = datetime.strptime(str(spend.period), "%Y-%m-%d")
            str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            data[str_date] = spend.price


        data_pred = dict.fromkeys(data, 0)
        for predict in session.query(Prediction).filter_by(product=str(id)).all():

            temp_date = datetime.strptime(str(predict.date), "%Y-%m-%d")
            str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            data_pred[str_date] = predict.Prediction
    
    return render_template("chart.html", x = list(data.keys()), y=list(data.values()),ids=ids, liney=liney,linex=linex,plafond=plafond, id=id, x_pred=list(data_pred.keys()), y_pred = list(data_pred.values()))






@home_blue.route("/ap", methods=['POST'])
def a_post():
    id = request.form.get("id")
    return str(id)


# @home_blue.route("/", methods=["POST"])
# @login_required
# def graph_page():
#     id = request.form.get("id")
    
#     temp = df_predictions.loc[df_predictions.unique_id == str(id)].sort_values("ds")
#     predictions = temp["prediction"].values.tolist()

#     temp = df.loc[df.unique_id == str(id)].sort_values("ds")
#     x = temp["ds"].values.tolist()
#     y = temp["y"].fillna(0).values.tolist()
    
#     pred = [0 for i in range(len(y))]
#     reverse_predictions = predictions[::-1]
#     for i in range(len(predictions)):
#         pred[i]= reverse_predictions[i]
#     pred = pred[::-1]
#     pred = temp["predictions"].values.tolist()
    
#     user = User.query.filter_by(id=current_user.id).first()
#     ids = [i.tangram_id for i in  user.product]

#     liney = []
#     n = 0
#     linedata = temp.loc[temp.ds > "2022-12-01"].dropna()
#     liney=linedata.y.cumsum().values.tolist()
#     linex=linedata.ds.values.tolist()
#     plafond= linedata.forecast_2023.str.replace("$","").str.replace(",","").astype("float64").values.tolist()
    
    
#     return render_template("chart.html", x = x, y=y,ids=ids, predictions=pred, liney=liney,linex=linex,plafond=plafond, id=id)


@home_blue.route("/", methods=["POST"])
@login_required
def graph_page():

    # get user products
    user = User.query.filter_by(id=current_user.id).first()
    ids = [i.tangram_id for i in  user.product]
    

    # get selected product id and loc it in df
    id = request.form.get("id")
    temp = df.loc[df.unique_id == str(id)].sort_values("ds")
    # x (dates) and y (spent and predictions) to list

    with Session(engine) as session:

        data = {}
        for spend in session.query(product_spend).filter_by(title=str(id)).all():

            temp_date = datetime.strptime(str(spend.period), "%Y-%m-%d")
            str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            data[str_date] = spend.price


        data_pred = dict.fromkeys(data, 0)
        for predict in session.query(Prediction).filter_by(product=str(id)).all():

            temp_date = datetime.strptime(str(predict.date), "%Y-%m-%d")
            str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            data_pred[str_date] = predict.Prediction
            




    
    
    # cunsum of spent in 2023 for linechart
    liney = []
    linedata = temp.loc[temp.ds > "2022-12-01"][["y","ds","forecast_2023"]].dropna()
    liney=linedata.y.cumsum().values.tolist()
    linex=linedata.ds.values.tolist()
    plafond= linedata.forecast_2023.values.tolist()
    
    
    return render_template("chart.html", x = list(data.keys()), y=list(data.values()),ids=ids, liney=liney,linex=linex,plafond=plafond, id=id, x_pred=list(data_pred.keys()), y_pred = list(data_pred.values()))


@home_blue.route("/route")

def testing():
    with Session(engine) as session:
        for predict in session.query(Prediction).distinct(Prediction.product).all():
            print(predict.product)
    return "ok"