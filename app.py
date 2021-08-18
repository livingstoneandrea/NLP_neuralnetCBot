# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 14:46:57 2021

@author: livin
"""
from chatapp import chatbot_repsonse
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("main.html")

@app.route("/get")
def get_bot_response():
    
    data = request.args.get('msg')
    
    print(data)
    return jsonify(str(chatbot_repsonse(data)))


if __name__ == "__main__":
    app.run(debug=True) 