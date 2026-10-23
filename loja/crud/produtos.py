from loja.database import conexao, cursor

def tabela_produtos():
    sql = (
        "CREATE TABLE IF NOT EXISTS produtos ("
        "id SERIAL PRIMARY KEY, "
        "produto VARCHAR (30) NOT NULL, "
        "preco NUMERIC (10,2) NOT NULL "
        ")"
    )
    cursor.execute(sql)
    conexao.commit()


def colocar_produto(produto, preco):
    try:
        sql = (
            "INSERT INTO produtos "
            "(produto, preco) "
            "VALUES "
            "(%s, %s); "
        )
        cursor.execute(sql, (produto, preco))
        conexao.commit()

        registro = {"Produto": produto, "Preco": preco}
        produtos = registro
        return produtos

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao colocar produto {e}')
        return False


def listar_produtos():
    cursor.execute(
        "SELECT id, produto, preco "
        "FROM produtos "
        "WHERE ativo = TRUE"
    )
    produtos = cursor.fetchall()
    lista_produto = []
    
    for p in produtos:
        id, produto, preco = p
        produtos_formatados = {"ID": id, "Produto": produto, "Preco": preco}
        lista_produto.append(produtos_formatados)
    
    return lista_produto


def atualizar_produto(novo_produto, novo_preco, id_produto):
    try:
        sql = (
            "UPDATE produtos "
            "SET produto = %s, "
            "preco = %s "
            "WHERE id= %s AND ativo = TRUE "
        )
        cursor.execute(sql, (novo_produto, novo_preco, id_produto))
        linhas = cursor.rowcount
        conexao.commit()
        if linhas == 0:
            return False
        
        registro_produtos = {"Produto_novo": novo_produto, "Preco_novo": novo_preco}
        return registro_produtos

    except Exception as e:
        conexao.rollback()
        print (f'Erro ao atualizar cliente {e}')
        return False


def apagar_produto(id_produto):
    try:
        sql = (
            "UPDATE produtos "
            "SET ativo = FALSE "
            "WHERE id = %s AND ativo = TRUE "
        )
        cursor.execute(sql, (id_produto, ))
        linhas = cursor.rowcount
        conexao.commit()
        if linhas == 0:
            return False
        
        produto_id = {"ID": id_produto}
        return produto_id
    
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao apagar produto {e}')
        return False


def restricao_produto():
    sql = (
        "CREATE UNIQUE INDEX produtos_nome_unico "
        "ON produtos (LOWER(produto))"
    )
    cursor.execute(sql)
    conexao.commit()