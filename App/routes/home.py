
import pandas as pd
from flask import render_template,Blueprint, request
from App import df, df_predictions, db
from flask_login import login_required,current_user
from ..models import User, Product
from ..models_predictions import Prediction, engine, product_spend
from sqlalchemy.orm import Session
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import and_, func
from ..utils import get_years, get_data
from pmdarima.arima import auto_arima

home_blue = Blueprint("home", __name__, static_folder="../static", template_folder="../templates")

@home_blue.route("/")
@login_required
def home():
    user = User.query.filter_by(id=current_user.id).first()
    ids = [i.tangram_id for i in  user.product]
    id = ids[0]
 
    temp = df.loc[df.unique_id == str(id)].sort_values("ds")
    linedata = temp.loc[temp.ds > "2022-12-01"][["y","ds","forecast_2023"]].dropna()
    plafond= linedata.forecast_2023.values.tolist()
    
    years = get_years(Session(engine), str(id))

    year = years[-1]
    next_year = int(year) +1
    date = f"{year}-01-01"
    next_year = f"{next_year}-01-01"

    temp = df.loc[df.unique_id == str(id)].sort_values("ds")
    linedata = temp.loc[(temp.ds >= date) & (temp.ds < next_year)][["y","ds","forecast_2023"]].dropna()
    plafond= linedata.forecast_2023.values.tolist()

    with Session(engine) as session:

        data = {}
        for spend in session.query(product_spend).filter_by(title=str(id))\
            .filter(and_(func.date(product_spend.columns.period)>=date),
                        and_(func.date(product_spend.columns.period)<next_year)).all():
            
            try:
                temp_date = spend.period
                str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            except:
                temp_date = datetime.strptime(str(spend.period), "%Y-%m-%d")
                str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            data[str_date] = spend.price


        data_pred = dict.fromkeys(data, 0)
        for predict in session.query(Prediction).filter_by(product=str(id)).all():
            try:
                temp_date = datetime.strptime(str(predict.date), "%Y-%m-%d")
                str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            except:
                temp_date =predict.date
                str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            
            data_pred[str_date] = predict.prediction
    

    budget_evolution = {}
    passed_price = 0
    for i in data.keys():
        price_value = data[i]
        try:

            budget_evolution[i] = float(price_value) + float(passed_price)
            passed_price = budget_evolution[i]
            
        except Exception as e:
            budget_evolution[i] = float(price_value)

    color_line = ["bleu" for i in range(len(budget_evolution))]

    
    return render_template("chart.html",
                            x = list(data.keys()),
                            y=list(data.values()),
                            ids=ids,
                            liney=list(budget_evolution.values()),
                            linex=list(budget_evolution.keys()),
                            plafond=plafond,
                            color_line=color_line,
                            id=id,
                            x_pred=list(data_pred.keys()),
                            y_pred = list(data_pred.values()),
                            years = years,
                            year=year)






@home_blue.route("/", methods=["POST"])
@login_required
def graph_page():

    # get user products
    user = User.query.filter_by(id=current_user.id).first()
    ids = [i.tangram_id for i in  user.product]
    

    # get selected product id and loc it in df
    id = request.form.get("id")

    years = get_years(Session(engine), str(id))

    year = request.form.get("year")

    next_year = int(year) +1
    date = f"{year}-01-01"
    next_year = f"{next_year}-01-01"
    
    temp = df.loc[df.unique_id == str(id)].sort_values("ds")
    linedata = temp.loc[(temp.ds >= date) & (temp.ds < next_year)][["y","ds","forecast_2023"]].dropna()
    plafond= linedata.forecast_2023.values.tolist()
    temp = df.loc[df.unique_id == str(id)].sort_values("ds")
    linedata = temp.loc[(temp.ds >= date) & (temp.ds < next_year)][["y","ds","forecast_2023"]].dropna()
    plafond= linedata.forecast_2023.values.tolist()


    

    with Session(engine) as session:

        data = {}
        for spend in session.query(product_spend).filter_by(title=str(id)).filter(and_(func.date(product_spend.columns.period)>=date),
                                                                                  and_(func.date(product_spend.columns.period)<next_year)).all():
            
            try:
                temp_date = spend.period
                str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            except:
                temp_date = datetime.strptime(str(spend.period), "%Y-%m-%d")
                str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            data[str_date] = spend.price


        data_pred = dict.fromkeys(data, 0)
        for predict in session.query(Prediction).filter_by(product=str(id)).all():
            try:
                temp_date = datetime.strptime(str(predict.date), "%Y-%m-%d")
                str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            except:
                temp_date =predict.date
                str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            
            data_pred[str_date] = predict.prediction
    
    budget_evolution = {}
    passed_price = 0
    for i in data.keys():
        price_value = data[i]
        try:
            passed_date = datetime.strptime(i, "%Y-%m") - relativedelta(months=1)
            passed_date = f"{passed_date.year}-{'{:02d}'.format(passed_date.month)}"


            budget_evolution[i] = float(price_value) + float(passed_price)
            passed_price = budget_evolution[i]
            
        except Exception as e:
            budget_evolution[i] = float(price_value)
    color_line = ["bleu" for i in range(len(budget_evolution))]
    

    return render_template("chart.html",
                            x = list(data.keys()),
                            y=list(data.values()),
                            ids=ids,
                            liney=list(budget_evolution.values()),
                            linex=list(budget_evolution.keys()),
                            plafond=plafond,
                            color_line=color_line,
                            id=id,
                            x_pred=list(data_pred.keys()),
                            y_pred = list(data_pred.values()),
                            years = years,
                            year=year)

@home_blue.route("/predictions")
@login_required
def form_predictions():
    user = User.query.filter_by(id=current_user.id).first()
    ids = [i.tangram_id for i in  user.product]

    min_date = datetime.now().strftime("%Y-%m")

    return render_template("formpredictions.html", ids=ids, min_date=min_date)

@home_blue.route("/predictions", methods=["POST"])
@login_required
def make_predictions():
    id = request.form.get("product")
    start_date= request.form.get("start_date")
    end_date = request.form.get("end_date")


    with Session(engine) as session:
        r= session.query(product_spend.c.period, product_spend.c.price).filter_by(title=f"{id}").all()


    df_prediction = pd.DataFrame.from_records(r)
    df_prediction.columns = ["period","price"]

    diff = relativedelta( datetime.strptime(end_date, "%Y-%m"),df_prediction["period"].max())
    n_months = diff.years * 12 + diff.months
    
    df_prediction["period"] = pd.to_datetime(df_prediction["period"])
    df_prediction["price"] = df_prediction["price"].astype("float32")
    df_prediction = df_prediction.sort_values("period").set_index("period")
    model_temp = auto_arima(df_prediction[["price"]])
    model_temp.fit_predict(df_prediction[["price"]], )
    predictions_temp = model_temp.predict(start = df_prediction.shape[0] -19, n_periods=n_months)


    y = df_prediction["price"].to_list()
    x = [df_prediction.index.astype("object").values]


    data={}
    data_pred = {}
    for i in df_prediction.index:
        data[f"{i.year}-{i.month}-01"] = df_prediction.loc[i].values[0]
        try:
            data_pred[f"{i.year}-{i.month}-01"] = predictions_temp.loc[i].values[0]
        except Exception:
            data_pred[f"{i.year}-{i.month}-01"] = 0
    for i in predictions_temp.index:
        data_pred[f"{i.year}-{i.month}-01"] = predictions_temp.loc[i]


    budget_evolution = {}
    passed_price = 0
    for i in data.keys():
        price_value = data[i]
        try:

            budget_evolution[i] = float(price_value) + float(passed_price)
            passed_price = budget_evolution[i]
            
        except Exception as e:
            budget_evolution[i] = float(price_value)

    budget_evolution_pred = budget_evolution.copy()
    budget_evolution_pred["2023-07-01"] = 1500
    color_line = ["bleu" for i in range(len(budget_evolution))]
    

    # return "1"
    
    return render_template("chart.html",
                                        x = list(data.keys()),
                                        y=list(data.values()),
                                        ids=None,
                                        liney=list(budget_evolution.values()),
                                        linex=list(budget_evolution.keys()),
                                        color_line=color_line,
                                        plafond=[1,1,1],
                                        id=id,
                                        x_pred=list(data_pred.keys()),
                                        y_pred =list(data_pred.values()),
                                        years = None,
                                        year=None)