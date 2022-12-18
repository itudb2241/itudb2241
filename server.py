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
    players = cursor.execute('SELECT playerId, firstName, lastName FROM Master WHERE playerId NOT NULL ORDER BY FirstName').fetchall()
    connection.close()

    return render_template('players.html', players=players)
@app.route('/games')
def games():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    games = cursor.execute('SELECT playerId, lgId FROM Goalies WHERE playerId NOT NULL').fetchall()
    connection.close()

    return render_template('games.html', games=games)

@app.route('/player/<playerId>')
def player_info(playerId):

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    players = cursor.execute('SELECT playerId, firstName, lastName FROM Master WHERE playerId NOT NULL ORDER BY FirstName').fetchall()
    player = cursor.execute('SELECT * FROM Master WHERE playerId = ?', (playerId,)).fetchone()
    awards = cursor.execute('SELECT awardsPlayersId, Year, LgId, Award FROM AwardsPlayers WHERE playerId = ?', (playerId,)).fetchall()
    scorings = cursor.execute('SELECT u.scoringId, u.year, u.TmId, u.LgId, u.Pos,u.G, u.A, u.Pts, p.Name FROM (SELECT scoringId, year, tmId, LgId, Pos, Pts, G, A FROM Scoring WHERE playerId = ?) u LEFT JOIN (SELECT year,TmId,LgId, Name FROM Teams) p ON u.TmId = p.TmId AND u.year = p.year', (playerId,)).fetchall()
    goalies = cursor.execute('SELECT * FROM Goalies WHERE playerId = ?', (playerId,)).fetchall()
    shootouts = cursor.execute('SELECT * FROM GoaliesShootout WHERE playerId = ?', (playerId,)).fetchall()
    teams = cursor.execute('Select DISTINCT TmId, Name, LgId from Teams').fetchall() 
    print(scorings)
    try:
        goaliesteam = goalies[0][4]
        if(goaliesteam != None):
            goalies_team = cursor.execute('SELECT Name FROM Teams WHERE TmId = ?', (str(goalies[0][4]),)).fetchone()
    except:
        goaliesteam = None
        goalies_team = None
    try:
        shootouteam = shootouts[0][4]
        if(shootouteam != None):
            shootouts_team = cursor.execute('SELECT Name FROM Teams WHERE TmId = ?', (str(shootouts[0][4]),)).fetchone()
    except:
        shootouteam = None
        shootouts_team = None

    return render_template('players.html', player=player, players= players,awards=awards if awards is not None and len(awards) > 0 else None, goalies=goalies if goalies is not None and len(goalies) > 0 else None, scorings=scorings if scorings is not None and len(scorings) > 0 else None, teams=teams if teams is not None and len(teams) > 0 else None, goalies_team=goalies_team if goalies_team is not None and len(goalies_team) > 0 else None, shootouts=shootouts if shootouts is not None and len(shootouts) > 0 else None, shootouts_team=shootouts_team if shootouts_team is not None and len(shootouts_team) > 0 else None)


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


@app.route("/player/<playerId>/addgoalie", methods=['POST'])
def add_goalie(playerId):
    GoalieYear = request.form['GoalieYear']
    GoalieTeam = request.form['GoalieTeam']
    GoalieLeague = request.form['GoalieLeague']
    GoaliePoints = request.form['GoaliePoints']
    GoalieWinsLoseTie  = request.form['GoalieWinsLoseTie']
    GoalieWinsLoseTie = GoalieWinsLoseTie.split('/')
    GoalieStint = int(GoalieWinsLoseTie[0]) + int(GoalieWinsLoseTie[1]) + int(GoalieWinsLoseTie[2])

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Goalies (playerId, year, tmId, lgId, Min, W, L , TOL) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (playerId, GoalieYear, GoalieTeam, GoalieLeague, GoaliePoints, GoalieWinsLoseTie[0], GoalieWinsLoseTie[1], GoalieWinsLoseTie[2], GoalieStint))
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

@app.route("/player/<playerId>/addshootout", methods=['POST'])
def add_shootout(playerId):
    ShootoutYear = request.form['ShootoutYear']
    ShootoutTeam = request.form['ShootoutTeam']
    ShootoutWinsLose   = request.form['ShootoutWinsLose']
    ShootoutWinsLose = ShootoutWinsLose.split('/')
    ShootoutAgainst = request.form['ShootsAgainst']
    GoalsoutAgainst = request.form['GoalsAgainst']
    ShootoutStint = int(ShootoutWinsLose[0]) + int(ShootoutWinsLose[1])

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Shootouts (playerId, year, tmId, W, L, SA, GA, Stint) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (playerId, ShootoutYear, ShootoutTeam, ShootoutWinsLose[0], ShootoutWinsLose[1], ShootoutAgainst, GoalsoutAgainst, ShootoutStint))
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


@app.route("/player/<playerId>/addscoring", methods=['POST'])
def add_scoring(playerId):
    ScoringYear = request.form['ScoringYear']
    ScoringTeam = request.form['ScoringTeam']
    ScoringLeague = request.form['ScoringLeague']
    ScoringPosition = request.form['ScoringPosition']
    ScoringGoals = request.form['ScoringGoals']
    ScoringAssists = request.form['ScoringAssists']
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
        cursor.execute('DELETE FROM Scoring WHERE scoringId = ?', (args['scoringId'],))
        connection.commit()
        
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete data into sqlite table", error)
    finally:
        if (connection):
            connection.close()
            print("The SQLite connection is closed")
    
    return redirect(url_for('player_info', playerId=playerId))

@app.route("/player/<playerId>/deletegoalie", methods=['GET'])
def delete_goalie(playerId):
    
        args = request.args
    
        if not args: return redirect(url_for('player_info', playerId=playerId))
    
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('DELETE FROM Goalies WHERE goalieId = ?', (args['goalieId'],))
            connection.commit()
            
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to delete data into sqlite table", error)
        finally:
            if (connection):
                connection.close()
                print("The SQLite connection is closed")
        
        return redirect(url_for('player_info', playerId=playerId))

@app.route("/player/<playerId>/deleteshootout", methods=['GET'])
def delete_shootout(playerId):
        args = request.args
        if not args: return redirect(url_for('player_info', playerId=playerId))
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('DELETE FROM Shootouts WHERE ShootoutId = ?', (args['ShootoutId'],))
            connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to delete data into sqlite table", error)
        finally:
            if (connection):
                connection.close()
                print("The SQLite connection is closed")
        return redirect(url_for('player_info', playerId=playerId))

@app.route("/player/<playerId>/deleteaward", methods=['GET'])
def delete_award(playerId):

    args = request.args

    if not args: return redirect(url_for('player_info', playerId=playerId))

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM AwardsPlayers WHERE awardsPlayersId = ?', (args['awardsPlayersId'],))
        connection.commit()
        
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete data into sqlite table", error)
    finally:
        if (connection):
            connection.close()
            print("The SQLite connection is closed")
    
    return redirect(url_for('player_info', playerId=playerId))

@app.route("/player/<playerId>/updatescoring", methods=['GET'])
def edit_scoring(playerId):

    args = request.args

    if not args: return redirect(url_for('player_info', playerId=playerId))

    if(args["type"] == "increment"):
        if(args["column"] == "G"):
            try:
                connection = sqlite3.connect('database.db')
                cursor = connection.cursor()
                cursor.execute('UPDATE Scoring SET G = G + 1 WHERE scoringId = ?', (args['scoringId'],))
                cursor.execute('UPDATE Scoring SET Pts = Pts + 1 WHERE scoringId = ?', (args['scoringId'],))
                connection.commit()

                cursor.close()
            except sqlite3.Error as error:
                print("Failed to update data into sqlite table", error)
            finally:
                if (connection):
                    connection.close()
                    print("The SQLite connection is closed")

        elif(args["column"] == "A"):
            try:
                connection = sqlite3.connect('database.db')
                cursor = connection.cursor()
                cursor.execute('UPDATE Scoring SET A = A + 1 WHERE scoringId = ?', (args['scoringId'],))
                cursor.execute('UPDATE Scoring SET Pts = Pts + 1 WHERE scoringId = ?', (args['scoringId'],))
                connection.commit()

                cursor.close()
            except sqlite3.Error as error:
                print("Failed to update data into sqlite table", error)
            finally:
                if (connection):
                    connection.close()
                    print("The SQLite connection is closed")
    elif (args["type"] == "decrement"):

        if(args["column"] == "G"):
            try:
                connection = sqlite3.connect('database.db')
                cursor = connection.cursor()
                cursor.execute('UPDATE Scoring SET G = G - 1 WHERE scoringId = ?', (args['scoringId'],))
                cursor.execute('UPDATE Scoring SET Pts = Pts - 1 WHERE scoringId = ?', (args['scoringId'],))
                connection.commit()

                cursor.close()
            except sqlite3.Error as error:
                print("Failed to update data into sqlite table", error)
            finally:
                if (connection):
                    connection.close()
                    print("The SQLite connection is closed")

        elif(args["column"] == "A"):
            try:
                connection = sqlite3.connect('database.db')
                cursor = connection.cursor()
                cursor.execute('UPDATE Scoring SET A = A - 1 WHERE scoringId = ?', (args['scoringId'],))
                cursor.execute('UPDATE Scoring SET Pts = Pts - 1 WHERE scoringId = ?', (args['scoringId'],))
                connection.commit()

                cursor.close()
            except sqlite3.Error as error:
                print("Failed to update data into sqlite table", error)
            finally:
                if (connection):
                    connection.close()
                    print("The SQLite connection is closed")


    return redirect(url_for('player_info', playerId=playerId))

if __name__ == '__main__':
    app.run(debug=True)