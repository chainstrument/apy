from moviepy.editor import ImageSequenceClip

# Liste des chemins des images
image_files = ['image1.jpg', 'image2.jpg', 'image3.jpg']

# Créer une vidéo à partir des images
clip = ImageSequenceClip(image_files, fps=1)

# Sauvegarder la vidéo dans le dossier monté
output_path = "/app/output/output_video.mp4"
clip.write_videofile(output_path)

print(f"Vidéo générée : {output_path}")