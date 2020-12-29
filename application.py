import os
import time

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from tkinter import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///studyperiods.db")

@app.route("/", methods=["GET", "POST"])
def index():
    topic = request.form.get("topic")
    period = request.form.get("period")

    if request.method == "GET":
        return render_template("index.html", topic=topic, period=period)
    else: #get input
        topic = request.form.get("topic")
        if not topic:
            return ("YOU MUST ENTER A STUDY TOPIC")

        period = request.form.get("period")
        if not period:
            return ("YOU MUST ENTER A STUDY PERIOD")

        #input into table and go to history
        result=db.execute("INSERT INTO studytopics (topic, period) VALUES (:topic, :period);", topic=request.form.get("topic"), period=request.form.get("period"))

        return redirect("/")

@app.route("/history")
def history():
    #show study history table
    rows = db.execute("SELECT * FROM studytopics")
    return render_template("history.html", rows=rows)



