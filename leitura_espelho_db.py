import sqlite3

class leitura_espelho_db:
    @staticmethod    
    def buscar(cur_db, espelho):
        lista_resultado = []
        try:
            result = cur_db.execute(f"""SELECT
             cod, descricao, volume_previsto, peso_previsto, volume_real, peso_real,
              (volume_real - volume_previsto), (peso_real - peso_previsto)
               FROM tb_espelho INNER JOIN tb_produto on tb_produto.cod = tb_espelho.tb_produto_cod
                WHERE espelho = '{espelho}' ORDER BY cod;""")
            for busca in result:
                lista_resultado.append(busca)
            return lista_resultado
        except Exception as e:
            print('Erro na Busca de Dados: ', e)
            r = ('000',"Produto Não Encontrado!", 0, 0, 0, 0, 0, 0)
            return r

    @staticmethod    
    def buscar_espelho_produto_restante(cur_db, espelho, produto):
        """Faz busca no banco filtrando por:
        - Espelho 
        - Produto

        Args:
            cur_db (cursor): cursor do banco
            espelho (str): espelho de carregamento
            produto (int): codigo do produto

        Returns:
            [tupla]: [volume_restante, peso_restante]
        """                 
        try:
            result = cur_db.execute(f"""SELECT
              (volume_real - volume_previsto), (peso_real - peso_previsto)
               FROM tb_espelho INNER JOIN tb_produto on tb_produto.cod = tb_espelho.tb_produto_cod
                WHERE espelho = '{espelho}' AND tb_espelho.tb_produto_cod = {produto};""")
            for busca in result:
                return busca
        except Exception as e:
            print('Erro na Busca de Dados: ', e)
            r = (0, 0)
            return r

    @staticmethod    
    def buscar_etiqueta(cur_db, etiqueta):
        """Faz busca no banco filtrando por:
        - Etiqueta

        Args:
            cur_db (cursor): cursor do banco
            espelho (str): etiqueta

        Returns:
            [str]: [espelho relacionado a etiqueta]
        """                 
        try:
            result = cur_db.execute(f"""SELECT
             espelho FROM tb_carregamento
              WHERE volume = '{etiqueta}';""")
            for busca in result:
                return busca
        except Exception as e:
            print('Erro na buscar_etiqueta: ', e)
            r = None
            return r

    @staticmethod    
    def buscar_produto(cur_db, espelho, produto):
        """Verifica se o produto está relacionado ao espelho
        """
        try:
            result = cur_db.execute(f"""SELECT
             tb_produto_cod FROM tb_espelho
                WHERE espelho = '{espelho}' and tb_produto_cod = {int(produto)};""")
            for busca in result:
                if busca[0] == produto:
                    return  True
                return False

        except Exception as e:
            print('Erro na Busca de Dados: ', e)
            return False

    @staticmethod
    def buscar_valor_geral(cur_db, espelho):
        try:
            result = cur_db.execute(f"""SELECT
             sum(volume_previsto), sum(peso_previsto), sum(volume_real), sum(peso_real)
              FROM tb_espelho
               WHERE espelho = '{espelho}';""")
            for busca in result:
                return busca
        except Exception as e:
            print('Erro na Busca de Dados: ', e)
            r = (0, 0.0, 0, 0.0)
            return r
        
    @staticmethod
    def buscar_qtde_etqta_lida(cur_db, espelho, produto):
        try:
            result = cur_db.execute(f"""SELECT
             COUNT(volume), peso*COUNT(volume)
              FROM tb_carregamento
               INNER JOIN tb_produto on cod = produto
                WHERE espelho = '{espelho}' and produto = {produto};""")
            for busca in result:
                return busca
        except Exception as e:
            print('Erro na Busca etiquetas lidas: ', e)
            r = (0, 0.0)
            return r

    @staticmethod
    def buscar_estorno(cur_db, espelho):
        try:
            lista_volumes = list()
            result = cur_db.execute(f"""SELECT
             volume, descricao
              FROM tb_carregamento
               INNER JOIN tb_produto on cod = produto
                WHERE espelho = '{espelho}';""")
            for busca in result:
                lista_volumes.append((busca))
            return lista_volumes
        except Exception as e:
            print('Erro na Busca etiquetas lidas: ', e)
            r = (0, "Não encontrado")
            return r

    @staticmethod
    def inserir_volume (cursor, conexao, volume, espelho, produto):
        try:
            cursor.execute(f"""INSERT INTO "main"."tb_carregamento"
            ("volume", "espelho", "produto")
            VALUES ('{volume}', '{espelho}', {produto});""")
            conexao.commit()
            return 1
        except sqlite3.IntegrityError as e:
            print("Erro no SQL: ", e)
            return 2

        except Exception as e:
            print("Erro ao incluir volume: ", e)
            return 3
     
    @staticmethod
    def atualizar_espelho_lido(cursor, conexao, espelho, produto, volume_real, peso_real):
        try:
            cursor.execute(f"""UPDATE tb_espelho
            SET volume_real = {volume_real}, peso_real = {peso_real}
            WHERE espelho = '{espelho}' and tb_produto_cod = {produto};""")
            conexao.commit()
        except Exception as e:
            print("Erro ao atualiza a 'tb_espelho': ", e)
     
    @staticmethod
    def remove_vol_espelho(cursor, conexao, espelho, volume):
        """Remove o volume(etiqueta) do espelho de carregamento

        Args:
            cursor (cur): cursor de acesso ao banco
            conexao (con): conexao ao banco de dabos
            espelho (str): espelho de carregamento
            volume (str): codigo de barras do volume
        """        
        try:
            cursor.execute(f"""DELETE FROM tb_carregamento 
            WHERE volume = '{volume}' AND espelho = '{espelho}';""")
            conexao.commit()
        except Exception as e:
            print(f"Erro ao estornar o '{volume}': ", e)

