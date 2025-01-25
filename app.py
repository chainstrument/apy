from flask import Flask, request, jsonify, send_file
from moviepy.editor import (
    ImageSequenceClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip, ColorClip
)
from gtts import gTTS
from PIL import Image
import os

app = Flask(__name__)

# Taille cible (largeur, hauteur)
target_size = (640, 480)

# Dossiers
images_folder = 'images'
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

@app.route('/generate-video', methods=['GET'])
def generate_video():
    try:
        text = request.args.get('text', default="Ceci est un texte par défaut")

        # Lire les images du dossier
        image_files = [os.path.join(images_folder, f) for f in os.listdir(images_folder) if f.endswith(('.jpg', '.png'))]
        if not image_files:
            return jsonify({"error": "Aucune image trouvée dans le dossier 'images'"}), 400

        # Redimensionner les images et préserver les proportions
        resized_images = []
        for image_file in image_files:
            with Image.open(image_file) as img:
                img.thumbnail(target_size, Image.ANTIALIAS)
                resized_path = os.path.join(output_folder, os.path.basename(image_file))
                img.save(resized_path)
                resized_images.append(resized_path)

        # Créer une vidéo avec des images redimensionnées
        clip = ImageSequenceClip(resized_images, fps=1)

        # Ajouter un arrière-plan noir si nécessaire
        background_clip = ColorClip(size=target_size, color=(0, 0, 0), duration=clip.duration)
        clip = CompositeVideoClip([background_clip, clip.set_position('center')])

        # Générer une voix à partir du texte
        tts = gTTS(text, lang='fr')
        tts_path = os.path.join(output_folder, "tts_audio.mp3")
        tts.save(tts_path)
        tts_audio = AudioFileClip(tts_path)

        # Durée de la vidéo
        video_duration = tts_audio.duration
        clip = clip.set_duration(video_duration)

        # Afficher le texte par groupe de mots
        words = text.split()
        group_size = 3
        word_groups = [" ".join(words[i:i+group_size]) for i in range(0, len(words), group_size)]
        word_duration = video_duration / len(word_groups)
        text_clips = []

        for i, group in enumerate(word_groups):
            start_time = i * word_duration
            txt_clip = TextClip(
                group,
                fontsize=50,
                color='yellow',
                font='Arial',
                stroke_color='black',
                stroke_width=2
            ).set_position('center').set_start(start_time).set_duration(word_duration)
            text_clips.append(txt_clip)

        # Ajouter les clips texte
        final_text_clip = CompositeVideoClip(text_clips)

        # Combiner texte et vidéo
        final_clip = CompositeVideoClip([clip, final_text_clip]).set_audio(tts_audio)

        # Sauvegarder la vidéo finale
        video_path = os.path.join(output_folder, "output_video.mp4")
        final_clip.write_videofile(video_path, codec='libx264', fps=24)

        # Nettoyage des fichiers temporaires
        os.remove(tts_path)
        for resized_image in resized_images:
            os.remove(resized_image)

        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
