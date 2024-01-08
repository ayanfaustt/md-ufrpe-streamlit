import utils.database as db

cursor = db.connection.cursor()

print(cursor.stored_results)

query = "select count(*) from fato_licitacao"

cursor.execute(query)

result = cursor.fetchall()

print(result)