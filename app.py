from flask import Flask, request, jsonify, send_file
from moviepy.editor import ImageSequenceClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from gtts import gTTS
from PIL import Image
import os

app = Flask(__name__)

# Taille cible (largeur, hauteur)
target_size = (640, 480)

# Dossiers
images_folder = 'images'
sound_folder = 'sound'
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

@app.route('/generate-video', methods=['GET'])
def generate_video():
    try:
        # Récupérer les paramètres de l'URL
        text = request.args.get('text', default="Ceci est un texte par défaut")

        # Lire les images du dossier "images"
        image_files = [os.path.join(images_folder, f) for f in os.listdir(images_folder) 
                       if f.endswith('.jpg') or f.endswith('.png')]
        if not image_files:
            return jsonify({"error": "Aucune image trouvée dans le dossier 'images'"}), 400

        # Redimensionner les images
        resized_images = []
        for image_file in image_files:
            with Image.open(image_file) as img:
                img_resized = img.resize(target_size)
                resized_path = os.path.join(output_folder, os.path.basename(image_file))
                img_resized.save(resized_path)
                resized_images.append(resized_path)

        # Créer une vidéo à partir des images redimensionnées
        clip = ImageSequenceClip(resized_images, fps=1)

        # Générer une voix à partir du texte
        tts = gTTS(text, lang='fr')  # Générer la voix en français
        tts_path = os.path.join(output_folder, "tts_audio.mp3")
        tts.save(tts_path)
        tts_audio = AudioFileClip(tts_path)

        # Calculer la durée de la vidéo en fonction de la durée de l'audio
        video_duration = tts_audio.duration
        clip = clip.set_duration(video_duration)

        # Ajouter le texte mot par mot en synchronisation avec la voix
        words = text.split()
        word_duration = video_duration / len(words)  # Durée d'affichage par mot
        text_clips = []

        for i, word in enumerate(words):
            start_time = i * word_duration
            end_time = (i + 1) * word_duration

            # Créer un clip texte pour chaque mot
            txt_clip = TextClip(
                " ".join(words[:i + 1]),  # Afficher les mots jusqu'à l'index actuel
                fontsize=70,  # Taille du texte
                color='yellow',  # Couleur du texte
                font='DejaVuSans-Bold',  # Police en gras
                stroke_color='black',  # Couleur de la bordure
                stroke_width=2  # Épaisseur de la bordure
            )
            txt_clip = txt_clip.set_position('center').set_duration(end_time - start_time).set_start(start_time)
            text_clips.append(txt_clip)

        # Combiner les clips texte
        final_text_clip = CompositeVideoClip(text_clips)

        # Combiner la vidéo et le texte
        final_clip = CompositeVideoClip([clip, final_text_clip])

        # Ajouter l'audio à la vidéo
        final_clip = final_clip.set_audio(tts_audio)

        # Sauvegarder la vidéo finale
        video_path = os.path.join(output_folder, "output_video.mp4")
        final_clip.write_videofile(video_path, codec='libx264')

        # Renvoyer la vidéo générée
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)