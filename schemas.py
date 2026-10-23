from pydantic import BaseModel

class NovoCliente(BaseModel):
    nome: str
    email: str

class AtualizarClientes(BaseModel):
    nome : str
    email: str


class NovoProduto(BaseModel):
    produto : str
    preco : float

class AtualizarProdutos(BaseModel):
    produto: str
    preco: float


class NovoPedido(BaseModel):
    cliente_id: int

class AtualizarPedido(BaseModel):
    cliente_id: int


class NovoItemPedido(BaseModel):
    pedido_id : int
    produto_id : int
    quantidade : int

class AtualizarItemPedido(BaseModel):
    quantidade: int