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

def upload_imagem_sombra():
    """
    Faz o upload de uma imagem de sombra para o Firebase e retorna a URL pública.
    """
    # Verifica se as imagens estão presentes na requisição
    if 'imagem_sombra' not in request.files:
        return jsonify({"error": "A imagem 'imagem_sombra' é necessária."}), 400

    sombra_image = request.files['imagem_sombra']
    mime_type = sombra_image.content_type or 'image/png'
    
    # Verifica se já existe uma imagem com o mesmo nome e gera o próximo nome disponível
    available_name = get_next_available_filename(sombra_image.filename, 'imagens/sombra')
    
    sombra_blob = bucket.blob(f'imagens/sombra/{available_name}')
    sombra_blob.upload_from_file(sombra_image, content_type=mime_type)
    sombra_blob.make_public()

    # Gera a URL da imagem
    sombra_url = sombra_blob.public_url

    print(sombra_url)

    return jsonify({
        "imagem_sombra_url": sombra_url,
    })
