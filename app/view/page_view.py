from app import app
from flask import render_template


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/url-list', methods=['GET'])
def url_list():
    return render_template('url-list.html')
