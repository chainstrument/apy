# Utiliser une image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt .
COPY app.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel Flask écoute
EXPOSE 5000

# Commande à exécuter lorsque le conteneur démarre
CMD ["python", "app.py"]