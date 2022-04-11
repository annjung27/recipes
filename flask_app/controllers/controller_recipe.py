from flask import Flask,render_template, redirect, request, session, url_for
from flask_app import app, bcrypt
from flask_app.models import model_recipe, model_user


@app.route('/recipe/new') #dispaly
def new_recipe():
    if 'uuid' not in session:
        return redirect('/')
    data = {
        'id' : session['uuid']
    }
    user = model_user.User.get_one(data)    
    return render_template("recipe_new.html", user = user)

@app.route('/recipe/create', methods= ['post'])    # Action
def create_recipe():
    # session
    if 'uuid' not in session:
        return redirect('/')    

    #run validation
    is_valid = model_recipe.Recipe.is_valid_recipe(request.form)

    if is_valid == False:
        return redirect ('/recipe/new')

    data = {
        **request.form,        
        'user_id' : session['uuid']
    }
    model_recipe.Recipe.create(data)               
    return redirect('/dashboard')

@app.route('/recipe/edit/<int:id>')
def recipe_edit(id):
    if 'uuid' not in session:
        return redirect('/')

    recipe_data = {
        'id' : id
    }
    data = {
        'id' : session['uuid']
    }
    user = model_user.User.get_one(data)
    recipe = model_recipe.Recipe.get_one(recipe_data)
    return render_template('recipe_edit.html', user=user, recipe=recipe)


@app.route('/recipe/update/<int:id>', methods=['post'])
def recipe_update(id):
    if 'uuid' not in session:
        return redirect('/')
    if not model_recipe.Recipe.is_valid_recipe(request.form):
        return redirect(f"/recipe/edit/{id}")

    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "created_at" : request.form['created_at'],
        "under_30min" : request.form['under_30min'],
        "id" :id
    }
    model_recipe.Recipe.update_one(data)
    return redirect('/dashboard')

@app.route('/recipe/view/<int:id>')
def recipe_show(id):
    if 'uuid' not in session:
        return redirect('/')
    recipe_data = {
        'id' : id
    }
    data = {
        'id' : session['uuid']
    }
    recipe = model_recipe.Recipe.get_one(recipe_data)
    user = model_user.User.get_one(data)
    return render_template('recipe_show.html', recipe=recipe, user=user)

@app.route('/recipe/delete/<int:id>')
def recipe_delete(id):
    if 'uuid' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    model_recipe.Recipe.delete_one(data)
    return redirect('/dashboard')