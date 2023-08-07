import unittest
from flask import Flask, session, current_app, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin
from App import create_app, db, migrate  
from App import models
from App.models import User,Product
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash



class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config.from_object('config')

        self.db = db
        self.db.init_app(self.app)

        
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()



        self.db.create_all() # Créez la base de données pour les tests
        # Vous pouvez effectuer ici d'autres initialisations avant les tests
        @self.login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))
        
        self.email = 'test@test.com'
        self.pwd = 'password'
        self.products = ['PYXIS','OMNISTORE']



    def test_signup_get(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_login_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        
    def test_signup(self):


        response = self.client.post('/signup', data={'email': self.email, 'password':self.pwd,'categorie1': self.products}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app_context:
            user = User.query.filter_by(email=self.email).first()
            products = [i.tangram_id for i in user.product]
        self.assertTrue(user != None)
        self.assertListEqual(self.products, products)

    def test_login_successful(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'test_password',
            'remember': 'true',
        }

        with current_app.test_request_context():
            # Effectuez une requête POST vers la route de connexion.
            response = self.client.post(url_for('auth.login_post'), data=form_data, follow_redirects=True)

            # Vérifiez que la redirection a eu lieu en vérifiant le code de statut HTTP.
            self.assertEqual(response.status_code, 302)
            # Vérifiez que la redirection a eu lieu vers la page d'accueil.
            self.assertEqual(response.location, url_for('home.home'))

            # Vérifiez que l'utilisateur est maintenant connecté.
            self.assertTrue(current_user.is_authenticated)

    def test_delete_user(self):
        with self.app_context:
            user = User.query.filter_by(email=self.email).first() 
            print(user)
            db.session.delete(user)
            db.session.commit()

            user = User.query.filter_by(email=self.email).first() 
            print(user)
        self.assertTrue(user == None)
        
    
    # def test_signup(self):


    # def test_login(self):
    #     # Ajoutez un utilisateur de test à la base de données (vous pouvez utiliser une factory pour créer des utilisateurs)
    #     # new_user = User(email='tete@dstdest.com', password=generate_password_hash('password', method='sha256'),is_admin=False)

    #     # db.session.add(new_user)
    #     # db.session.commit()
    #     # user_id = User.query.filter_by(email = 'tedste@test.com').first().id

    #     # new_product = Product(user_id=user_id, tangram_id='id_test')
    #     # db.session.add(new_product)
    #     # db.session.commit()
    #     # Effectuez la connexion avec le client de test
    #     print(current_user)
    #     response = self.client.post('/login', data={'email': 'teste@test.com', 'password': 'password', 'remember':'true'}, follow_redirects=False)
    #     self.assertEqual(response.status_code, 302)

    #     response = self.client.post('/login', data={'email': 'wrong@test.com', 'password': 'wrong', 'remember':'true'}, follow_redirects=True)
    #     self.assertEqual(response.status_code, 302)

    #     self.assertTrue(current_user.is_authenticated)

        # db.session.remove(new_user)
        # Ajoutez d'autres assertions pour tester le comportement attendu après la connexion

    # def test_logout(self):
    #     # Assurez-vous qu'un utilisateur est connecté (par exemple, en utilisant self.client.post('/login', ...))
    #     self.assertTrue(current_user.is_authenticated)

    #     # Effectuez la déconnexion avec le client de test
    #     response = self.client.get('/logout', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(current_user.is_authenticated)
    #     # Ajoutez d'autres assertions pour tester le comportement attendu après la déconnexion

if __name__ == '__main__':
    unittest.main()