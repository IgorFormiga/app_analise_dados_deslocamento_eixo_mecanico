class Propriedades:

    def __init__(self):
        self._Fy1 = None
        self._Fy2 = None
        self._Myz = None
        self._A = None
        self._D1 = None
        self._Tipodoeixo = None
        self._L = None
        self._T = None
        self._R1 = None
        self._R2 = None
        self._Diametros = None
        self._Efad = None
        self._E = None
        self._n = None
        self._Sy = None
        self._Sut = None
        self._Criterio = None
        self._ka = None
        self._kb = None
        self._kc = None
        self._kd = None
        self._ke = None
        self._kf = None
        self._KF = None
        self._KFS = None
        self._Lvf = None
        self._Lvi = None
        self._Lvinc = None
        self._L_v = None
        self._Diametro_L = None
        self._R1vi = None
        self._R1vf = None
        self._R1vinc = None
        self._R1_v = None
        self._R2_R1 = None
        self._diametro = None
        self._R2vi = None
        self._R2vf = None
        self._R2vinc = None
        self._R2_v = None
        self._R1_R2 = None
        self._DF = None

    @property
    def Fy1(self):
        return self._Fy1

    @Fy1.setter
    def Fy1(self, fy1):
        self._Fy1 = fy1

    @property
    def Fy2(self):
        return self._Fy2

    @Fy2.setter
    def Fy2(self, fy2):
        self._Fy2 = fy2

    @property
    def Myz(self):
        return self._Myz

    @Myz.setter
    def Myz(self, myz):
        self._Myz = myz

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, a):
        self._A = a

    @property
    def D1(self):
        return self._D1

    @D1.setter
    def D1(self, d1):
        self._D1 = d1

    @property
    def Tipodoeixo(self):
        return self._Tipodoeixo

    @Tipodoeixo.setter
    def Tipodoeixo(self, tipo):
        self._Tipodoeixo = tipo

    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, lc):
        self._L = lc

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, t):
        self._T = t

    @property
    def R1(self):
        return self._R1

    @R1.setter
    def R1(self, r1):
        self._R1 = r1

    @property
    def R2(self):
        return self._R2

    @R2.setter
    def R2(self, r2):
        self._R2 = r2

    @property
    def Diametros(self):
        return self._Diametros

    @Diametros.setter
    def Diametros(self, diametros):
        self._Diametros = diametros

    @property
    def Efad(self):
        return self._Efad

    @Efad.setter
    def Efad(self, efad):
        self._Efad = efad

    @property
    def E(self):
        return self._E

    @E.setter
    def E(self, e):
        self._E = e

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, cs):
        self._n = cs

    @property
    def Sy(self):
        return self._Sy

    @Sy.setter
    def Sy(self, sy):
        self._Sy = sy

    @property
    def Sut(self):
        return self._Sut

    @Sut.setter
    def Sut(self, sut):
        self._Sut = sut

    @property
    def Criterio(self):
        return self._Criterio

    @Criterio.setter
    def Criterio(self, criterio):
        self._Criterio = criterio

    @property
    def ka(self):
        return self._ka

    @ka.setter
    def ka(self, KA):
        self._ka = KA

    @property
    def kb(self):
        return self._kb

    @kb.setter
    def kb(self, KB):
        self._kb = KB

    @property
    def kc(self):
        return self._kc

    @kc.setter
    def kc(self, KC):
        self._kc = KC

    @property
    def kd(self):
        return self._kd

    @kd.setter
    def kd(self, KD):
        self._kd = KD

    @property
    def ke(self):
        return self._ke

    @ke.setter
    def ke(self, KE):
        self._ke = KE

    @property
    def kf(self):
        return self._kf

    @kf.setter
    def kf(self, Kf):
        self._kf = Kf

    @property
    def KF(self):
        return self._KF

    @KF.setter
    def KF(self, kf):
        self._KF = kf

    @property
    def KFS(self):
        return self._KFS

    @KFS.setter
    def KFS(self, kfs):
        self._KFS = kfs

    @property
    def Lvi(self):
        return self._Lvi

    @Lvi.setter
    def Lvi(self, lvi):
        self._Lvi = lvi

    @property
    def Lvf(self):
        return self._Lvf

    @Lvf.setter
    def Lvf(self, lvf):
        self._Lvf = lvf

    @property
    def L_v(self):
        return self._L_v

    @L_v.setter
    def L_v(self, l_v):
        self._L_v = l_v

    @property
    def Lvinc(self):
        return self._Lvinc

    @Lvinc.setter
    def Lvinc(self, lvinc):
        self._Lvinc = lvinc

    @property
    def Diametro_L(self):
        return self._Diametro_L

    @Diametro_L.setter
    def Diametro_L(self, diametrol):
        self._Diametro_L = diametrol

    @property
    def R1vi(self):
        return self._R1vi

    @R1vi.setter
    def R1vi(self, r1vi):
        self._R1vi = r1vi

    @property
    def R1vf(self):
        return self._R1vf

    @R1vf.setter
    def R1vf(self, r1vf):
        self._R1vf = r1vf

    @property
    def R1vinc(self):
        return self._R1vinc

    @R1vinc.setter
    def R1vinc(self, r1vinc):
        self._R1vinc = r1vinc

    @property
    def R1_v(self):
        return self._R1_v

    @R1_v.setter
    def R1_v(self, r1v):
        self._R1_v = r1v

    @property
    def diametro(self):
        return self._diametro

    @diametro.setter
    def diametro(self, diam):
        self._diametro = diam

    @property
    def R2vi(self):
        return self._R2vi

    @R2vi.setter
    def R2vi(self, r2vi):
        self._R2vi = r2vi

    @property
    def R2vf(self):
        return self._R2vf

    @R2vf.setter
    def R2vf(self, r2vf):
        self._R2vf = r2vf

    @property
    def R2vinc(self):
        return self._R2vinc

    @R2vinc.setter
    def R2vinc(self, r2vinc):
        self._R2vinc = r2vinc

    @property
    def R2_v(self):
        return self._R2_v

    @R2_v.setter
    def R2_v(self, r2v):
        self._R2_v = r2v

    @property
    def R1_R2(self):
        return self._R1_R2

    @R1_R2.setter
    def R1_R2(self, r2r1):
        self._R1_R2 = r2r1

    @property
    def R2_R1(self):
        return self._R2_R1

    @R2_R1.setter
    def R2_R1(self, r2r1):
        self._R2_R1 = r2r1

    @property
    def DF(self):
        return self._DF

    @DF.setter
    def DF(self, df):
        self._DF = df


propriedades = Propriedades()

# P = Propriedades()
# P.tipodoeixo = 'Maciço'
# print(P.tipodoeixo)
