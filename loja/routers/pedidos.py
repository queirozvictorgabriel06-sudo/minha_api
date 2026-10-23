from fastapi import APIRouter, HTTPException
from loja.schemas import NovoPedido, AtualizarPedido
from crud import pedidos as crud_pedidos

router = APIRouter(tags=["Pedidos"])

@router.post("/pedidos")
def adicionar_pedido(id_cliente: NovoPedido):
    resultado = crud_pedidos.colocar_pedido(id_cliente.cliente_id)
    if resultado == False:
        raise HTTPException(status_code=400, detail='Cliente não existe ou esta desativado')
    return {"Mensagem": "Pedido adicionado ao cliente", "Registro": resultado}


@router.get("/pedidos")
def listar_pedido():
    pedidos = crud_pedidos.listar_pedidos()
    return {"Pedidos": pedidos}


@router.put("/pedidos/{id_pedido}")
def alterar_pedido(id_pedido: int, novo_id_cliente: AtualizarPedido):
    resultado = crud_pedidos.atualizar_pedido(novo_id_cliente.cliente.id, id_pedido)
    if resultado == False:
        raise HTTPException(status_code=404, detail='Pedido esta desativado ou não existe')
    return {"Mensagem": "Pedido alterado", "Registro": resultado}


@router.delete("/pedidos/{id_pedido}")
def remover_pedido(id_pedido: int):
    sucesso = crud_pedidos.deletar_pedido(id_pedido)
    if sucesso == False:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')

    return {"Mensagem": "Pedido apagado", "Registro": sucesso}