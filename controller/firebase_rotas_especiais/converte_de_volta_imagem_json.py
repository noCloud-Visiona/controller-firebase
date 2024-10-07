from flask import request, jsonify, send_file
import base64
import json

def transforma_json_em_imagem(image_json, output_path):
    try:
        image_data = image_json.get("img_tratada", "")
        
        if not image_data:
            raise ValueError("Imagem não encontrada na chave 'img_tratada' do JSON")

        missing_padding = len(image_data) % 4
        if missing_padding:
            image_data += '=' * (4 - missing_padding)

        with open(output_path, "wb") as output_file:
            output_file.write(base64.b64decode(image_data))

        return True, "Imagem decodificada com sucesso"
    except json.JSONDecodeError as json_err:
        return False, f"Erro ao decodificar JSON: {str(json_err)}"
    except ValueError as val_err:
        return False, str(val_err)
    except Exception as e:
        return False, f"Erro ao decodificar a imagem: {str(e)}"