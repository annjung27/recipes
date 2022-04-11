from flask import Flask,render_template, redirect, request, session
from flask_app import app, bcrypt
from flask_app.models import model_user, model_recipe

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    
    data = {
        'id': session['uuid']
    }
    user = model_user.User.get_one(data)
    all_recipes = model_recipe.Recipe.get_all()           
    return render_template('dashboard.html', all_recipes = all_recipes, user=user  )
    
@app.route('/user/login', methods= ['post'])    # Action
def login():
    is_valid = model_user.User.is_valid_login(request.form)

    if not is_valid:
        return redirect('/')

    return redirect('/')

@app.route('/logout')
def logout():
    del session['uuid']
    return redirect('/')

@app.route('/user/create', methods= ['post'])    # Action
def create_user():

    #run validation
    is_valid = model_user.User.is_valid(request.form)

    if is_valid == False:
        return redirect ('/')
    
    #hash the incoming password
    hash_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form, 
        'password': hash_pw
    }
    #save user data into database
    id= model_user.User.create(data)            
    return redirect('/')




