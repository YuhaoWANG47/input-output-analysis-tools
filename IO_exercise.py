import numpy as np
import IO_basic_function as IO
import IO_commodity_industry as SIOT
import IO_2Regions as IO2R
import IO_energy as IOE

# HW 1-4
A = [[1/8, 0, 1/4], [0, 1/8, 1/4], [1/6, 0, 1/6]]
Y = [50, 30, 20]
IO_1_4 = IO.IO(A, Y, 'A', 'Y')
print(IO_1_4.X)
print(IO_1_4.B)

# HW 2-3
Z = [[225, 600, 110], [250, 125, 425], [325, 700, 150]]
X = [1200, 2000, 1500] # list
IO_2_3 = IO.IO(Z, X)
dy = [100, 40, 30]
dv = [50, 100, 20]
print (IO_2_3.X + IO_2_3.get_new_X_by_Y(dy))
print (IO_2_3.X.T + IO_2_3.get_new_X_by_V(dv))

# HW 2-4
Z = [[9177, 60961, 2980], [20156, 316544, 47784], [6282, 50200, 38732]]
X = [78074, 548400, 192385]
IO_2_4 = IO.IO(Z, X)
print(IO_2_4.backward())
print(IO_2_4.forward())

# HW 3-4
U = [[20, 12, 18], [10, 13, 11], [12, 17, 40]]
V = [[99, 0, 10], [8, 137, 10], [0, 12, 150]]
X = [107, 149, 170]
Q = [109, 155, 162]
SIOT_W3 = SIOT.SIOT(U, V, X, Q)
L1 = SIOT_W3.get_L('i', 'c', 'c')
L2 = SIOT_W3.get_L('i', 'c', 'i')
print(L1)
print(L2)
Y = [30+6+16+5 + 10, 50+3+40+22 + 15, 70+12+8+11 + 20]
X1 = SIOT_W3.get_X_by_Y(Y, 'c', 'i', 'c')
X2 = SIOT_W3.get_X_by_Y(Y, 'c', 'i', 'i')
print(X1)
print(X2)

# HW 4
R = [[40, 50], [60, 10]]
S = [[30, 45], [70, 45]]
RR = [50, 50]
RS = [60, 80]
SR = [70, 50]
SS = [70, 50]
HW4 = IO2R.IO_2Regions(R, S, RR, RS, SR, SS)
FR = [50, 50]
FS = [40, 60]
print(HW4.get_X_by_F(FR, FS))


# 能源投产练习

Z = [[0, 40, 0], [10, 10, 10], [0, 0, 0]]
f = [0, 30,100]
E = [[0, 120, 0], [20, 20, 30]]
q = [0, 50]
IOE1 = IOE.IO_energy_value(Z, f, E, q)

Z = [[0, 20, 20, 0], [1, 3, 0, 1], [2.5, 1.25, 1.25, 2.5], [0, 0, 0, 0]]
f = [0, 15, 12.5, 20]
IOE2 = IOE.IO_energy_mixed(Z, f)
#print(IOE2.alpha)

Z = [[0, 20, 20, 0], [1, 3, 0, 1], [2.5, 1.25, 1.25, 2.5], [0, 0, 0, 0]]    # 英文教材p.409 例9.2 9.3
f = [0, 15, 12.5, 20]
IOE2 = IOE.IO_energy_mixed(Z, f, 'f', [1, 2, 3])
print(IOE2.alpha)

#Z = [[0, 300, 0], [20, 20, 20], [0, 0, 0]]
#f = [0, 60, 100]
#IOE3 = IOE.IO_energy_mixed(Z, f, 'f', [1, 2])
#IOE3 = IOE.IO_energy_value(Z, f, Z[0:1], f[0:1])
#print(IOE3.A)
#IOE3.Gx = np.mat([[0, 0, 0], [0, 300/120, 0]])
#print(IOE3.Gx)
#print(IOE3.Gx * IOE3.L)
#能源投产PPT pp. 55-58 & 英文教材p.412 不懂

Z = [[10, 20], [60, 80]]    # 英文教材p.407例9.1
f = [70, 100]
IOE4 = IOE.IO_energy_mixed(Z, f)
#print(IOE4.x)
#print(IOE4.A)
#print(IOE4.L)
#print(IOE4.delta)
#print(IOE4.alpha)
#print(IOE4.G)