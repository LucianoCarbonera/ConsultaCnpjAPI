import inc_database

def select_url_ws():
    con = inc_database.Db()
    sql_url = "select cca002_url from cca002 where cca002_ser = 1"
    url =  inc_database.Db.select(con, sql_url)
    sql_chave = "select cca002_chave from cca002 where cca002_ser = 1"
    chave = inc_database.Db.select(con, sql_chave)
    infos = [url, chave]
    return infos

def select_url_simples_nfe_io():
    con = inc_database.Db()
    sql_url = "select cca002_url from cca002 where cca002_ser = 2"
    url =  inc_database.Db.select(con, sql_url)
    sql_chave = "select cca002_chave from cca002 where cca002_ser = 2"
    chave = inc_database.Db.select(con, sql_chave)
    infos = [url, chave]
    return infos

def select_url_ie_nfe_io():
    con = inc_database.Db()
    sql_url = "select cca002_url from cca002 where cca002_ser = 4"
    url =  inc_database.Db.select(con, sql_url)
    sql_chave = "select cca002_chave from cca002 where cca002_ser = 4"
    chave = inc_database.Db.select(con, sql_chave)
    infos = [url, chave]
    return infos

def select_url_cnpj_nfe_io():
    con = inc_database.Db()
    sql_url = "select cca002_url from cca002 where cca002_ser = 7"
    url =  inc_database.Db.select(con, sql_url)
    sql_chave = "select cca002_chave from cca002 where cca002_ser = 7"
    chave = inc_database.Db.select(con, sql_chave)
    infos = [url, chave]
    return infos

def select_url_ie_sim_consultas():
    con = inc_database.Db()
    sql_url = "select cca002_url from cca002 where cca002_ser = 9"
    url =  inc_database.Db.select(con, sql_url)
    sql_chave = "select cca002_chave from cca002 where cca002_ser = 9"
    chave = inc_database.Db.select(con, sql_chave)
    infos = [url, chave]
    return infos

def manipular():
    con = inc_database.Db()
    sql = "update rel001 set rel001_nome = 'Romaneio de coletas teste 2' where rel001_ser = 1"
    test = inc_database.Db.manipular(con, sql)

