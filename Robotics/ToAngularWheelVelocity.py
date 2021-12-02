import numpy as np

def ToAngularWheelVelocity(v_t,w_t):
    LinearVelocity = np.array([v_t,w_t])
    r = (195)/2000
    L = (381)/2000
    #RobotDimensionsMatrix = np.array([0.5*r,0.5*r,0.5*r/L,-0.5*r/L ]).reshape(2,2)
    InvRobotDimensionsMatrix = np.array([1/r,L/r,
                                         1/r,-L/r]).reshape(2,2)
    #InvRobotDimensionsMatrix = np.linalg.inv(RobotDimensionsMatrix) 
    AngularWheelVelocity = np.matmul(InvRobotDimensionsMatrix,LinearVelocity)
    return AngularWheelVelocity