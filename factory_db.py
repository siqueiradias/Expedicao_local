import sqlite3
import os

class factory_db:
    def __init__(self):
        self._db = 'base/BD_EXPEDICAO.db'
        # Cria uma conexão com o banco de dados.
        # Se o banco de dados não existir, ele é criado neste momento.
        self._con = sqlite3.connect(self._db)
        # Criando um cursor
        self._cur = self._con.cursor() # (Um cursor permite percorrer todos os registros em um conjunto de dados)

    def excluir_db(self):
        # Remove o arquivo com o banco de dados SQLite (caso exista)
        os.remove(self._db) if os.path.exists(self._db) else None

    def get_cursor(self):
        return self._cur
    
    def get_conexao(self):
        return self._con

    def close_db(self):
        self._cur.close()
        self._con.close()