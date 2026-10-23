from fastapi import APIRouter, HTTPException
from loja.schemas import NovoCliente, AtualizarClientes
from crud import clientes as crud_clientes

router = APIRouter(tags=["Clientes"])

#Usando post para adicionar um cliente novo
@router.post("/clientes")
def adicionar_cliente(cliente: NovoCliente):
    crud_clientes.colocar_cliente(cliente.nome, cliente.email)
    return {"mensagem": f"Cliente criado "}


#Usando get para ver clientes dentro do banco
@router.get("/clientes")
def ver_clientes():
    lista_clientes = crud_clientes.listar_cliente()
    return {"Clientes": lista_clientes}


#Usando o put para atualizar um cliente que existe dentro do banco
@router.put("/clientes/{id_cliente}")
def atualizar_cliente(id_cliente: int, novo_dados: AtualizarClientes):
    resultado = crud_clientes.atualiza_cliente(novo_dados.nome, novo_dados.email, id_cliente)
    if resultado == False:
        raise HTTPException(status_code=404, detail='Cliente não esta ativado')
    return {"Mensagem": "Dados clientes alterados", "Registro": resultado}


#Usando o delete para apagar um cliente existente dentro do banco
@router.delete("/clientes/{id_cliente}")
def excluir_cliente(id_cliente: int):
    sucesso = crud_clientes.excluir_cliente(id_cliente)
    if sucesso == False:
        raise HTTPException(status_code=404, detail='Cliente não encontrado')
    
    return {"Mensagem": "Cliente apagado", "Registro": sucesso}