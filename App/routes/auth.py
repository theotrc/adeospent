from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from App import db
from App.utils import generate_code
from logging import FileHandler, WARNING

from flask_login import login_user, login_required, current_user, logout_user

from datetime import date, datetime, timedelta
from hashlib import sha256
from ..models import User, Product
from App import df_predictions,df
import smtplib
from email.message import EmailMessage
import ssl
import os
from ..models_predictions import engine, Prediction,product_spend
from sqlalchemy.orm import Session


pwd =os.environ.get('EMAIL_PWD')
email_sender = os.environ.get('EMAIL_SENDER')
email_receiver = 'theotricot12@gmail.com'



auth_blue= Blueprint("auth", __name__, static_folder="../static", template_folder="../templates")

#routes for login
@auth_blue.route('/signup')
def signup():
    with Session(engine) as session:
        ids = [predict.product for predict in session.query(Prediction).distinct(Prediction.c.product).all()]
        
    return render_template('signup.html', ids=ids)


@auth_blue.route('/signup', methods=['POST'])
def signup_post():
    
    email = request.form.get('email')
    password = request.form.get('password')
    ids = request.form.getlist('categorie1')
    
    user = User.query.filter_by(email=email).first() 
    # if this returns a user, then the email already exists in database

    if user: 
    # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))
    if not password or len(password)<8:
        flash("le mot de passe doit faire 8 caractères minimum", "info")
        return render_template('signup.html')

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'),is_admin=False)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    user_id = User.query.filter_by(email = email).first().id

    for id in ids:
        new_product = Product(user_id=user_id, tangram_id=id)
        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for("auth.login"))


@auth_blue.route('/login')
def login():
    return render_template('login.html')


@auth_blue.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    

    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        message = f"Utilisateur ou mot de passe incorrect"
        flash(message, "info")
        return redirect(url_for('auth.login')) 

   
    login_user(user, remember=remember)


    return redirect(url_for('home.home'))

@auth_blue.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))



@auth_blue.route('/resetpwd')
def resetpwd():

    return render_template('Password.html')

@auth_blue.route("/resetpwd", methods=['POST'])
def resetpwd_post():


    url_app = os.environ.get('URLAPP')
    email_receiver = request.form.get('email')

    
    user = User.query.filter_by(email=email_receiver).first()

    ## if user exist
    if user:
        id = user.id

        code = sha256(str(generate_code()).encode()).hexdigest()
        expiry = datetime.now() + timedelta(days=1)


        User.query.filter_by(id=id).update(values={"reset_token":code,"reset_token_expiry":expiry})
        db.session.commit()

        
        subject = "réinitialisation de mot de passe"
        body = f"lien de réinitialisation: {url_app}/mailvalidation/{id}/{code}"

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] =  subject
        em.set_content(body)



        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, pwd)
            smtp.sendmail(email_sender,email_receiver,em.as_string())

        message = f"Un email vous a été envoyé"
        flash(message, "info")

    elif not user:

        message = f"L'adresse mail que vous avez rentré n'est associé à aucun compte"
        flash(message, "info")

    return render_template("Password.html")

@auth_blue.route("/mailvalidation/<id>/<code>")
def mailvalidation(id,code):
    
    user = User.query.filter_by(id=int(id)).filter_by(reset_token=code).first()


    if user:
        if user.reset_token_expiry > datetime.now():
            return render_template('ValidateMail.html', id=id,code=code)
        else:
            return redirect(url_for('/resetpwd'))
    else:
        return redirect(url_for('/resetpwd'))



@auth_blue.route('/mailvalidation/<id>/<code>', methods=['POST'])
def change_pwd(id, code):
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password == confirm_password:    
        try:



            User.query.filter_by(id=int(id)).filter_by(reset_token=code).update(values={"reset_token":None,
                                                                                "reset_token_expiry":None,
                                                                                "password":generate_password_hash(password, method='sha256')})
            db.session.commit()
            
        except Exception as e:
            return "error"
    else:
        flash("les deux mots de passe ne sont pas indentiques", "info")
        return render_template('ValidateMail.html', id=id,code=code)
    
    return redirect(url_for('auth.login'))