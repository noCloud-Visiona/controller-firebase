from firebase import db, bucket
from flask import jsonify, request

def upload_image_tratada():
    # Verifica se as imagens estão presentes na requisição
    if 'tratada' not in request.files:
        return jsonify({"error": "A imagem 'tratada' é necessário."}), 400

    tratada_image = request.files['tratada']

    # Salva a imagem tratada
    tratada_blob = bucket.blob(f'imagens/tratada/{tratada_image.filename}')
    tratada_blob.upload_from_file(tratada_image)
    tratada_blob.make_public()

    # Gera a URL da imagem
    tratada_url = tratada_blob.public_url

    print(tratada_url)

    return jsonify({
        "tratada_url": tratada_url
    })