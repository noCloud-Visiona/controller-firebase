from firebase import db, bucket
from flask import jsonify, request

def get_next_available_filename(full_filename, folder):
    # Obtém a lista de blobs no bucket no diretório específico
    blobs = bucket.list_blobs(prefix=f'{folder}/')
    
    # Divide o nome do arquivo e a extensão
    base_name, extension = full_filename.rsplit('.', 1)
    
    # Cria uma lista de nomes de arquivos existentes que começam com o nome base
    existing_filenames = [blob.name for blob in blobs if blob.name.startswith(f'{folder}/{base_name}')]

    if f'{folder}/{full_filename}' not in existing_filenames:
        # Se o nome base não existe, retorna o nome original
        return full_filename
    else:
        # Caso contrário, busca o próximo número disponível
        i = 1
        new_filename = f'{base_name}_{i}.{extension}'
        while f'{folder}/{new_filename}' in existing_filenames:
            i += 1
            new_filename = f'{base_name}_{i}.{extension}'
        return new_filename

def upload_image_original():
    # Verifica se as imagens estão presentes na requisição
    if 'original' not in request.files:
        return jsonify({"error": "A imagem 'original' é necessária."}), 400

    original_image = request.files['original']
    mime_type = original_image.content_type or 'image/png'

    # Verifica se já existe uma imagem com o mesmo nome e gera o próximo nome disponível
    available_name = get_next_available_filename(original_image.filename, 'imagens/original')

    mime_type = original_image.content_type or 'image/png'
    original_blob = bucket.blob(f'imagens/original/{available_name}')
    original_blob.upload_from_file(original_image, content_type=mime_type)
    original_blob.make_public()

    # Gera a URL da imagem
    original_url = original_blob.public_url

    return jsonify({
        "original_url": original_url,
    }), 200
