# -----------------------------------------------------------------------------+
# Transportes Eireli                                                      |
# Consulta de CNPJ via web services                                            |
# Cacador, 25 de Junho de 2021                                                 |
# Luciano Carbonera                                                            |
# -----------------------------------------------------------------------------+
import inc_api, inc_util, inc_database
from pprint import pprint
uf = ''
dados_ie = {}
dados_simples = {}
dados = {}
#--------------------------------------------------------------------------------------------------------
# RECEBE O CNPJ DO USUARIO CHAMANDO A FUNÇÃO PARA VALIDAR CNPJ
def input_user():
    cnpj= input("Digite o CNPJ:")
    if len(cnpj) == 14:
            cnpj = str(inc_util.format_string(cnpj))
    else:
        print("Número de caracteres inválidos")
    return cnpj
cnpj = input_user()
#--------------------------------------------------------------------------------------------------------
# PRIMEIRA CHAMADA RECEITA WS
if cnpj:
        dados = inc_api.dados_cnpj_receita_ws(cnpj)
        #print(dados)
        if dados['estado']:
            uf = dados['estado']
#--------------------------------------------------------------------------------------------------------
# TRAZ OS CAMPOS DA CCA003
def consulta_cca003(uf):
    cca002_ser_cnpj ="select cca002_ser_cnpj from cca003\
                inner join loc002 on loc002.loc002_ser = cca003.loc002_ser\
                where loc002_uf  like ('" + uf + "')"

    cca002_ser_ie = "select cca002_ser_ie from cca003\
                inner join loc002 on loc002.loc002_ser = cca003.loc002_ser\
                where loc002_uf  like ('" + uf + "')"

    cca002_ser_simples = "select cca002_ser_simples from cca003\
                inner join loc002 on loc002.loc002_ser = cca003.loc002_ser\
                where loc002_uf  like ('" + uf + "')"

    con = inc_database.Db()

    cca002_ser_cnpj = inc_database.Db.select(con, cca002_ser_cnpj)
    cca002_ser_cnpj = inc_util.format_cca003(cca002_ser_cnpj)

    cca002_ser_ie = inc_database.Db.select(con, cca002_ser_ie)
    cca002_ser_ie = inc_util.format_cca003(cca002_ser_ie)

    cca002_ser_simples = inc_database.Db.select(con, cca002_ser_simples)
    cca002_ser_simples = inc_util.format_cca003(cca002_ser_simples)

    cca003 = {
        'cca002_ser_cnpj': cca002_ser_cnpj,
        'cca002_ser_ie': cca002_ser_ie,
        'cca002_ser_simples': cca002_ser_simples
    }
    return cca003
cca003 = ''
if uf:
    cca003 = consulta_cca003(uf)
#--------------------------------------------------------------------------------------------------------
# REALIZA SEGUNDA (ie )CONSULTA, E A TERCEIRA(simples) SE HOUVER
if (cca003): #se a consulta tiver retonro
# DETERMINA QUAL DAS API IRA USAR, PELO ID CADASTRADO NO BD

        #consulta IE
        if cca003['cca002_ser_ie'] != '': #se o campo nao estiver vazio

            if cca003['cca002_ser_ie'] == '4':
                if dados['cnae'] == '84.11-6-00':
                    print("Órgão Público não contribuinte estatal")
                else:
                    dados_ie = inc_api.dados_ie_nfe_io(cnpj, uf)
                if dados_ie != '':
                    dados_ie = dados_ie
                else:
                    print("Não foi possivel recuperar os dados IE. Tente novamente")


            elif cca003['cca002_ser_ie'] == '9':
                if dados['cnae'] == '84.11-6-00':
                    print("Órgão Público não contribuinte estatal")
                else:
                    dados_ie = inc_api.dados_ie_sim_consultas(cnpj, uf)
                if dados_ie != '':
                    dados_ie = dados_ie
                else:
                    print("Não foi possivel recuperar os dados IE. Tente novamente")
        else:
            print("Fonte de consulta IE não foi preenchida")



        # ESCOLHE API SIMPLES
        if cca003['cca002_ser_simples'] != '':

            if cca003['cca002_ser_simples'] == '2':
                if dados['nat_jur'] == '213-5 - Empresário (Individual)':
                    print("Não é possivel resgatar informações SIMPLES de CNPJ com natureza juridica Empresario individual(MEI) para a API Atual")
                else:
                    dados_simples = inc_api.dados_simples_nfe_io(cnpj)
                if dados_simples != '':
                    dados_simples = dados_simples
                else:
                    print("Não foi possivel recuperar os dados SIMPLES. Tente novamente")


            elif cca003['cca002_ser_simples'] == '9':
                dados_simples = inc_api.dados_simples_sim_consultas(cnpj)
                if dados_simples != '':
                    dados_simples = dados_simples
                else:
                    print("Não foi possivel recuperar os dados SIMPLES. Tente novamente")

        else:
            print("Fonte de consulta SIMPLES não foi preenchida")
else:
    print('Não foi possivel consultar todos os dados da empresa. Tente outra fonte de consulta.')
#--------------------------------------------------------------------------------------------------------
# MONTAR DICT DE RETORNO
dict_dados = {
        'ws': dados,
        'ie': dados_ie,
        'simples': dados_simples
    }
pprint(dict_dados)
#--------------------------------------------------------------------------------------------------------

#cnpj = ''
#print(inc_api.dados_cnpj_receita_ws(cnpj))
#print(inc_api.dados_simples_nfe_io(cnpj))
#print(inc_api.dados_ie_nfe_io(cnpj))
#print(inc_api.dados_cnpj_nfe_io(cnpj))
#print(inc_api.dados_simples_sim_consultas(cnpj))
#print(inc_api.dados_ie_sim_consultas(cnpj, uf))
#print(inc_api.dados_cnpj_ndd_sim_consulta(cnpj)
















