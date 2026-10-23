from loja.database import conexao, cursor

def tabela_cliente():
    sql = (
        "CREATE TABLE IF NOT EXISTS clientes ("
        "id SERIAL PRIMARY KEY, "
        "nome VARCHAR (50) NOT NULL, "
        "email VARCHAR (80) NOT NULL "
        ")"
    )
    cursor.execute(sql)
    conexao.commit()


def colocar_cliente(nome, email):
    try:
        sql =(
            "INSERT INTO clientes "
            "(nome, email) "
            "VALUES "
            "(%s, %s); "
        )
        cursor.execute(sql, (nome, email))
        conexao.commit()

        registros = {"Nome" : nome, "Email": email}
        cliente_formatado = registros
        return cliente_formatado
    
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao criar cliente: {e}')
        return False

def listar_cliente():
    cursor.execute(
        "SELECT id, nome, email "
        "FROM clientes "
        "WHERE ativo =TRUE "
        )
    registros = cursor.fetchall()
    
    lista_clientes = []

    for registro in registros:
        id, nome, email = registro
        cliente_formatado = {'ID': id, "Nome": nome, "Email": email}
        lista_clientes.append(cliente_formatado)
    
    return lista_clientes


def atualiza_cliente(novo_nome, novo_email, id_cliente):
    try:
        sql =(
            "UPDATE clientes "
            "SET nome = %s, "
            "email = %s "
            "WHERE id = %s AND ativo = TRUE "
        )
        cursor.execute(sql, (novo_nome, novo_email, id_cliente))
        linhas = cursor.rowcount
        conexao.commit()

        if linhas == 0:
            return False
        
        registro_clientes = {"Id_cliente": id_cliente, "Nome_novo": novo_nome, "Email_novo": novo_email}
        novo_registro_clientes = registro_clientes

        return novo_registro_clientes
    
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao atualizar cliente: {e}')
        return False
    

def excluir_cliente(id_cliente):
    try:
        sql = (
            "UPDATE clientes "
            "SET ativo = FALSE "
            "WHERE id = %s AND ativo =TRUE "
        )
        cursor.execute(sql, (id_cliente, ))
        linhas = cursor.rowcount
        conexao.commit()
        if linhas == 0:
            return False

        cliente_apagado = {"id_cliente": id_cliente}
        return cliente_apagado
    except Exception as e:
        conexao.rollback()
        print (f'Erro ao excluir cliente {e}')
        return False