from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import bcrypt, DATABASE
from flask_app.models import model_recipe



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    def __init__( self , data ):
            self.id = data['id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.email = data['email']
            self.password = data['password']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
            self.recipes = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s,%(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)

        recipes = []
        if results:
            recipes_list = []
            for recipe in results:
                recipes_list.append( cls(recipe) )
            return recipes_list
        return []


    @classmethod
    def get_one(cls, data:dict) -> object:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return []

    @classmethod
    def get_one_by_email(cls, data:dict) -> object:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False       

    @staticmethod
    def is_valid(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'err_user_first_name')
            is_valid = False
        
        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters.", 'err_user_last_name')
            is_valid = False
        
        if len(form_data['email']) < 2:
            flash("email is required", 'err_user_email')
            is_valid = False

        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", 'err_user_email')
            is_valid = False        

        if len(form_data['password']) < 2:
            flash("pw is required", 'err_user_password')
            is_valid = False

        if len(form_data['password_confirm']) < 2:
            flash("Confirm password is required", 'err_user_password_confirm')
            is_valid = False
        elif form_data['password_confirm'] != form_data['password']:
            flash("Passwords do not match", 'err_user_password_confirm')
            is_valid = False
        return is_valid

    @staticmethod
    def is_valid_login(form_data):
        is_valid = True        
        
        if len(form_data['email']) < 2:
            flash("email is required", 'err_user_email_login')
            is_valid = False

        elif not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", 'err_user_email_login')
            is_valid = False
        
        if len(form_data['password']) < 2:
            flash("pw is required", 'err_user_password_login')
            is_valid = False

        else:
            potential_user = User.get_one_by_email({'email': form_data['email']})
            if not potential_user:
                is_valid = False
                flash("no user found", 'err_user_password_login')
            elif not bcrypt.check_password_hash(potential_user.password, form_data['password']):
                is_valid = False
                flash('Wrong Password', 'err_user_password_login' )
            else:
                session['uuid'] = potential_user.id
        
        return is_valid
    