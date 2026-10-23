from database import conexao, cursor

def tabela_pedidos():
    sql = (
        "CREATE TABLE IF NOT EXISTS pedidos ("
        "id SERIAL PRIMARY KEY, "
        "clientes_id INTEGER,"
        "FOREIGN KEY (clientes_id) references clientes(id) "
        ")"
    )
    cursor.execute(sql)
    conexao.commit()


def colocar_pedido(cliente_id):
    try:
        cursor.execute(
            "SELECT id FROM clientes WHERE id = %s AND ativo = TRUE ", 
            (cliente_id, )
        )
        cliente = cursor.fetchone()
        if not cliente:
            return False
        
        sql = (
            "INSERT INTO pedidos "
            "(clientes_id) "
            "VALUES "
            "(%s)"
        )
        cursor.execute(sql, (cliente_id, ))
        conexao.commit()

        pedido = {"id_cliente": cliente_id}
        return pedido

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao colocar pedido {e}')
        return False


def listar_pedidos():
    sql = (
        "SELECT pedidos.id, clientes.id "
        "FROM pedidos "
        "JOIN clientes "
        "ON pedidos.clientes_id = clientes.id "
        "WHERE pedidos.ativo = TRUE AND clientes.ativo = TRUE "
    )
    cursor.execute(sql)
    registros = cursor.fetchall()
    lista_pedidos = []

    for pedido in registros:
        id_pedido, id_cliente = pedido
        pedido_formatado = {"ID_pedido": id_pedido, "ID_cliente": id_cliente}
        lista_pedidos.append(pedido_formatado)
    
    return lista_pedidos


def atualizar_pedido(novo_id_cliente, id_pedido):
    try:
        cursor.execute("SELECT id FROM clientes WHERE id = %s AND ativo = TRUE ", (novo_id_cliente, ))
        cliente = cursor.fetchone()
        if not cliente:
            return False
        
        sql = (
            "UPDATE pedidos "
            "SET clientes_id = %s "
            "WHERE id = %s AND ativo = TRUE "
        )
        cursor.execute(sql, (novo_id_cliente, id_pedido) )
        linhas = cursor.rowcount
        conexao.commit()
        if linhas == 0:
            return False
        
        pedido_novo = {"Id_cliente_novo": novo_id_cliente, "Id_pedido": id_pedido}
        return pedido_novo

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao atualizar o pedido {e}')
        return False


def deletar_pedido(id_pedido):
    try:
        sql =(
            "UPDATE pedidos "
            "SET ativo = FALSE "
            "WHERE id = %s AND ativo = TRUE "
        )
        cursor.execute(sql, (id_pedido, ))
        linhas = cursor.rowcount
        conexao.commit()
        if linhas == 0:
            return False
        
        pedido = {"Id_pedido": id_pedido}
        return pedido

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao apagar pedido {e}')
        return False