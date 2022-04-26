from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.bubble import Bubble
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from ClassePropriedade.propriedades import Propriedades
from kivy.properties import BooleanProperty
import Funcoes.Funcoes_Calculo as Fc
from garden_matplotlib.backend_kivyagg import FigureCanvas
from matplotlib import pyplot as plt
from numpy import arange


#Configurando para que não seja possivel colocar em full screen
from kivy.config import Config
Config.set("graphics", "resizable", '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.write()

class MyInput(TextInput):
    validated = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(text=self.validate)

    def validate(self, input, value):
        try:
            status = float(value)
        except Exception:
            status = False

        if not status:
            self.validated = False
        else:
            self.validated = True


class MyInputList(TextInput):
    validatedlist = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(text=self.validatelist)

    def validatelist(self, input, value):
        lista = list()
        try:
            if ';' in value:
                lista_eixo = []
                value = list(value.split(';'))

                for c in value:
                    a = list(c.split(','))
                    for i in range(0, 2):
                        status = float(a[i])
                        lista_eixo.append(status)

                    lista.append(lista_eixo[:])
                    lista_eixo.clear()


            else:
                value = list(value.split(','))
                for i in value:
                    status = float(i)
                    lista.append(status)

        except Exception:
            status = False

        if not status:
            self.validatedlist = False
        else:
            self.validatedlist = True

        return lista


class CheckBoxCriterio(Widget):
    def Explicacao(self, titulo, texto):
        box = BoxLayout(orientation='vertical', padding=10)

        pop = Popup(title=titulo, content=box, size_hint=(None, None),
                    size=(650, 150), pos_hint={'x': 0.1, 'y': 0.7})
        label = Label(text=texto)
        box.add_widget(label)
        pop.open()


class CheckBoxTipo(Widget):
    tipo = StringProperty("")


class Menu(Screen):

    def confirmacao(self, *args):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        botoes = BoxLayout(padding=10, spacing=10)
        pop = Popup(title='Sair', content=box, size_hint=(None, None),
                    size=(600, 250))

        sim = Button(text='Sim', on_release=App.get_running_app().stop)
        nao = Button(text='Não', on_release=pop.dismiss)

        botoes.add_widget(sim)
        botoes.add_widget(nao)

        atencao = Image(source='Imagens/atencao.png')
        texto = Label(text='Sair limpará os dados armazenados em cache.\n             Realmente deseja sair do App?')
        box.add_widget(atencao)
        box.add_widget(texto)
        box.add_widget(botoes)

        pop.open()


class Mensagem(Bubble):
    pass


class CalculoTotalImportacaoDiametros(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = None
        # self.bubble = Mensagem()

    def Explicacao(self, titulo, texto):

        box = BoxLayout(orientation='vertical', padding=10)

        pop = Popup(title=titulo, content=box, size_hint=(None, None),
                    size=(650, 100), pos_hint={'x': 0.1, 'y': 0.8})
        label = Label(text=texto)
        box.add_widget(label)
        pop.open()

    def Atribuir(self):
        if propriedades.Fy1 is not None:
            self.ids.valor_Fy1.text = str(propriedades.Fy1)
        if propriedades.Fy2 is not None:
            self.ids.valor_Fy2.text = str(propriedades.Fy2)
        if propriedades.Myz is not None:
            self.ids.valor_Myz.text = str(propriedades.Myz)
        if propriedades.A is not None:
            self.ids.valor_A.text = str(propriedades.A)
        if propriedades.D1 is not None:
            self.ids.valor_D1.text = str(propriedades.D1)
        if propriedades.L is not None:
            self.ids.valor_L.text = str(propriedades.L)
        if propriedades.E is not None:
            self.ids.valor_E.text = str(propriedades.E)
        if propriedades.R1 is not None:
            self.ids.valor_R1.text = str(propriedades.R1)
        if propriedades.R2 is not None:
            self.ids.valor_R2.text = str(propriedades.R2)

    def avancar(self):
        lista = list()

        try:
            propriedades.Fy1 = float(self.ids.valor_Fy1.text)
            propriedades.Fy2 = float(self.ids.valor_Fy2.text)
            propriedades.Myz = float(self.ids.valor_Myz.text)
            propriedades.A = float(self.ids.valor_A.text)
            propriedades.D1 = float(self.ids.valor_D1.text)
            propriedades.L = float(self.ids.valor_L.text)
            propriedades.E = float(self.ids.valor_E.text)
            propriedades.R1 = float(self.ids.valor_R1.text)
            propriedades.R2 = float(self.ids.valor_R2.text)
            propriedades.Tipodoeixo = self.ids.valor_Tipo.text

            if ';' in self.ids.valor_Diametros.text and propriedades.Tipodoeixo == 'Vazado':
                lista_eixo = []
                L = list(self.ids.valor_Diametros.text.split(';'))
                for c in L:
                    a = list(c.split(','))
                    print(len(a))
                    print(type(a))
                    for i in range(0, 2):
                        d = float(a[i])
                        lista_eixo.append(d)

                    lista.append(lista_eixo[:])
                    lista_eixo.clear()
            else:
                L = list(self.ids.valor_Diametros.text.split(','))
                for i in L:
                    d = float(i)
                    lista.append(d)

            propriedades.Diametros = lista
            self.status = True

        except Exception:
            self.status = False

        if self.status:
            self.parent.current = 'ResultadoCalculoTotalImportacaoDiametros'

        else:
            box = BoxLayout(orientation='vertical', padding=10)
            pop = Popup(title='Erro de Atribuição', content=box, size_hint=(None, None),
                        size=(650, 150), pos_hint={'x': 0.1, 'y': 0.7})
            label = Label(
                text='Os dados importados precisam serguir o padrão númerico americano, \nou seja, o separador decimal como sendo ponto. Em caso de duvidas sobre \nalgum parâmetro, basta clicar sobre o nome do parâmetro.')
            box.add_widget(label)
            pop.open()


class ResultadoCalculoTotalImportacaoDiametros(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resultados_dict = None
        self.resultados_Ytotal = None

    def Calcular(self):
        self.resultados_dict, self.resultados_Ytotal = Fc.calculoY(propriedades.Fy1, propriedades.Fy2,
                                                                   propriedades.Myz, propriedades.A, propriedades.L,
                                                                   propriedades.E, propriedades.R1, propriedades.R2,
                                                                   propriedades.D1, propriedades.Diametros,
                                                                   propriedades.Tipodoeixo)

        self.DF = Fc.Exibição(self.resultados_dict)
        # Definindo a exibição da tabela
        Layout_GridLayout = GridLayout(pos_hint={'x': 0, 'y': 1},
                                       cols=1,
                                       spacing=10,
                                       size_hint=(None, None),
                                       height=515,
                                       width=785)

        # 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
        Layout_GridLayout.bind(minimum_height=Layout_GridLayout.setter('height'))

        self.lista = list()
        self.lista_df = list()
        # Primeiro elemento da lista_df vai ser cabeçalho da tabela:
        self.cabeçalho = ['Diâmetros', 'y1', 'y2', 'y3', 'y4', 'y5', 'Ytotal']
        self.lista_df.append(self.cabeçalho)

        for i in range(0, len(self.DF)):
            index = str(self.DF.index[i])
            self.lista.append(index)
            valores = self.DF.iloc[i].values
            for v in valores:
                v_str = str(v)
                self.lista.append(v_str)
            self.lista_df.append(self.lista[:])
            self.lista.clear()

        for linha in self.lista_df:
            layout_criando_linha = BoxLayout(spacing=10,
                                             orientation='horizontal',
                                             size_hint=(None, None),
                                             height=15,
                                             width=790)

            for l in linha:
                layout_criando_linha.add_widget(Label(text=l, font_size=15, color=(1, 1, 1, 1)))

            Layout_GridLayout.add_widget(layout_criando_linha)

        self.Scroll = ScrollView(pos_hint={'center_x': .5, 'center_y': .5},
                                 size_hint=(None, None),
                                 height=400,
                                 width=785)
        self.Scroll.add_widget(Layout_GridLayout)

        self.add_widget(self.Scroll)

    def Limpar(self):
        try:
            self.remove_widget(self.Scroll)
        except Exception:
            pass


class CalculoTotalFadiga(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = None
        # self.bubble = Mensagem()

    def Explicacao(self, titulo, texto):

        box = BoxLayout(orientation='vertical', padding=10)

        pop = Popup(title=titulo, content=box, size_hint=(None, None),
                    size=(650, 100), pos_hint={'x': 0.1, 'y': 0.8})
        label = Label(text=texto)
        box.add_widget(label)
        pop.open()

    def Atribuir(self):

        if propriedades.Fy1 is not None:
            self.ids.valor_Fy1.text = str(propriedades.Fy1)
        if propriedades.Fy2 is not None:
            self.ids.valor_Fy2.text = str(propriedades.Fy2)
        if propriedades.Myz is not None:
            self.ids.valor_Myz.text = str(propriedades.Myz)
        if propriedades.A is not None:
            self.ids.valor_A.text = str(propriedades.A)
        if propriedades.D1 is not None:
            self.ids.valor_D1.text = str(propriedades.D1)
        if propriedades.L is not None:
            self.ids.valor_L.text = str(propriedades.L)
        if propriedades.R1 is not None:
            self.ids.valor_R1.text = str(propriedades.R1)
        if propriedades.R2 is not None:
            self.ids.valor_R2.text = str(propriedades.R2)

    def avancar(self):

        try:
            propriedades.Fy1 = float(self.ids.valor_Fy1.text)
            propriedades.Fy2 = float(self.ids.valor_Fy2.text)
            propriedades.Myz = float(self.ids.valor_Myz.text)
            propriedades.A = float(self.ids.valor_A.text)
            propriedades.D1 = float(self.ids.valor_D1.text)
            propriedades.L = float(self.ids.valor_L.text)
            propriedades.R1 = float(self.ids.valor_R1.text)
            propriedades.R2 = float(self.ids.valor_R2.text)
            propriedades.Tipodoeixo = self.ids.valor_Tipo.text
            propriedades.Criterio = self.ids.valor_Criterio.text
            propriedades.n = float(self.ids.valor_n.text)
            propriedades.T = float(self.ids.valor_T.text)
            propriedades.ka = float(self.ids.valor_ka.text)
            propriedades.kb = float(self.ids.valor_kb.text)
            propriedades.kc = float(self.ids.valor_kc.text)
            propriedades.kd = float(self.ids.valor_kd.text)
            propriedades.ke = float(self.ids.valor_ke.text)
            propriedades.kf = float(self.ids.valor_kf.text)
            propriedades.KF = float(self.ids.valor_KF.text)
            propriedades.KFS = float(self.ids.valor_KFS.text)

            # Para o valor de E_fad:
            E = list(self.ids.valor_E_fad.text.split(','))
            lista_E = list()
            for i in E:
                e = float(i)
                lista_E.append(e)

            propriedades.Efad = lista_E

            # Para o valor de Sy:
            Sy = list(self.ids.valor_Sy.text.split(','))
            lista_Sy = list()
            for i in Sy:
                sy = float(i)
                lista_Sy.append(sy)

            propriedades.Sy = lista_Sy

            # Para o valor de Sut:
            Sut = list(self.ids.valor_Sut.text.split(','))
            lista_Sut = list()
            for i in Sut:
                sut = float(i)
                lista_Sut.append(sut)

            propriedades.Sut = lista_Sut
            if len(lista_E) == len(lista_Sy) == len(lista_Sut):
                self.status = True
            else:
                self.status = False
                self.Explicacao('Erro de atribuição',
                                'O número de parâmetros fornecidos em E, Sy e Sut precisam ser iguais.')

        except Exception:
            self.status = False

        if self.status:
            self.parent.current = 'ResultadoCalculoTotalFadiga'
        else:
            box = BoxLayout(orientation='vertical', padding=10)

            pop = Popup(title='Erro de Atribuição', content=box, size_hint=(None, None),
                        size=(650, 150), pos_hint={'x': 0.1, 'y': 0.7})
            label = Label(
                text='Os dados importados precisam serguir o padrão númerico americano, \nou seja, o separador decimal como sendo ponto. Em caso de duvidas sobre \nalgum parâmetro, basta clicar sobre o nome do parâmetro.')
            box.add_widget(label)
            pop.open()


class ResultadoCalculoTotalFadiga(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resultados_dict_fad = None
        self.resultados_Ytotal_fad = None
        self.M_max = None
        self.x_Max = None
        self.diametro_fad = None
        self.de = None
        self.di = None

    def Grafico(self, x, M):
        fig = plt.figure(figsize=(0.5, 0.5))  # figsize=(2,1)
        ax1 = fig.add_subplot()

        plt.plot(x, M, 'b')
        plt.fill_between(x, M, color='g')
        plt.xlabel('x (mm)')
        plt.ylabel('Momento Fletor (N.mm)')
        plt.grid()
        wid = FigureCanvas(fig)
        return wid

    def Calcular(self):
        self.M_max, self.x_Max, x, M = Fc.DMF(propriedades.Fy1, propriedades.Fy2,
                                              propriedades.Myz, propriedades.A,
                                              propriedades.L, propriedades.D1)

        box = BoxLayout(orientation='vertical', padding=10)

        pop = Popup(title='Grafico de Momento Fletor', content=box, size_hint=(None, None),
                    size=(650, 500))
        box.add_widget(self.Grafico(x, M))
        pop.open()

        self.diametro_fad, self.de, self.di = Fc.diâmetro_fad_com_parametros(propriedades.n, propriedades.Sy,
                                                                             propriedades.Sut, self.M_max,
                                                                             propriedades.T, propriedades.Criterio,
                                                                             propriedades.ka, propriedades.kb,
                                                                             propriedades.kc, propriedades.kd,
                                                                             propriedades.ke, propriedades.kf,
                                                                             propriedades.KF, propriedades.KFS)

        self.resultados_dict_fad, self.resultados_Ytotal_fad = Fc.calculoY_fad(propriedades.Fy1, propriedades.Fy2,
                                                                               propriedades.Myz, propriedades.A,
                                                                               propriedades.L, propriedades.Efad,
                                                                               propriedades.R1, propriedades.R2,
                                                                               propriedades.D1, self.diametro_fad,
                                                                               propriedades.Tipodoeixo)

        self.DF = Fc.Exibição(self.resultados_dict_fad)

        Layout_GridLayout = GridLayout(pos_hint={'x': 0, 'y': 1},
                                       cols=1,
                                       spacing=10,
                                       size_hint=(None, None),
                                       height=515,
                                       width=785)

        Layout_GridLayout.bind(minimum_height=Layout_GridLayout.setter('height'))

        self.lista = list()
        self.lista_df = list()
        # Primeiro elemento da lista_df vai ser cabeçalho da tabela:
        self.cabeçalho = ['Diâmetros', 'y1', 'y2', 'y3', 'y4', 'y5', 'Ytotal']
        self.lista_df.append(self.cabeçalho)

        for i in range(0, len(self.DF)):
            index = str(self.DF.index[i])
            self.lista.append(index)
            valores = self.DF.iloc[i].values
            for v in valores:
                v_str = str(v)
                self.lista.append(v_str)
            self.lista_df.append(self.lista[:])
            self.lista.clear()

        for linha in self.lista_df:
            layout_criando_linha = BoxLayout(spacing=10,
                                             orientation='horizontal',
                                             size_hint=(None, None),
                                             height=15,
                                             width=790)

            for l in linha:
                layout_criando_linha.add_widget(Label(text=l, font_size=15, color=(1, 1, 1, 1)))

            Layout_GridLayout.add_widget(layout_criando_linha)

        self.Scroll = ScrollView(pos_hint={'center_x': .5, 'center_y': .5},
                                 size_hint=(None, None),
                                 height=400,
                                 width=785)
        self.Scroll.add_widget(Layout_GridLayout)

        self.add_widget(self.Scroll)

    def Limpar(self):
        try:
            # self.ids.figura.clear_widgets()
            self.remove_widget(self.Scroll)
        except Exception:
            print('erro ao remover')


class GraficoDistanciaEntreMancais(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = None
        # self.bubble = Mensagem()

    def Explicacao(self, titulo, texto):
        box = BoxLayout(orientation='vertical', padding=10)

        pop = Popup(title=titulo, content=box, size_hint=(None, None),
                    size=(650, 100), pos_hint={'x': 0.1, 'y': 0.7})
        label = Label(text=texto)
        box.add_widget(label)
        pop.open()

    def Atribuir(self):

        if propriedades.Fy1 is not None:
            self.ids.valor_Fy1.text = str(propriedades.Fy1)
        if propriedades.Fy2 is not None:
            self.ids.valor_Fy2.text = str(propriedades.Fy2)
        if propriedades.Myz is not None:
            self.ids.valor_Myz.text = str(propriedades.Myz)
        if propriedades.A is not None:
            self.ids.valor_A.text = str(propriedades.A)
        if propriedades.D1 is not None:
            self.ids.valor_D1.text = str(propriedades.D1)
        if propriedades.R1 is not None:
            self.ids.valor_R1.text = str(propriedades.R1)
        if propriedades.R2 is not None:
            self.ids.valor_R2.text = str(propriedades.R2)
        if propriedades.E is not None:
            self.ids.valor_E.text = str(propriedades.E)

    def avancar(self):

        try:
            propriedades.Fy1 = float(self.ids.valor_Fy1.text)
            propriedades.Fy2 = float(self.ids.valor_Fy2.text)
            propriedades.Myz = float(self.ids.valor_Myz.text)
            propriedades.A = float(self.ids.valor_A.text)
            propriedades.D1 = float(self.ids.valor_D1.text)
            propriedades.E = float(self.ids.valor_E.text)
            propriedades.Tipodoeixo = self.ids.valor_Tipo.text
            propriedades.R1 = float(self.ids.valor_R1.text)
            propriedades.R2 = float(self.ids.valor_R2.text)

            # Criando a lista composta pelos valores de L
            propriedades.Lvi = float(self.ids.valor_Li.text)
            propriedades.Lvf = float(self.ids.valor_Lf.text)
            propriedades.Lvinc = float(self.ids.valor_Linc.text)
            propriedades.L_v = arange(propriedades.Lvi, propriedades.Lvf + propriedades.Lvinc,
                                      propriedades.Lvinc).tolist()

            # Criando a lista composta pelos 3 valores de diâmetro
            d1 = float(self.ids.valor_d1.text)
            d2 = float(self.ids.valor_d2.text)
            d3 = float(self.ids.valor_d3.text)

            propriedades.Diametro_L = [d1, d2, d3]

            self.status = True

        except Exception:
            self.status = False

        if self.status:
            self.parent.current = 'ResultadoGraficoDistanciaEntreMancais'
        else:
            box = BoxLayout(orientation='vertical', padding=10)

            pop = Popup(title='Erro de Atribuição', content=box, size_hint=(None, None),
                        size=(650, 150), pos_hint={'x': 0.1, 'y': 0.7})
            label = Label(
                text='Os dados importados precisam serguir o padrão númerico americano, \nou seja, o separador decimal como sendo ponto. Em caso de duvidas sobre \nalgum parâmetro, basta clicar sobre o nome do parâmetro.')
            box.add_widget(label)
            pop.open()


class ResultadoGraficoDistanciaEntreMancais(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def Calcular(self):
        Fc.calculoY_variando_L(propriedades.Fy1, propriedades.Fy2, propriedades.Myz, propriedades.A,
                               propriedades.L_v, propriedades.E, propriedades.R1, propriedades.R2,
                               propriedades.D1, propriedades.Diametro_L, propriedades.Tipodoeixo)

        fig1 = plt.gcf()
        self.wid = FigureCanvas(fig1)

        self.figura.add_widget(self.wid)

    def Limpar(self):
        try:
            self.ids.figura.clear_widgets()
        except Exception:
            print('erro ao remover')


class GraficoRigidezMancalDianteiro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = None
        # self.bubble = Mensagem()

    def Explicacao(self, titulo, texto):
        box = BoxLayout(orientation='vertical', padding=10)

        pop = Popup(title=titulo, content=box, size_hint=(None, None),
                    size=(650, 100), pos_hint={'x': 0.1, 'y': 0.7})
        label = Label(text=texto)
        box.add_widget(label)
        pop.open()

    def Atribuir(self):
        if propriedades.Fy1 is not None:
            self.ids.valor_Fy1.text = str(propriedades.Fy1)
        if propriedades.Fy2 is not None:
            self.ids.valor_Fy2.text = str(propriedades.Fy2)
        if propriedades.Myz is not None:
            self.ids.valor_Myz.text = str(propriedades.Myz)
        if propriedades.A is not None:
            self.ids.valor_A.text = str(propriedades.A)
        if propriedades.D1 is not None:
            self.ids.valor_D1.text = str(propriedades.D1)
        if propriedades.L is not None:
            self.ids.valor_L.text = str(propriedades.L)
        if propriedades.diametro is not None:
            self.ids.valor_d.text = str(propriedades.diametro)
        if propriedades.E is not None:
            self.ids.valor_E.text = str(propriedades.E)

    def avancar(self):

        try:
            propriedades.Fy1 = float(self.ids.valor_Fy1.text)
            propriedades.Fy2 = float(self.ids.valor_Fy2.text)
            propriedades.Myz = float(self.ids.valor_Myz.text)
            propriedades.A = float(self.ids.valor_A.text)
            propriedades.D1 = float(self.ids.valor_D1.text)
            propriedades.E = float(self.ids.valor_E.text)
            propriedades.Tipodoeixo = self.ids.valor_Tipo.text
            propriedades.L = float(self.ids.valor_L.text)
            propriedades.diametro = float(self.ids.valor_d.text)

            # Criando a lista compostas pelos valores de R1_v
            propriedades.R1vi = float(self.ids.valor_R1i.text)
            propriedades.R1vf = float(self.ids.valor_R1f.text)
            propriedades.R1vinc = float(self.ids.valor_R1inc.text)
            propriedades.R1_v = arange(propriedades.R1vi, propriedades.R1vf + propriedades.R1vinc,
                                       propriedades.R1vinc).tolist()

            # Criando a lista compsostas pelos 2 valores de R2
            R21 = float(self.ids.valor_R21.text)
            R22 = float(self.ids.valor_R22.text)
            propriedades.R2_R1 = [R21, R22]
            self.status = True

        except Exception:
            self.status = False

        if self.status:
            self.parent.current = 'ResultadoGraficoRigidezMancalDianteiro'
        else:
            box = BoxLayout(orientation='vertical', padding=10)

            pop = Popup(title='Erro de Atribuição', content=box, size_hint=(None, None),
                        size=(650, 150), pos_hint={'x': 0.1, 'y': 0.7})
            label = Label(
                text='Os dados importados precisam serguir o padrão númerico americano, \nou seja, o separador decimal como sendo ponto. Em caso de duvidas sobre \nalgum parâmetro, basta clicar sobre o nome do parâmetro.')
            box.add_widget(label)
            pop.open()


class ResultadoGraficoRigidezMancalDianteiro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def Calcular(self):
        Fc.calculoY_variando_R1(propriedades.Fy1, propriedades.Fy2, propriedades.Myz, propriedades.A,
                                propriedades.L, propriedades.E, propriedades.R1_v, propriedades.R2_R1,
                                propriedades.D1, propriedades.diametro, propriedades.Tipodoeixo)
        fig1 = plt.gcf()
        self.wid = FigureCanvas(fig1)

        self.figura.add_widget(self.wid)

    def Limpar(self):
        try:
            self.ids.figura.clear_widgets()
        except Exception:
            print('erro ao remover')


class GraficoRigidezMancalTraseiro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = None
        # self.bubble = Mensagem()

    def Explicacao(self, titulo, texto):
        box = BoxLayout(orientation='vertical', padding=10)

        pop = Popup(title=titulo, content=box, size_hint=(None, None),
                    size=(650, 100), pos_hint={'x': 0.1, 'y': 0.7})
        label = Label(text=texto)
        box.add_widget(label)
        pop.open()

    def Atribuir(self):
        if propriedades.Fy1 is not None:
            self.ids.valor_Fy1.text = str(propriedades.Fy1)
        if propriedades.Fy2 is not None:
            self.ids.valor_Fy2.text = str(propriedades.Fy2)
        if propriedades.Myz is not None:
            self.ids.valor_Myz.text = str(propriedades.Myz)
        if propriedades.A is not None:
            self.ids.valor_A.text = str(propriedades.A)
        if propriedades.D1 is not None:
            self.ids.valor_D1.text = str(propriedades.D1)
        if propriedades.L is not None:
            self.ids.valor_L.text = str(propriedades.L)
        if propriedades.diametro is not None:
            self.ids.valor_d.text = str(propriedades.diametro)
        if propriedades.E is not None:
            self.ids.valor_E.text = str(propriedades.E)

    def avancar(self):

        try:
            propriedades.Fy1 = float(self.ids.valor_Fy1.text)
            propriedades.Fy2 = float(self.ids.valor_Fy2.text)
            propriedades.Myz = float(self.ids.valor_Myz.text)
            propriedades.A = float(self.ids.valor_A.text)
            propriedades.D1 = float(self.ids.valor_D1.text)
            propriedades.E = float(self.ids.valor_E.text)
            propriedades.Tipodoeixo = self.ids.valor_Tipo.text
            propriedades.L = float(self.ids.valor_L.text)
            propriedades.diametro = float(self.ids.valor_d.text)

            # Criando a lista compostas pelos valores de R1_v
            propriedades.R2vi = float(self.ids.valor_R2i.text)
            propriedades.R2vf = float(self.ids.valor_R2f.text)
            propriedades.R2vinc = float(self.ids.valor_R2inc.text)
            propriedades.R2_v = arange(propriedades.R2vi, propriedades.R2vf + propriedades.R2vinc,
                                       propriedades.R2vinc).tolist()

            # Criando a lista compsostas pelos 2 valores de R1
            R11 = float(self.ids.valor_R11.text)
            R12 = float(self.ids.valor_R12.text)
            propriedades.R1_R2 = [R11, R12]

            self.status = True

        except Exception:
            self.status = False

        if self.status:
            self.parent.current = 'ResultadoGraficoRigidezMancalTraseiro'

        else:
            box = BoxLayout(orientation='vertical', padding=10)

            pop = Popup(title='Erro de Atribuição', content=box, size_hint=(None, None),
                        size=(650, 150), pos_hint={'x': 0.1, 'y': 0.7})
            label = Label(
                text='Os dados importados precisam serguir o padrão númerico americano, \nou seja, o separador decimal como sendo ponto. Em caso de duvidas sobre \nalgum parâmetro, basta clicar sobre o nome do parâmetro.')
            box.add_widget(label)
            pop.open()


class ResultadoGraficoRigidezMancalTraseiro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def Calcular(self):

        Fc.calculoY_variando_R2(propriedades.Fy1, propriedades.Fy2, propriedades.Myz, propriedades.A,
                                propriedades.L, propriedades.E, propriedades.R1_R2, propriedades.R2_v,
                                propriedades.D1, propriedades.diametro, propriedades.Tipodoeixo)

        self.fig1 = plt.gcf()
        self.wid = FigureCanvas(self.fig1)
        self.figura.add_widget(self.wid)

    def Limpar(self):
        try:
            self.ids.figura.clear_widgets()

        except Exception:
            print('erro ao remover')


class Gerenciador(ScreenManager):
    pass


class GuiApp(App):
    def build(self):
        return Gerenciador()


propriedades = Propriedades()
GuiApp().run()
