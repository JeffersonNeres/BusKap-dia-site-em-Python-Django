from requests import get
from bs4 import BeautifulSoup
import pymysql
import re

def extrai_titulo(site_intro):
    #sera feita a extração do titulo da pagina
    site = get(site_intro)
    tags = BeautifulSoup(site.text, "html5lib")
    title = tags.find("title").text
    #sera removido caracteres que não são aceitos no banco de dados
    title = re.sub(' – Wikipédia, a enciclopédia livre', '', title)
    remove = " .:(),'@*%#!;?+/&¨<>"
    for i in range(len(remove)):
        title = title.replace(remove[i], "_")
    return title
 

def extrai_links(site_intro):
    #captura o erro caso usuario não digite uma url valida
    try:
        nome_tabela = extrai_titulo(site_intro)
    except:
        erro = {"erro": "erro"}
        return erro
    #captura um erro caso não seja salvo no banco de dados, site continua normal
    try:
        conexao = pymysql.connect(
                                    host='localhost', # é necessario fazer o loguin com sues dados no Workbench mysql
                                    user='root',
                                    password='*******',
                                    database='BusKapedia', #para realizar o salvamento, crie o banco de dados Buskpedia
        )
        
        Deleta_tabela = f"DROP TABLE IF EXISTS {nome_tabela}"

        link_vira_tabela = f"""
                            CREATE TABLE {nome_tabela} (
                                id_link INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                titulo_wikipedia VARCHAR(2048),
                                link_resultado VARCHAR(2048)
                                )"""
        cursor = conexao.cursor()
        cursor.execute(Deleta_tabela)
        cursor.execute(link_vira_tabela)
        acesso_a_db = "ok"
    except:
        acesso_a_db = "erro"
        print("erro! nada salvo do banco de dados!")
    
    #criação da nova url extraida
    site = get(site_intro)
    tags = BeautifulSoup(site.text, "html5lib")
    subtitles = tags.find_all("a", attrs = {"class" : "mw-redirect"})
    [h2.text for h2 in subtitles]
    paginas = ["https://pt.wikipedia.org" + h2["href"] for h2 in subtitles]

    #criação do dicionario com o titulo e link de cada url extraida
    links_resultados = {}
    n_pagina = 0
    chave = ""
    numero_da_pagina = 0
    for pagina in paginas:
        numero_da_pagina += 1
        chave = extrai_titulo(paginas[n_pagina])
        links_resultados[chave] = paginas[n_pagina]
        if acesso_a_db == "ok":
            link_para_db = f"""INSERT INTO {nome_tabela} (titulo_wikipedia, link_resultado)
                                    VALUES ("{chave}", "{paginas[n_pagina]}")"""
            cursor.execute(link_para_db)
            conexao.commit()
        n_pagina += 1
        if numero_da_pagina >= 10:
            break
    if acesso_a_db == "ok":
        cursor.close
        conexao.close()
    return links_resultados

