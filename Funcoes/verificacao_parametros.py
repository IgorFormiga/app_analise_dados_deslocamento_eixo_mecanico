from Funcoes.Funcoes_Calculo import leiaFloat, leiaInt, linha
from numpy import arange

Fy1 = Fy2 = Myz = A = L = L_v = E = E_fad = R1 = R1_R2 = R2 = D1 = diâmetro = TipodoEixo = None
n = Sy = Sut = critério = diâmetro_L = diâmetros = R2_R1 = R1_v = T = R1_R2 = R2_v = None
ka = kb = kc = kd = ke = kf = Kf = Kfs = None


def parametros_comuns():
    global Fy1, Fy2, Myz, A, D1, TipodoEixo
    if Fy1 is None:
        Fy1 = leiaFloat('Digite o valor da Componente da força de corte, Fy1[N]: ')
    if Fy2 == None:
        Fy2 = leiaFloat('Digite o valor da Componente da força de acionamento, Fy2[N]: ')
    if Myz == None:
        Myz = leiaFloat(
            'Digite o valor do Momento devido a componente Fy1, e aplicado na extremidade do eixo Myz[N/mm]: ')
    if A == None:
        A = leiaFloat('Digite o valor do Comprimento em balanço, A[mm]: ')
    if D1 == None:
        D1 = leiaFloat(
            'Digite o valor da Distância do ponto de aplicação da força de acionamento ao apoio secundário, D1[mm]: ')
    if TipodoEixo == None:
        print()
        print('Qual o tipo do eixo?\n 1-Maciço\n 2-Vazado')
        Tipo = leiaInt('Digite o número correspondente ao tipo do eixo: ')
        while True:
            if Tipo == 1:
                TipodoEixo = 'Maciço'
                break
            if Tipo == 2:
                TipodoEixo = 'Vazado'
                break
            else:
                print('\033[33mERRO: por favor, dígite uma opção válida.\033[m')
                Tipo = leiaInt('Digite o número correspondente ao tipo do eixo: ')


def verificao_parametros_calculoY():
    global Fy1, Fy2, Myz, A, L, E, R1, R2, D1, diâmetros
    parametros_comuns()
    if L == None:
        L = leiaFloat('Digite o valor da Distância entre mancais, L[mm]: ')
    if E == None:
        E = leiaFloat('Digite o valor do Módulo de elasticidade do material, E[N/mm²]: ')
    if R1 == None:
        R1 = leiaFloat('Digite o valor da Rigidez do mancal dianteiro, R1[N/mm]: ')
    if R2 == None:
        R2 = leiaFloat('Digite o valor da Rigidez do mancal traseiro, R2[N/mm]: ')
    if diâmetros == None:
        diâmetros = list()
        if TipodoEixo == 'Maciço':
            diâmetros.append(leiaFloat('Digite o valor do diâmetro[mm]: '))
            while True:
                v = leiaFloat(
                    'Se deseja não acrescentar outro diâmetro digite 0(zero), se não, digite mais um valor diâmetro[mm]: ')
                if v == 0:
                    break
                diâmetros.append(v)
        else:
            diâmetros_i_e = list()
            while True:
                v_1 = leiaFloat('Digite o valor do diâmetro interno[mm]: ')
                if v_1 == 0:
                    break
                v_2 = leiaFloat('Digite o valor do diâmetro externo[mm]: ')
                diâmetros_i_e.append(v_1)
                diâmetros_i_e.append(v_2)
                if v_2 == 0:
                    break
                print('Se não deseja adicionar outros diâmetros digite 0(zero)')
                diâmetros.append(diâmetros_i_e[:])
                diâmetros_i_e.clear()


def verificao_parametros_calculoY_fad():
    global Fy1, Fy2, Myz, A, L, E_fad, R1, R2, D1, diâmetro_fad, TipodoEixo, n, \
        Sy, Sut, critério, T
    parametros_comuns()
    if L == None:
        L = leiaFloat('Digite o valor da Distância entre mancais, L[mm]: ')
    if T == None:
        T = leiaFloat('Digite o valor do Torque, T[Nmm]: ')
    if E_fad == None:
        E_fad = list()
        E_fad.append(leiaFloat('Digite o valor do Módulo de elasticidade do material E[N/mm²]: '))
        while True:
            v1 = leiaFloat(
                'Se deseja não acrescentar outro Módulo de elasticidade digite 0(zero), se não, digite mais um valor do Módulo de elasticidade E[N/mm²]: ')
            if v1 == 0:
                break
            E_fad.append(v1)
    if R1 == None:
        R1 = leiaFloat('Digite o valor da Rigidez do mancal dianteiro, R1[N/mm]: ')
    if R2 == None:
        R2 = leiaFloat('Digite o valor da Rigidez do mancal traseiro, R2[N/mm]: ')
    if n == None:
        n = leiaFloat('Digite o valor do coeficiente de segurança: ')
    if Sy == None:
        num = 0
        Sy = list()
        Sy.append(leiaFloat('Digite o valor do Sy[N/mm²]: '))
        while True:
            v2 = leiaFloat(
                'Se deseja não acrescentar outro Sy digite 0(zero), se não, digite mais um valor de Sy[N/mm²]: ')
            if v2 == 0:
                print(num)
                break
            Sy.append(v2)
            num += 1
    if Sut == None:
        Sut = list()
        Sut.append(leiaFloat('Digite o valor do Sut[N/mm²]:'))
        for i in range(0, num):
            v3 = leiaFloat(
                'Digite o próximo valor de Sut[N/mm²]: ')
            Sut.append(v3)

        '''while True:
            v3 = leiaFloat(
                'Se deseja não acrescentar outro Sut digite 0(zero), se não, digite mais um valor de Sut[N/mm²]: ')
            if v3 == 0:
                break
            Sut.append(v3)'''
    if critério == None:
        print()
        print('Qual o critério de fadiga deseja calcular?\n 1-Gerber\n 2-ASME-Elíptico')
        while True:
            Tipo_c = leiaInt('Digite o número correspondente ao críterio: ')
            if Tipo_c == 1:
                critério = 'Gerber'
                break
            if Tipo_c == 2:
                critério = 'ASME-Elíptico'
                break
            else:
                print('\033[33mERRO: por favor, dígite uma opção válida.\033[m')
                Tipo_c = leiaInt('Digite o número correspondente ao críterio: ')


def verificao_parametros_calculoY_variando_L():
    global Fy1, Fy2, Myz, A, L_v, E, R1, R2, D1, diâmetro_L, TipodoEixo
    parametros_comuns()
    if L_v == None:
        print('Forneça o intervalo e o incremento para o valor da Distância entre mancais, L[mm]')
        i = leiaFloat('Valor incial[mm]: ')
        f = leiaFloat('Valor final[mm]: ')
        Inc = leiaFloat('Valor do incremento: ')
        L_v = arange(i, f + Inc, Inc).tolist()
    if E == None:
        E = leiaFloat('Digite o valor do Módulo de elasticidade do material, E[N/mm²]: ')
    if R1 == None:
        R1 = leiaFloat('Digite o valor dA Rigidez do mancal dianteiro, R1[N/mm]: ')
    if R2 == None:
        R2 = leiaFloat('Digite o valor da Rigidez do mancal traseiro, R2[N/mm]: ')
    if diâmetro_L == None:
        diâmetro_L = list()
        diâmetro_L.append(leiaFloat('Digite o primeiro valor do diâmetro[mm]:'))
        diâmetro_L.append(leiaFloat('Digite o segundo valor do diâmetro[mm]:'))
        diâmetro_L.append(leiaFloat('Digite o terceiro valor do diâmetro[mm]:'))


def verificao_parametros_calculoY_variando_R2():
    global Fy1, Fy2, Myz, A, L, E, R1_R2, R2_v, D1, diâmetro, TipodoEixo
    parametros_comuns()
    if L == None:
        L = leiaFloat('Digite o valor da Distância entre mancais, L[mm]: ')
    if E == None:
        E = leiaFloat('Digite o valor do Módulo de elasticidade do material, E[N/mm²]: ')
    if R2_v == None:
        print('Forneça o intervalo e o incremento para o valor da Rigidez do mancal traseiro, R2[N/mm]')
        i = leiaFloat('Valor incial [N/mm]: ')
        f = leiaFloat('Valor final [N/mm]: ')
        Inc = leiaFloat('Valor do incremento: ')
        R2_v = arange(i, f + Inc, Inc).tolist()
    if R1_R2 == None:
        R1_R2 = list()
        R1_R2.append(leiaFloat('Digite o primeiro valor da Rigidez do mancal dianteiro, R1[N/mm]: '))
        R1_R2.append(leiaFloat('Digite o segundo valor da Rigidez do mancal dianteiro, R1[N/mm]: '))
    if diâmetro == None:
        diâmetro = leiaFloat('Digite o diâmetro[mm]: ')


def verificao_parametros_calculoY_variando_R1():
    global Fy1, Fy2, Myz, A, L, E, R2_R1, R1_v, D1, diâmetro, TipodoEixo
    parametros_comuns()
    if L == None:
        L = leiaFloat('Digite o valor da Distância entre mancais, L[mm]: ')
    if E == None:
        E = leiaFloat('Digite o valor do Módulo de elasticidade do material, E[N/mm²]: ')
    if R1_v == None:
        print('Forneça o intervalo e o incremento para o valor da Rigidez do mancal dianteiro, R1[N/mm]')
        i = leiaFloat('Valor incial [N/mm]: ')
        f = leiaFloat('Valor final [N/mm]: ')
        Inc = leiaFloat('Valor do incremento: ')
        R1_v = arange(i, f + Inc, Inc).tolist()
    if R2_R1 == None:
        R2_R1 = list()
        R2_R1.append(leiaFloat('Digite o primeiro valor da Rigidez do mancal traseiro, R2[N/mm]: '))
        R2_R1.append(leiaFloat('Digite o segundo valor da Rigidez do mancal traseiro, R2[N/mm]: '))
    if diâmetro == None:
        diâmetro = leiaFloat('Digite o diâmetro[mm]: ')


def ver():
    print(linha(70))
    print(f' Força de corte, Fy1 = {Fy1} N\n Força de acionamento, Fy2 = {Fy2} N\n\
 Momento devido a componente Fy1,  Myz = {Myz} N/mm \n Comprimento em balanço, A = {A} mm\n\
 Distância do ponto de aplicação da força de acionamento ao apoio secundário, D1 = {D1} mm\n\
 Tipo do eixo = {TipodoEixo}\n Torque, T = {T} Nmm\n Coeficiente de segurança, n = {n}\n\
 Críterio = {critério}')
    if L_v == None:
        print(f' Distância entre mancais:\n    L = {L} mm')
    else:
        print(f' Distância entre mancais:\n    L = {L} mm\n    L_v = [{L_v[0]},{L_v[-1]}] mm')
        print(f' Módulo de elasticidade do material:\n    E = {E} N/mm²\n    E_fad = {E_fad} N/mm²')
    if R1_v == None:
        print(f' Rigidez do mancal dianteiro\n    R1 = {R1} N/mm\n    R1_R2 = {R1_R2} N/mm')
    else:
        print(
            f' Rigidez do mancal dianteiro\n    R1 = {R1} N/mm\n    R1_R2 = {R1_R2} N/mm    R1_v = [{R1_v[0]},{R1_v[-1]}] N/mm')
    if R2_v == None:
        print(f' Rigidez do mancal traseiro:\n    R2 = {R2} N/mm\n    R2_R1 = {R2_R1} N/mm')
    else:
        print(
            f' Rigidez do mancal traseiro:\n    R2 = {R2} N/mm\n    R2_R1 = {R2_R1} N/mm    R2_v = [{R2_v[0]},{R2_v[-1]}] N/mm')
    print(f' Sy = {Sy} N/mm²')
    print(f' Sut = {Sut} N/mm²')
    print(f'Diâmetros:\n    diâmetro = {diâmetro}mm\n    diâmetros = {diâmetros}mm\n    diâmetro_L = {diâmetro_L}mm')
    print(f'Obs1: Variáveis do tipo X_v representam o vetor de X que varia no intervalo especificado')
    print(
        f'Obs2: Variáveis do tipo Rx_Ry representam a lista de valores de Rx utilizadas para gerar o Gráfico do delocamento total na ponta do eixo-árvore em função da Rigidez do mancal Ry')
    print(
        f'Obs3: A váriavel diâmetros é utilizada para Cálculo do deslocamento total na ponta do eixo-árvore com importaçãodos diâmetros')
    print(
        f'Obs4: A váriavel diâmetro_L é utilizada para gerar o Gráfico do delocamento total na ponta do eixo-árvore em função da variação da distância entre mancais(L)')
    print(linha(70))


def verificao_parametros_calculoY_fad_com_parametros():
    global Fy1, Fy2, Myz, A, L, E_fad, R1, R2, D1, diâmetro_fad, TipodoEixo, n, \
        Sy, Sut, critério, T, ka, kb, kc, kd, ke, kf, Kf, Kfs
    parametros_comuns()
    if L == None:
        L = leiaFloat('Digite o valor da Distância entre mancais, L[mm]: ')
    if T == None:
        T = leiaFloat('Digite o valor do Torque, T[Nmm]: ')
    if E_fad == None:
        E_fad = list()
        E_fad.append(leiaFloat('Digite o valor do Módulo de elasticidade do material E[N/mm²]: '))
        while True:
            v1 = leiaFloat(
                'Se deseja não acrescentar outro Módulo de elasticidade digite 0(zero), se não, digite mais um valor do Módulo de elasticidade E[N/mm²]: ')
            if v1 == 0:
                break
            E_fad.append(v1)
    if R1 == None:
        R1 = leiaFloat('Digite o valor da Rigidez do mancal dianteiro, R1[N/mm]: ')
    if R2 == None:
        R2 = leiaFloat('Digite o valor da Rigidez do mancal traseiro, R2[N/mm]: ')
    if n == None:
        n = leiaFloat('Digite o valor do coeficiente de segurança: ')
    if ka == None:
        ka = leiaFloat('Digite o valor do fator de modificação de condição de superfície, ka: ')
    if kb == None:
        kb = leiaFloat('Digite o valor do fator de modificação de tamanho, kb: ')
    if kc == None:
        kc = leiaFloat('Digite o valor do fator de modificação de carga, kc: ')
    if kd == None:
        kd = leiaFloat('Digite o valor do fator de modificação de temperatura, kd: ')
    if ke == None:
        ke = leiaFloat('Digite o valor do fator de modificação de confiabilidade, ke: ')
    if kf == None:
        kf = leiaFloat('Digite o valor do fator de modificação por efeitos variados, kf: ')
    if Kf == None:
        Kf = leiaFloat('Digite o valor do fator de modificação de concetração de tensão em fadiga, Kf: ')
    if Kfs == None:
        Kfs = leiaFloat('Digite o valor do fator de modificação de concetração de tensão em fadiga, Kfs: ')
    if Sy == None:
        num = 0
        Sy = list()
        Sy.append(leiaFloat('Digite o valor do Sy[N/mm²]: '))
        while True:
            v2 = leiaFloat(
                'Se deseja não acrescentar outro Sy digite 0(zero), se não, digite mais um valor de Sy[N/mm²]: ')
            if v2 == 0:
                break
            Sy.append(v2)
            num += 1
    if Sut == None:
        Sut = list()
        Sut.append(leiaFloat('Digite o valor do Sut[N/mm²]:'))
        for i in range(0, num):
            v3 = leiaFloat(
                'Digite o próximo valor de Sut[N/mm²]: ')
            Sut.append(v3)
    if critério == None:
        print()
        print('Qual o critério de fadiga deseja calcular?\n 1-Gerber\n 2-ASME-Elíptico')
        while True:
            Tipo_c = leiaInt('Digite o número correspondente ao críterio: ')
            if Tipo_c == 1:
                critério = 'Gerber'
                break
            if Tipo_c == 2:
                critério = 'ASME-Elíptico'
                break
            else:
                print('\033[33mERRO: por favor, dígite uma opção válida.\033[m')
                Tipo_c = leiaInt('Digite o número correspondente ao críterio: ')