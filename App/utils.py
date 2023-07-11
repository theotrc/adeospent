import random
from datetime import datetime
from .models_predictions import product_spend, Prediction
from sqlalchemy import and_, func

def generate_code():
    code = int(str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)))
    return code

def get_years(session, product_title):

    with session as session:
        
        query = session.query(product_spend.columns.period).filter_by(title=str(product_title)).order_by(product_spend.columns.period).all()
        min_year = datetime.strptime(query[0].period, "%Y-%m-%d").year
        max_year = datetime.strptime(query[-1].period, "%Y-%m-%d").year
    years=[]
    for i in range(max_year - min_year+1):
        years.append(min_year + i)
    return years



def get_data(session, date, next_year):

    with session as session:

        data = {}
        print( session.query(product_spend).filter_by(title=str(id)).filter(and_(func.date(product_spend.columns.period)>=date),
                                                                                    and_(func.date(product_spend.columns.period)<next_year)).all())
        for spend in session.query(product_spend).filter_by(title=str(id)).filter(and_(func.date(product_spend.columns.period)>=date),
                                                                                    and_(func.date(product_spend.columns.period)<next_year)).all():

            temp_date = datetime.strptime(str(spend.period), "%Y-%m-%d")
            str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            data[str_date] = spend.price


        data_pred = dict.fromkeys(data, 0)
        for predict in session.query(Prediction).filter_by(product=str(id)).all():

            temp_date = datetime.strptime(str(predict.date), "%Y-%m-%d")
            str_date = f"{temp_date.year}-{'{:02d}'.format(temp_date.month)}"
            data_pred[str_date] = predict.Prediction
            
    budget_evolution = {}
    x = 0
    for i in data.keys():
        price_value = data[i]
        try:
            
            x += price_value

            budget_evolution[i] = x
            
            
        except Exception as e:
            budget_evolution[i] = float(price_value)

    return data, budget_evolution, data_pred