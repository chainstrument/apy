# main.py
from flask import Flask

# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir une route pour la racine ("/")
@app.route('/')
def hello():
    return "Bonjdour, Flask !"

# Démarrer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)