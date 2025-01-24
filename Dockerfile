FROM python:3.9

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY app.py .
COPY images/ ./images/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande à exécuter
CMD ["python", "app.py"]