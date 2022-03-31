import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    choice = None
    for club in clubs:
        if club['email'] == request.form['email']:
            choice = club
    if not choice:
        return render_template('index.html', errors=['This email doesn\'t exist'])
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    date = foundCompetition['date']
    if datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]), int(date[17:19])) < datetime.now():
        flash("This competition has already happened, you can\'t book places for it'")
        return render_template('welcome.html', club=foundClub, competitions=competitions)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if int(club['points']) < placesRequired:
        flash('You are not allowed to book more places than your amount of points')
        return render_template('welcome.html', club=club, competitions=competitions)
    clubPlaceBooked = getattr(club['booked'], competition['name'], None)
    if (clubPlaceBooked and clubPlaceBooked + placesRequired > 12 ) or placesRequired > 12:
        return render_template('welcome.html',club=club,competitions=competitions, errors=['You can\'t book more than 12 places in 1 competition'])
    else:
        club['booked'][competition['name']] = placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))