import numpy as np

class SIOT():
    def __init__(self, U_input, V_input, X_input, Q_input):
        '''
        以list形式输入四个矩阵，建立供给-使用(UV)表投入产出模型
        :param U_input: 输入一个包含n个长度为n的list的list, 表示使用表 产品x产业投入矩阵
        :param V_input: 输入一个包含n个长度为n的list的list, 表示供给表 产业x产品产出矩阵
        :param X_input: 输入一个长度为n的list，表示产品总产出
        :param Q_input: 输入一个长度为n的list，表示产业总产出
        '''
        self.U = np.mat(U_input)    # 使用表：产品x产业-投入矩阵
        self.V = np.mat(V_input)    # 供给表：产业x产品-产出矩阵
        self.X = np.mat(X_input).T  # 产品总产出  
        self.Q = np.mat(Q_input).T  # 部门总产出   
        self.B = self.U * np.mat(np.diag(Q_input)).I   # 投入系数矩阵
        self.C = self.V.T * np.mat(np.diag(Q_input)).I  # 产品比例系数矩阵
        self.D = self.V * np.mat(np.diag(X_input)).I    # 市场份额系数矩阵
    
    def __str__(self):
        return "U = \n {} \nV = \n {} \nX = \n {} \nQ = \n {} \n".format(self.U, self.V, self.X, self.Q)
    
    def get_L(self, row = 'c', col = 'c', assume = 'c'):    
        '''
        求完全需求系数矩阵L（相当于列昂惕夫逆），默认为在产品技术假定下求产品x产品的L
        :param row: 指定要求的L的行含义，输入c（产品）或i（产业）
        :param col: 指定要求的L的列含义，输入c（产品）或i（产业）
        :param assume: 指定所使用的技术假定，输入c（产品）或i（产业）
        '''
        I = np.eye(len(self.U))
        if assume == 'c':
            if row == 'c':
                if col == 'c':
                    return (I - self.B * self.C.I).I    # 产品技术假定，产品*产品
                elif col == 'i':
                    return (I - self.B * self.C.I).I * self.C    # 产品技术假定，产品*产业
            elif row == 'i':
                if col == 'c':
                    return self.C.I * (I - self.B * self.C.I).I    # 产品技术假定，产业*产品
                elif col == 'i':
                    return (I - self.C.I * self.B).I    # 产品技术假定，产业*产业
        elif assume == 'i':
            if row == 'c':
                if col == 'c':
                    return (I - self.B * self.D).I     # 产业技术假定，产品*产品
                elif col == 'i':
                    return (I - self.B * self.D).I * self.D.I    # 产业技术假定，产品*产业
            elif row == 'i':
                if col == 'c':
                    return self.D * (I - self.B * self.D).I     # 产业技术假定，产业*产品
                elif col == 'i':
                    return (I - self.D * self.B).I     # 产业技术假定，产业*产业

    def get_X_by_Y(self, Y, Y_rep = 'c', X_rep = 'c', assume = 'c'):    
        '''
        给定最终需求Y求总生产量X，默认为在产品技术假定下 输入产品的最终需求 求产品的总生产量
        :param Y: 最终需求，输入一个长度为n的list
        :param Y_rep: 指定最终需求的表示方法，输入c（产品）或i（产业）
        :param X_rep: 指定总生产量的表示方法，输入c（产品）或i（产业）
        :param assume: 指定所使用的技术假定，输入c（产品）或i（产业）
        '''
        L = self.get_L(X_rep, Y_rep, assume)
        X = L * np.mat(Y).T
        return X