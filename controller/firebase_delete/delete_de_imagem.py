from firebase import db, bucket
from flask import jsonify

def delete_image(id_imagem, id_usuario):
    collection_ref = db.collection("historico_imagens_ia")

    # Recupera o documento que tem o campo "id_imagem" e "id_usuario" igual ao fornecido
    documentos = collection_ref.where("id_imagem", "==", id_imagem).where("id_usuario", "==", id_usuario).stream()

    doc_to_delete = None
    for doc in documentos:
        doc_to_delete = doc
        break

    if not doc_to_delete:
        return jsonify({"message": "Imagem não encontrada ou não pertence ao usuário"}), 404

    # Pegando os dados do documento
    doc_data = doc_to_delete.to_dict()
    original_url = doc_data.get("thumbnail")
    treated_url = doc_data.get("img_tratada")

    try:
        # Extrair o caminho do bucket a partir das URLs
        if original_url:
            original_blob_name = "/".join(original_url.split("/")[-3:])  # Obtém o caminho relativo do blob
            bucket.delete_blob(original_blob_name)

        if treated_url:
            treated_blob_name = "/".join(treated_url.split("/")[-3:])  # Obtém o caminho relativo do blob
            bucket.delete_blob(treated_blob_name)

        # Deletando o documento do Firestore
        doc_to_delete.reference.delete()

        return jsonify({"message": "Imagem deletada com sucesso"}), 200

    except Exception as e:
        return jsonify({"message": f"Erro ao deletar imagem: {str(e)}"}), 500