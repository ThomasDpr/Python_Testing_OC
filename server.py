import json
from datetime import datetime

from email_validator import EmailNotValidError, validate_email
from flask import Flask, flash, redirect, render_template, request, url_for


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


# Ancien code :

# @app.route('/showSummary',methods=['POST'])
# def showSummary():
#     club = [club for club in clubs if club['email'] == request.form['email']][0]
#     return render_template('welcome.html',club=club,competitions=competitions)

# Nouveau code (correction Issues #1) :

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        # Récupérer l'email du formulaire et supprimer les espaces autour
        email = request.form['email'].strip()  # strip() pour enlever les espaces 
        
        # Vérifier si l'email est vide
        if not email:
            flash("Email field is required")  # Message d'erreur si le champ email est vide
            return redirect(url_for('index'))  # Rediriger vers la page d'accueil
            
        # Valider le format de l'email
        # check_deliverability=False car on ne veut pas vérifier si le domaine peut réellement envoyer des emails
        # On vérifie uniquement la syntaxe de l'email (présence de @, format correct)
        # Sans cette option, les domaines fictifs comme irontemple.com seraient rejetés
        validate_email(email, check_deliverability=False)
        
        # Chercher le club correspondant à l'email
        club = [club for club in clubs if club['email'] == email][0]  # Trouver le club avec l'email donné
        return render_template('welcome.html', club=club, competitions=competitions)  # Afficher la page de bienvenue avec les informations du club et des compétitions
        
    except EmailNotValidError:
        # Si le format de l'email est invalide même si dans l'html on met le type="email" 
        flash("Invalid email format")  # Message d'erreur pour un format d'email invalide
    except IndexError:
        # Si l'email n'est pas trouvé dans la liste des clubs
        flash("Sorry, that email wasn't found.")  # Message d'erreur si l'email n'existe pas
    
    # Rediriger vers la page d'accueil en cas d'erreur
    return redirect(url_for('index'))


# Ancien code (correction Issues #5) :
# @app.route('/book/<competition>/<club>')
# def book(competition,club):
#     foundClub = [c for c in clubs if c['name'] == club][0]
#     foundCompetition = [c for c in competitions if c['name'] == competition][0]
#     if foundClub and foundCompetition:
#         return render_template('booking.html',club=foundClub,competition=foundCompetition)
#     else:
#         flash("Something went wrong-please try again")
#         return render_template('welcome.html', club=club, competitions=competitions)


# Nouveau code (correction Issues #5) :
def is_past_competition(competition_date_str):
    competition_date = datetime.strptime(competition_date_str, "%Y-%m-%d %H:%M:%S")
    return competition_date < datetime.now()

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    
    if foundClub and foundCompetition:
        # Utiliser la méthode pour vérifier si la compétition est passée
        if is_past_competition(foundCompetition['date']):
            flash(f"Cannot book {foundCompetition['name']} because it is a past competition")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
            
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)
# Ancien code (correction Issues #2) :
# @app.route('/purchasePlaces',methods=['POST'])
# def purchasePlaces():
#     competition = [c for c in competitions if c['name'] == request.form['competition']][0]
#     club = [c for c in clubs if c['name'] == request.form['club']][0]
#     placesRequired = int(request.form['places'])
#     competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
#     flash('Great-booking complete!')
#     return render_template('welcome.html', club=club, competitions=competitions)

# Nouveau code (correction Issues #2) :
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    # Récupérer la compétition et le club à partir des données du formulaire
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Si un compet est passé alors : 
        # pass

    # Bonus
    # Vérifier si le nombre de places est positif
    if placesRequired <= 0:
        flash('You cannot book a negative or null number of places')
        return render_template('welcome.html', club=club, competitions=competitions)


    # Vérifier les points disponibles
    club_points = int(club['points'])
    if placesRequired > club_points:
        flash('Not enough points available!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérifier si le nombre de places demandées dépasse la limite de 12
    if placesRequired > 12:
        flash('You can only book up to 12 places per competition')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérifier si suffisamment de places sont disponibles dans la compétition
    competition_places = int(competition['numberOfPlaces'])
    if placesRequired > competition_places:
        flash('Not enough places available in the competition!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Mettre à jour les points du club et les places de la compétition
    club['points'] = club_points - placesRequired
    competition['numberOfPlaces'] = competition_places - placesRequired

    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)
# TODO: Add route for points display
@app.route('/points')
def points():
    clubs = loadClubs()
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)