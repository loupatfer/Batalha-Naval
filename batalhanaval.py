import random

nomes_barcos = ["Carrier", "Battleship", "Fragate", "Submarine", "Destroyer"]
#Tamanho por ordem de nome: 5,4,3,3,2
tamanho_barcos = {"Carrier": 5, "Battleship": 4, "Fragate": 3, "Submarine": 3, "Destroyer": 2}

def obter_tamanho_barco(nome):
    return tamanho_barcos.get(nome, 0)

def nome_jogador():
    while True:
        username = input("Insere o teu nome: ")
        if username:
            print(f'Bem vindo {username}!')
            return username
        
tamanho_mapa = 10

def criar_campo(tamanho_mapa):
    return [["_" for _ in range(tamanho_mapa)] for _ in range(tamanho_mapa)]

def mostrar_campo(campo):
    for row in campo:
        print(" ".join(row))

def coordenada_barco_utilizador(campo_utilizador, campo_ocupado, nome):
    existe = 0
    i = 0
    while True:
        try:
            row = int(input(f"Insere a linha para o {nome} (0-9): "))
            col = int(input(f"Insere a coluna para o {nome} (0-9): "))
            sentido = int(input("Insere o sentido da colocação (0-Horizontal; 1-Vertical): "))
            tamanho = obter_tamanho_barco(nome)

            if sentido == 1:  # Vertical
                if row + tamanho > 10:
                    print(f"O {nome} nao cabe no tabuleiro na vertical")
                    continue
                if any(campo_ocupado[row + i][col] == "X" for i in range(tamanho)):
                    print(f"Existem coordenadas ja ocupadas, reposicione o {nome}")
                    continue
                for i in range(tamanho):
                    campo_ocupado[row + i][col] = "X"
                    campo_utilizador[row + i][col] = nome[0]
                break
            elif sentido == 0:  # Horizontal
                if col + tamanho > 10:
                    print(f"O {nome} nao cabe no tabuleiro na horizontal")
                    continue
                if any(campo_ocupado[row][col + i] == "X" for i in range(tamanho)):
                    print(f"Existem coordenadas ja ocupadas, reposicione o {nome}")
                    continue
                for i in range(tamanho):
                    campo_ocupado[row][col + i] = "X"
                    campo_utilizador[row][col + i] = nome[0]
                break
            else:
                print("Sentido inválido. Insira 0 para horizontal ou 1 para vertical.")

        except ValueError:
            print("Por favor, insere um inteiro válido.")
        except IndexError:
            print("Coordenadas fora do limite do mapa. Tente novamente.")

def verifica_posicao_valida(campo_ocupados, row, col, tamanho, sentido):
    if sentido == 1:
        if row + tamanho > tamanho_mapa:
            return False
        if any(campo_ocupados[row + i][col] == "X" for i in range(tamanho)):
            return False
    elif sentido == 0:
        if col + tamanho > tamanho_mapa:
            return False
        if any(campo_ocupados[row][col + i] == "X" for i in range(tamanho)):
            return False
    return True

def coloca_barco_aleatorio(campo, campo_ocupados, nome):
    tamanho = obter_tamanho_barco(nome)
    sentido = random.choice([0,1])
    while True:
        row = random.randint(0, tamanho_mapa - 1)
        col = random.randint(0, tamanho_mapa - 1)
        if verifica_posicao_valida(campo_ocupados, row, col, tamanho, sentido):
            if sentido == 1:
                for i in range(tamanho):
                    campo_ocupados[row + i][col] = "X"
                    campo[row + i][col] = nome[0]
            elif sentido == 0:
                for i in range(tamanho):
                    campo_ocupados[row][col + i] = "X"
                    campo[row][col + i] = nome[0]
            return

if __name__ == "__main__":
    nome_jogador()
    
    campo_utilizador = criar_campo(tamanho_mapa)
    campo_computador = criar_campo(tamanho_mapa)
    campo_ocupados_usuario = criar_campo(tamanho_mapa)
    campo_ocupados_usuario.append("teste user")
    campo_ocupados_computador = criar_campo(tamanho_mapa)
    campo_ocupados_computador.append("teste comp")

    for nome_barcos in nomes_barcos:
        coordenada_barco_utilizador(campo_utilizador, campo_ocupados_usuario, nome_barcos)
    
    for nome_barcos in nomes_barcos:
        coloca_barco_aleatorio(campo_computador, campo_ocupados_computador, nome_barcos)

    print("\n\n****************CAMPOS USUARIO**********************\n\n")
    mostrar_campo(campo_ocupados_usuario)
    mostrar_campo(campo_utilizador)
    
    print("\n\n\n****************CAMPOS COMPUTADOR**********************\n\n")
    mostrar_campo(campo_ocupados_computador)
    mostrar_campo(campo_computador)