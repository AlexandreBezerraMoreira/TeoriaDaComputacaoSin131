def criar_afd():
    estados = []
    alfabeto = []
    transicoes = {}
    estado_inicial = ""
    estados_finais = []

    # Recebendo os dados do AFD
    print("Informe o conjunto de estados:")
    estados = input().split()

    print("Informe o alfabeto de entrada:")
    alfabeto = input().split()

    print("Informe o estado inicial:")
    estado_inicial = input()

    print("Informe o(s) estado(s) final(is):")
    estados_finais = input().split()

    print("Defina as funções de transição (ex: Q0 a Q1):")
    for estado in estados:
        for simbolo in alfabeto:
            print(f"{estado} -- {simbolo} -->", end="")
            destino = input()
            transicoes[(estado, simbolo)] = destino

    # Retornando o AFD como um dicionário
    afd = {
        'estados': estados,
        'alfabeto': alfabeto,
        'transicoes': transicoes,
        'estado_inicial': estado_inicial,
        'estados_finais': estados_finais
    }

    # Exibindo o AFD criado para verificação
    print("\nAFD Criado:")
    print(f"Estados: {afd['estados']}")
    print(f"Alfabeto: {afd['alfabeto']}")
    print(f"Estado Inicial: {afd['estado_inicial']}")
    print(f"Estados Finais: {afd['estados_finais']}")
    print("Transições:")
    for (estado, simbolo), destino in afd['transicoes'].items():
        print(f"{estado} -- {simbolo} --> {destino}")
    
    return afd

def testar_linguagem(afd):
    print("Informe a linguagem a ser testada:")
    entrada = input()

    estado_atual = afd['estado_inicial']
    for simbolo in entrada:
        if (estado_atual, simbolo) in afd['transicoes']:
            estado_atual = afd['transicoes'][(estado_atual, simbolo)]
        else:
            print("Linguagem não reconhecida (transição inexistente).")
            return

    if estado_atual in afd['estados_finais']:
        print("Linguagem reconhecida.")
    else:
        print("Linguagem não reconhecida.")

    input()

def criar_afd_minimizado():
    afd = criar_afd()  # Usa a função de criação de AFD existente
    afd_minimizado = minimizar(afd)
    print("\nAFD Minimizado:")
    exibir_afd(afd_minimizado)
    testar_linguagem(afd_minimizado)  # Testa a linguagem no AFD minimizado

def exibir_afd(afd):
    print("\nAlfabeto:", afd['alfabeto'])
    print("Estados:", afd['estados'])
    print("Transições:")
    for (estado, simbolo), destino in afd['transicoes'].items():
        print(f"{estado} -- {simbolo} --> {destino}")
    print("Estado Inicial:", afd['estado_inicial'])
    print("Estados Finais:", afd['estados_finais'])

def minimizar(afd):
    estados = afd['estados']
    transicoes = afd['transicoes']
    estados_finais = set(afd['estados_finais'])
    estado_inicial = afd['estado_inicial']
    alfabeto = afd['alfabeto']
    
    # Criação da tabela de equivalência
    tabela = {}
    
    # Inicializa a tabela com estados não equivalentes (diagonal principal e estados finais vs não finais)
    for i in range(len(estados)):
        for j in range(i):
            if (estados[i] in estados_finais) != (estados[j] in estados_finais):
                tabela[(estados[i], estados[j])] = 'x'  # Diferentes

    # Função para verificar se estados são equivalentes
    def verificar_equivalencia(e1, e2):
        for simbolo in alfabeto:
            destino1 = transicoes.get((e1, simbolo))
            destino2 = transicoes.get((e2, simbolo))
            if destino1 != destino2:
                if (destino1, destino2) in tabela and tabela[(destino1, destino2)] == 'x':
                    return False
        return True

    # Marca estados equivalentes na tabela
    mudanca = True
    while mudanca:
        mudanca = False
        for i in range(len(estados)):
            for j in range(i):
                if (estados[i], estados[j]) not in tabela:
                    if not verificar_equivalencia(estados[i], estados[j]):
                        tabela[(estados[i], estados[j])] = 'x'
                        mudanca = True

    # Combina estados equivalentes
    novos_estados = []
    representante = {}
    
    for i in range(len(estados)):
        for j in range(i):
            if (estados[i], estados[j]) not in tabela:
                representante[estados[j]] = estados[i]
    
    for estado in estados:
        if estado not in representante:
            novos_estados.append(estado)
    
    # Criação do novo conjunto de transições
    novas_transicoes = {}
    for (origem, simbolo), destino in transicoes.items():
        nova_origem = representante.get(origem, origem)
        novo_destino = representante.get(destino, destino)
        novas_transicoes[(nova_origem, simbolo)] = novo_destino

    # Ajusta estados finais
    novos_estados_finais = {representante.get(estado, estado) for estado in estados_finais}

    # Criação do AFD minimizado
    afd_minimizado = {
        'estados': novos_estados,
        'alfabeto': alfabeto,
        'transicoes': novas_transicoes,
        'estado_inicial': representante.get(estado_inicial, estado_inicial),
        'estados_finais': list(novos_estados_finais)
    }

    # Print do resultado final da minimização
    print("\nResultado Final da Minimização:")
    print("Estados:", afd_minimizado['estados'])
    print("Estado Inicial:", afd_minimizado['estado_inicial'])
    print("Estados Finais:", afd_minimizado['estados_finais'])
    print("Transições:")
    for (estado, simbolo), destino in afd_minimizado['transicoes'].items():
        print(f"{estado} -- {simbolo} --> {destino}")

    return afd_minimizado

def criar_afn():
    estados = []
    alfabeto = []
    FuncTransicao = {}
    EstadoInicial = ""
    EstadoFinal = []

    # Recebendo os dados do autômato
    print("Informe o conjunto de estados:", end="")
    estados = input().split()

    print("Informe o seu alfabeto de entrada (use 'eps' para representar ε-transição):", end="")
    alfabeto = input().split()

    print("Informe o estado inicial:", end="")
    EstadoInicial = input()

    print("Informe o(s) estado(s) final(s):", end="")
    EstadoFinal = input().split()

    print("Defina as funções de transição (pode definir múltiplos estados separados por espaço):")
    for estado in estados:
        for simbolo in alfabeto:
            print(f"{estado} -- {simbolo} -->", end="")
            ProximosEstados = input().split()

            # Quando eu digitar o "ponto(.)", quer dizer que não vai mapear para estado nenhum.
            if ProximosEstados == ["."]:
                FuncTransicao[(estado, simbolo)] = []
            else:
                FuncTransicao[(estado, simbolo)] = ProximosEstados

    # Função para realizar o fechamento epsilon (ε-closure)
    def epsilon_closure(estados):
        fechamento = set(estados) # Inicializa o fechamento com o conjunto de estados de entrada
        stack = list(estados)     # Inicializa a pilha com os estados de entrada

        while stack:              # Continua enquanto houver estados na pilha
            estado = stack.pop()  # Remove e retorna o último estado da pilha
            if (estado, 'eps') in FuncTransicao: #Verifica se há uma transição epsilon para esse estado
                for prox_estado in FuncTransicao[(estado, 'eps')]: # Para cada estado de destino da transição epsilon
                    if prox_estado not in fechamento:              # Se o estado de destino ainda não está no fechamento
                        fechamento.add(prox_estado)                # Adiciona o estado ao fechamento
                        stack.append(prox_estado)                  # Adiciona o estado à pilha para explorar suas transições epsilon
        return list(fechamento)                                    # Retorna o fechamento como uma lista

    # Função para processar a linguagem no AFN
    def reconhecer_linguagem(entrada):
        # Inicializa o conjunto de estados atuais com o fechamento epsilon do estado inicial
        estados_atuais = epsilon_closure([EstadoInicial])

        for simbolo in entrada:
            novos_estados = []
            for estado in estados_atuais:
                if (estado, simbolo) in FuncTransicao:
                    novos_estados.extend(FuncTransicao[(estado, simbolo)])
            estados_atuais = epsilon_closure(novos_estados)

        # Verificar se algum estado atual é estado final
        if any(estado in EstadoFinal for estado in estados_atuais):
            print("A linguagem foi reconhecida.")
        else:
            print("A linguagem não foi reconhecida.")

    # Reconhecimento da linguagem
    print("Informe a linguagem a ser reconhecida:", end="")
    entrada = input()

    reconhecer_linguagem(entrada)

def gerar_palavras_teste(alfabeto, n_max=4):
    """
    Gera todas as combinações possíveis de palavras com o alfabeto fornecido até um comprimento máximo n_max.
    """
    palavras = []
    for n in range(1, n_max + 1):
        palavras += gerar_combinacoes(alfabeto, "", n)
    return palavras

def gerar_combinacoes(alfabeto, prefixo, n):
    """
    Função auxiliar para gerar combinações recursivamente.
    """
    if n == 0:
        return [prefixo]
    combinacoes = []
    for simbolo in alfabeto:
        combinacoes += gerar_combinacoes(alfabeto, prefixo + simbolo, n - 1)
    return combinacoes

def simular_afd_com_palavra(estados, transicoes, estado_inicial, estados_finais, palavra):
    """
    Simula o processamento de uma palavra no AFD.
    Retorna True se a palavra for aceita e False caso contrário.
    """
    estado_atual = estado_inicial
    for simbolo in palavra:
        if (estado_atual, simbolo) in transicoes:
            estado_atual = transicoes[(estado_atual, simbolo)]
        else:
            return False
    return estado_atual in estados_finais

def simular_afnd(estados, transicoes, estado_inicial, estados_finais, palavra):
    """
    Simula o processamento de uma palavra no AFND.
    Retorna True se a palavra for aceita e False caso contrário.
    """
    def epsilon_closure(estados):
        fechamento = set(estados)
        stack = list(estados)
        while stack:
            estado = stack.pop()
            if (estado, 'eps') in transicoes:
                for prox_estado in transicoes[(estado, 'eps')]:
                    if prox_estado not in fechamento:
                        fechamento.add(prox_estado)
                        stack.append(prox_estado)
        return fechamento

    estados_atuais = epsilon_closure([estado_inicial])
    for simbolo in palavra:
        novos_estados = set()
        for estado in estados_atuais:
            if (estado, simbolo) in transicoes:
                novos_estados.update(transicoes[(estado, simbolo)])
        estados_atuais = epsilon_closure(novos_estados)
    
    return any(estado in estados_finais for estado in estados_atuais)

def verificar_equivalencia_afnd_afd(estados_afnd, transicoes_afnd, estado_inicial_afnd, estados_aceitacao_afnd, 
                                    estados_afd, transicoes_afd, estado_inicial_afd, estados_aceitacao_afd, alfabeto, n_max=4):
    """
    Verifica se o AFND e o AFD aceitam as mesmas palavras geradas até um comprimento máximo n_max.
    Retorna True se forem equivalentes, ou False e a palavra onde divergem.
    """
    palavras_teste = gerar_palavras_teste(alfabeto, n_max)  # Gera palavras de teste até um comprimento máximo
    for palavra in palavras_teste:
        aceita_afnd = simular_afnd(estados_afnd, transicoes_afnd, estado_inicial_afnd, estados_aceitacao_afnd, palavra)
        aceita_afd = simular_afd_com_palavra(estados_afd, transicoes_afd, estado_inicial_afd, estados_aceitacao_afd, palavra)
        if aceita_afnd != aceita_afd:
            print(f"Divergência encontrada na palavra: {palavra}")
            return False, palavra
    print("O AFND e o AFD são equivalentes para todas as palavras testadas.")
    return True, None

def converter_afn_para_afd():
    def epsilon_closure(estados, transicoes):
        """
        Calcula o fechamento epsilon para um conjunto de estados.
        """
        fechamento = set(estados)
        stack = list(estados)

        while stack:
            estado = stack.pop()
            if (estado, 'eps') in transicoes:
                for prox_estado in transicoes[(estado, 'eps')]:
                    if prox_estado not in fechamento:
                        fechamento.add(prox_estado)
                        stack.append(prox_estado)
        return fechamento

    # Entrada do AFND
    estados = input("Informe o conjunto de estados do AFN: ").split()
    alfabeto = input("Informe o alfabeto de entrada (use 'eps' para representar ε-transição): ").split()
    estado_inicial = input("Informe o estado inicial do AFN: ")
    estados_finais = input("Informe o(s) estado(s) final(is) do AFN: ").split()
    transicoes = {}

    # Recebendo as transições do AFND
    print("Defina as funções de transição do AFN (pode definir múltiplos estados separados por espaço):")
    for estado in estados:
        for simbolo in alfabeto + ['eps']:  # Incluindo transições epsilon
            print(f"{estado} -- {simbolo} -->", end="")
            destinos = input().split()
            if destinos != ["."]:  # Para representar transições inexistentes
                transicoes[(estado, simbolo)] = destinos

    novo_alfabeto = [simbolo for simbolo in alfabeto if simbolo != 'eps']
    estado_inicial_closure = tuple(sorted(epsilon_closure([estado_inicial], transicoes)))
    novo_estados = {estado_inicial_closure}
    novo_transicoes = {}
    novos_estados_finais = set()

    estados_a_processar = [estado_inicial_closure]

    while estados_a_processar:
        estado_atual = estados_a_processar.pop()

        for simbolo in novo_alfabeto:
            novos_destinos = set()

            for subestado in estado_atual:
                if (subestado, simbolo) in transicoes:
                    for destino in transicoes[(subestado, simbolo)]:
                        novos_destinos.update(epsilon_closure([destino], transicoes))

            novo_estado_destino = tuple(sorted(novos_destinos))

            # Adiciona apenas estados não vazios para evitar transições para estados sem saída
            if novo_estado_destino:
                if novo_estado_destino not in novo_estados:
                    novo_estados.add(novo_estado_destino)
                    estados_a_processar.append(novo_estado_destino)

                # Adiciona a transição ao novo conjunto de transições do AFD
                novo_transicoes[(estado_atual, simbolo)] = novo_estado_destino

                # Verifica se o novo estado deve ser um estado final do AFD
                if any(subestado in estados_finais for subestado in novo_estado_destino):
                    novos_estados_finais.add(novo_estado_destino)

    afd = {
        'estados': list(novo_estados),
        'alfabeto': novo_alfabeto,
        'transicoes': novo_transicoes,
        'estado_inicial': estado_inicial_closure,
        'estados_finais': list(novos_estados_finais)
    }

    print("\nAFD Gerado a partir do AFN:")
    exibir_afd(afd)

    # Verificação de equivalência entre o AFND original e o AFD convertido
    print("\nVerificando equivalência entre o AFND e o AFD convertido...")
    equivalente, palavra = verificar_equivalencia_afnd_afd(
        estados, transicoes, estado_inicial, estados_finais,
        afd['estados'], afd['transicoes'], afd['estado_inicial'], afd['estados_finais'],
        novo_alfabeto
    )

    if equivalente:
        print("\nO AFND e o AFD convertido são equivalentes para todas as palavras testadas.")
    else:
        print(f"\nO AFND e o AFD convertido não são equivalentes. Divergem na palavra: {palavra}")

    return afd

def exibir_afd(afd):
    print("\nAlfabeto:", afd['alfabeto'])
    print("Estados:", afd['estados'])
    print("Transições:")
    for (estado, simbolo), destino in afd['transicoes'].items():
        print(f"{estado} -- {simbolo} --> {destino}")
    print("Estado Inicial:", afd['estado_inicial'])
    print("Estados Finais:", afd['estados_finais'])

# Funções adicionais de simulação e geração de palavras são necessárias para equivalência

def verificar_equivalencia_afnd_afd(estados_afnd, transicoes_afnd, estado_inicial_afnd, estados_aceitacao_afnd, 
                                    estados_afd, transicoes_afd, estado_inicial_afd, estados_aceitacao_afd, alfabeto, n_max=4):
    """
    Verifica se o AFND e o AFD aceitam as mesmas palavras geradas até um comprimento máximo n_max.
    Retorna True se forem equivalentes, ou False e a palavra onde divergem.
    """
    palavras_teste = gerar_palavras_teste(alfabeto, n_max)  # Gera palavras de teste até um comprimento máximo
    for palavra in palavras_teste:
        aceita_afnd = simular_afnd(estados_afnd, transicoes_afnd, estado_inicial_afnd, estados_aceitacao_afnd, palavra)
        aceita_afd = simular_afd_com_palavra(estados_afd, transicoes_afd, estado_inicial_afd, estados_aceitacao_afd, palavra)
        if aceita_afnd != aceita_afd:
            print(f"Divergência encontrada na palavra: {palavra}")
            return False, palavra
    print("O AFND e o AFD são equivalentes para todas as palavras testadas.")
    return True, None

def maquina_turing(estado_inicial=None, branco=None, inicio=None, regras=[], fita=[], estados_finais=None, pos=0):
    estado = estado_inicial
    if not fita:
        fita = [branco]
    if pos < 0:
        pos += len(fita)
    if pos >= len(fita) or pos < 0:
        raise ValueError("Posição inicial inválida na fita")

    transicoes = dict(((s0, v0), (v1, direcao, s1)) for (s0, v0, v1, direcao, s1) in regras)
    
    while True:
        print(estado, '\t', end=" ")
        for i, v in enumerate(fita):
            if i == pos:
                print("[%s]" % (v,), end=" ")
            else:
                print(v, end=" ")
        print()

        if estado in estados_finais:
            print("Máquina de Turing aceitou a palavra. Sim")
            break
        if (estado, fita[pos]) not in transicoes:
            print("Máquina de Turing rejeitou a palavra. Não")
            break

        (v1, direcao, s1) = transicoes[(estado, fita[pos])]
        fita[pos] = v1

        if direcao == 'left':
            if pos > 0:
                pos -= 1
            else:
                fita.insert(0, branco)
        elif direcao == 'right':
            pos += 1
            if pos >= len(fita):
                fita.append(branco)
        estado = s1

def criar_maquina_turing():
    E = input("Informe o conjunto de estados (separados por espaço): ").split()
    Sigma = input("Informe o alfabeto de entrada (separados por espaço): ").split()
    Gamma = input("Informe o alfabeto da fita (separados por espaço): ").split()
    x = input("Informe o símbolo marcador de início da fita: ")
    y = input("Informe o símbolo de células vazias da fita: ")
    i = input("Informe o estado inicial: ")
    F = input("Informe o conjunto de estados finais (separados por espaço): ").split()

    regras = []
    print("Defina as regras de transição (ex: estado símbolo_lido símbolo_escrito direção novo_estado):")
    while True:
        regra = input()
        if regra.lower() == 'fim':
            break
        regras.append(tuple(regra.split()))

    fita = list(input("Informe a fita inicial: "))

    maquina_turing(estado_inicial=i, branco=y, inicio=x, fita=fita, estados_finais=F, regras=regras)

def menu():
    while True:
        print("\nMenu Principal")
        print("1. Executar AFD")
        print("2. Executar AFN")
        print("3. Converter AFN para AFD")
        print("4. Minimizar AFD")
        print("5. Executar Máquina de Turing")
        print("6. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            afd = criar_afd()
            testar_linguagem(afd)
        elif escolha == "2":
            criar_afn()
        elif escolha == "3":
            converter_afn_para_afd()
        elif escolha == "4":
            criar_afd_minimizado()
        elif escolha == "5":
            criar_maquina_turing()
        elif escolha == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
