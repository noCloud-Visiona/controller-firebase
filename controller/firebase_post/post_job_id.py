from firebase import db, bucket
from flask import jsonify, request

def post_job_id():
    # Recebe o JSON da requisição
    json_data = request.get_json()

    # Referência à coleção no Firestore
    collection_ref = db.collection("historico_job_id")

    try:
        # Conta quantos documentos já existem para o usuário, para criar um ID único
        docs = collection_ref.where("id_usuario", "==", json_data['id_usuario']).stream()
        doc_count = sum(1 for _ in docs)
    except Exception as e:
        # Se ocorrer algum erro ao contar documentos, o doc_count será 0
        doc_count = 0
        print(f"Erro ao buscar documentos no Firestore: {e}")

    id_imagem_final = f"{json_data['id_usuario']}_{doc_count + 1}"

    # Prepara o JSON final com os dados necessários
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

    # Salva o JSON no Firestore
    collection_ref.document(id_imagem_final).set(jsonFinal)

    return jsonify(jsonFinal), 201