import numpy as np
import time
import sys
import numpy as np
from numpy import sin,cos
import matplotlib.pyplot as plt
from PIL import Image
import cv2

class RoboPionner():
    def __init__(self) -> None:
        self.rodaDiametro = (195)/1000 #R
        self.raio = self.rodaDiametro/2
        self.rodaDireitaRaio = self.rodaDiametro/2 #Rd
        self.rodaEsquerdaRaio = self.rodaDiametro/2 #Re
        self.distanciaRodaEixo = ((381)/1000)/2 #L
        self.velocidadeAngularRodaDireita = 0.5
        self.velocidadeAngularRodaEsquerda = 0.5
        self._posicaoRoboXYtheta = np.array([0,0,0]).reshape(3,1)

    @property
    def posicaoRobo(self) -> np.ndarray:
        return self._posicaoRoboXYtheta

    @property
    def velocidadeAngularRodas(self) -> np.ndarray:
        return np.array([self.velocidadeAngularRodaDireita,
                        self.velocidadeAngularRodaEsquerda]).reshape((2,1))

    @property
    def velocidadeLinearRodas(self) -> float:
        return self.velocidadeAngularRodaDireita * self.raio, self.velocidadeAngularRodaEsquerda * self.raio
    @property
    def posicaoX(self) -> float:
        return float(self._posicaoRoboXYtheta[0])
    @property
    def posicaoY(self) -> float:
        return float(self._posicaoRoboXYtheta[1])
    @property  
    def rotacaoTheta(self) -> float:
        return float(self._posicaoRoboXYtheta[2])

    @posicaoRobo.setter
    def posicaoRobo(self,Posicao:np.ndarray) -> np.ndarray:
        self._posicaoRoboXYtheta = Posicao.reshape(3,1)

    @velocidadeAngularRodas.setter
    def velocidadeAngularRodas(self,velocidadesAngularesRodas):
        self.velocidadeAngularRodaDireita, self.velocidadeAngularRodaEsquerda = velocidadesAngularesRodas

def Simula(velocidadeAngularRodaDireita,velocidadeAngularRodaEsquerda,Passo=0.05,TempoSimulacaoSegundos=10):
    try:
        import sim
    except:
        print ('--------------------------------------------------------------')
        print ('"sim.py" could not be imported. This means very probably that')
        print ('either "sim.py" or the remoteApi library could not be found.')
        print ('Make sure both are in the same folder as this file,')
        print ('or appropriately adjust the file "sim.py"')
        print ('--------------------------------------------------------------')
        print ('')

    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
    if clientID!=-1:
        print ('Connected to remote API server')
        print("Simulation Started", end =" ")
        # enable the synchronous mode on the client:
        sim.simxSynchronous(clientID,True)

        # start the simulation:
        sim.simxStartSimulation(clientID,sim.simx_opmode_blocking)

        ## Handle 
        returnCode,Robot = sim.simxGetObjectHandle(clientID,'Pioneer_p3dx',sim.simx_opmode_blocking)
        returnCode,left_Motor= sim.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',sim.simx_opmode_blocking)
        returnCode,right_Motor= sim.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',sim.simx_opmode_blocking)
        returnCode,front_Sensor =sim.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor5',sim.simx_opmode_blocking)
        returnCode,camera= sim.simxGetObjectHandle(clientID,'Vision_sensor',sim.simx_opmode_blocking)
        returnCode,resolution,image = sim.simxGetVisionSensorImage(clientID,camera,1,sim.simx_opmode_streaming)
    
            
        #Periodo de amostragem e tempo de simulacao
        T = Passo # Tempo de passo. Tem de estar em concordancia com Vrep!
        Tsim = TempoSimulacaoSegundos  # segundos
        t = np.arange(0,Tsim,T)
        N = len(t)

        #Pose inicial
        returnCode,Real_Robot_position = sim.simxGetObjectPosition(clientID,Robot,-1,sim.simx_opmode_blocking)
        P = np.array(Real_Robot_position).reshape((3,1))
        PosicaoInicial = P
        PosicaoRealHistorico = P - PosicaoInicial

    
        # Now step a few times:
        for i in range(0,N-1):
            #Anda um passo de simulacao
            sim.simxSynchronousTrigger(clientID)
            
            
            #Velocidade de referencia
            v_motor_l= velocidadeAngularRodaEsquerda
            v_motor_r= velocidadeAngularRodaDireita
            
            returnCode=sim.simxSetJointTargetVelocity(clientID,left_Motor,v_motor_l,sim.simx_opmode_blocking)
            returnCode=sim.simxSetJointTargetVelocity(clientID,right_Motor,v_motor_r,sim.simx_opmode_blocking)

            
            returnCode,Real_Robot_position = sim.simxGetObjectPosition(clientID,Robot,-1,sim.simx_opmode_blocking)
            P = np.array(Real_Robot_position).reshape((3,1)) - PosicaoInicial
            PosicaoRealHistorico = np.append(PosicaoRealHistorico,P,axis=1)
            b = "Simulando " + str((i/(N-1))*100) + '%'
            #print (b)
            sys.stdout.write('\r'+b)
            returnCode,resolution,image =sim.simxGetVisionSensorImage(clientID,camera,1,sim.simx_opmode_buffer)
            if returnCode == sim.simx_return_ok :
                imageAcquisitionTime=sim.simxGetLastCmdTime(clientID)
                #time.sleep(.5)
                img = np.array(image,dtype=np.uint8)
                img.resize([resolution[1],resolution[0]])

                img = np.flip(img)
                img = np.fliplr(img)
                cv2.imshow('image',img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        
        # stop the simulation:
        sim.simxStopSimulation(clientID,sim.simx_opmode_blocking)
        print()
        print('Simulation Stopped')

        # Now close the connection to CoppeliaSim:
        sim.simxFinish(clientID)
        print('Simulation Closed')


    else:
        print ('Failed connecting to remote API server')
        print ('Program ended')
    return PosicaoRealHistorico

def plotaGrafico(PosicaoRoboHistorico,PosicaoRealHistorico):    
    PosicaoX = PosicaoRoboHistorico[0,:]
    PosicaoY = PosicaoRoboHistorico[1,:]
    Angulo = PosicaoRoboHistorico[2,:]


    PosicaoRealX = PosicaoRealHistorico[0,:]
    PosicaoRealY = PosicaoRealHistorico[1,:]
    AnguloReal = PosicaoRealHistorico[2,:]

    plt.plot(PosicaoRealX,PosicaoRealY,color='red', label="Ground Truth")

    
    plt.plot(PosicaoX,PosicaoY,color='blue',ls='--', label="Modelo")
    Title = 'Trajetória Robô'
    plt.title(Title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('square')
    plt.legend()