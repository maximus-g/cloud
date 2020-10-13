from flask import (Blueprint, render_template, url_for, request,
redirect, session, flash, send_file)
from cloud import app


@app.route("/")
def index():
    flash("Welcome to Cloud")
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/contacts")
def contacts():
    return render_template('contacts.html')
