import os
from flask import Flask, render_template
from app.routes import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

app.register_blueprint(BoardF)
app.register_blueprint(CrmF)
app.register_blueprint(AlgoF)

app.secret_key = 'secret_key'
app.template_folder  = os.path.abspath("app/templates")
app.static_folder    = os.path.abspath("app/statics")

app.static_url_path  = "/statics"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)