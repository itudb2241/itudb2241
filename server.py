from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import re

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True,
)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/addplayer')
def addplayer():
    return render_template('addplayer.html')

@app.route('/addplayer', methods=['POST'])
def addplayer1():

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        (playerId, firstName, lastName, playerHeight, playerWeight) = (request.form['playerId'], request.form['firstName'], request.form['lastName'], request.form['playerHeight'], request.form['playerWeight'])
        cursor.execute('INSERT INTO Master (playerId, firstName, lastName, height, weight) VALUES (?, ?, ?, ?, ?)', (playerId, firstName, lastName, playerHeight, playerWeight))
        print(cursor.rowcount)
        connection.commit()

        myRow = cursor.execute('SELECT * FROM Master WHERE playerId = ?', (playerId,)).fetchone()

        print(myRow)
        
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (connection):
            connection.close()
            print("The SQLite connection is closed")

    return render_template('addplayer.html')

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
    awards = cursor.execute('SELECT * FROM AwardsPlayers WHERE playerId = ?', (playerId,)).fetchall()
    scorings = cursor.execute('SELECT * FROM Scoring WHERE playerId = ?', (playerId,)).fetchall()
    goalies = cursor.execute('SELECT * FROM Goalies WHERE playerId = ?', (playerId,)).fetchall()
    print(awards)

    return render_template('players.html', player=player, players= players,awards=awards if awards is not None and len(awards) > 0 else None, goalies=goalies if goalies is not None and len(goalies) > 0 else None, scorings=scorings if scorings is not None and len(scorings) > 0 else None)


@app.route('/teams')
def team_page():

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    teams = cursor.execute('SELECT tmId, name FROM Teams WHERE tmId NOT NULL').fetchall()

    return render_template('teams.html', teams=teams)


@app.route('/teams/<tmId>')
def team_info(tmId):

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    teams = cursor.execute('SELECT tmId, name FROM Teams WHERE tmId NOT NULL').fetchall()
    team = cursor.execute('SELECT * FROM Teams WHERE tmId = ?', (tmId,)).fetchone()
    coach_id = cursor.execute("SELECT CoachId FROM Coaches WHERE tmId = ?",(tmId,)).fetchall()
    
    coach_id[0] = re.sub('[^A-Za-z0-9]+', '', str(coach_id[0]))
    coach_name = cursor.execute("SELECT NameGiven FROM Master WHERE CoachId = ?",(str(coach_id[0]),)).fetchall()
    coach_name = re.sub('[^A-Za-z0-9]+', ' ', str(coach_name))
    return render_template('teams.html', team=team, teams= teams,coach_id=coach_id, coach_name=coach_name)




@app.route("/player/<playerId>/addscoring", methods=['POST'])
def add_scoring(playerId):
    ScoringYear = request.form['ScoringYear']
    ScoringTeam = request.form['ScoringTeam']
    ScoringLeague = request.form['ScoringLeague']
    ScoringPosition = request.form['ScoringPosition']
    ScoringPoints = request.form['ScoringPoints']

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Scoring (playerId, year, tmId, lgId, pos, Pts) VALUES (?, ?, ?, ?, ?, ?)', (playerId, ScoringYear, ScoringTeam, ScoringLeague, ScoringPosition, ScoringPoints))
        print(cursor.rowcount)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (connection):
            connection.close()
            print("The SQLite connection is closed")
    
    return redirect(url_for('player_info', playerId=playerId))

@app.route("/player/<playerId>/addgoalie", methods=['POST'])
def add_goalie(playerId):
    GoalieYear = request.form['GoalieYear']
    GoalieTeam = request.form['GoalieTeam']
    GoalieLeague = request.form['GoalieLeague']
    GoaliePoints = request.form['GoaliePoints']

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Goalies (playerId, year, tmId, lgId, Min) VALUES (?, ?, ?, ?, ?)', (playerId, GoalieYear, GoalieTeam, GoalieLeague, GoaliePoints))
        print(cursor.rowcount)
        connection.commit()
        
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (connection):
            connection.close()
            print("The SQLite connection is closed")
    
    return redirect(url_for('player_info', playerId=playerId))

@app.route("/player/<playerId>/addaward", methods=['POST'])
def add_award(playerId):
    awardYear = request.form['awardYear']
    awardLeague = request.form['awardLeague']
    awardName = request.form['awardName']

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO AwardsPlayers (playerId, year, lgId, award) VALUES (?, ?, ?, ?)', (playerId, awardYear, awardLeague, awardName))
        print(cursor.rowcount)
        connection.commit()
        
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (connection):
            connection.close()
            print("The SQLite connection is closed")
    
    return redirect(url_for('player_info', playerId=playerId))

@app.route("/player/<playerId>/deletescoring", methods=['GET'])
def delete_scoring(playerId):

    args = request.args

    if not args: return redirect(url_for('player_info', playerId=playerId))

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Scoring WHERE playerId = ? AND year = ? AND tmId = ? AND lgId = ? AND pos = ? AND Pts = ?', (playerId, args.get("year"), args.get("team"), args.get("league"), args.get("position"), args.get("points")))
        connection.commit()
        
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete data into sqlite table", error)
    finally:
        if (connection):
            connection.close()
            print("The SQLite connection is closed")
    
    return redirect(url_for('player_info', playerId=playerId))


if __name__ == '__main__':
    app.run(debug=True)