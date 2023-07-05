from flask import render_template,Blueprint

from flask_login import login_required, current_user


account_blue = Blueprint("account", __name__, static_folder="../static", template_folder="../templates")

@account_blue.route("/account")
@login_required
def account():

    return render_template("account.html",data={"user":current_user})

