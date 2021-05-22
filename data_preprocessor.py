import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import math

from PIL import Image


class Data_preprocessor(object):
    """docstring for data_preprocessor"""
    def __init__(self):
        # self.contrast_rate = contrast_rate
        # self.line_rate = line_rate
        

    def data_preprocess(self, img, contrast_rate = 0.5, line_rate = 0.2):
        # 降噪
        img = self.dec_noise(img, contrast_rate)
        # 将一页曲谱裁成一行
        res_line = self.cnt_line(img)

        res = []
        # 将一行曲谱裁剪成单个音符
        for item in res_line:
            res += self.cut_note(item, line_rate)
        return res


    # 加载图片
    def load_img(self, pos):
        img = (plt.imread(pos)).astype(np.float64)
        return img


    # 保存数据
    def save_preprocessed_data(self, res, pos="", constrain_img_size=False, width=40, height=40):
        if constrain_img_size:
            for i in range(len(res)):
                img = self.cut_down_border(res[i])
                img = self.zero_padding(img)
                Image.fromarray((img * 255).astype('uint8')).resize((width, height)).save(pos + str(i) + ".png")
        else:
            for i in range(len(res)):
                Image.fromarray(np.uint8(cut_down_border(res[i]) * 255)).save(pos + str(i) + ".png")


    def dec_noise(self, img, contrast_rate = 0.65):
        img[img >= contrast_rate] = 1
        img[img < contrast_rate] = 0
        return img


    # 将一行曲谱裁成音符
    def cut_note(self, img, line_rate = 0.2):
        # 裁去上下白色多余部分
        img = img[(img.sum(1).sum(1) / img.shape[2] / img.shape[1]) != 1]
        # 去掉连音线
    #     tmp = img[:, (img.sum(2).sum(0) / img.shape[2] / img.shape[0]) != 1]
    #     if ((tmp.sum(1).sum(1) / tmp.shape[2] / tmp.shape[1])[:int(tmp.shape[0] * 0.2)].sum() / int(tmp.shape[0] * 0.2) > 0.95):
        img = img[int(img.shape[0] * line_rate):]
        # 开始裁切
        i = 0
        pre_i = 0
        flag = 0
        cmp = img.sum(2).sum(0) / img.shape[0] / img.shape[2]
        cmp2 = (img.sum(2) / img.shape[2])[int(img.shape[0] * 0.7):].sum(0) / (img.shape[0] - int(img.shape[0] * 0.7))
        cmp3 = (img.sum(2) / img.shape[2])[:int(img.shape[0] * 0.7)].sum(0) / int(img.shape[0] * 0.7) 
        res = []
        while i < img.shape[1]:
            if (cmp[i] > 0.94 or cmp3[i] > 0.995):
                if (flag == 1):
                    flag = 0
                    res.append(img[:, pre_i:i])
            elif (cmp2[i] > 0.7 or cmp3[i] < 0.93): # 面没有双下划线, 或上面有东西
                if (flag == 0):
                    flag = 1
                    pre_i = i
            i += 1
        return res

        
    # 将一页曲谱裁成多行
    def cnt_line(self, img):
        i = 0
        pre_i = 0
        cmp = img.sum(2).sum(1) / img.shape[2] / img.shape[1]
        flag = 0
        res = []
        while i < img.shape[0]:
            if (cmp[i] >= 1):
                if (flag == 1):
                    flag = 0
                    if (i - pre_i > 30):
                        res.append(img[pre_i:i])
            else:
                if (flag == 0):
                    flag = 1
                    pre_i = i
            i += 1
        return res


    # 添加白色边界至1：1
    def zero_padding(self, x):
        width = x.shape[1]
        height = x.shape[0]
        if height > width:
            total_width = height
            pad_left = int((total_width - width) / 2)
            pad_right = total_width - width - pad_left
            x_pad = np.pad(x, ((1, 1), (pad_left, pad_right), (0, 0)), mode='constant', constant_values=1)
        else:
            total_heigth = width
            pad_up = int((total_heigth - height) / 2)
            pad_down = total_heigth - height - pad_up
            x_pad = np.pad(x, ((pad_up, pad_down), (1, 1), (0, 0)), mode='constant', constant_values=1)
        return x_pad


    def constrain_img_size(self, img, width=60, height=60):
        img = self.cut_down_border(img)
        img = self.zero_padding(img)
        img = Image.fromarray((img * 255).astype('uint8'))
        img = img.resize((width, height))
        img = np.array(img)
        return img


    def cut_down_border(self, img):
        length = img.shape[0]
        cmp = img.sum(2).sum(1) / img.shape[2] / img.shape[1]
        for i in range(0, length - 1):
            if cmp[i] != 1:
                head = i
                break
        for i in range(0, length):
            if cmp[length - 1 - i] != 1:
                tail = length - 1 - i
                break
        return img[head: tail]