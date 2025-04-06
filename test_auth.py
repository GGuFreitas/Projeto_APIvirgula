from modules.auth import carregar_token, obter_token_valido

print("Token carregado diretamente:", carregar_token())
print("Token válido (com renovação):", obter_token_valido())