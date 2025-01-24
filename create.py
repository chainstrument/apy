from moviepy.editor import ImageSequenceClip
from PIL import Image
import os

# Taille cible (largeur, hauteur)
target_size = (640, 480)

# Dossier contenant les images
input_folder = 'images'
output_folder = 'resized_images'

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(output_folder, exist_ok=True)

# Redimensionner toutes les images
resized_images = []
for image_file in os.listdir(input_folder):
    if image_file.endswith('.jpg') or image_file.endswith('.png'):
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, image_file)

        # Ouvrir et redimensionner l'image
        with Image.open(input_path) as img:
            img_resized = img.resize(target_size)
            img_resized.save(output_path)
        
        # Ajouter le chemin de l'image redimensionnée à la liste
        resized_images.append(output_path)

# Créer une vidéo à partir des images redimensionnées
clip = ImageSequenceClip(resized_images, fps=1)

# Sauvegarder la vidéo
clip.write_videofile("/app/output/output_video.mp4")

print("Vidéo générée avec succès !")