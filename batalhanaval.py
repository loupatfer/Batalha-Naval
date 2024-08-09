import random

nomes_barcos = ["Carrier", "Battleship", "Fragate", "Submarine", "Destroyer"]
#Tamanho por ordem de nome: 5,4,3,3,2
tamanho_barcos = {"Carrier": 5, "Battleship": 4, "Fragate": 3, "Submarine": 3, "Destroyer": 2}
pontos_barcos = {"C": 100, "B": 80, "F": 60, "S": 60, "D": 40}

def obter_tamanho_barco(nome):
    return tamanho_barcos.get(nome, 0)

def obter_pontos_barco(nome):
    return pontos_barcos.get(nome,0)

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
        
def atacar(campo_oponente, campo_visivel, row, col, pontuacao_jogador):
    if campo_visivel[row][col] != "_":
        print("Esta coordenada já foi atacada")
        return False
    
    if campo_oponente[row][col] != "_":
        print("Acertou em um barco!")
        barco_acertado = campo_oponente[row][col]
        campo_visivel[row][col] = "X"
        campo_oponente[row][col] = "X"

        if not any(barco_acertado == campo_oponente[r][c] for r in range(tamanho_mapa) for c in range(tamanho_mapa)):
            for nome, inicial in zip(nome_barcos, [n[0] for n in nome_barcos]):
                if inicial == barco_acertado:
                    pontuacao_jogador += obter_pontos_barco(nome)
                    print(f"Destruíste um {nome}! Ganhou {obter_pontos_barco(nome)} pontos!")
                    break
    else:
        print("Errou")
        campo_visivel[row][col] = "-"
    return True

def computador_ataca(campo_jogador, campo_visivel_computador, pontuacao_computador):
    while True:
        row = random.randint(0, tamanho_mapa - 1)
        col = random.randint(0, tamanho_mapa -1)

        if campo_visivel_computador[row][col] != "_":
            continue

        print(f"Computador ataca na linha {row}, coluna {col}.")

        if campo_jogador[row][col] != "_":
            print("Computador acertou em um dos teus barcos!")
            barco_acertado = campo_jogador[row][col]
            campo_visivel_computador[row][col] = "X"
            campo_jogador[row][col] = "X"

            if not any(barco_acertado == campo_jogador[r][c] for r in range(tamanho_mapa) for c in range(tamanho_mapa)):
                for nome, inicial in zip(nome_barcos, [n[0] for n in nome_barcos]):
                    if inicial == barco_acertado:
                        pontuacao_computador += obter_pontos_barco(nome)
                        print(f"O Computador destruiu o teu {nome} e ganhou {obter_pontos_barco(nome)} pontos!")
                        break
        else:
            print("Computador errou!")
            campo_visivel_computador[row][col] = "-"
        break   

if __name__ == "__main__":
    nome_jogador()
    
    campo_utilizador = criar_campo(tamanho_mapa)
    campo_computador = criar_campo(tamanho_mapa)
    campo_ocupados_usuario = criar_campo(tamanho_mapa)
    campo_ocupados_computador = criar_campo(tamanho_mapa)

    pontuacao_jogador = 0
    pontuacao_computador = 0
    
    for nome_barcos in nomes_barcos:
        coordenada_barco_utilizador(campo_utilizador, campo_ocupados_usuario, nome_barcos)
    
    for nome_barcos in nomes_barcos:
        coloca_barco_aleatorio(campo_computador, campo_ocupados_computador, nome_barcos)

    print("\n\n****************CAMPOS USUARIO***********************\n\n")
    mostrar_campo(campo_utilizador)
    
    print("\n\n\n****************CAMPOS COMPUTADOR**********************\n\n")
    mostrar_campo(campo_computador)

    campo_visivel_jogador = criar_campo(tamanho_mapa)
    campo_visivel_computador = criar_campo(tamanho_mapa)

    while True:
        while True:
            try:
                print("\nAtaca o tabuleiro do computador!")
                row = int(input(f"Insere a linha para o ataque (0-9): "))
                col = int(input(f"Insere a coluna para o ataque (0-9): "))
                if atacar(campo_computador, campo_visivel_jogador, row, col,pontuacao_jogador):
                    break
            except ValueError:
                print("Por favor, insere um inteiro válido.")
            except IndexError:
                print("Coordenadas fora do limite do mapa. Tente novamente.")
        
        print("\nTabuleiro do jogador após o ataque:\n")
        mostrar_campo(campo_visivel_jogador)
        print(f"A tua pontuação é de {pontuacao_jogador} pontos!")

        computador_ataca(campo_utilizador, campo_visivel_computador, pontuacao_computador)

        print("\nTabuleiro do jogador após o ataque do computador: ")
        mostrar_campo(campo_visivel_jogador)
        print(f"Pontuação do computador: {pontuacao_computador} pontos")

