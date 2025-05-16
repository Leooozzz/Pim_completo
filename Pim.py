import os
import time
import json
import shutil  # 🆕 Para backup
from cryptography.fernet import Fernet
import webbrowser as wb
from statistics import mean, median, mode, StatisticsError  # 🆕 Estatísticas

# Config
ARQUIVO_USUARIOS = "usuarios.json"
CHAVE_CRIPTOGRAFIA = "chave_criptografia.key"

# Funções de criptografia 
def gerar_ou_carregar_chave():
    if os.path.exists(CHAVE_CRIPTOGRAFIA):
        with open(CHAVE_CRIPTOGRAFIA, "rb") as f:
            return f.read()
    else:
        chave = Fernet.generate_key()
        with open(CHAVE_CRIPTOGRAFIA, "wb") as f:
            f.write(chave)
        return chave

def criptografar_dados(dados, chave):
    fernet = Fernet(chave)
    return fernet.encrypt(json.dumps(dados).encode())

def descriptografar_dados(dados_criptografados, chave):
    fernet = Fernet(chave)
    try:
        dados = fernet.decrypt(dados_criptografados).decode()
        return json.loads(dados)
    except:
        return {}

# 🆕 Backup dos dados
def fazer_backup():
    if os.path.exists(ARQUIVO_USUARIOS):
        shutil.copy(ARQUIVO_USUARIOS, f"backup_{ARQUIVO_USUARIOS}")

# Funções para manipulação de usuários
def carregar_usuarios():
    chave = gerar_ou_carregar_chave()
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "rb") as file:
            dados_criptografados = file.read()
            return descriptografar_dados(dados_criptografados, chave)
    return {}

def salvar_usuarios():
    chave = gerar_ou_carregar_chave()
    dados_criptografados = criptografar_dados(usuarios, chave)
    with open(ARQUIVO_USUARIOS, "wb") as file:
        file.write(dados_criptografados)
    fazer_backup()  # 🆕 Backup automático

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def login():
    limpar_terminal()
    print("🔑 Sistema de Login 🔑")
    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")

    if usuario == "administrador" and senha == "admin123":
        print(f"Bem-vindo, {usuario}!\nAcessando painel de estatísticas...")
        time.sleep(2)
        menu_estatisticas()
        return True

    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        print(f"Bem-vindo, {usuario}!\nRedirecionando para o menu inicial, aguarde...")
        usuarios[usuario]["acessos"] += 1
        usuarios[usuario]["ultimo_login"] = time.time()
        salvar_usuarios()
        time.sleep(2)
        menu_inicial(usuario)
        return True
    else:
        print("Usuário ou senha incorretos. Tente novamente.")
        time.sleep(2)
        return False

def registrar():
    limpar_terminal()
    print("📋 Sistema de Registro 📋")
    usuario = input("Digite um nome de usuário: ")
    if usuario in usuarios:
        print("Usuário já existe. Tente outro nome.")
        time.sleep(2)
        return False

    senha = input("Digite uma senha: ")
    senha_confirmada = input("Confirme sua senha: ")
    if senha != senha_confirmada:
        print("❌ As senhas não coincidem. Tente novamente.")
        time.sleep(2)
        return False

    try:
        idade = int(input("Digite sua idade: "))
    except ValueError:
        print("Idade inválida. Tente novamente.")
        time.sleep(2)
        return False

    usuarios[usuario] = {
        "senha": senha,
        "idade": idade,
        "acessos": 0,
        "tempo_total": 0,
        "ultimo_login": time.time()
    }
    salvar_usuarios()
    print(f"✅ Usuário {usuario} registrado com sucesso!")
    time.sleep(2)
    return True

def loginregistro():
    while True:
        limpar_terminal()
        print("Selecione a opção abaixo:")
        print("[1] - Login")
        print("[2] - Registrar")
        print("[3] - Voltar")
        
        try:
            opcao = int(input("Digite sua escolha: "))
            if opcao == 1:
                if login():
                    break
            elif opcao == 2:
                if registrar():
                    print("✅ Agora você pode fazer login.")
            elif opcao == 3:
                break
            else:
                print("⚠️ Opção inválida. Tente novamente.")
        except ValueError:
            print("⚠️ Por favor, insira um número válido.")

def menu_inicial(usuario):
    inicio = time.time()
    while True:
        limpar_terminal()
        try:
            inicial = int(input(f"Olá {usuario}, Selecione a opção abaixo:\n[1] - Office\n[2] - Aulas\n[3] - Sair\n"))
            if inicial == 1:
                office()
            elif inicial == 2:
                aulas()
            elif inicial == 3:
                tempo = time.time() - inicio
                usuarios[usuario]["tempo_total"] += tempo
                salvar_usuarios()
                limpar_terminal()
                print("\nSaindo... Até mais!")
                break
            else:
                print("⚠️ Opção inválida. Tente novamente.")
        except ValueError:
            print("⚠️ Entrada inválida. Use números.")

def menu_estatisticas():
    while True:
        limpar_terminal()
        print("📊 Painel de Estatísticas do Sistema 📊")
        total_usuarios = len(usuarios)
        total_acessos = sum(user["acessos"] for user in usuarios.values())
        total_idade = sum(user["idade"] for user in usuarios.values() if "idade" in user)
        tempo_total_uso = sum(user["tempo_total"] for user in usuarios.values())

        idades = [user["idade"] for user in usuarios.values()]
        idade_media = total_idade / total_usuarios if total_usuarios > 0 else 0
        idade_mediana = median(idades) if idades else 0  
        try:
            idade_moda = mode(idades)  
        except StatisticsError:
            idade_moda = "Não definida (valores únicos)"  

        tempo_medio = tempo_total_uso / total_usuarios if total_usuarios > 0 else 0

        print(f"Usuários registrados: {total_usuarios}")
        print(f"Idade média dos usuários: {idade_media:.1f}")
        print(f"Idade mediana dos usuários: {idade_mediana}")
        print(f"Idade moda dos usuários: {idade_moda}")
        print(f"Total de acessos ao sistema: {total_acessos}")
        print(f"Tempo médio de uso (em segundos): {tempo_medio:.2f}")
        
        opcao = input("\nDigite [1] para voltar: ")
        if opcao == "1":
            break

def office():
    while True:
        limpar_terminal()
        office = int(input("Para voltar ao menu inicial digite 2: "))
        if office == 2:
            print("Voltando ao menu inicial...")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")

def aulas():
    while True:
        limpar_terminal()
        aulas = int(input("Selecione uma opção de Aulas:\n[1] - Pensamento Lógico Computacional\n[2] - Infraestrutura Computacional\n[3] - Cibersegurança\n[4] - Voltar ao menu inicial\n"))
        if aulas == 1:
            print("Você escolheu Pensamento Lógico Computacional.")
            wb.open('https://drive.google.com/file/d/1zwUZLDHG1bZTvdsqryX_hWWxiIqq7I82/view?usp=sharing')
            time.sleep(10)
        elif aulas == 2:
            print("Você escolheu Infraestrutura Computacional.")
            wb.open('https://drive.google.com/file/d/1tYR5bL6RBdus49-VhmKr0y4TRhF98vwo/view?usp=sharing')
            time.sleep(10)
        elif aulas == 3:
            print("Você escolheu Cibersegurança.")
            wb.open('https://drive.google.com/file/d/1C6i84NHOEU0KoJlG9dq94SPP1KjNtogX/view?usp=sharing')
            time.sleep(10)
        elif aulas == 4:
            print("Voltando ao menu inicial...")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")

usuarios = carregar_usuarios()
loginregistro()