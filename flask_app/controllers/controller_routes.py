from flask import Flask,render_template, redirect, request, session
from flask_app import app
from flask_app.models import model_user

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')
    return render_template('index.html')