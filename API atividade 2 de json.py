import requests

USUARIOS_DB = {
    1: {"email": "joaovictorcazabonet@gmail.com", "senha": "1234"},
    2: {"email": "ricardolopezgarcia@gmail.com", "senha": "abcd"},
    3: {"email": "robertogomez@gmail.com", "senha": "senha123"},
}

INTERACOES = {"posts_visualizados": 0, "comentarios_visualizados": 0, "posts_criados": 0}
BASE_URL = "https://jsonplaceholder.typicode.com"
LIMIT_EXIBICAO = 5

def requisicao_get(endpoint, params=None):
    """Busca dados do endpoint e retorna em formato JSON, ou None em caso de erro."""
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro: {e}")
        return None

def requisicao_post(endpoint, payload):
    """Cria dados no endpoint e retorna o objeto criado, ou None em caso de erro."""
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", json=payload)
        if response.status_code == 201:
            return response.json()
    except requests.RequestException as e:
        print(f"Erro: {e}")
    return None

def login():
    """Faz login com e-mail e senha. Retorna o ID do usuário ou None se falhar."""
    email = input("E-mail: ")
    senha = input("Senha: ")
    for user_id, dados in USUARIOS_DB.items():
        if dados["email"] == email and dados["senha"] == senha:
            print("Login bem-sucedido!\n")
            return user_id
    print("Credenciais inválidas.\n")
    return None

def exibir_posts(posts):
    """Exibe os posts passados e incrementa o contador de posts visualizados."""
    for post in posts[:LIMIT_EXIBICAO]:
        print(f"Post ID: {post['id']}\nTítulo: {post['title']}\n")
        INTERACOES["posts_visualizados"] += 1

def menu_interativo(user_id):
    """Exibe o menu de opções para o usuário e executa a escolha."""
    while True:
        escolha = input("""
1. Visualizar posts
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
    """Inicia o programa, solicitando login e executando o menu."""
    while True:
        user_id = login()
        if user_id:
            menu_interativo(user_id)
        else:
            break

if __name__ == "__main__":
    main()
