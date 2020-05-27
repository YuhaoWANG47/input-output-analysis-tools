import numpy as np

class IO_2Regions():
    def __init__(self, R_input, S_input, RR_input, RS_input, SR_input, SS_input):
        '''
        以list形式输入六个矩阵，建立两区域间投入产出模型
        :param R_input: 区域R购买矩阵，输入一个包含n个长度为n的list的list
        :param S_input: 区域S购买矩阵，输入一个包含n个长度为n的list的list
        :param RR_input: RR之间的产品运输量，输入一个长度为n的list [RR1, RR2, ... RRn]
        :param RS_input: RS之间的产品运输量，输入一个长度为n的list [RS1, RS2, ... RSn]
        :param SR_input: SR之间的产品运输量，输入一个长度为n的list [SR1, SR2, ... SRn] 
        :param SS_input: SS之间的产品运输量，输入一个长度为n的list [SS1, SS2, ... SSn]
        '''
        self.R = np.mat(R_input)    # 区域R购买矩阵
        self.S = np.mat(S_input)    # 区域S购买矩阵
        self.Z = np.mat(np.block([[self.R, np.zeros((self.R.shape[0], self.S.shape[1]))],
            [np.zeros((self.S.shape[0], self.R.shape[1])), self.S]])) # 区域R, S合并购买矩阵
        self.RR = np.mat(np.diag(RR_input)) # RR之间的产品运输量，对角矩阵
        self.RS = np.mat(np.diag(RS_input)) # RS之间的产品运输量，对角矩阵
        self.SR = np.mat(np.diag(SR_input)) # SR之间的产品运输量，对角矩阵
        self.SS = np.mat(np.diag(SS_input)) # SS之间的产品运输量，对角矩阵
        self.Q = np.mat(np.block([[self.RR, self.RS], [self.SR, self.SS]]))  # 区域间总产品运输量矩阵
        self.X = self.Q.sum(1)  # Q行求和，表示两区域产品总产出量
        self.T = self.Q.sum(0)  # Q列求和，表示两区域产品总流入量
        self.A = self.Z * np.mat(np.diag(self.X.reshape(-1).tolist()[0])).I  # 区域技术系数矩阵
        self.C = self.Q * np.mat(np.diag(self.T.tolist()[0])).I # 区域流量系数矩阵

    def __str__(self):
        return "U = \n {} \nV = \n {} \nX = \n {} \nQ = \n {} \n".format(self.U, self.V, self.X, self.Q)

    def get_X_by_F(self, FR, FS):
        '''
        输入两地区计划需求，输出两地区总产出
        :param FR: 地区R计划需求，输入一个长度为n的list
        :param FS: 地区S计划需求，输入一个长度为n的list
        :return: 地区R和S的总产出，一个2n*1的mat（上半代表地区R，下半代表地区S；两个结果也会分别print）
        '''
        F = np.mat(FR + FS).T
        I = np.eye(len(self.A))
        X = (I - self.C * self.A).I * self.C * F
        X_list = X.reshape(-1).tolist()[0]
        n = int(len(X_list) / 2)
        XR = X_list[:n]
        XS = X_list[n:]
        print('\nXR = {} \nXS = {} \n'.format(XR, XS))
        return X