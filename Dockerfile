# Utiliser une image Python officielle
FROM python:3.9-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt .
COPY app.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Commande à exécuter lorsque le conteneur démarre
CMD ["python", "app.py"]