from flask import Flask, render_template
from init_database import init_db

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True,
)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/players')
def players_page():
    return render_template('players.html')


if __name__ == '__main__':
    app.run(debug=True)