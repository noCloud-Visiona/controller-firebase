from firebase import db, bucket
from flask import jsonify, request

def upload_image_original():
    # Verifica se as imagens estão presentes na requisição
    if 'original' not in request.files:
        return jsonify({"error": "A imagem 'original' é necessária."}), 400

    original_image = request.files['original']

    # Salva a imagem original
    original_blob = bucket.blob(f'imagens/original/{original_image.filename}')
    original_blob.upload_from_file(original_image)
    original_blob.make_public()

    # Gera a URL da imagem
    original_url = original_blob.public_url

    return jsonify({
        "original_url": original_url,
    }), 200