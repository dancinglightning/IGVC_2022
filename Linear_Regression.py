import numpy as np

def linear_regression(x, n, lamda=0):
    x = np.array(x)
    z0 = np.array([1 for i in range(n)])
    z1 = np.array([i+1 for i in range(n)])
    z2 = z1**2
    z3 = z1**3
    z4 = z1**4
    z5 = z1**5
    z6 = z1**6
    z7 = z1**7
    z = np.vstack((z0, z1, z2, z3, z4, z5, z6, z7)).T
    return np.dot((np.linalg.inv(np.dot(z.T,z))), np.dot(z.T,x))

def output(x):
    weights = curve_fitting([(i+1)**2 for i in range(100)], 100)
    print(weights)
    powers = np.array([1, x, x**2, x**3, x**4, x**5, x**6, x**7])
    return np.dot(weights,powers)


print(output(9))