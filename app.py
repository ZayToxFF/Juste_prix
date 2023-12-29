from flask import Flask, render_template, request
import random
import time

app = Flask(__name__)
i = None
cible = None
pseudo = None
message = ""

@app.route('/')
def debut():
    global i, cible
    i = 1
    # Tirage d'un prix (entier) au hasard entre 1 et 10
    cible = random.randint(1, 10)
    return render_template('index.html')

@app.route('/loading')
def loading_page():
    # Supposons que vous effectuiez un traitement ou une requête ici
    # Simulons un délai de chargement de 3 secondes
    time.sleep(3)
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
            message = "Veuillez entrer un nombre valide."
        else:
            i += 1
            if cible == essai:
                message = "BRAVO !!!"
                return render_template('index.html')
                i = 1
            elif i > 5:
                message = "PERDU..."
                i = 1
                return render_template('index.html')

            elif cible > essai:
                message = "PAS ASSEZ..."
            else:
                message = "TROP ELEVE..."

    return render_template('essai.html', i=i, pseudo=pseudo, message=message)

