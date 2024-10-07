from firebase import db
from flask import jsonify

def get_image(id_imagem, id_usuario):
    collection_ref = db.collection("historico_imagens_ia")

    # Recupera o documento que tem o campo "id_imagem" igual ao valor passado e "id_usuario" igual ao fornecido
    documentos = collection_ref.where("id_imagem", "==", id_imagem).where("id_usuario", "==", id_usuario).stream()

    doc_to_get = None
    for doc in documentos:
        doc_to_get = doc
        break

    if not doc_to_get:
        return jsonify({"message": "Imagem não encontrada ou não pertence ao usuário"}), 404

    # Pegando os dados do documento
    doc_data = doc_to_get.to_dict()

    resposta = {
        "id_usuario": doc_data.get("id_usuario"),
        "id_imagem": doc_data.get("id_imagem"),
        "data": doc_data.get("data"),
        "hora": doc_data.get("hora"),
        "geometry": doc_data.get("geometry"),
        "resolucao_imagem": doc_data.get("resolucao_imagem"),
        "satelite": doc_data.get("satelite"),
        "sensor": doc_data.get("sensor"),
        "percentual_nuvem": doc_data.get("percentual_nuvem"),
        "area_visivel_mapa": doc_data.get("area_visivel_mapa"),
        "thumbnail": doc_data.get("thumbnail"),
        "img_tratada": doc_data.get("img_tratada")
    }

    return jsonify(resposta), 200