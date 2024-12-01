from firebase import db
from flask import jsonify

def get_todos_jobs_id(id_usuario):
    # Referência à coleção "historico_job_id"
    collection_ref = db.collection("historico_job_id")
    
    # Filtra os documentos onde "id_usuario" é igual ao fornecido
    documentos = collection_ref.where("id_usuario", "==", id_usuario).stream()

    # Lista para armazenar todos os job_id encontrados
    job_ids = []

    # Itera pelos documentos filtrados
    for doc in documentos:
        item = doc.to_dict()
        # Verifica se o campo "job_id" existe no documento
        if "job_id" in item:
            job_ids.append(item["job_id"])

    # Retorna todos os job_id encontrados ou uma mensagem se não houver nenhum
    if job_ids:
        return jsonify({"job_ids": job_ids}), 200
    else:
        return jsonify({"message": "Nenhum job_id encontrado para o id_usuario fornecido"}), 404
