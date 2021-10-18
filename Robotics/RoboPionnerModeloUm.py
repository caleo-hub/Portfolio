import numpy as np
from numpy import sin,cos
from RoboPionner import RoboPionner

class RoboPionnerModeloUm(RoboPionner):
    def __init__(self) -> None:
        super().__init__()

    @property
    def posicaoGlobal(self) -> np.ndarray:
        rotacao = self.rotacaoTheta
        posicaoGlobal = np.array([cos(rotacao),   -sin(rotacao),  0, 
                            sin(rotacao),   cos(rotacao),   0,
                             0           ,0,                 1]).reshape((3,3))

        coefposicaoGlobal =  np.array([1,0,
                                       0,0,
                                       0,1]).reshape((3,2))

        return np.matmul(posicaoGlobal,coefposicaoGlobal)

    @property
    def velocidadeRobo(self) -> np.ndarray:

        rD = self.rodaDireitaRaio
        rE = self.rodaEsquerdaRaio
        L =  self.distanciaRodaEixo

        RelacaoVelocidadeRodaRobo = np.array([rD/2, rE/2, 
                                            (rD/(2*L)), (-rE/(2*L))]).reshape((2,2))
        
        velocidadeAngularRoda = self.velocidadeAngularRodas
        velocidadeRobo = np.matmul(RelacaoVelocidadeRodaRobo,velocidadeAngularRoda)
        return velocidadeRobo

    def calculaNovaPosicaoRobo(self, Passo: float = 0.05):
        velocidadeGlobalRobo = np.matmul(self.posicaoGlobal,self.velocidadeRobo)
        deslocamentoRobo = velocidadeGlobalRobo*Passo
        self.posicaoRobo = self.posicaoRobo + deslocamentoRobo
        return self.posicaoRobo
    
    

    