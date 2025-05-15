import requests

USUARIOS_DB = {
    1: {"email": "joaovictorcazabonet@gmail.com", "senha": "1234"},
    2: {"email": "ricardolopezgarcia@gmail.com", "senha": "abcd"},
    3: {"email": "robertogomez@gmail.com", "senha": "senha123"},
}

INTERACOES = {
    "posts_visualizados": 0,
    "comentarios_visualizados": 0,
    "posts_criados": 0
}

BASE_URL = "https://jsonplaceholder.typicode.com"
LIMIT_EXIBICAO = 5


def requisicao_get(endpoint, params=None):
    """
    Faz uma requisição GET para o endpoint da API.

    Tenta buscar os dados no endpoint passado, lidando com erros de rede ou falhas na API.
    Se der tudo certo, retorna os dados em formato JSON.

    :param endpoint: O caminho do endpoint que você quer acessar (ex: "posts", "comments").
    :param params: Parâmetros opcionais que podem ser passados na requisição (padrão é None).
    :return: Dados no formato JSON, ou None se algo der errado.
    """
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro: {e}")
        return None


def requisicao_post(endpoint, payload):
    """
    Faz uma requisição POST para criar um novo dado na API.

    Envia os dados para o endpoint informado. Se a requisição for bem-sucedida,
    ela retorna os dados criados; caso contrário, mostra um erro.

    :param endpoint: O caminho do endpoint onde você quer enviar os dados (ex: "posts").
    :param payload: Os dados que você quer enviar para a API (geralmente um dicionário).
    :return: Dados criados no formato JSON ou None se der erro.
    """
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", json=payload)
        if response.status_code == 201:
            return response.json()
    except requests.RequestException as e:
        print(f"Erro: {e}")
    return None


def login():
    """
    Permite que o usuário faça login no sistema.

    Pede um e-mail e uma senha, e valida se as credenciais estão corretas.
    Se o login for bem-sucedido, retorna o ID do usuário; caso contrário, retorna None.

    :return: O ID do usuário se o login for bem-sucedido, ou None se as credenciais estiverem erradas.
    """
    email = input("E-mail: ")
    senha = input("Senha: ")
    for user_id, dados in USUARIOS_DB.items():
        if dados["email"] == email and dados["senha"] == senha:
            print("Login bem-sucedido!\n")
            return user_id
    print("Credenciais inválidas.\n")
    return None


def exibir_posts(posts):
    """
    Exibe os posts passados e incrementa o contador de posts visualizados.

    Mostra um máximo de 5 posts por vez.

    :param posts: Lista de posts que será exibida.
    """
    for post in posts[:LIMIT_EXIBICAO]:
        print(f"Post ID: {post['id']}\nTítulo: {post['title']}\n")
        INTERACOES["posts_visualizados"] += 1


def menu_interativo(user_id):
    """
    Exibe o menu e permite ao usuário navegar entre diferentes opções.

    O usuário pode visualizar posts, comentários, seus próprios posts,
    filtrar posts por outro usuário, criar um novo post ou sair.

    :param user_id: O ID do usuário que está logado e que será usado para ações específicas, como visualizar seus posts.
    """
    while True:
        escolha = input("""\n1. Visualizar posts
2. Visualizar comentários
3. Meus posts
4. Filtrar posts por usuário
5. Criar post
6. Sair
Escolha: """)

        if escolha == "1":
            exibir_posts(requisicao_get("posts"))
        elif escolha == "2":
            comentarios = requisicao_get("comments")
            for c in comentarios[:LIMIT_EXIBICAO]:
                print(f"Comentário ID: {c['id']}\n{c['body']}")
            INTERACOES["comentarios_visualizados"] += 1
        elif escolha == "3":
            exibir_posts(requisicao_get("posts", params={"userId": user_id}))
        elif escolha == "4":
            user_id_filtro = int(input("ID do usuário: "))
            exibir_posts(requisicao_get("posts", params={"userId": user_id_filtro}))
        elif escolha == "5":
            titulo = input("Título: ")
            corpo = input("Conteúdo: ")
            novo_post = requisicao_post("posts", {"userId": user_id, "title": titulo, "body": corpo})
            if novo_post:
                print("Post criado com sucesso!")
            INTERACOES["posts_criados"] += 1
        elif escolha == "6":
            print(f"Resumo: {INTERACOES}")
            break
        else:
            print("Opção inválida.")


def main():
    """
    Função principal do programa.

    Aqui começa o fluxo. O usuário precisa fazer login primeiro para poder acessar o menu interativo.
    O programa continuará até o usuário decidir sair.

    """
    while True:
        user_id = login()  # Guarda o valor retornado de login()
        if user_id:
            menu_interativo(user_id)  # Passa o user_id para menu_interativo()
        else:
            break


if __name__ == "__main__":
    main()
