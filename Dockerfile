FROM python:3.9

# Mettre à jour les dépôts et installer les dépendances système
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    fonts-dejavu \
    fonts-freefont-ttf \
    fonts-liberation \  
    # Polices supplémentaires
    fonts-opensymbol \  
    # Polices supplémentaires
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

RUN apt-get update && apt-get install -y ghostscript

# Assurez-vous que le binaire convert est accessible
ENV IMAGEMAGICK_BINARY=/usr/bin/convert

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY app.py .
COPY images/ ./images/
# Remplacer la politique de sécurité
COPY policy.xml /etc/ImageMagick-6/policy.xml 

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 5000
EXPOSE 5000

# Commande à exécuter
CMD ["python", "app.py"]