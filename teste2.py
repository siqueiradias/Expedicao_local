import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("base/BD_EXPEDICAO.db")
df = pd.read_sql_query("SELECT * FROM tb_carregamento WHERE espelho = 2;", con)

# Verify that result of SQL query is stored in the dataframe
print(df.head())

#df.to_excel("saida.xlsx", index=False)

df.to_csv("saida.txt", sep=";")

con.close()