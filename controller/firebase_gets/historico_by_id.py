from firebase import db
from flask import jsonify

def get_historico(id_usuario):
    collection_ref = db.collection("historico_imagens_ia")

    # Recuperando os documentos que têm o campo "id_usuario" igual ao valor passado
    documentos = collection_ref.where("id_usuario", "==", id_usuario).stream()

    # Criando uma lista para armazenar os dados
    historico = [doc.to_dict() for doc in documentos]

    return jsonify(historico)