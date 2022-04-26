from numpy import arange, array, pi, zeros, max, where
from numpy.core.fromnumeric import around
from pandas import DataFrame
from matplotlib.pyplot import figure, title, plot, xlabel, ylabel, legend, grid, draw, bar, xticks
'''Momento de inércia de um eixo vazado de seção constante [mm^4]'''


def Iv(diâmetro):
    Ieixovazado = list()
    if type(diâmetro) == int or type(diâmetro) == float:
        d0 = diâmetro / (1 - 0.7 ** 4)
        di = 0.7 * d0
        Iv = (pi * (d0 ** 4 - di ** 4)) / 64
        Ieixovazado.append(Iv)
    else:
        if type(diâmetro[0]) == list:
            for c in range(0, len(diâmetro)):
                Iv = (pi * (diâmetro[c][1] ** 4 - diâmetro[c][0] ** 4)) / 64
                Ieixovazado.append(Iv)
        else:
            for d in diâmetro:
                d0 = d / (1 - 0.7 ** 4)
                di = 0.7 * d0
                Iv = (pi * (d0 ** 4 - di ** 4)) / 64
                Ieixovazado.append(Iv)
    #print(Ieixovazado)
    return Ieixovazado


'''Momento de inércia de um eixo maciço de seção constante [mm^4]'''


def Im(diâmetro):
    Ieixomaciço = list()
    if type(diâmetro) != list:
        Im = (pi * (diâmetro / 2) ** 4) / 4
        Ieixomaciço.append(Im)
    else:
        for d in diâmetro:
            Im = (pi * (d / 2) ** 4) / 4
            Ieixomaciço.append(Im)
    #print(Ieixomaciço)
    return Ieixomaciço


'''Cálculo dos deslocamento na ponta do eixo-árvore, na direção y do 
sistema de coordenadas'''


def y1(Fy1, A, L, E, I):
    y1 = ((Fy1 * L * A ** 2) / (3 * E * I)) + ((Fy1 * A ** 3) / (3 * E * I))
    return y1


def y2(Fy1, A, L, R1, R2):
    y2 = Fy1 * ((((A / L) ** 2) * ((1 / R1) + (1 / R2))) + ((2 / R1) * (A / L)) + (1 / R1))
    return y2


def y3(Fy2, A, L, E, D1, I):
    y3 = (Fy2 / (6 * E * I)) * (((A * D1 ** 3) / L) - A * L * D1)
    return y3


def y4(Fy2, A, L, R1, R2, D1):
    y4 = Fy2 * ((A * D1 / L ** 2) * ((1 / R1) + (1 / R2)) + (1 / L) * ((D1 / R1) - (A / R2)))
    return y4


def y5(Myz, A, L, E, R1, R2, I):
    y5 = Myz * (((A ** 2) / (2 * E * I)) + ((L * A) / (3 * E * I)) + (1 / R1) * ((L + A) / L ** 2) \
                + (1 / R2) * (A / L ** 2))
    return y5


'''Cálculo do deslocamento total na ponta do eixo-árvore, na direção y do 
sistema de coordenadas. Apenas o diâmetro[mm²] vária dentro de uma lista'''


def calculoY(Fy1, Fy2, Myz, A, L, E, R1, R2, D1, diâmetros, TipodoEixo):
    resultados = list()
    valoresdeY = list()
    if TipodoEixo == 'Maciço':
        i = Im(diâmetros)
    if TipodoEixo == 'Vazado':
        i = Iv(diâmetros)
    for I in i:
        valoresdeY.append(y1(Fy1, A, L, E, I))
        valoresdeY.append(y2(Fy1, A, L, R1, R2))
        valoresdeY.append(y3(Fy2, A, L, E, D1, I))
        valoresdeY.append(y4(Fy2, A, L, R1, R2, D1))
        valoresdeY.append(y5(Myz, A, L, E, R1, R2, I))
        valoresdeY = list(map(lambda x: x * 1000, valoresdeY))
        resultados.append(valoresdeY[:])
        valoresdeY.clear()
    if TipodoEixo == 'Maciço':
        resultados_dict = Imprimir(resultados, diâmetros)
        resultados_Ytotal = Ytotal(resultados_dict)
    else:
        lista_imprimir = list()
        for l in range(0, len(diâmetros)):
            if diâmetros[0] == list:
                lista_imprimir.append(f'di={diâmetros[l][0]}/d0={diâmetros[l][1]}')
            else:
                lista_imprimir.append(diâmetros[l])
        resultados_dict = Imprimir(resultados, lista_imprimir)
        resultados_Ytotal = Ytotal(resultados_dict)
    return resultados_dict, resultados_Ytotal


'''FADIGA'''
'''Cálculo do Diagrama do Momento fletor do eixo'''


def DMF(Fy1, Fy2, Myz, A, L, D1):
    R2 = (D1 * Fy2 + (L + A) * Fy1 + Myz) / L
    R1 = - (-R2 + Fy2 + Fy1)
    x = arange(0, L + A, 0.5)
    M = zeros(len(x))

    for i in range(0, len(x)):
        if x[i] < D1:
            M[i] = x[i] * R1
        if D1 <= x[i] and x[i] < L:
            M[i] = R1 * x[i] + Fy2 * (x[i] - D1)
        if L <= x[i] and x[i] <= L + A:
            M[i] = R1 * x[i] + Fy2 * (x[i] - D1) - R2 * (x[i] - L)

    M_max = max(M)
    P_Mmax = where(M == max(M))
    x_Mmax = x[P_Mmax]
    return M_max, x_Mmax, x, M


'''Cálculo dos diâmetros por fadiga'''


def diâmetro_fad(n, Sy, Sut, M_max, T, critério):
    Sy = array(Sy)  # [MPa]
    Sut = array(Sut)  # [MPa]
    Se_linha = 0.5 * Sut
    ka = kb = kc = kd = ke = kf = 1
    Se = ka * kb * kc * kd * ke * kf * Se_linha  # [MPa]
    Kf = Kfs = 1.5
    Ma = M_max
    # Mm = 0
    # Ta = 0
    Tm = T
    if critério == 'Gerber':
        # DE-Gerber
        d_Gerber_r = (((16 * n * Kf * Ma) / (pi * Se)) * (
                1 + (1 + (3 * ((Kfs * Tm * Se) / (Kf * Ma * Sut)) ** 2)) ** 0.5)) ** (1 / 3)
        d_Gerber = d_Gerber_r.tolist()
        d0_Gerber = d_Gerber_r / (1 - 0.7 ** 4)
        di_Gerber = 0.7 * d0_Gerber
        return d_Gerber, d0_Gerber, di_Gerber
    else:
        # DE-ASME Elíptico
        d_ASME_r = (((16 * n) / pi) * ((4 * ((Kf * Ma) / Se) ** 2) + (3 * ((Kfs * Tm) / Sy) ** 2)) ** 0.5) ** (1 / 3)
        d_ASME = d_ASME_r.tolist()
        # Eixo vazado
        d0_ASME = d_ASME_r / (1 - 0.7 ** 4)
        di_ASME = 0.7 * d0_ASME
        return d_ASME, d0_ASME, di_ASME


'''Cálculo dos deslocamentos por fadiga'''
'''Obs: É necessário fornecer na mesma sequencia E e o diâmetro, pq o diâmetro
foi calculado em função de cada material. Exemplo: E[aço, aluminio, titânio] e
o diâmetro[valor corresponte ao aço, v.c. ao aluminio, v.c. ao titânio]'''


def calculoY_fad(Fy1, Fy2, Myz, A, L, E_fad, R1, R2, D1, diâmetro_fad, TipodoEixo):
    if TipodoEixo == 'Maciço':
        I = Im(diâmetro_fad)
    if TipodoEixo == 'Vazado':
        I = Iv(diâmetro_fad)
    resultados = list()
    valoresdeY = list()
    for c in range(0, len(diâmetro_fad)):
        valoresdeY.append(y1(Fy1, A, L, E_fad[c], I[c]))
        valoresdeY.append(y2(Fy1, A, L, R1, R2))
        valoresdeY.append(y3(Fy2, A, L, E_fad[c], D1, I[c]))
        valoresdeY.append(y4(Fy2, A, L, R1, R2, D1))
        valoresdeY.append(y5(Myz, A, L, E_fad[c], R1, R2, I[c]))
        valoresdeY = list(map(lambda x: x * 1000, valoresdeY))
        resultados.append(valoresdeY[:])
        valoresdeY.clear()
    resultados_dict_fad = Imprimir(resultados, diâmetro_fad)
    resultados_Ytotal_fad = Ytotal(resultados_dict_fad)
    return resultados_dict_fad, resultados_Ytotal_fad


'''Plote um gráfico YX sendo Y o valor total do deslocamento (em micrometros) 
na ponta de um eixo-árvore, sendo que L deve variar
de 250 mm a 350 mm. Maciço e no mesmo gráfico plote três curvas (cores diferentes) 
sendo curva 1 para o eixo com diâmetro=50 mm, curva 2 para o eixo com diâmetro=75mm
e curva 3 para o eixo com diâmetro=100 mm.'''


def calculoY_variando_L(Fy1, Fy2, Myz, A, L_v, E, R1, R2, D1, diâmetro_L, TipodoEixo):
    if TipodoEixo == 'Maciço':
        I = Im(diâmetro_L)
    if TipodoEixo == 'Vazado':
        I = Iv(diâmetro_L)

    Y = list()
    Y_t = list()
    valoresdeY = list()

    for c in range(0, len(diâmetro_L)):
        for l in L_v:
            valoresdeY.append(y1(Fy1, A, l, E, I[c]))
            valoresdeY.append(y2(Fy1, A, l, R1, R2))
            valoresdeY.append(y3(Fy2, A, l, E, D1, I[c]))
            valoresdeY.append(y4(Fy2, A, l, R1, R2, D1))
            valoresdeY.append(y5(Myz, A, l, E, R1, R2, I[c]))
            valoresdeY = list(map(lambda x: x * 1000, valoresdeY))
            SomaY = sum(valoresdeY)
            Y.append(SomaY)
            valoresdeY.clear()
        Y_t.append(Y[:])
        Y.clear()

    figure()
    title('Influência da variação da distância entre eixos em Y')
    label_1 = 'd = {}mm'.format(diâmetro_L[0])
    plot(L_v, Y_t[0], color='r', label=label_1)
    label_2 = 'd = {}mm'.format(diâmetro_L[1])
    plot(L_v, Y_t[1], color='g', label=label_2)
    label_3 = 'd = {}mm'.format(diâmetro_L[2])
    plot(L_v, Y_t[2], color='b', label=label_3)
    xlabel('L(mm)')
    ylabel('Yt ($\mu$m)')
    legend()
    grid()
    #plt.pause(0.01)
    #plt.show()  #block=True
    draw()
    # return Y_t




'''p) Plote um gráfico YX sendo Y o valor total do deslocamento na ponta de um eixo
árvore maciço(material aço) com diâmetro de 75 mm com diâmetro de 75 mm e X o 
valor da Rigidez do mancal traseiro R2, sendo que R2 deve variar de 900 
N/micrometros a 1500 N/micrometros. No mesmo
gráfico plote duas curvas (cores diferentes) sendo curva 1 para a Rigidez 
do mancal dianteiro R1=1600 N/micrometros e a curva 2 para a Rigidez do 
mancal dianteiro R1=1800 N/micrometros.'''


def calculoY_variando_R2(Fy1, Fy2, Myz, A, L, E, R1_R2, R2_v, D1, diâmetro, \
                         TipodoEixo):
    if TipodoEixo == 'Maciço':
        I = Im(diâmetro)
    if TipodoEixo == 'Vazado':
        I = Iv(diâmetro)
    Y = list()
    Y_t = list()
    valoresdeY = list()
    for r1 in R1_R2:
        for r2 in R2_v:
            valoresdeY.append(y1(Fy1, A, L, E, I[0]))
            valoresdeY.append(y2(Fy1, A, L, r1, r2))
            valoresdeY.append(y3(Fy2, A, L, E, D1, I[0]))
            valoresdeY.append(y4(Fy2, A, L, r1, r2, D1))
            valoresdeY.append(y5(Myz, A, L, E, r1, r2, I[0]))
            valoresdeY = list(map(lambda x: x * 1000, valoresdeY))
            SomaY = sum(valoresdeY)
            Y.append(SomaY)
            valoresdeY.clear()
        Y_t.append(Y[:])
        Y.clear()

    R2_v = list(map(lambda x: x / 1000, R2_v))
    figure()
    title('Influência da rigidez do mancal traseiro(R2) em Y')
    label_R1_0 = 'R1 = {}N/$\mu$m'.format(R1_R2[0] / 1000)
    plot(R2_v, Y_t[0], color='r', label=label_R1_0)
    label_R1_1 = 'R1 = {}N/$\mu$m'.format(R1_R2[1] / 1000)
    plot(R2_v, Y_t[1], color='g', label=label_R1_1)
    xlabel('Rigidez do mancal R2 (N/$\mu$m)')
    ylabel('Yt ($\mu$m)')
    legend()
    grid()
    #plt.pause(0.01)
    # plt.show(block=True)
    # plt.draw()
    #return


'''r) Plote um gráfico YX sendo Y o valor total do deslocamento (em micrometros)
na ponta de um eixo árvore maciço (material aço) com diâmetro de 75 mm e X o 
valor da Rigidez do mancal dianteiro R1, sendo que R1 deve variar de 
1500 N/micrometros a 2100N/micrometros. No mesmo gráfico plote duas curvas 
(cores diferentes) sendo curva 1 para a Rigidez do mancal Traseiro 
R2=1000 N/micrometros e a curva 2 para a Rigidez do mancal Traseiro R2=1200 N/micrometros.'''


def calculoY_variando_R1(Fy1, Fy2, Myz, A, L, E, R1_v, R2_R1, D1, diâmetro, \
                         TipodoEixo):
    if TipodoEixo == 'Maciço':
        I = Im(diâmetro)
    if TipodoEixo == 'Vazado':
        I = Iv(diâmetro)
    Y = list()
    Y_t = list()
    valoresdeY = list()
    for r2 in R2_R1:
        for r1 in R1_v:
            valoresdeY.append(y1(Fy1, A, L, E, I[0]))
            valoresdeY.append(y2(Fy1, A, L, r1, r2))
            valoresdeY.append(y3(Fy2, A, L, E, D1, I[0]))
            valoresdeY.append(y4(Fy2, A, L, r1, r2, D1))
            valoresdeY.append(y5(Myz, A, L, E, r1, r2, I[0]))
            valoresdeY = list(map(lambda x: x * 1000, valoresdeY))
            SomaY = sum(valoresdeY)
            Y.append(SomaY)
            valoresdeY.clear()
        Y_t.append(Y[:])
        Y.clear()

    R1_v = list(map(lambda x: x / 1000, R1_v))
    figure()
    title('Influência da rigidez do mancal dianteiro(R1) em Y')
    label_R2_0 = 'R2 = {}N/$\mu$m'.format(R2_R1[0] / 1000)
    plot(R1_v, Y_t[0], color='r', label=label_R2_0)
    label_R2_1 = 'R2 = {}N/$\mu$m'.format(R2_R1[1] / 1000)
    plot(R1_v, Y_t[1], color='g', label=label_R2_1)
    xlabel('Rigidez do mancal R1 (N/$\mu$m)')
    ylabel('Yt ($\mu$m)')
    legend()
    grid()
    #plt.pause(0.01)
    # plt.show(block=False)
    #return


def Imprimir(resultado, diâmetro):
    Imprimir_resultados = dict()
    if type(diâmetro[0]) == list:
        for chave, valor in zip(diâmetro, resultado):
            Imprimir_resultados['di='+str(chave[0])+'/'+'de='+str(chave[1])] = valor
    else:
        for chave, valor in zip(diâmetro, resultado):
            Imprimir_resultados[chave] = valor
        # print(Imprimir_resultados)
    return Imprimir_resultados


def Ytotal(resultados):
    resultadosYtotal = list()
    for c in resultados.values():
        resultadosYtotal.append(sum(c))
    return resultadosYtotal


def Grafico_bar(Ytotal_Material_1, Ytotal_Material_2, Ytotal_Material_3, diâmetro):
    # Largura da barra:
    largura = 0.25
    # Definindo as posições da barra:
    x1 = arange(len(Ytotal_Material_1))
    x2 = [x + largura for x in x1]
    x3 = [x + largura for x in x2]
    # Criando as barras:
    figure(1)
    M1 = str(input('Qual o primeiro material? '))
    bar(x1, Ytotal_Material_1, color='y', width=0.25, label=M1)
    M2 = str(input('Qual o segundo material? '))
    bar(x2, Ytotal_Material_2, color='r', width=0.25, label=M2)
    M3 = str(input('Qual o terceiro material? '))
    bar(x3, Ytotal_Material_3, color='g', width=0.25, label=M3)
    # Legendas:
    xlabel('Diâmetro (mm)')
    xticks([r + largura for r in range(len(Ytotal_Material_1))], diâmetro)
    ylabel('Deslocamento da ponta do eixo ($\mu$m)')
    legend()


'''Menu interativo'''


def leiaInt(msg):
    while True:
        try:
            n = int(input(msg))
        except(ValueError, TypeError):
            print('\033[33mERRO: por favor, dígite um número inteiro válido.\033[m')
            continue
        else:
            return n


def leiaFloat(msg):
    while True:
        try:
            n = float(input(msg))
        except(ValueError, TypeError):
            print('\033[33mERRO: por favor, dígite um valor válido.\033[m')
            continue
        else:
            return n


def linha(tam=42):
    return '-' * tam


def Exibição(dicionario):
    #print('Tabela de cálculo dos valores de Y\'s em \u03BCm')
    #print()
    DF = DataFrame(dicionario, index=['y1', 'y2', 'y3', 'y4', 'y5']).transpose()
    DF_exibição = DF.assign(Y=DF.eval('y1 + y2 + y3 + y4 + y5')).rename_axis('Diâmetros', axis='columns')
    #print(round(DF_exibição, 2))
    return round(DF_exibição, 2)


def menu():
    print(linha(70))
    print('Menu Principal'.center(70))
    print(linha(70))
    print('1 - Cálculo do deslocamento total na ponta do eixo-árvore com importação dos diâmetros')
    print(
        '2 - Cálculo do deslocamento total na ponta do eixo-árvore com os com o(s) diâmetro(s) cálculado(s) por fadiga')
    print(
        '3 - Gráfico do delocamento total na ponta do eixo-árvore em função da variação da distância entre mancais(L)')
    print('4 - Gráfico do delocamento total na ponta do eixo-árvore em função da Rigidez do mancal dianteiro R1')
    print('5 - Gráfico do delocamento total na ponta do eixo-árvore em função da Rigidez do mancal traseiro R2')
    print('10 - Ver/Modificar variáveis')
    print('0 - Finalizar o programa')
    print(linha(70))


def diâmetro_fad_com_parametros(n, Sy, Sut, M_max, T, critério, ka, kb, kc, kd, ke,
                                kf, Kf, Kfs):
    Sy = array(Sy)  # [MPa]
    Sut = array(Sut)  # [MPa]
    Se_linha = 0.5 * Sut
    # ka = kb = kc = kd = ke = kf = 1
    Se = ka * kb * kc * kd * ke * kf * Se_linha  # [MPa]
    # Kf = Kfs = 1.5
    Ma = M_max
    # Mm = 0
    # Ta = 0
    Tm = T
    if critério == 'Gerber':
        # DE-Gerber
        d_Gerber_r = around((((16 * n * Kf * Ma) / (pi * Se)) * (1 + (1 + (3 * ((Kfs * Tm * Se) / (Kf * Ma * Sut)) ** 2)) ** 0.5)) ** (1 / 3), 2)
        d_Gerber = d_Gerber_r.tolist()
        d0_Gerber = d_Gerber_r / (1 - 0.7 ** 4)
        di_Gerber = 0.7 * d0_Gerber
        return d_Gerber, d0_Gerber, di_Gerber
    else:
        # DE-ASME Elíptico
        d_ASME_r = around((((16 * n) / pi) * ((4 * ((Kf * Ma) / Se) ** 2) + (3 * ((Kfs * Tm) / Sy) ** 2)) ** 0.5) ** (1 / 3), 2)
        d_ASME = d_ASME_r.tolist()
        # Eixo vazado
        d0_ASME = d_ASME_r / (1 - 0.7 ** 4)
        di_ASME = 0.7 * d0_ASME
        return d_ASME, d0_ASME, di_ASME