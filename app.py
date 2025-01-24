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
        duration = int(request.args.get('duration', default=5))  # Durée en secondes

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

        # Lire la bande son du dossier "sound"
        audio_files = [os.path.join(sound_folder, f) for f in os.listdir(sound_folder) 
                       if f.endswith('.mp3') or f.endswith('.wav')]
        if audio_files:
            background_audio = AudioFileClip(audio_files[0])  # Utiliser le premier fichier audio trouvé
        else:
            background_audio = None

        # Générer une voix à partir du texte
        tts = gTTS(text, lang='fr')  # Générer la voix en français
        tts_path = os.path.join(output_folder, "tts_audio.mp3")
        tts.save(tts_path)
        tts_audio = AudioFileClip(tts_path)

        # Combiner les pistes audio
        if background_audio or tts_audio:
            audio_clips = []
            if background_audio:
                audio_clips.append(background_audio)
            if tts_audio:
                audio_clips.append(tts_audio)
            final_audio = CompositeAudioClip(audio_clips)
            clip = clip.set_audio(final_audio)

        # Ajouter du texte à la vidéo
        txt_clip = TextClip(text, fontsize=50, color='white', bg_color='black')
        txt_clip = txt_clip.set_position('bottom').set_duration(clip.duration)
        clip = CompositeVideoClip([clip, txt_clip])

        # Ajuster la durée de la vidéo
        if duration > 0:
            clip = clip.set_duration(duration)

        # Sauvegarder la vidéo finale
        video_path = os.path.join(output_folder, "output_video.mp4")
        clip.write_videofile(video_path, codec='libx264')

        # Renvoyer la vidéo générée
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)