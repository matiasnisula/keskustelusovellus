from app import app
import users
from flask import render_template

@app.route("/")
def index():
    return "sd"