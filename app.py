from flask import Flask, render_template, request
import random
import time
from threading import Lock

app = Flask(__name__)
lock = Lock()
i = 1
cible = None
pseudo = "Guest"
message = ""

@app.route('/')
def debut():
    global i, cible
    with lock:
        i = 1
        # Tirage d'un prix (entier) au hasard entre 1 et 100 si cible n'est pas encore initialisée
        if cible is None:
            cible = random.randint(1, 100)
    return render_template('index.html')

@app.route('/loading')
def loading_page():
    # Supposons que vous effectuiez un traitement ou une requête ici
    # Simulons un délai de chargement de 3 secondes
    time.sleep(2)
    global pseudo
    pseudo = request.values['pseudo']
    return render_template('loading.html', pseudo=pseudo)

@app.route('/essai', methods=['GET', 'POST'])
def essai():
    global i, cible, pseudo, message

    if request.method == 'POST':
        try:
            essai = int(request.form['essai'])
        except ValueError:
            message = "Please enter a valid number."
        else:
            with lock:
                i += 1
                if cible == essai:
                    message = "WIN !!!"
                    i = 1
                    # Réinitialiser cible si vous le souhaitez
                    cible = None
                    return render_template('index.html')
                elif i > 5:
                    message = "Lost..."
                    i = 1
                    # Réinitialiser cible si vous le souhaitez
                    cible = None
                    return render_template('index.html')
                elif cible > essai:
                    message = "NOT ENOUGH..."
                else:
                    message = "TOO HIGH..."

    return render_template('essai.html', i=i, pseudo=pseudo, message=message)

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"An error occurred: {str(e)}")
    return "Internal Server Error", 500


