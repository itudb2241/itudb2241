from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True,
)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/players')
def players():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    players = cursor.execute('SELECT playerId, firstName, lastName FROM Master WHERE playerId NOT NULL').fetchall()
    connection.close()

    return render_template('players.html', players=players)

@app.route('/player/<playerId>')
def player_info(playerId):

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    players = cursor.execute('SELECT playerId, firstName, lastName FROM Master WHERE playerId NOT NULL').fetchall()
    player = cursor.execute('SELECT * FROM Master WHERE playerId = ?', (playerId,)).fetchone()
    goalies = cursor.execute('SELECT ALL FROM Goalies WHERE playerId = ?', (playerId,)).fetchall()



    return render_template('players.html', player=player, players=players)


if __name__ == '__main__':
    app.run(debug=True)