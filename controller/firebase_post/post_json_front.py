from firebase import db, bucket
from flask import jsonify, request

def post_json_front():
    # Recebe o JSON da requisição
    json_data = request.get_json()

    # Referência à coleção no Firestore
    collection_ref = db.collection("historico_imagens_ia")

    # Conta quantos documentos já existem para o usuário, para criar um ID único
    docs = collection_ref.where("id_usuario", "==", json_data['id_usuario']).stream()
    doc_count = sum(1 for _ in docs)

    id_imagem_final = f"{json_data['id_imagem']}_{doc_count + 1}"

    # Prepara o JSON final com os dados necessários
    jsonFinal = {
        "id_usuario": json_data['id_usuario'],
        "id_imagem": id_imagem_final,
        "data": json_data['data'],
        "hora": json_data['hora'],
        "geometry": json_data['geometry'],
        "resolucao_imagem": json_data['resolucao_imagem'],
        "satelite": json_data['satelite'],
        "sensor": json_data['sensor'],
        "percentual_nuvem": json_data['percentual_nuvem'],
        "area_visivel_mapa": json_data['area_visivel_mapa'],
        "imagem": json_data['imagem'],
        "thumbnail": json_data['thumbnail'],
        "img_tratada": json_data['img_tratada'],
    }

    # Adiciona o JSON final à coleção no Firestore
    collection_ref.add(jsonFinal)

    # Retorna o JSON final como resposta
    return jsonify(jsonFinal), 201