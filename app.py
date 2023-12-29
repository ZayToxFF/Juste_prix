from flask import Flask, render_template, request
import random

app = Flask(__name__)
i = 1
pseudo = "Guest"
message = ""
cible = 0

def generate_target():
    return random.randint(1, 100)

@app.route('/')
def debut():
    global i, cible
    i = 1
    cible = generate_target()
    return render_template('index.html', cible=cible)

@app.route('/loading', methods=['GET', 'POST'])
def loading_page():
    global pseudo, cible

    if request.method == 'POST':
        pseudo = request.form['pseudo']

    return render_template('loading.html', pseudo=pseudo, cible=cible)

@app.route('/essai', methods=['GET', 'POST'])
def essai():
    global i, cible, pseudo, message

    if request.method == 'POST':
        try:
            essai = int(request.form['essai'])
            if not (1 <= essai <= 100):
                raise ValueError("Le nombre doit être entre 1 et 100.")
        except ValueError as e:
            message = str(e)
        else:
            i += 1
            if essai == cible:
                message = "WIN !!!"
                return render_template('index.html')
            elif i > 10:
                message = "Lost..."
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
