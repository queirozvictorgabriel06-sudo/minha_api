from fastapi import APIRouter, HTTPException
from loja.schemas import NovoProduto, AtualizarProdutos
from crud import produtos as crud_produtos

router = APIRouter(tags=["Produtos"])

@router.post("/produtos")
def adicionar_produtos(produto: NovoProduto):
    produto_novo = crud_produtos.colocar_produto(produto.produto, produto.preco)
    return {"Mensagem": "Produto adicionado", "Registro": produto_novo}


@router.get("/produtos")
def ver_produtos():
    produtos = crud_produtos.listar_produtos()
    return {"Produtos": produtos}


@router.put("/produtos/{id_produto}")
def alterar_produto(id_produto: int, produto_novo: AtualizarProdutos):
    resultado = crud_produtos.atualizar_produto(produto_novo.produto, produto_novo.preco, id_produto)
    if resultado == False:
        raise HTTPException(status_code=404, detail='Produto não existe ou esta desativado')
    return {"Mensagem": "Produto alterado", "Registro": resultado}


@router.delete("/produtos/{id_produto}")
def remover_produto(id_produto: int):
    sucesso = crud_produtos.apagar_produto(id_produto)
    if sucesso == False:
        raise HTTPException(status_code= 404, detail='Produto não encontrado')
    
    return {"Mensagem": "Produto apagado", "Registro": sucesso}