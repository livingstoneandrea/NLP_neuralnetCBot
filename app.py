# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 14:46:57 2021

@author: livin
"""
from chatapp import chatbot_repsonse
from flask import Flask, render_template, request, jsonify
import sys

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

    try:
        port = int(sys.argv[1]) # for a command-line input 5000
    except:
        port = 5000 # set the default port the port 5000

    app.run(port=port, debug=True)