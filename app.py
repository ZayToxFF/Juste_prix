from flask import Flask, render_template, request
import random
import time

app = Flask(__name__)
i = 1
pseudo = "Guest"
message = ""
cible = 0  # Déclarer cible en dehors des routes pour éviter des erreurs

@app.route('/')
def debut():
    global i,cible
    i = 1
    cible = random.randint(1, 100)

    return render_template('index.html')

@app.route('/loading', methods=['GET', 'POST'])
def loading_page():
    global pseudo,cible
    

    if request.method == 'POST':
        pseudo = request.form['pseudo']

    time.sleep(2)
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
            i += 1
            if essai == cible:
                message = "WIN !!!"
                time.sleep(3)
                return render_template('index.html')
            elif i > 10:
                message = "Lost..."
                time.sleep(3)
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
