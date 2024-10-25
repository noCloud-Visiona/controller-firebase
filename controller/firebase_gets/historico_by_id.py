from firebase import db
from flask import jsonify

def transformar_coordenadas(coordenadas):
    # Ordena as coordenadas pela chave (coordinate1, coordinate2, ...)
    ordered_keys = sorted(coordenadas.keys())
    # Converte para uma lista de listas em ordem
    return [[coordenadas[key]["longitude"], coordenadas[key]["latitude"]] for key in ordered_keys]

def get_historico(id_usuario):
    collection_ref = db.collection("historico_imagens_ia")
    documentos = collection_ref.where("id_usuario", "==", id_usuario).stream()

    historico = []
    for doc in documentos:
        item = doc.to_dict()

        # Transforma "geometry" se existir
        if "geometry" in item and "coordinates" in item["geometry"]:
            item["geometry"]["coordinates"] = [transformar_coordenadas(item["geometry"]["coordinates"])]

        # Transforma "user_geometry" se existir
        if "user_geometry" in item and "coordinates" in item["user_geometry"]:
            item["user_geometry"]["coordinates"] = [transformar_coordenadas(item["user_geometry"]["coordinates"])]

        historico.append(item)

    return jsonify(historico)
