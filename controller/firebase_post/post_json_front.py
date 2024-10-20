from firebase import db, bucket
from flask import jsonify, request

def post_json_front():
    # Recebe o JSON da requisição
    json_data = request.get_json()

    # Referência à coleção no Firestore
    collection_ref = db.collection("historico_imagens_ia")

    try:
        # Conta quantos documentos já existem para o usuário, para criar um ID único
        docs = collection_ref.where("id_usuario", "==", json_data['identificacao_ia'].get('id_usuario')).stream()
        doc_count = sum(1 for _ in docs)
    except Exception as e:
        # Se ocorrer algum erro ao contar documentos, o doc_count será 0
        doc_count = 0
        print(f"Erro ao buscar documentos no Firestore: {e}")

    id_imagem_final = f"{json_data['identificacao_ia'].get('id')}_{doc_count + 1}"

    def transform_coordinate_array(coordinates):
            transformed = {}
            for i, coordinate_set in enumerate(coordinates[0], start=1):  # Acessa o array aninhado
                transformed[f"coordinate{i}"] = {
                    "longitude": coordinate_set[0],
                    "latitude": coordinate_set[1]
                }
            return transformed

    # Transforma as coordenadas em geometry
    transformed_geometry = {
        "type": json_data['geometry'].get('type', None),
        "coordinates": transform_coordinate_array(json_data['geometry'].get('coordinates', []))
    }

    # Transforma as coordenadas em user_geometry
    transformed_user_geometry = {
        "type": json_data['user_geometry'].get('type', None),
        "coordinates": transform_coordinate_array(json_data['user_geometry'].get('coordinates', []))
    }

    # Prepara o JSON final com os dados necessários
    jsonFinal = {
        "type": json_data.get('type', None),
        "id": id_imagem_final,
        "id_usuario": json_data['identificacao_ia'].get('id_usuario', None),
        "collection": json_data.get('collection', None),
        "stac_version": json_data.get('stac_version', None),
        "stac_extensions": json_data.get('stac_extensions', []),  
        "data": json_data['identificacao_ia'].get('data', None),
        "hora": json_data['identificacao_ia'].get('hora', None),
        "geometry": transformed_geometry,
        "links": [
            {
                "href": link.get('href'),
                "rel": link.get('rel')
            } for link in json_data.get('links', [])  
        ],
        "bbox": json_data.get('bbox', None),
        "assets": {
            "EVI": {
                "href": json_data['assets']['EVI'].get('href', None),
                "type": json_data['assets']['EVI'].get('type', None),
                "roles": json_data['assets']['EVI'].get('roles', []),  
                "created": json_data['assets']['EVI'].get('created', None),
                "updated": json_data['assets']['EVI'].get('updated', None),
                "bdc:size": json_data['assets']['EVI'].get('bdc:size', None),
                "bdc:chunk_size": json_data['assets']['EVI'].get('bdc:chunk_size', None),
                "bdc:raster_size": json_data['assets']['EVI'].get('bdc:raster_size', None),
                "checksum:multihash": json_data['assets']['EVI'].get('checksum:multihash', None)
            },
            "thumbnail": {
                "href": json_data['assets']['thumbnail'].get('href', None),
                "type": json_data['assets']['thumbnail'].get('type', None),
                "roles": json_data['assets']['thumbnail'].get('roles', []),  
                "created": json_data['assets']['thumbnail'].get('created', None),
                "updated": json_data['assets']['thumbnail'].get('updated', None),
                "bdc:size": json_data['assets']['thumbnail'].get('bdc:size', None),
                "checksum:multihash": json_data['assets']['thumbnail'].get('checksum:multihash', None)
            }
        },
        "properties": {
            "datetime": json_data['properties'].get('datetime', None),
            "start_datetime": json_data['properties'].get('start_datetime', None),
            "end_datetime": json_data['properties'].get('end_datetime', None),
            "created": json_data['properties'].get('created', None),
            "updated": json_data['properties'].get('updated', None),
            "eo:cloud_cover": json_data['properties'].get('eo:cloud_cover', None)
        },
        "user_geometry": transformed_user_geometry,
        "identificacao_ia": {
            "id": id_imagem_final,
            "area_visivel_mapa": json_data['identificacao_ia'].get('area_visivel_mapa', None),
            "percentual_nuvem": json_data['identificacao_ia'].get('percentual_nuvem', None),
            "percentual_sombra_nuvem": None,
            "img_original_png": json_data['identificacao_ia'].get('img_original_png', None),
            "img_original_tiff": json_data['identificacao_ia'].get('img_original_tiff', None),
            "img_tratada": json_data['identificacao_ia'].get('img_tratada', None),
            "mask_nuvem": json_data['identificacao_ia'].get('mask_nuvem', None),
            "mask_sombra": None,
            "tiff_tratado": None,
            "resolucao_imagem_png": json_data['identificacao_ia'].get('resolucao_imagem_png', None),
            "resolucao_imagem_tiff": None,
            "bbox": json_data['identificacao_ia'].get('bbox', None)
        }
    }

    # Adiciona o JSON final à coleção no Firestore
    collection_ref.add(jsonFinal)

    # Retorna o JSON final como resposta
    return jsonify(jsonFinal), 201