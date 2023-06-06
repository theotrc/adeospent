from flask import render_template,Blueprint, request
from App import df, df_predictions


home_blue = Blueprint("home", __name__, static_folder="../static", template_folder="../templates")


@home_blue.route("/")
def home():
    print("mnfklwemfkew")
    ids = df["unique_id"].unique()
    return render_template("index.html", ids=ids)



@home_blue.route("/chart", methods=["POST"])
def graph_page():
    id = request.form.get("id")
    temp = df.loc[df.unique_id == str(id)].sort_values("ds")
    x = temp["ds"].values.tolist()
    y = temp["y"].values.tolist()
    ids = df["unique_id"].unique()

    
    return render_template("chart.html", x = x, y=y,ids=ids)


@home_blue.route("/ap", methods=['POST'])
def a_post():
    id = request.form.get("id")
    return str(id)


@home_blue.route("/chart_predictions", methods=["POST"])
def graph_page_predictions():
    id = request.form.get("id")
    temp = df_predictions.loc[df_predictions.unique_id == str(id)].sort_values("ds")
    predictions = temp["prediction"].values.tolist()

    temp = df.loc[df.unique_id == str(id)].sort_values("ds")
    x = temp["ds"].values.tolist()
    y = temp["y"].values.tolist()
    pred = [0 for i in range(len(y))]
    reverse_predictions = predictions[::-1]
    for i in range(len(predictions)):
        pred[i]= reverse_predictions[i]
    pred = pred[::-1]
    ids = df["unique_id"].unique()

    
    return render_template("chart.html", x = x, y=y,ids=ids, predictions=pred)

