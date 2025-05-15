import requests

API_KEY = '08611eb9326947c8b93855d73e7d83a8'


def buscar_noticias(tema, quantidade):
    """
    Função que busca notícias da NewsAPI com base em um tema e uma quantidade.

    Parâmetros:
    tema (str): O tema que o usuário pretende pesquisar nas notícias.
    quantidade (int): A quantidade de notícias a ser retornada (entre 1 e 10).

    Retorna:
    list: Uma lista de artigos encontrados para o tema, tendo título, entre outras especificidades que estão o autor,fonte  etc.
    """
    url = 'https://newsapi.org/v2/everything'

    parametros = {
        'q': tema,
        'language': 'pt',
        'pageSize': quantidade,
        'sortBy': 'publishedAt',
        'apiKey': API_KEY
    }

    resposta = requests.get(url, params=parametros)


    if resposta.status_code != 200:
        print("Erro ao buscar notícias.")
        return []

    dados = resposta.json()
    return dados['articles']


def mostrar_noticias(lista_noticias):
    """
    Função que exibe as notícias de uma lista fornecida.

    Parâmetros:
    lista_noticias (list): A lista de notícias que será exibida, cada item contém um artigo com título, fonte e autor.

    Retorna:
    None
    """
    for i, noticia in enumerate(lista_noticias, start=1):
        print(f"\nNotícia {i}")
        print("Título:", noticia.get('title', 'Sem título'))
        print("Fonte:", noticia.get('source', {}).get('name', 'Desconhecida'))
        print("Autor:", noticia.get('author', 'Desconhecido'))



tema = input("Digite o tema que deseja pesquisar: ")


while True:
    try:
        quantidade = int(input("Quantas notícias deseja? (1 a 10): "))
        if 1 <= quantidade <= 10:
            break
        else:
            print("Digite um número entre 1 e 10.")
    except:
        print("Por favor, digite um número válido.")


noticias = buscar_noticias(tema, quantidade)
mostrar_noticias(noticias)
