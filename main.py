from fastapi import FastAPI
from routers import clientes, item_pedido, pedidos, produtos

app = FastAPI(
    title= 'API vendas',    
    description= 'Sistema de vendas'
)

app.include_router(clientes.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)
app.include_router(item_pedido.router)