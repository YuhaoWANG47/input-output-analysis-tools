import numpy as np

# 能源型投入产出模型部分我还没有完全弄懂，目前只能用来建立价值型和混合型两种模型并计算相应参数，尚不完善，请谨慎使用

class IO_energy_value():
    def __init__(self, Z_input, f_x_input, E_input, q_g_input, f_x = 'f', q_g = 'q'):
        '''
        以list形式输入四个矩阵建立价值能源型投入产出模型
        :param Z_input: 输入一个包含n个长度为n的list的list, 表示价值流量表的中间流量
        :param f_x_input: 输入一个长度为n的list
        :param E_input: 输入一个包含m个长度为n的list的list, 表示能源流量表的中间流量（m小于n因为非能源行业不计产出）
        :param q_g_input: 输入一个长度为m的list
        :param f_x: 输入'f'或'x', 表示第二个参数为价值流量表的 最终使用f 或 总产出x, 默认为前者
        :param q_g: 输入'q'或'g',表示第四个参数为能源流量表的 最终使用q 或 总产出g, 默认为前者
        '''
        self.Z = np.mat(Z_input)
        self.E = np.mat(E_input)
        if f_x == 'f':
            self.f = np.mat(f_x_input).T
            self.x = self.Z.sum(1) + self.f
        elif f_x == 'x':
            self.x = np.mat(f_x_input).T
            self.f = self.Z.sum(1) - self.x
        if q_g == 'q':
            self.q = np.mat(q_g_input).T
            self.g = self.E.sum(1) + self.q
        elif q_g == 'g':
            self.g = np.mat(q_g_input).T
            self.q = self.E.sum(1) - self.g
        self.A = self.Z * np.mat(np.diag(self.x.reshape(-1).tolist()[0])).I
        self.L = (np.eye(len(self.A)) - self.A).I
        self.alpha = self.g * self.f.I
        self.D = self.E * np.mat(np.diag(self.x.reshape(-1).tolist()[0])).I
        self.pf = self.get_pf()
        self.Q_tilde = self.get_Q_tilde()
        self.epsilon = self.D * self.L + self.Q_tilde
        
    def get_pf(self):   # 求pf的工具函数，不需要在外部使用
        f_list = self.f.reshape(-1).tolist()[0]
        q_list = self.q.reshape(-1).tolist()[0]
        pf_list = []
        count = 0
        for q in q_list:
            if q != 0:
                pf = f_list[count] / q
            else:
                pf = 0
            pf_list.append([pf])
            count += 1
        return np.mat(pf_list)
    
    def get_Q_tilde(self):  #求Q~的工具函数，不需要在外部使用
        n_nonen = self.f.shape[0] - self.q.shape[0]
        pf_list = self.pf.reshape(-1).tolist()[0]
        q_list = []
        for pf in pf_list:
            if pf != 0:
                q = 1 / pf
            else:
                q = 0
            q_list.append(q)
        q_diag = np.mat(np.diag(q_list))
        return np.block([q_diag, np.zeros((q_diag.shape[0], n_nonen))])


class IO_energy_mixed():
    def __init__(self, Z_input, f_x_input, f_x = 'f', energy = [0]):
        '''
        以list形式输入两个矩阵建立混合能源型投入产出模型
        :param Z_input: 输入一个包含n个长度为n的list的list, 表示混合流量表的中间流量
        :param f_x_input: 输入一个长度为n的list
        :param f_x: 输入'f'或'x', 表示第二个参数为混合流量表的 最终使用f 或 总产出x, 默认为前者
        :param energy: 输入一个由正整数构成的list，表示混合流量表中哪几行为能源行业（从1开始编号），默认为倒数第一行
        '''
        self.Z = np.mat(Z_input)
        if f_x == 'f':
            self.f = np.mat(f_x_input).T
            self.x = self.Z.sum(1) + self.f
        elif f_x == 'x':
            self.x = np.mat(f_x_input).T
            self.f = self.Z.sum(1) - self.x
        self.A = self.Z * np.mat(np.diag(self.x.reshape(-1).tolist()[0])).I
        self.L = (np.eye(len(self.A)) - self.A).I
        self.energy = [i - 1 for i in energy]   # 输入能源行业所在行数，从1开始编号
        self.G = np.mat(np.diag(self.x.reshape(-1).tolist()[0])[self.energy])
        self.Gx = self.G * np.mat(np.diag(self.x.reshape(-1).tolist()[0])).I
        self.alpha = self.Gx * self.L
        self.delta = self.Gx * self.A
        self.g = self.alpha * self.f