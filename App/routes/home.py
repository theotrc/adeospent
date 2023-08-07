from flask import render_template,Blueprint, request
from App import df, df_predictions, db
from flask_login import login_required,current_user
from ..models import User, Product
from ..models_predictions import Prediction, engine, product_spend
from sqlalchemy.orm import Session
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import and_, func
from ..utils import get_years, get_data


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

    

    
    return render_template("chart.html",
                            x = list(data.keys()),
                            y=list(data.values()),
                            ids=ids,
                            liney=list(budget_evolution.values()),
                            linex=list(budget_evolution.keys()),
                            plafond=plafond,
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
            print(data_pred)
            print(predict,'\n\n\n\n\n')
    
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


    return render_template("chart.html",
                            x = list(data.keys()),
                            y=list(data.values()),
                            ids=ids,
                            liney=list(budget_evolution.values()),
                            linex=list(budget_evolution.keys()),
                            plafond=plafond,
                            id=id,
                            x_pred=list(data_pred.keys()),
                            y_pred = list(data_pred.values()),
                            years = years,
                            year=year)