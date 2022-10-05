from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['TITLE'] = 'Konoha book'
Bootstrap(app)

@app.route("/")
def index():
    shinobis = ['Naruto', 'Sasuke', 'Sakura']
    context = {'shinobis': shinobis}
    return render_template('index.html', **context)
