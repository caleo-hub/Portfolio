import numpy as np
from numpy import tan,matmul,sqrt
import matplotlib.pyplot as plt

def NonHolonomicTrajectory(InitialPose,FinalPose,LinearVelocity = 1,Step = 0.05):
    jxi = float(InitialPose[0])
    jyi = float(InitialPose[1])
    jOi = float(InitialPose[2])

    jxf = float(FinalPose[0])
    jyf = float(FinalPose[1])
    jOf = float(FinalPose[2])

    deltax = jxf - jxi
    deltay = jyf - jyi
    di = tan(jOi)
    df = tan(jOf)

    a0 = jxi
    a1 = deltax
    a2 = 0
    a3 = deltax - a2 - a1
    b0 = jyi
    b1 = di*a1
    b2 = 3*(deltay - df*deltax) + df*a2 - 2*(di-df)*a1
    b3 = 3*df*deltax-2*deltay-df*a2 - (2*df-di)*a1

    LambdaParameter = np.array([0]).reshape((1,1))
    lambda_k = float(LambdaParameter[0])
    T = Step
    v_k = LinearVelocity

    while lambda_k < 1:
        dx_k = matmul([a1, 2*a2, 3*a3],[1,lambda_k,lambda_k**2])
        dy_k = matmul([b1, 2*b2, 3*b3], [1,lambda_k,lambda_k**2])

        dlambda_k = v_k/(sqrt(dx_k**2 + dy_k**2))
        lambda_k = lambda_k+ dlambda_k*T
        LambdaParameter = np.append(LambdaParameter,lambda_k)

    StepsNumber = LambdaParameter.shape
    StepsNumber = int(StepsNumber[0])
    LambdaParameter = LambdaParameter.reshape((1,StepsNumber))

    lambda_matrix_cubic = np.array([np.ones((1,StepsNumber)),
                             LambdaParameter, 
                             LambdaParameter**2,
                             LambdaParameter**3]).reshape((4,StepsNumber))

    lambda_matrix_square = np.array([np.ones((1,StepsNumber)),
                             LambdaParameter, 
                             LambdaParameter**2]).reshape((3,StepsNumber))

    dx_dlambda = matmul([a1,2*a2,3*a3],lambda_matrix_square)
    dy_dlambda = matmul([b1,2*b2,3*b3],lambda_matrix_square)

    PathX = matmul([a0, a1, a2, a3],lambda_matrix_cubic)
    PathY = matmul([b0, b1, b2, b3],lambda_matrix_cubic)
    PathO = np.divide(dy_dlambda,dx_dlambda)
    PathO = np.arctan(PathO)

    dx_dt = np.gradient(PathX,Step)
    dy_dt = np.gradient(PathY,Step)
    dO_dt = np.gradient(PathO,Step)

    v_t = sqrt(dx_dt**2 + dy_dt**2)
    w_t = dO_dt

    
    plt.scatter(PathX,PathY)
    plt.show()

    return v_t,w_t