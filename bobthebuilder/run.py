import os
from flask import Flask, render_template
from app.services.BoardService import BoardF
from app.services.CrmService import CrmF

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('auth/main.html')

app.register_blueprint(BoardF)
app.register_blueprint(CrmF)

app.secret_key = 'secret_key'
app.template_folder = os.path.abspath("templates")
app.static_folder = os.path.abspath("static")



if __name__ == '__main__':
    # 여기서 전원을 켭니다!
    app.run(host='0.0.0.0', port=5000, debug=True)