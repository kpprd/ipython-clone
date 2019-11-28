#!/usr/bin/python2
from flask import Flask
from flask import request
from flask import render_template
from feedline import feedline

"""
Initiates a python web interface using flask.
"""

app = Flask(__name__)
history="In [0]: "
@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    # The following is the code for the submit button:
    submit= """    <form action="." method="POST">
        <input type="text" name="text">
        <input type="submit" name="my-form" value="submit">
    </form>"""
    inn=request.form['text'] # input text
    ut = feedline(inn) # feed input to feedline
    global history
    history=history+ inn+"\n"+ut+"\n"
    history= history.replace("\n", "<br>")
    return history+ submit # updates web interface by wrtiting out the full history + submit button

if __name__ == '__main__':
    app.run()