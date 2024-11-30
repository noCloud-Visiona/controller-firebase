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

def upload_mask_sombra():
    """
    Faz o upload de uma máscara de sombra para o Firebase e retorna a URL pública.
    """
    # Verifica se o arquivo está presente na requisição
    if 'mask_sombra' not in request.files:
        return jsonify({"error": "A máscara 'mask_sombra' é necessária."}), 400

    mask_image = request.files['mask_sombra']
    mime_type = mask_image.content_type or 'image/png'
    
    # Verifica se já existe um arquivo com o mesmo nome e gera o próximo nome disponível
    available_name = get_next_available_filename(mask_image.filename, 'masks/sombra')
    
    mask_blob = bucket.blob(f'masks/sombra/{available_name}')
    mask_blob.upload_from_file(mask_image, content_type=mime_type)
    mask_blob.make_public()

    # Gera a URL da máscara
    mask_url = mask_blob.public_url

    print(mask_url)

    return jsonify({
        "mask_sombra_url": mask_url,
    })
