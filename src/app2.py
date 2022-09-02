from flask import Flask, request
from flask_pymongo import PyMongo
from pydub import AudioSegment, silence
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb+srv://system:system@nodejs-cap9.dgqpz.mongodb.net/silencio'
# app.config['MONGO_URI'] = 'mongodb://grupo3:boovae9X@172.0.0.68/?authSource=Grupo3Duoc'
mongo = PyMongo(app)



@app.route('/silence', methods=['POST'])
def silenceAPI():
    # Audio request
    req_audio = request.files['files']

    # Validar extensión de audio
    extension = req_audio.filename.split(".")[-1]
    if extension == "mp3":
        audio = AudioSegment.from_mp3(req_audio)
    elif extension == "wav":
        audio = AudioSegment.from_wav(req_audio)
    else:
         return {'msg': 'Formato no compatible, Pruebe con .mp3 y .wav'}
         
    silence_detect = silence.detect_silence(
        audio, min_silence_len=1000, silence_thresh=audio.dBFS-6)
    seconds_duration = audio.duration_seconds
    if silence_detect:
        # Tiempo de espera

        # Detectar silencio en segundos, para esto puedes dividir por 1000 para convertir de ms a s
        silence_ranges = [((start / 1000), (stop / 1000))
                          # Retorna tuplas con rangos de silencios detectados (start, stop)
                          for start, stop in silence_detect]
        # Obtener la primera tupla (silencio inicial)
        position_silence = silence_ranges[0]
        # Si dentro de los primeros 3 segundos no hay "silencio", no será considero "silencio inicial"
        if position_silence[0] > 3:
            # Si no es considerado, se asignan los valores de 0 a las variables
            initial_percentage, initial_silence = 0, 0
        else:
            # Obtener el silencio en segundos (stop - start)
            initial_silence = float("{:.3f}".format(
                position_silence[1] - position_silence[0]))

            # Calcula el porcentaje que representa el silencio del total del audio
            initial_percentage = float("{:.3f}".format(
                initial_silence * 100 / seconds_duration))

        # Silencio total

        total_silence = 0
        for tuple in silence_ranges:
            # Obtener el silencio en segundos (stop - start)
            silence_seconds = float("{:.3f}".format(tuple[1]-tuple[0]))
            # Sumar el silencio en segundos
            total_silence += silence_seconds

        # Silencio final

        final_tuple = silence_ranges[-1][1]
        if final_tuple == seconds_duration:
            # Obtener el silencio en segundos (stop - start)
            final_silence = float("{:.3f}".format(
                silence_ranges[-1][1] - silence_ranges[-1][0]))
            # Calcula el porcentaje que representa el silencio del total del audio
            final_percentage = float("{:.3f}".format(
                final_silence * 100 / seconds_duration))
        else:
            # Si el audio no tiene silencio, inicializar las variables en 0
            final_silence, final_percentage = 0, 0

    else:
        # Si el audio no tiene silencio, inicializa las variables en 0
        initial_silence, initial_percentage, total_silence, final_silence, final_percentage = 0, 0, 0, 0, 0

    if initial_silence and initial_percentage and total_silence and final_silence and final_percentage and seconds_duration:

        # Devolver las variables
        id = mongo.db.silencio.insert_one({
            'initial_silence': initial_silence,
            'percentage_initial': initial_percentage,
            'total_silence': total_silence,
            'audio_duration': seconds_duration,
            'final_silence': final_silence,
            'percentage_final': final_percentage
        }).inserted_id

        response = {
            'id': str(id),
            'initial_silence': initial_silence,
            'percentage_initial': initial_percentage,
            'total_silence': total_silence,
            'audio_duration': seconds_duration,
            'final_silence': final_silence,
            'percentage_final': final_percentage
        }
        return response

    else:
        return {'msg': 'error'}


if __name__ == "__main__":
    app.run(debug=True)

