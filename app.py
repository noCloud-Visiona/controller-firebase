from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# GET
from controller.firebase_gets.historico_by_id import get_historico
from controller.firebase_gets.imagem_by_id import get_image
from controller.firebase_gets.pega_job_id import get_job_id
from controller.firebase_gets.pega_todos_jobs_id import get_todos_jobs_id

# POST
from controller.firebase_post.post_imagem_original_png import upload_image_original
from controller.firebase_post.post_imagem_tratada_png import upload_image_tratada
from controller.firebase_post.post_mask_nuvem import upload_mask_nuvem
from controller.firebase_post.post_mask_sombra import upload_mask_sombra
from controller.firebase_post.post_imagem_sem_nuvem import upload_imagem_sem_nuvem
from controller.firebase_post.post_imagem_sem_sombra import upload_imagem_sem_sombra
from controller.firebase_post.post_imagem_nuvem import upload_imagem_nuvem
from controller.firebase_post.post_imagem_sombra import upload_imagem_sombra
from controller.firebase_post.post_thumbnail_sem_nuvem import upload_thumbnail_sem_nuvem
from controller.firebase_post.post_thumbnail_sem_sombra import upload_thumbnail_sem_sombra
from controller.firebase_post.post_thumbnail_imagem_original import upload_thumbnail_imagem_original
from controller.firebase_post.post_thumbnail_nuvem import upload_thumbnail_nuvem
from controller.firebase_post.post_thumbnail_sombra import upload_thumbnail_sombra
from controller.firebase_post.post_json_front import post_json_front
from controller.firebase_post.post_uma_imagem_qualquer import upload_uma_imagem_qualquer
from controller.firebase_post.post_job_id import post_job_id


# DELETE
from controller.firebase_delete.delete_de_imagem import delete_image

# ESPECIAL
from controller.firebase_rotas_especiais.converte_de_volta_imagem_json import transforma_json_em_imagem

app = Flask(__name__)
CORS(app)

######################################################
################### Rotas de Get #####################
######################################################

# Retorna o job_id de um determinado processamento
@app.route('/get_job_id/<id_usuario>/<job_id>', methods=['GET'])
def pega_job_id(id_usuario, job_id):
    return get_job_id(id_usuario, job_id)

# Retorna o job_id de um determinado processamento
@app.route('/get_todos_jobs_id/<id_usuario>', methods=['GET'])
def pega_todos_jobs_id(id_usuario):
    return get_todos_jobs_id(id_usuario)

# Retorna todos os documentos/jsons de um usuário especifico
@app.route('/historico/<id_usuario>', methods=['GET'])
def historico_usuario(id_usuario):
    return get_historico(id_usuario)

# Retorna uma imagem especifica de um usuário
@app.route('/get_image/<id_imagem>/<id_usuario>', methods=['GET'])
def pega_imagem(id_imagem, id_usuario):
    return get_image(id_imagem, id_usuario)

######################################################
################### Rotas de Post #################### 
######################################################

@app.route('/post_job_id/<id_usuario>/<job_id>', methods=['POST'])
def salva_job_id(id_usuario, job_id):
    return post_job_id(id_usuario, job_id)

# Salva o json do frontend completo no firebase
@app.route('/post_json', methods=['POST'])
def salva_json_do_usuario():
    return post_json_front()

###### Imagens de sombra e nuvem com e sem na imagem

@app.route('/upload_imagem_sem_nuvem', methods=['POST'])
def salvar_imagem_sem_nuvem():
    return upload_imagem_sem_nuvem()

@app.route('/upload_imagem_sem_sombra', methods=['POST'])
def salvar_imagem_sem_sombra():
    return upload_imagem_sem_sombra()

@app.route('/upload_imagem_nuvem', methods=['POST'])
def salvar_imagem_nuvem():
    return upload_imagem_nuvem()

@app.route('/upload_imagem_sombra', methods=['POST'])
def salvar_imagem_sombra():
    return upload_imagem_sombra()

###### Thumbnails ######

@app.route('/upload_thumbnail_sem_nuvem', methods=['POST'])
def salvar_thumbnail_sem_nuvem():
    return upload_thumbnail_sem_nuvem()

@app.route('/upload_thumbnail_sem_sombra', methods=['POST'])
def salvar_thumbnail_sem_sombra():
    return upload_thumbnail_sem_sombra()

@app.route('/upload_thumbnail_nuvem', methods=['POST'])
def salvar_thumbnail_nuvem():
    return upload_thumbnail_nuvem()

@app.route('/upload_thumbnail_sombra', methods=['POST'])
def salvar_thumbnail_sombra():
    return upload_thumbnail_sombra()

@app.route('/upload_thumbnail_imagem_original', methods=['POST'])
def salvar_thumbnail_imagem_original():
    return upload_thumbnail_imagem_original()

###### Máscaras nuvem e sombra

# Salva e retorna a URL da mask "nuvem" no bucket
@app.route('/upload_mask_nuvem', methods=['POST'])
def salvar_mask_nuvem():
    return upload_mask_nuvem()

@app.route('/upload_mask_sombra', methods=['POST'])
def salvar_mask_sombra():
    return upload_mask_sombra()

@app.route('/upload_image_nuvem_png', methods=['POST'])
def salvar_imagem_nuvem_antigo():
    return upload_mask_nuvem()

##### Imagem original e tratada antiga

# Salva e retorna a URL da imagem "original" no bucket
@app.route('/upload_image_original_png', methods=['POST'])
def salvar_imagem_original():
    return upload_image_original()

# Salva e retorna a URL da imagem "tratada" no bucket
@app.route('/upload_image_tratada_png', methods=['POST'])
def salvar_imagem_tratada():
    return upload_image_tratada()

###### Salvar qualquer coisa

# Caso queira salvar alguma imagem não relacionada ao fluxo padrão no Bucket pra usar a URL dela
@app.route('/upload_de_uma_imagem_qualquer', methods=['POST'])
def salva_uma_imagem():
    return upload_uma_imagem_qualquer()

######################################################
################### Rotas de Delete ##################
######################################################

# Deleta uma imagem especifica de um usuário
@app.route('/delete_image/<id_imagem>/<id_usuario>', methods=['DELETE'])
def deletar_imagem(id_imagem, id_usuario):
    return delete_image(id_imagem, id_usuario)

######################################################
################### Rotas Especiais ##################
######################################################

# Transforma imagens em base64 de volta para imagem normal
@app.route('/show_image', methods=['POST'])
def exibe_imagem_json():
    json_data = request.get_json()

    # Chama a função para transformar a imagem codificada em um arquivo PNG
    success, mensagem = transforma_json_em_imagem(json_data, "IA/img/output_image.png")

    if success:
        try:
            return send_file("IA/img/output_image.png", mimetype='image/png')
        except FileNotFoundError:
            return jsonify({"message": "Erro: Imagem não encontrada"})
    else:
        return jsonify({"message": mensagem})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3004)