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
        # Initialiser cible uniquement si elle n'est pas déjà initialisée
        if cible is None:
            cible = random.randint(1, 100)
    return render_template('index.html')

@app.route('/loading')
def loading_page():
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
                if cible is not None:
                    i += 1
                    if cible == essai:
                        message = "WIN !!!"
                        i = 1
                        cible = None
                        return render_template('index.html')
                    elif i > 5:
                        message = "Lost..."
                        i = 1
                        cible = None
                        time.sleep(2)
                        return render_template('index.html')
                    elif cible > essai:
                        message = "NOT ENOUGH..."
                    else:
                        message = "TOO HIGH..."
                else:
                    message = "Error: cible is not initialized."

    return render_template('essai.html', i=i, pseudo=pseudo, message=message)



