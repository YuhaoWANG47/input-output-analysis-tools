import numpy as np

class IO():
    def __init__(self, Z_A_input, X_Y_input, Z_A = 'Z', X_Y = 'X'):
        '''
        以list形式输入两个矩阵建立投入产出模型，可以输入 Z & X, A & X, A & Y 三种组合（默认为第一种）
        :param Z_A_input: 输入一个包含n个长度为n的list的list
        :param X_Y_input: 输入一个长度为n的list
        :param Z_A: 输入'Z'或'A', 表示第一个参数为中间流量表Z 或 直接消耗系数表A, 默认为前者
        :param X_Y: 输入'X'或'Y',表示第二个参数为总产出X 或 最终产出Y, 默认为前者
        '''
        if Z_A == 'Z' and X_Y == 'X':
            self.X = np.mat(X_Y_input).T    # 总产出
            self.Z = np.mat(Z_A_input)  # 中间流量矩阵 
            self.A = self.Z * np.mat(np.diag(self.X.reshape(-1).tolist()[0])).I    # 直接消耗系数矩阵
            self.L = (np.eye(len(self.A)) - self.A).I   # 列昂惕夫逆
            self.Y = self.L.I * self.X  # 最终产出
        elif Z_A == 'A':
            if X_Y == 'X':
                self.X = np.mat(X_Y_input).T    # 总产出
                self.A = np.mat(Z_A_input)  # 直接消耗系数矩阵
                self.Z = self.A * np.mat(np.diag(self.X.reshape(-1).tolist()[0]))   # 中间流量矩阵 
                self.L = (np.eye(len(self.A)) - self.A).I   # 列昂惕夫逆
                self.Y = self.L.I * self.X  # 最终产出
            if X_Y == 'Y':
                self.Y = np.mat(X_Y_input).T    # 最终产出
                self.A = np.mat(Z_A_input)  # 直接消耗系数矩阵
                self.L = (np.eye(len(self.A)) - self.A).I   # 列昂惕夫逆
                self.X = self.L * self.Y    # 总产出
                self.Z = self.A * np.mat(np.diag(self.X.reshape(-1).tolist()[0]))    # 中间流量矩阵
        self.B = self.L - np.eye(len(self.A)) # 完全消耗系数矩阵
        self.R = np.mat(np.diag(self.X.reshape(-1).tolist()[0])).I * self.Z   # 直接分配系数矩阵
        self.G = (np.eye(len(self.R)) - self.R).I   # 高希逆

    def __str__(self):
        return "Z = \n {} \nX = \n {} \n".format(self.Z, self.X)

    def get_new_Y_by_X(self, new_X):
        '''
        给定新的总产出X，求新的最终产出Y
        :param new_X: 新的总产出X, 输入一个长度为n的list
        :return: 新的最终产出Y, 一个n*1的mat
        '''
        Y = self.L.I * np.mat(new_X).T
        return Y

    def get_new_X_by_Y(self, new_Y):
        '''
        给定新的最终产出Y，求新的总产出X；需求拉动模型
        :param new_Y: 新的最终产出Y, 输入一个长度为n的list
        :return: 新的总产出X, 一个n*1的mat
        '''
        X = self.L * np.mat(new_Y).T
        return X
    
    def get_new_X_by_V(self, new_V):
        '''
        给定新的产品附加值V，求新的总产出X；供给驱动模型
        :param new_V: 新的产品附加值V, 输入一个长度为n的list
        :return: 新的总产出X, 一个1*n的mat
        '''
        X = np.mat(new_V) * self.G
        return X

    def get_Av(self, V):
        '''
        给定产品附加值/劳动报酬V，求直接劳动报酬系数矩阵Av
        :param V: 产品附加值/劳动报酬V, 输入一个长度为n的list
        :return: 直接劳动报酬系数矩阵Av, 一个1*n的mat
        '''
        Av_input = []
        con = 0
        for num in V:
            v = num / self.X[con].tolist()[0][0]
            Av_input.append(v)
            con += 1
        return np.mat(Av_input)

    def get_P(self, V0): 
        '''
        给定任意劳动力成本V0，求相应的部门产品价格P；通过分别输入新旧V可以求出新旧P，以便进一步计算劳动力成本变化造成的影响
        :param V0: 任意劳动力成本V0, 输入一个长度为n的list
        :return: 部门产品价格P, 一个1*n的mat
        '''
        return self.get_Av(V0) * self.L
    
    def get_Price_Change(self, good_X, good_Y, ratio): 
        '''
        求产品价格变化造成的影响
        :param good_X: 输入自变量产品编号int(1, 2...)
        :param good_Y: 输入因变量产品编号int(1, 2...)
        :ratio: 自变量产品价格变化幅度float
        :return: 因变量产品价格变化幅度float
        '''
        X_list = self.L[good_X - 1].tolist()[0]
        change = ratio / X_list[good_X - 1] * X_list[good_Y - 1]
        return change
    
    def backward(self):
        '''
        求部门的后向联系：影响力系数delta
        :return: 一个1*n的mat [delta1, delta2, ...]
        '''
        L_SUM = self.L.sum() # sum all
        L_COL_SUM = self.L.sum(0).tolist()[0]    # sum the columns 格式为[a, b, c]
        delta = []  # 后向联系：影响力系数
        for l in L_COL_SUM: 
            d = l * len(L_COL_SUM) / self.L.sum()  #计算影响力系数，用列求和除以总和的列平均值
            delta.append(d)
        return delta

    def forward(self):
        '''
        求部门的后向联系：影响力系数theta
        :return: 一个1*n的mat [theta1, theta2, ...]
        '''
        G_SUM = self.G.sum()
        G_ROW_SUM = self.G.sum(1).tolist()  # sum the rows 格式为[[a], [b], [c]]
        theta = []  # 前向联系：感应度系数
        for g in G_ROW_SUM:
            t = g[0] * len(G_ROW_SUM) / self.G.sum()   #计算感应度系数，用行求和除以总和的行平均值
            theta.append(t)
        return theta