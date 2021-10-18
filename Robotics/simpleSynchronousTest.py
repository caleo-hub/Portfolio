# This small example illustrates how to use the remote API
# synchronous mode. The synchronous mode needs to be
# pre-enabled on the server side. You would do this by
# starting the server (e.g. in a child script) with:
#
# simRemoteApi.start(19999,1300,false,true)
#
# But in this example we try to connect on port
# 19997 where there should be a continuous remote API
# server service already running and pre-enabled for
# synchronous mode.
#
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

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


import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:
    print ('Connected to remote API server')

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
    T = 0.05 # Tempo de passo. Tem de estar em concordancia com Vrep!
    Tsim = 2  # segundos
    t = np.arange(0,Tsim,T)
    N = len(t)

    #Pose inicial
    returnCode,Robot_Position = sim.simxGetObjectPosition(clientID,Robot,-1,sim.simx_opmode_blocking)
    P = Robot_Position

    # Now step a few times:
    for i in range(1,N-1):
        #Anda um passo de simulacao
        sim.simxSynchronousTrigger(clientID)
        
        
        #Velocidade de referencia
        v_motor_l=1
        v_motor_r=1
        
        returnCode=sim.simxSetJointTargetVelocity(clientID,left_Motor,v_motor_l,sim.simx_opmode_blocking)
        returnCode=sim.simxSetJointTargetVelocity(clientID,right_Motor,v_motor_r,sim.simx_opmode_blocking)

        
        returnCode,Robot_Position = sim.simxGetObjectPosition(clientID,Robot,-1,sim.simx_opmode_blocking)
        P = Robot_Position

        returnCode,resolution,image =sim.simxGetVisionSensorImage(clientID,camera,1,sim.simx_opmode_buffer)
        if returnCode == sim.simx_return_ok :
            imageAcquisitionTime=sim.simxGetLastCmdTime(clientID)
            #time.sleep(.5)
            img = np.array(image,dtype=np.uint8)
            img.resize([resolution[1],resolution[0]])

            img = np.flip(img)
            img = np.fliplr(img)
            cv2.imshow('image',img)
            print('.')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    
    # stop the simulation:
    sim.simxStopSimulation(clientID,sim.simx_opmode_blocking)
    print('Simulation Stopped')

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
    print('Simulation Closed')




else:
    print ('Failed connecting to remote API server')
    print ('Program ended')
