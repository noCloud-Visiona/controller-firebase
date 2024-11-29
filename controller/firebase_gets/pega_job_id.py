from firebase import db
from flask import jsonify

def get_job_id(id_usuario, job_id):
    collection_ref = db.collection("historico_job_id")
    documentos = collection_ref.where("id_usuario", "==", id_usuario).stream()

    for doc in documentos:
        item = doc.to_dict()
        if item["job_id"] == job_id:
            return jsonify(item), 201
    return jsonify({"message": "job_id não encontrado"}), 404