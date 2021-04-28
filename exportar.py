import pandas as pd
import sqlite3

class Exportar:
    """Classe para geração de arquivos com a finalidade de
     exportar os dados disponivel no banco da aplicação
    """    

    @staticmethod
    def exp_to_excel(con, espelho, file_dest):
        """Gerar e salvar um arquivo no formato '.xlsx' com o resultado da consulta:
        SELECT * FROM tb_carregamento WHERE espelho = '{espelho}';

        Args:
            con (conexão sqlite): conexão com o banco de dados
            espelho (str): espelho para a filtragem
            file_dest (str): Nome e destino do arquivo exportado
        """        
        df = pd.read_sql_query(f"SELECT * FROM tb_carregamento WHERE espelho = '{espelho}';", con)        
        df.to_excel(f"{file_dest}.xlsx", index=False)
    
    @staticmethod
    def exp_to_csv(con, espelho, file_dest):
        """Gerar e salvar um arquivo no formato '.csv' com o resultado da consulta:
        SELECT * FROM tb_carregamento WHERE espelho = '{espelho}';

        Args:
            con (conexão sqlite): conexão com o banco de dados
            espelho (str): espelho para a filtragem
            file_dest (str): Nome e destino do arquivo exportado
        """        
        df = pd.read_sql_query(f"SELECT * FROM tb_carregamento WHERE espelho = '{espelho}';", con)        
        df.to_csv(f"{file_dest}.csv", sep=";", index= False)
    
    @staticmethod
    def exp_to_txt(con, espelho, file_dest):
        """Gerar e salvar um arquivo no formato '.txt' com o resultado da consulta:
        SELECT * FROM tb_carregamento WHERE espelho = '{espelho}';

        Args:
            con (conexão sqlite): conexão com o banco de dados
            espelho (str): espelho para a filtragem
            file_dest (str): Nome e destino do arquivo exportado
        """        
        df = pd.read_sql_query(f"SELECT * FROM tb_carregamento WHERE espelho = '{espelho}';", con)        
        df.to_csv(f"{file_dest}.txt", sep=";", index= False)