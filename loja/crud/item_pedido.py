from loja.database import conexao,cursor

def tabela_itens_pedido():
    sql = (
        "CREATE TABLE IF NOT EXISTS itens_pedido ("
        "id SERIAL PRIMARY KEY, "
        "pedido_id INTEGER, "
        "FOREIGN KEY (pedido_id) references pedidos(id), "
        "produtos_id INTEGER, "
        "FOREIGN KEY (produtos_id) references produtos(id), "
        "quantidade INTEGER "
        ")"
    )
    cursor.execute(sql)
    conexao.commit()


def colocar_item_pedido(pedido_id, produto_id, quantidade):
    try:
        sql = (
            "SELECT produtos.preco "
            "FROM produtos "
            "JOIN pedidos ON pedidos.id = %s "
            "WHERE produtos.id = %s AND produtos.ativo = TRUE AND pedidos.ativo = TRUE "
        )
        cursor.execute(sql, (pedido_id, produto_id,) )
        preco = cursor.fetchone()

        if preco is None:
            return False
        
        preco = preco[0]

        sql1 =(
            "INSERT INTO itens_pedido "
            "(pedido_id, produtos_id, quantidade, preco_unitario) "
            "VALUES "
            "(%s, %s, %s, %s) "
        ) 
        cursor.execute(sql1, (pedido_id, produto_id, quantidade, preco) )
        conexao.commit()
        itens_pedido = {"Id_pedido": pedido_id, "Id_produto": produto_id, "quantidade": quantidade, "preco_unitario": preco}
        
        return itens_pedido

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao colocar o item {e}')
        return False


def listar_item_pedido():
    sql = (
        "SELECT itens_pedido.id, pedidos.id, clientes.nome, produtos.produto, itens_pedido.quantidade, itens_pedido.preco_unitario, itens_pedido.preco_unitario * itens_pedido.quantidade, "
        "SUM(itens_pedido.quantidade * itens_pedido.preco_unitario) OVER (PARTITION BY pedidos.id) "
        "FROM pedidos "
        "JOIN clientes "
        "ON pedidos.clientes_id = clientes.id "
        "JOIN itens_pedido "
        "ON itens_pedido.pedido_id = pedidos.id "
        "JOIN produtos "
        "ON itens_pedido.produtos_id = produtos.id "
        "WHERE itens_pedido.ativo = TRUE AND clientes.ativo = TRUE AND produtos.ativo = TRUE "
        "ORDER BY pedidos.id, itens_pedido.id"
    )
    cursor.execute(sql)
    itens_pedido = cursor.fetchall()

    lista_itens_pedido = []
    for itens_p in itens_pedido:
        id_item_pedido, id_pedido, cliente_nome, produto, quantidade, preco, total_item, total_pedido = itens_p
        itens_formatado = {
            "id_item_pedido": id_item_pedido,
            "id_pedido": id_pedido,
            "nome_cliente": cliente_nome,
            "produto": produto,
            "quantidade": quantidade,
            "preco_unitario": preco,
            "total_item": total_item,
            "total_do_pedido": total_pedido
        }
        lista_itens_pedido.append(itens_formatado)

    return lista_itens_pedido


def atualizar_item_pedido(quantidade, id_item_pedido):
    try:
        sql = (
            "UPDATE itens_pedido "
            "SET quantidade = %s "
            "WHERE id = %s AND ativo = TRUE "
        )
        cursor.execute(sql, (quantidade, id_item_pedido))
        linhas = cursor.rowcount
        conexao.commit()

        if linhas == 0:
            return False
        
        item_atualizado = {"Id_item_pedido": id_item_pedido, "nova_quantidade": quantidade}
        
        return item_atualizado

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao atualizar item {e}')
        return False


def deletar_itens_pedido(id_item_pedido):
    try:
        sql = (
            "UPDATE itens_pedido "
            "SET ativo = FALSE "
            "WHERE id = %s AND ativo = TRUE "
        )
        cursor.execute(sql, (id_item_pedido, ))
        linhas = cursor.rowcount
        conexao.commit()
        if linhas == 0:
            return False
        
        item_pedido = {"id_item_pedido": id_item_pedido}
        return item_pedido

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao apagar um item {e}')
        return False