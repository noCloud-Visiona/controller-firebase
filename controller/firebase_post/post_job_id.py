from firebase import db, bucket
from flask import jsonify, request

from firebase import db, bucket
from flask import jsonify, request

def post_job_id(id_usuario=None, job_id=None):
    json_data = request.get_json()

    if id_usuario:
        json_data['id_usuario'] = id_usuario
    if job_id:
        json_data['job_id'] = job_id

    collection_ref = db.collection("historico_job_id")

    try:
        docs = collection_ref.where("id_usuario", "==", json_data['id_usuario']).stream()
        doc_count = sum(1 for _ in docs)
    except Exception as e:
        doc_count = 0
        print(f"Erro ao buscar documentos no Firestore: {e}")

    id_imagem_final = f"{json_data['id_usuario']}_{doc_count + 1}"

    jsonFinal = {
        "id_usuario": json_data.get('id_usuario', None),
        "job_id": json_data.get('job_id', None),
        "data": json_data.get('data', None),
        "hora": json_data.get('hora', None),
        "status": json_data.get('status', None),
        "links": [
            {
                "href": link.get('href'),
                "rel": link.get('rel')
            } for link in json_data.get('links', [])  
        ]
    }

    collection_ref.document(id_imagem_final).set(jsonFinal)
    
    print(jsonFinal)

    return jsonify(jsonFinal), 201