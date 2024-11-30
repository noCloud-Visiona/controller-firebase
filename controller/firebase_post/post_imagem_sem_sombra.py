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

def upload_imagem_sem_sombra():
    """
    Faz o upload de uma imagem sem sombra para o Firebase e retorna a URL pública.
    """
    # Verifica se as imagens estão presentes na requisição
    if 'imagem_sem_sombra' not in request.files:
        return jsonify({"error": "A imagem 'imagem_sem_sombra' é necessária."}), 400

    sem_sombra_image = request.files['imagem_sem_sombra']
    mime_type = sem_sombra_image.content_type or 'image/png'
    
    # Verifica se já existe uma imagem com o mesmo nome e gera o próximo nome disponível
    available_name = get_next_available_filename(sem_sombra_image.filename, 'imagens/sem_sombra')
    
    sem_sombra_blob = bucket.blob(f'imagens/sem_sombra/{available_name}')
    sem_sombra_blob.upload_from_file(sem_sombra_image, content_type=mime_type)
    sem_sombra_blob.make_public()

    # Gera a URL da imagem
    sem_sombra_url = sem_sombra_blob.public_url

    print(sem_sombra_url)

    return jsonify({
        "imagem_sem_sombra_url": sem_sombra_url,
    })
