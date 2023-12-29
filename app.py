from flask import Flask, render_template, request
import random
import time

app = Flask(__name__)
i = 1
cible = 0
pseudo = "Guest"
message = ""

@app.route('/')
def debut():
    global i
    i = 1
    return render_template('index.html')

@app.route('/loading')
def loading_page():
    time.sleep(2)
    global pseudo,cible

    cible = random.randint(1, 100)
    pseudo = request.values['pseudo']
    return render_template('loading.html', pseudo=pseudo)

@app.route('/essai', methods=['GET', 'POST'])
def essai():
    global i,cible, pseudo, message

    if request.method == 'POST':
        try:
            essai = int(request.form['essai'])
        except ValueError:
            message = "Please enter a valid number."
        else:
            i += 1
            if cible == essai:
                message = "WIN !!!"
                i = 1  # Déplacer cette ligne ici
                time.sleep(3)                
                return render_template('index.html')
            elif i > 10:
                message = "Lost..."
                i = 1
                time.sleep(3)
                return render_template('index.html')

            elif cible > essai:
                message = "NOT ENOUGH..."
            else:
                message = "TOO HIGH..."

    return render_template('essai.html', i=i, pseudo=pseudo, message=message, cible=cible)

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"An error occurred: {str(e)}")
    return "Internal Server Error", 500
