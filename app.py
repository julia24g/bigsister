from flask import Flask, request, render_template, redirect, url_for
import os
import cohere

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

co = cohere.Client("rSdxnPjCDd10gxJr1SooZMMAD9jFKsHBmA2kKqHU")


from sandbox.qa import answer_with_search

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index", methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':
        form_data = request.form['enter']
        x = answer_with_search(form_data, co=co, serp_api_token="5d72ef7db0451d51e3dd03206c03ce36e50f30029004dfc241ecf606c1384e4e")
        print(x)
        return render_template('index.html',answer_data = x)

if __name__ == '__main__':
    app.run(debug=True, host='localhost',port=5001)