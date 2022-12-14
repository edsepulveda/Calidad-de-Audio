from flask import Flask, request
from flask_pymongo import PyMongo
from pydub import silence
from function import total_silence, final_silence, wait_time
from flask_cors import CORS
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb+srv://sebachaa:125230Seba.@firstcluster.dxsmkyn.mongodb.net/test'

mongo = PyMongo(app)


@app.route('/silence', methods=['POST'])
def silenceAPI():
    # Audio request
    req_audio = request.files['files']
    extension = req_audio.filename.split(".")[-1]
    if extension == "mp3":
        audio = AudioSegment.from_mp3(req_audio)
    elif extension == "wav":
        audio = AudioSegment.from_wav(req_audio)
    else:
        return {'msg': 'Formato no compatible, Pruebe con .mp3 y .wav'}

    silence_detect = silence.detect_silence(
        audio, min_silence_len=1000, silence_thresh=audio.dBFS-6)

    audio_duration = audio.duration_seconds
    if silence_detect:
        # Detectar silencio en segundos, para esto puedes dividir por 1000 para convertir de ms a s
        silence_ranges = [((start / 1000), (stop / 1000))
                          # Retorna tuplas con rangos de silencios detectados (start, stop)
                          for start, stop in silence_detect]

        # Tiempo de espera

        initial_silence, initial_percentage = wait_time(
            silence_ranges, audio_duration)

        # Silencio total

        silence_total = total_silence(silence_ranges)

        # Silencio final

        silence_final, final_percentage = final_silence(
            silence_ranges, audio_duration)
    else:
        # Si el audio no tiene silencio, inicializa las variables en 0
        initial_silence = initial_percentage = silence_total = silence_final = final_percentage = 0

    if initial_silence and initial_percentage and silence_total and silence_final and final_percentage and audio_duration:

        # Devolver las variables
        id = mongo.db.silence.insert_one({
            'initial_silence': initial_silence,
            'percentage_initial': initial_percentage,
            'total_silence': silence_total,
            'audio_duration': audio_duration,
            'final_silence': silence_final,
            'percentage_final': final_percentage
        }).inserted_id

        response = {
            'id': str(id),
            'initial_silence': initial_silence,
            'percentage_initial': initial_percentage,
            'total_silence': silence_total,
            'audio_duration': audio_duration,
            'final_silence': silence_final,
            'percentage_final': final_percentage
        }
        return response

    else:
        return {'msg': 'Error al calcular silencio. Consultar con Admin'}


if __name__ == "__main__":
    app.run(debug=True)  # Cambiar a false
