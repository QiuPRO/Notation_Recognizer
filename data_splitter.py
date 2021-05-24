import numpy as np
class Data_splitter(object):
    """docstring for Data_splitter"""
    def __init__(self):
        return


    def auto_split_data(self, num_valid, num_test, X, y):
        l = len(set(y))
        standard = self.cnt_labels_rate(y, l)
        # 首先分割出验证集
        valid_pre = self.lowest_square_idx(num_valid, y, l, standard)
        # print(valid_pre)
        # 分割
        X_valid = X[valid_pre:valid_pre+num_valid]
        y_valid = y[valid_pre:valid_pre+num_valid]
        # 分割后剩下的y合并
        y_ = np.r_[y[:valid_pre], y[valid_pre+num_valid:]]
        # 测试集
        test_pre = self.lowest_square_idx(num_test, y_, l, standard)
        # print(test_pre)
        if (test_pre >= valid_pre):
            test_pre += num_valid
            test_bck = test_pre + num_test
        elif (test_pre + num_test > valid_pre):
            test_bck = num_valid + num_test + test_pre
        # print(test_pre)
        X_test = X[test_pre:test_bck]
        y_test = y[test_pre:test_bck]
        X_train, y_train = self.split_train(valid_pre, test_pre, num_valid, num_test, X, y)
        return X_train, X_valid, X_test, y_train, y_valid, y_test


    # 分割训练集
    def split_train(self, valid_pre, test_pre, num_valid, num_test, X, y):
        if test_pre >= valid_pre:
            pre_l = test_pre
            pre_s = valid_pre
            num_l = num_test
            num_s = num_valid
        elif (test_pre + num_test > valid_pre):
            X_train = np.r_[X[:test_pre], X[num_valid + num_test + test_pre:]]
            y_train = np.r_[y[:test_pre], y[num_valid + num_test + test_pre:]]
            return X_train, y_train
        else:
            pre_s = test_pre
            pre_l = valid_pre
            num_l = num_valid
            num_s = num_test
        X_train = np.r_[np.r_[X[:pre_s], X[pre_s+num_s:pre_l]], X[pre_l+num_l:]]
        y_train = np.r_[np.r_[y[:pre_s], y[pre_s+num_s:pre_l]], y[pre_l+num_l:]]
        return X_train, y_train


    # 均方值最小的下标
    def lowest_square_idx(self, num, y, l, standard):
        square = np.zeros(len(y) - num)
        for i in range(len(y) - num):
            # 计算与标准方差最小的一组数据
            w = (self.cnt_labels_rate(y[i:i + num], l) - standard)
            square[i] = w.dot(w.T)
        # 找到最小值的下标
        pre = np.argwhere(square == min(square))[0][0]
        return pre


    # 计算当前数据的分布比例
    def cnt_labels_rate(self, y, l):
        cnt = np.zeros(l)
        for i in range(l):
            cnt[i] = (y == i).sum() / y.shape[0]
        return cnt