# -----------------------------------------------------------------------------+
# Alfa Transportes Eireli                                                      \
#  Classe para banco de dados                        		          \
# Cacador, 25 de Junho de 2021                                                 \
# Luciano Carbonera                                                            \
# -----------------------------------------------------------------------------+
import psycopg2

host = 'localhost'
db = 'banco'
class Db:

    def __init__(self):
        try:
            self._db = psycopg2.connect(host=host, database=db, user='postgres', password='postgres')
            #print("Conexao com DB realizada com sucesso")
        except:
            print("Não foi possivel conectar ao banco de dados. Verifique as informações da conexão e tente novamente")

    def select(self, select):
        global result, cur
        try:
            cur = self._db.cursor()
        except:
            print("Não foia possivel iniciar conexão")
        try:
            cur.execute(select)
            result = cur.fetchall()
            cur.close()
            return result
        except:
            print("Algo deu errado na consulta :(")


    def manipular(self, sql):
        global cur
        try:
            cur = self._db.cursor()
        except:
            print("Não foi possivel iniciar conexão")

        try:
            cur.execute(sql)
            self._db.commit()
            print("Query Executada com sucesso")
            cur.close()
        except:
            self._db.rollback()
            print("Algo deu errado na manipulação  :(")















