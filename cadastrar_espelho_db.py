from factory_db import *

class cadastrar_espelho_db:
    def __init__(self):
        banco = factory_db()
        self._cur = banco.get_cursor()
        self._con = banco.get_conexao()

    """Retorna o valor de acertos de uma das colunas de 'aertosXX'"""
    def buscar(self, cod):
        try:
            result = self._cur.execute(f"SELECT * FROM tb_produto WHERE cod = {cod};")
            for busca in result:
                return busca
        except Exception as e:
            print(e)
            r = ('000',"Produto Não Encontrado!", 0)
            return r
        

    """Atualiza o valor de acertos de uma das colunas de 'aertosXX'"""
    def atualizar(self, cur, con, id, colunaAcertos, nAcertos):
        atuAcertos = nAcertos + 1
        cur.execute("UPDATE tb_aposta SET {} = {} WHERE id = {}".format(colunaAcertos, atuAcertos, id))
        con.commit()


    # Larger example that inserts many records at a time
    def inserir (self, produto):
        self._cur.executemany('INSERT INTO tb_geral VALUES (?,?,?,?,?,?,?)', [produto])
        self._con.commit()