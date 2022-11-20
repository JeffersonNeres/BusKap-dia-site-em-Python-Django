from django.shortcuts import render
from buscas import raspagem
# Create your views here.

#arquivo raspagem.py tras duas funçoes que oferece a views um dicionario com chave titulo, valor url extraida
def index(request):
    if request.method == 'POST':
        link_busca = request.POST['input_link']
        resultado = raspagem.extrai_links(link_busca)
        erro = {"erro": "erro"}
        if resultado == erro:
            print(resultado, erro) 
            return render(request, 'index3.html')
        titulo_wiki = raspagem.extrai_titulo(link_busca)
        dados = {
            'resultados' : resultado,
            'titulo_wiki': titulo_wiki,
            'link_wiki': link_busca
        }
        return render(request, 'index2.html', dados)
    return render(request, 'index.html')

def index2(request):
    if request.method == 'POST':
        link_busca = request.POST['input_link2']
        resultado = raspagem.extrai_links(link_busca)
        titulo_wiki = raspagem.extrai_titulo(link_busca)
        dados = {
            'resultados' : resultado,
            'titulo_wiki': titulo_wiki,
            'link_wiki': link_busca
        }
        return render(request, 'index2.html', dados)
    return render(request, 'index.html')
        



