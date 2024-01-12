# -----------------------------------------------------------------------------+
# Transportes Eireli                                                      |
# Consulta de CNPJ via web services                                            |
# Cacador, 25 de Junho de 2021                                                 |
# Luciano Carbonera                                                            |
# -----------------------------------------------------------------------------+

def format_string(cnpj):
    char = "./-(),"
    for i in range(0, len(char)):
        cnpj = cnpj.replace(char[i], "").strip()
    if len(cnpj) == 14:
        return cnpj
    else:
        print("Número de caracteres para CNPJ invalido")


def format_string_api_nfe_io(url, cnpj, token):
    url = str(url)
    url_split = url.split("{}")
    url = (url_split[0])
    url = url + cnpj
    url = url + url_split[1]
    url = url + token
    char = "'(),[]"
    for i in range(0, len(char)):
        url = url.replace(char[i], "")
    return url

def format_string_api_ws(url, cnpj):
    url = str(url)
    url_split = url.split("{}")
    url = (url_split[0])
    url = url + cnpj
    url = url + url_split[1]
    char = "'(),[]"
    for i in range(0, len(char)):
        url = url.replace(char[i], "")
    return url

def format_string_api_sim_consultas(url, token, parser, cnpj, estado):
    url = str(url)
    url_split = url.split("{}")
    url = (url_split[0])
    url = url + token
    url = url + url_split[1]
    url = url + parser
    url = url + url_split[2]
    url = url + cnpj
    url = url + url_split[3]
    url = url + estado
    char = "'(),[]"
    for i in range(0, len(char)):
        url = url.replace(char[i], "")
    return url

def format_string_api_simples_sim_consultas(url, token, parser, cnpj):
    url = str(url)
    url_split = url.split("{}")
    url = (url_split[0])
    url = url + token
    url = url + url_split[1]
    url = url + parser
    url = url + url_split[2]
    url = url + cnpj
    url = url + url_split[3]
    char = "'(),[]"
    for i in range(0, len(char)):
        url = url.replace(char[i], "")
    return url


def format_string_token(token):
    token = str(token)
    char = "'(),[]"
    for i in range(0, len(char)):
        token = token.replace(char[i], "")
    return token

def format_cca003(cca002):
    cca002 = str(cca002)
    char = str(",()[]")
    for i in range(0, len(char)):
        cca002 = str(cca002.replace(char[i], ""))
    return cca002


def cod_uf(uf):
    estados = {
        'RR': '14',
        'PA': '15',
        'AP': '16',
        'TO': '17',
        'MA': '21',
        'PI': '22',
        'CE': '23',
        'RN': '24',
        'PB': '25',
        'PE': '26',
        'AL': '27',
        'SE': '28',
        'BA': '29',
        'MG': '31',
        'ES': '32',
        'RJ': '33',
        'SP': '35',
        'PR': '41',
        'SC': '42',
        'RS': '43',
        'MS': '50',
        'MT': '51',
        'GO': '52',
        'DF': '53'
    }
    return estados[uf]
