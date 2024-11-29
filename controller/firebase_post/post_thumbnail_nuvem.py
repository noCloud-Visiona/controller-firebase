from firebase import db, bucket
from flask import jsonify, request

def get_next_available_filename(full_filename, folder):
    """
    Gera o próximo nome de arquivo disponível no bucket.
    """
    # Obtém a lista de blobs no bucket no diretório específico
    blobs = bucket.list_blobs(prefix=f'{folder}/')
    
    # Dividindo o nome e a extensão
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

def upload_thumbnail_nuvem():
    """
    Faz o upload de um thumbnail de nuvem para o Firebase e retorna a URL pública.
    """
    # Verifica se o arquivo está presente na requisição
    if 'thumbnail_nuvem' not in request.files:
        return jsonify({"error": "O thumbnail 'thumbnail_nuvem' é necessário."}), 400

    thumbnail_image = request.files['thumbnail_nuvem']
    mime_type = thumbnail_image.content_type or 'image/png'
    
    # Verifica se já existe um arquivo com o mesmo nome e gera o próximo nome disponível
    available_name = get_next_available_filename(thumbnail_image.filename, 'thumbnails/nuvem')
    
    thumbnail_blob = bucket.blob(f'thumbnails/nuvem/{available_name}')
    thumbnail_blob.upload_from_file(thumbnail_image, content_type=mime_type)
    thumbnail_blob.make_public()

    # Gera a URL do thumbnail
    thumbnail_url = thumbnail_blob.public_url

    print(thumbnail_url)

    return jsonify({
        "thumbnail_nuvem_url": thumbnail_url,
    })
