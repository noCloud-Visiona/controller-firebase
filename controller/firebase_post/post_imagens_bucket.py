from firebase import db, bucket
from flask import jsonify, request

def upload_images():
    # Verifica se as imagens estão presentes na requisição
    if 'original' not in request.files or 'tratada' not in request.files:
        return jsonify({"error": "As imagens 'original' e 'tratada' são necessárias."}), 400

    original_image = request.files['original']
    tratada_image = request.files['tratada']

    # Salva a imagem original
    original_blob = bucket.blob(f'images/original/{original_image.filename}')
    original_blob.upload_from_file(original_image)
    original_blob.make_public()

    # Salva a imagem tratada
    tratada_blob = bucket.blob(f'images/tratada/{tratada_image.filename}')
    tratada_blob.upload_from_file(tratada_image)
    original_blob.make_public()

    # Gera as URLs das imagens
    original_url = original_blob.public_url
    tratada_url = tratada_blob.public_url

    return jsonify({
        "original_url": original_url,
        "tratada_url": tratada_url
    }), 200