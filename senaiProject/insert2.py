import sqlite3

# Conectar ao banco de dados (ou criá-lo se não existir)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Comando SQL para inserção de múltiplos registros
sql_insert = """
    INSERT INTO fornecedor (codiforn, nomeforn, razasocforn, foneforn) VALUES
        ('F001', 'Patrick', 'Lambisgoia', 190),
        ('F002', 'Isaac', 'McDonalds', 172);
"""
sql_insert2 = """
    INSERT INTO produto (codiprod, descprod, valorprod, qntdprod, idforn_id) VALUES
        ('P001', 'Tomate', 20, 10, 1),
        ('P002', 'Lanche', 25, 10, 2);
"""
sql_insert3 = '''
   INSERT INTO vendedor (codivende, nomevende, razasocvende, fonevende, porcvende) VALUES
        ('VD001', 'Carlos', 'Lava Jato', 150, 40),
        ('VD002', 'Gui', 'Pet Shop', 250, 30);
'''

# Executar o comando SQL
cursor.execute(sql_insert)
cursor.execute(sql_insert2)
cursor.execute(sql_insert3)

# Confirmar a transação (fazer o commit)
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()

print("Inserção de dados concluída com sucesso.")
