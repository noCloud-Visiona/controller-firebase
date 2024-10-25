from firebase import db
from flask import jsonify

def transformar_coordenadas(coordenadas):
    # Verifica se coordenadas é None
    if coordenadas is None:  
        return []  
    ordered_keys = sorted(coordenadas.keys())
    # Converte para uma lista de listas em ordem
    return [[coordenadas[key]["longitude"], coordenadas[key]["latitude"]] for key in ordered_keys]

def get_historico(id_usuario):
    collection_ref = db.collection("historico_imagens_ia")
    documentos = collection_ref.where("id_usuario", "==", id_usuario).stream()

    historico = []
    for doc in documentos:
        item = doc.to_dict()

        # Transforma "geometry" se existir e tem coordenadas válidas
        if "geometry" in item and "coordinates" in item["geometry"]:
            coordinates = item["geometry"]["coordinates"]
            if coordinates is not None:  # Verifica se não é None
                item["geometry"]["coordinates"] = [transformar_coordenadas(coordinates)]

        # Transforma "user_geometry" se existir e tem coordenadas válidas
        if "user_geometry" in item and "coordinates" in item["user_geometry"]:
            user_coordinates = item["user_geometry"]["coordinates"]
            if user_coordinates is not None:  # Verifica se não é None
                item["user_geometry"]["coordinates"] = [transformar_coordenadas(user_coordinates)]

        historico.append(item)

    return jsonify(historico)
