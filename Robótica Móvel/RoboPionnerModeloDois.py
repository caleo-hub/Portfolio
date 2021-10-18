import numpy as np
from numpy import sin,cos
from numpy.core.records import array
from RoboPionner import RoboPionner

class RoboPionnerModeloDois(RoboPionner):
    def __init__(self) -> None:
        super().__init__()

    @property
    def posicaoGlobal(self) -> np.ndarray:
        rotacao = self.ICCAngularVelocity*self.Passo
        posicaoGlobal = np.array([cos(rotacao),   -sin(rotacao),  0, 
                            sin(rotacao),   cos(rotacao),   0,
                             0           ,0,                 1]).reshape((3,3))

        return posicaoGlobal


    @property
    def ICCRadius(self) -> float:
        vD,vE  = self.velocidadeLinearRodas
        L = self.distanciaRodaEixo*2
        R = (L/2)*((vE+vD)/(vD-vE))

        return R
    
    
    @property
    def ICCAngularVelocity(self) -> float:
        vD,vE  = self.velocidadeLinearRodas
        L = self.distanciaRodaEixo*2
        w = (vD-vE)/(L)

        return w

    @property   
    def ICC(self) -> np.ndarray:
        
        X = self.posicaoX
        Y = self.posicaoY
        Theta = self.rotacaoTheta

        ICCx = X - self.ICCRadius*sin(Theta)
        ICCy = Y + self.ICCRadius*cos(Theta)
        ICCtheta = self.ICCAngularVelocity*self.Passo

        ICC = np.array([ICCx,ICCy,ICCtheta]).reshape((3,1))
        return ICC

    def velocidadeRodasDiferentes(self):
        vD,vE  = self.velocidadeAngularRodas
        if vD != vE:
            return True
        else:
            return False
    def calculaNovaPosicaoRobo(self, Passo: float = 0.05):
        
        self.Passo = Passo
        X = self.posicaoX
        Y = self.posicaoY
        Theta = self.rotacaoTheta

        if self.velocidadeRodasDiferentes():
            ICCx,ICCy,ICCtheta = self.ICC
            ICCx = float(ICCx)
            ICCy = float(ICCy)
            ICCtheta = float(ICCtheta)
            matrizPosicaoGlobal= self.posicaoGlobal

            distanciaICC = np.array([X - ICCx, Y - ICCy, Theta]).reshape(3,1)

            self.posicaoRobo = np.matmul(matrizPosicaoGlobal,distanciaICC) + self.ICC
        else:
            V, _ = self.velocidadeLinearRodas
            V = float(V)
            XNovo = X + V*cos(Theta)*self.Passo
            YNovo = Y + V*sin(Theta)*self.Passo
            ThetaNovo = Theta
            self.posicaoRobo = np.array([XNovo,YNovo,ThetaNovo]).reshape(3,1)
            

        
        return self.posicaoRobo


        

    
