from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import bcrypt, DATABASE
from flask_app.models import model_user


class Recipe:
    def __init__( self , data ):
            self.id = data['id']
            self.name = data['name']
            self.description = data['description']
            self.instructions = data['instructions']
            self.under_30min = data['under_30min']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
            self.user_id = data['user_id']

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            recipes_list = []
            for dictionary in results:
                recipe = cls(dictionary)
                data = {
                    'id': dictionary['users.id'],
                    'created_at': dictionary['users.created_at'],
                    'updated_at': dictionary['users.updated_at'], 
                    'first_name': dictionary['first_name'],
                    'last_name': dictionary['last_name'],
                    'email': dictionary['email'],
                    'password': dictionary['password']                    
                }
                user = model_user.User(data)
                recipe.owner = user
                recipes_list.append(recipe)
            return recipes_list
        return []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under_30min, user_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(under_30min)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, data:dict) -> object:
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False
    
    @classmethod
    def update_one(cls, data):
        query = 'UPDATE recipes SET name= %(name)s, description=%(description)s, instructions=%(instructions)s, under_30min=%(under_30min)s WHERE id=%(id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_one(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def is_valid_recipe(form_data):
        is_valid = True
        if len(form_data['name']) < 1:
            flash("Name is required", 'err_recipe_name')
            is_valid = False
        
        if len(form_data['description']) < 1:
            flash("Description is required", 'err_recipe_description')
            is_valid = False
        
        if len(form_data['instructions']) < 1:
            flash("instructions are required", 'err_recipe_instructions')
            is_valid = False

        if len(form_data['created_at']) < 1:
            flash("Date is required", 'err_recipe_created_at')
            is_valid = False        

        if (form_data['under_30min']) == "":
            flash("Select Yes or No", 'err_recipe_under_30min')
            is_valid = False
        
        return is_valid
