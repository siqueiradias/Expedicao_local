from factory_db import *

class cadastrar_espelho_db:
    def __init__(self):
        banco = factory_db()
        self._cur = banco.get_cursor()
        self._con = banco.get_conexao()

    def buscar(self, cod):
        """Faz a busca na tabela tb_produto pelo codigo do produto
        para retornar as informações de cod_produto, desc_produto, peso_produto

        Args:
            cod (int): Codigo do produto

        Returns:
            tupla: (cod_prod: int, desc_prod: str, peso_liq: float)
        """        
        try:
            result = self._cur.execute(f"SELECT * FROM tb_produto WHERE cod = {cod};")
            for busca in result:
                return busca
        except Exception as e:
            print(e)
            r = ('000',"Produto Não Encontrado!", 0)
            return r
    
    def buscar_espelho(self, espelho):
        """Faz consulta na tabela 'tb_espelho'

        Args:
            espelho (str): espelho de carregamento

        Returns:
            list: lista de tuplas(tb_produto_cod, descricao, volume_previsto, peso_previsto)
        """        
        try:
            result = self._cur.execute(f"""SELECT
             tb_produto_cod, descricao, volume_previsto, peso_previsto
              FROM tb_espelho INNER JOIN tb_produto on tb_produto.cod = tb_espelho.tb_produto_cod
               WHERE espelho = '{espelho}';""")
            lista_produtos = list()
            for busca in result:
                lista_produtos.append(busca)
            return lista_produtos

        except Exception as e:
            print(e)

    def verificar_espelho(self, espelho):
        
        try:
            result = self._cur.execute(f"SELECT * FROM tb_espelho WHERE espelho = '{espelho}';")
            for busca in result:
                if busca == '':
                    return False
                else:
                    return True
        except Exception as e:
            print(e)
            return False
    
    def verificar_produto(self, espelho, produto):
        """Verifica se um determinado produto pertence ao espelho

        Args:
            espelho (str): espelho
            produto (str): codigo do produto

        Returns:
            [boolean]: [se o produto existir: True, se Não: False]
        """        
        try:
            result = self._cur.execute(f"""SELECT * FROM tb_espelho
             WHERE espelho = '{espelho}' AND tb_produto_cod = {produto};""")
            for busca in result:
                if busca == '':
                    return False
                else:
                    return True
        except Exception as e:
            print(e)
            return False
    
    def atualizar_espelho(self, dados):
        """Atualiza os dados dos espelho

        Args:
            dados (tupla): (espelho, cod_produto, volume_prev., peso_prev)
        """        
        espelho = dados[0]
        produto = dados[1]
        volume = dados[2]
        peso = dados[3]
        try:
            if self.verificar_produto(espelho, produto):
                self._cur.execute(f"""UPDATE tb_espelho SET volume_previsto={volume}, peso_previsto={peso}
                WHERE espelho = '{espelho}' AND tb_produto_cod = {produto};""")
                self._con.commit()
            else:
                self.inserir_espelho([(espelho, produto, volume, peso, 0, 0.0)])
        except Exception as e:
            print("Erro ao Atualizar o espelho: ", e)
    

    def inserir_espelho (self, espelho):
        """Insere os dados da tabela GUI pra a tabela 'tb_espelho' no Banco de Dados

        Args:
            espelho (list): [lista de tuplas: ('espelho', 'tb_produto_cod',
             'volume_previsto', 'peso_previsto', 'volume_real', 'peso_real')]
        """        
        self._cur.executemany("""INSERT INTO 'main'.'tb_espelho'
        ('espelho', 'tb_produto_cod','volume_previsto','peso_previsto','volume_real','peso_real')
         VALUES (?,?,?,?,?,?);""", espelho)
        self._con.commit()

    def remover_produto (self, espelho, produto):
        try:
            self._cur.execute(f"""DELETE FROM tb_espelho
            WHERE espelho = '{espelho}' AND tb_produto_cod = '{produto}';""")
            self._con.commit()
        except Exception as e:
            print("Erro ao remover produto:", e)