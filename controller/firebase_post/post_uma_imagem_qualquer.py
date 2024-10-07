from firebase import db, bucket
from flask import jsonify, request

def upload_uma_imagem_qualquer():
    # Verifica se a imagem está presente na requisição
    if 'imagem' not in request.files:
        return jsonify({"error": "A imagem é necessária."}), 400

    imagem = request.files['imagem']

    # Salva a imagem na pasta 'imagem' do bucket
    blob = bucket.blob(f'imagens_qualquers/{imagem.filename}')
    blob.upload_from_file(imagem)
    blob.make_public()

    # Gera a URL da imagem
    imagem_url = blob.public_url

    return jsonify({
        "imagem_url": imagem_url
    }), 200
