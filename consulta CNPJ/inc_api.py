# -----------------------------------------------------------------------------+
# Transportes Eireli                                                      |
# Consulta de CNPJ via web services                                            |
# Cacador, 25 de Junho de 2021                                                 |
# Luciano Carbonera                                                            |
# -----------------------------------------------------------------------------+
import inc_api_aux, inc_util
import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup as bs

def dados_simples_nfe_io(cnpj):
    infos = inc_api_aux.select_url_simples_nfe_io()
    url = infos[0]
    token_nfe_io = str(infos[1])
    url = inc_util.format_string_api_nfe_io(url, cnpj, token_nfe_io)

    request = requests.get(url)
    dados = request.json()
    dados = dict({
        ('nome', (dados['name'])),
        ('regime',(dados['taxRegime']))
    })
    #print(json.dumps(dados, sort_keys=True, indent=4, separators=(',', ':'))) #sort key ordena chaves
    return dados

def dados_ie_nfe_io(cnpj, uf):
    global dados_ie, error
    infos = inc_api_aux.select_url_ie_nfe_io()
    url = infos[0]
    token_nfe_io = str(infos[1])
    url = inc_util.format_string_api_nfe_io(url, cnpj, token_nfe_io)

    request = requests.get(url)
    dados = dict(request.json())
    try:
        error = dados['errors']
        print("Não Contribuinte estadual")
    except:
        pass

    estado1 = []
    estado = []
    inscricao = []
    status = []

    ie_estadual = (dados.get('taxPayer'))

    if ie_estadual:
        for ie in ie_estadual:
            estado_aux = str([(ie['state']['abbreviation'])])
            estado_aux = inc_util.format_string_token(estado_aux)

            if uf == estado_aux:
                estado = [(ie['state']['abbreviation'])] + estado
                inscricao = [(ie['stateTaxNumber'])] + inscricao
                status = [(ie['statusStateTax'])] + status

    dados_ie = {
        'uf': estado,
        'inscricao': inscricao,
        'status': status
    }
    return dados_ie

def dados_cnpj_nfe_io(cnpj):
    infos = inc_api_aux.select_url_cnpj_nfe_io()
    url = infos[0]
    token_nfe_io = str(infos[1])
    url = inc_util.format_string_api_nfe_io(url, cnpj, token_nfe_io)

    request = requests.get(url)
    dados = request.json()

    cnpj = (dados['federalTaxNumber'])
    nome = (dados['name'])
    tipo_logradouro = (dados.get('address').get('streetSuffix'))
    logradouro = (tipo_logradouro + ": " + (dados.get('address').get('street')))
    numero = (dados.get('address').get('number'))
    bairro = (dados.get('address').get('district'))
    cep = (dados.get('address').get('postalCode'))
    municipio = dados.get('address').get('city').get('name')
    estado = (dados.get('address').get('state'))
    email = (dados['email']).lower()
    phones = (dados.get('phones'))
    telefone = (phones[0]['ddd']) + '-' + (phones[0]['number'])
    cnae = (dados.get('economicActivities'))
    cnae = (cnae[0]['code'])
    nat_jur = (dados.get('legalNature').get('code'))
    situacao= (dados['status'])

    dados = {
        'cnpj': cnpj,
        'nome': nome,
        'logradouro': logradouro,
        'numero': numero,
        'bairro': bairro,
        'cep': cep,
        'municipio': municipio,
        'estado': estado,
        'email': email,
        'telefone': telefone,
        'cnae': cnae,
        'nat_jur': nat_jur,
        'situacao': situacao
    }
    #print(json.dumps(dados, sort_keys=True, indent=4, separators=(',', ':')))
    return dados

def dados_cnpj_receita_ws(cnpj):
    infos = inc_api_aux.select_url_ws()
    url = infos[0]
    token_ws = str(infos[1])
    token_ws = inc_util.format_string_token(token_ws)
    url = inc_util.format_string_api_ws(url, cnpj)
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer {}" . format(token_ws)

    request = requests.get(url, headers=headers)
    dados = request.json()

    cnpj = (dados['cnpj'])
    nome = (dados['nome'])
    logradouro = (dados.get('logradouro'))
    numero = (dados.get('numero'))
    cep = (dados.get('cep'))
    municipio = dados.get('municipio')
    estado = (dados.get('uf'))
    email = (dados['email']).lower()
    telefone = (dados.get('telefone'))
    cnae = (dados.get('atividade_principal'))
    cnae = (cnae[0]['code'])
    nat_jur = (dados.get('natureza_juridica'))
    situacao = (dados['situacao'])

    dados = {
        'cnpj': cnpj,
        'nome': nome,
        'logradouro': logradouro,
        'numero': numero,
        'cep': cep,
        'municipio': municipio,
        'estado': estado,
        'email': email,
        'telefone': telefone,
        'cnae': cnae,
        'nat_jur': nat_jur,
        'situacao': situacao
    }
    #print(dados)
    return dados

def dados_ie_sim_consultas(cnpj, estado):
    global IE, situacao_flag, dados

    infos = inc_api_aux.select_url_ie_sim_consultas()
    url = infos[0]
    token_sim_consultas = str(infos[1])
    parser = 'Sintegra'
    url = inc_util.format_string_api_sim_consultas(url, token_sim_consultas, parser, cnpj, estado)

    xml = bs(requests.get(url).text, 'lxml')

    for linha in xml.findAll('parsedatacolumn'):

        tag = linha.find('key')
        val = linha.find('value')

        if tag.contents[0] == 'SituacaoFlag':
            situacao_flag = val.contents[0]

        if tag.contents[0] == 'IE':
            IE = val.contents[0]

    if situacao_flag == '1':
        dados = {
            'UF': estado,
            'IE': IE,
            'status': 'habilitado'
        }
        return dados
    else:
        print("Inscrição estadual Não ativa")

def dados_simples_sim_consultas(cnpj):
    global situacao_simples, situacao_simei
    infos = inc_api_aux.select_url_ie_sim_consultas()
    url = infos[0]
    token_sim_consultas = str(infos[1])
    parser = 'SimplesNacional'
    url = inc_util.format_string_api_simples_sim_consultas(url, token_sim_consultas, parser, cnpj)

    xml = bs(requests.get(url).text, 'lxml')

    for linha in xml.findAll('parsedatacolumn'):

        tag = linha.find('key')
        val = linha.find('value')

        if tag.contents[0] == 'SituacaoSIMPLES':
            situacao_simples = val.contents[0]

        if tag.contents[0] == 'SituacaoSIMEI':
            situacao_simei = val.contents[0]

    dados = {
        'simples': situacao_simples,
        'MEI': situacao_simei
    }
    return dados

def dados_cnpj_ndd_sim_consulta(cnpj):
    global situacao_cadastro, nat_jur, cnae, telefone, email, uf, municipio, cep, numero, \
        logradouro, fantasia, razao, complemento, bairro

    infos = inc_api_aux.select_url_ie_sim_consultas()
    url = infos[0]
    token_sim_consultas = str(infos[1])
    parser = 'RECEITAFEDERALCNPJ'
    url = inc_util.format_string_api_simples_sim_consultas(url, token_sim_consultas, parser, cnpj)

    xml = bs(requests.get(url).text, 'lxml')

    for linha in xml.findAll('parsedatacolumn'):

        tag = linha.find('key')
        val = linha.find('value')

        if tag.contents[0] == 'CodDescNaturezaJuridica':
            nat_jur = val.contents[0]

        elif tag.contents[0] == 'SituacaoCadastro':
            situacao_cadastro = val.contents[0]

        elif tag.contents[0] == 'CNPJ':
            cnpj = val.contents[0]

        elif tag.contents[0] == 'RazaoSocial':
            razao = val.contents[0]
            print(razao)

        elif tag.contents[0] == 'NomeFantasia':
            fantasia = val.contents[0]

        elif tag.contents[0] == 'Logradouro':
            logradouro = val.contents[0]

        elif tag.contents[0] == 'Numero':
            numero = val.contents[0]

        elif tag.contents[0] == 'Bairro':
            bairro = val.contents[0]

        elif tag.contents[0] == 'Complemento':
            complemento = val.contents[0]

        elif tag.contents[0] == 'CEP':
            cep = val.contents[0]

        elif tag.contents[0] == 'Municipio':
            municipio = val.contents[0]

        elif tag.contents[0] == 'UF':
            uf = val.contents[0]

        elif tag.contents[0] == 'Email':
            email = val.contents[0].lower()

        elif tag.contents[0] == 'Telefone':
            telefone = val.contents[0]

        elif tag.contents[0] == 'CodDescAtividadePrincipal':
            cnae = val.contents[0]

    dados = {
            'cnpj': cnpj,
            'razao': razao,
            'fantasia': fantasia,
            'logradouro': logradouro,
            'numero': numero,
            'bairro': bairro,
            'complemento': complemento,
            'cep': cep,
            'municipio': municipio,
            'estado': uf,
            'email': email,
            'telefone': telefone,
            'cnae': cnae,
            'nat_jur': nat_jur,
            'situacao': situacao_cadastro
        }
    return dados




















