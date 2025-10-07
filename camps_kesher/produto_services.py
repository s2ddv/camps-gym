from firebase_admin import firestore

db = firestore.client()

def cadastrar_produto(nome, cor, preco):
    produto = {
        "nome": nome,
        "cor": cor,
        "preço": float(preco)
    }
    db.collection("produtos").add(produto)

def listar_produtos():
    produtos_ref = db.collection("produtos").stream()
    produtos = []
    for p in produtos_ref:
        dados = p.to_dict()
        dados["id"] = p.id
        produtos.append(dados)
    return produtos
def atualizar_produto(produto_id, dados):
    db.collection("produtos").document(produto_id).update(dados)
def deletar_produto(produto_id):
    db.collection("produtos").document(produto_id).delete()