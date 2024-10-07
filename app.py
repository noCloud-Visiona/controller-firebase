from firebase import db, bucket, storage
from flask import Flask, request, jsonify, send_file
import base64
import json
from flask_cors import CORS

# GET
from controller.firebase_gets.historico_by_id import get_historico
from controller.firebase_gets.imagem_by_id import get_image

# POST
from controller.firebase_post.post_imagens_bucket import upload_images
from controller.firebase_post.post_json_front import post_json_front
from controller.firebase_post.post_uma_imagem_qualquer import upload_uma_imagem_qualquer

# DELETE
from controller.firebase_delete.delete_de_imagem import delete_image

# ESPECIAL
from controller.firebase_rotas_especiais.converte_de_volta_imagem_json import transforma_json_em_imagem

app = Flask(__name__)
CORS(app)

########## Rotas de Get #########

# Retorna todos os documentos/jsons de um usuário especifico
@app.route('/historico/<id_usuario>', methods=['GET'])
def historico_usuario(id_usuario):
    return get_historico(id_usuario), 200

# Retorna uma imagem especifica de um usuário
@app.route('/get_image/<id_imagem>/<id_usuario>', methods=['GET'])
def pega_imagem(id_imagem, id_usuario):
    return get_image(id_imagem, id_usuario), 200

########## Rotas de Post #########

# Salva o json do frontend completo no firebase
@app.route('/post_json', methods=['POST'])
def salva_json_do_usuario():
    return post_json_front(), 200
    
# Salva e retorna a URL da imagem "original" e "tratada" no bucket
@app.route('/upload_images', methods=['POST'])
def salvar_imagens():
    return upload_images(), 200

# Caso queira salvar alguma imagem não relacionada ao fluxo padrão no Bucket pra usar a URL dela
@app.route('/upload_de_uma_imagem_qualquer', methods=['POST'])
def salva_uma_imagem():
    return upload_uma_imagem_qualquer(), 200

########## Rotas de Delete #########

# Deleta uma imagem especifica de um usuário
@app.route('/delete_image/<id_imagem>/<id_usuario>', methods=['DELETE'])
def deletar_imagem(id_imagem, id_usuario):
    return delete_image(id_imagem, id_usuario)

######### Rotas Especiais ##########

# Transforma imagens em base64 de volta para imagem normal
@app.route('/show_image', methods=['POST'])
def exibe_imagem_json():
    json_data = request.get_json()

    # Chama a função para transformar a imagem codificada em um arquivo PNG
    success, mensagem = transforma_json_em_imagem(json_data, "IA/img/output_image.png")

    if success:
        try:
            return send_file("IA/img/output_image.png", mimetype='image/png'), 200
        except FileNotFoundError:
            return jsonify({"message": "Erro: Imagem não encontrada"}), 404
    else:
        return jsonify({"message": mensagem}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3002)