from firebase import db, bucket
from flask import jsonify, request

def upload_image_nuvem():
    # Verifica se as imagens estão presentes na requisição
    if 'nuvem' not in request.files:
        return jsonify({"error": "A mask 'nuvem' é necessária."}), 400

    nuvem_image = request.files['nuvem']

    # Salva a imagem nuvem
    nuvem_blob = bucket.blob(f'imagens/nuvem/{nuvem_image.filename}')
    nuvem_blob.upload_from_file(nuvem_image)
    nuvem_blob.make_public()

    # Gera a URL da imagem
    nuvem_url = nuvem_blob.public_url

    print(nuvem_url)

    return jsonify({
        "nuvem_url": nuvem_url,
    })