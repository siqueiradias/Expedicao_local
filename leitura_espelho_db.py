
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
        

    """Atualiza o valor de acertos de uma das colunas de 'aertosXX'"""
    def atualizar(self, cur, con, id, colunaAcertos, nAcertos):
        atuAcertos = nAcertos + 1
        cur.execute("UPDATE tb_aposta SET {} = {} WHERE id = {}".format(colunaAcertos, atuAcertos, id))
        con.commit()

    @staticmethod
    def inserir_volume (cursor, conexao, volume, espelho, produto):
        try:
            cursor.execute(f"""INSERT INTO "main"."tb_carregamento"
            ("volume", "espelho", "produto")
            VALUES ('{volume}', '{espelho}', {produto});""")
            #FALTA FAZER UPDATE NO ESPELHO
            conexao.commit()
        except Exception as e:
            print("Erro ao incluir volume: ", e)
    
    def consultar_etqtas_lidas(cur_db, espelho, produto):
        try:
            result = cur_db.execute(f"""SELECT 
            COUNT(volume), peso*COUNT(volume)
             FROM tb_carregamento 
             INNER JOIN tb_produto on cod = produto
              WHERE espelho = '{espelho}' and produto = {produto};"""
            for busca in result:
                return busca
        except Exception as e:
            print("Erro ao fazer a busca pelo volumes lidos: ", e)
            
