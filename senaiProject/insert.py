import sqlite3

# Conectar ao banco de dados (ou criá-lo se não existir)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Comando SQL para inserção de múltiplos registros
sql_insert = """
INSERT INTO cliente (codcli, nomecli, razasoccli, datacli, cnpjcli, fonecli, cidcli, estcli) VALUES
(1, 'Empresa A', 'Empresa A Ltda', '2024-07-01', '12.345.678/0001-90', '1234-5678', 'São Paulo', 'SP'),
(2, 'Empresa B', 'Empresa B Eireli', '2024-07-02', '23.456.789/0001-91', '2345-6789', 'Rio de Janeiro', 'RJ'),
(3, 'Empresa C', 'Empresa C SA', '2024-07-03', '34.567.890/0001-92', '3456-7890', 'Belo Horizonte', 'MG'),
(4, 'Empresa D', 'Empresa D ME', '2024-07-04', '45.678.901/0001-93', '4567-8901', 'Curitiba', 'PR'),
(5, 'Empresa E', 'Empresa E Ltda', '2024-07-05', '56.789.012/0001-94', '5678-9012', 'Porto Alegre', 'RS');


"""

# Executar o comando SQL
cursor.executescript(sql_insert)

# Confirmar a transação (fazer o commit)
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()

print("Inserção de dados concluída com sucesso.")
