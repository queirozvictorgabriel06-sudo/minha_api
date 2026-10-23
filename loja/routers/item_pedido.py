from fastapi import APIRouter, HTTPException
from loja.schemas import NovoItemPedido, AtualizarItemPedido
from crud import item_pedido as crud_item_pedido

router = APIRouter(tags=["Itens_pedidos"])

@router.post("/itens_pedidos")
def colocar_itens_pedidos(item: NovoItemPedido):
    resultado = crud_item_pedido.colocar_item_pedido(item.pedido_id, item.produto_id, item.quantidade)
    if resultado == False:
        raise HTTPException(status_code=400, detail='Não é possivel adicionar, o pedido esta desativado ou não existe')

    return {"Mensagem": "Itens adicionados", "Registro": resultado}


@router.get("/itens_pedidos")
def ver_itens_pedido():
    lista_itens_pedidos = crud_item_pedido.listar_item_pedido()
    return lista_itens_pedidos


@router.put("/itens_pedidos/{id_item_pedido}")
def alterar_item_pedido(id_item_pedido: int, item: AtualizarItemPedido):
    resultado = crud_item_pedido.atualizar_item_pedido(item.quantidade, id_item_pedido)
    if resultado == False:
        raise HTTPException(status_code=404, detail='Item do pedido não encontrado')
    
    return {"Mensagem": "Quantidade alterada", "Registro": resultado}


@router.delete("/itens_pedidos/{id_item_pedido}")
def remover_item_pedido(id_item_pedido: int):
    sucesso = crud_item_pedido.deletar_itens_pedido(id_item_pedido)
    if sucesso == False:
        raise HTTPException(status_code=404, detail='Nada encontrado')
    
    return {"Mensagem": "Item deletado", "Registro": sucesso}