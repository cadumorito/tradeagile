import sqlite3

# Conectar ao banco de dados (ou criá-lo se não existir)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Comando SQL para inserção de múltiplos registros
sql_insert = """

"""

# Executar o comando SQL
cursor.execute(sql_insert)

# Confirmar a transação (fazer o commit)
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()

print("Inserção de dados concluída com sucesso.")
