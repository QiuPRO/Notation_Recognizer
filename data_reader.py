from csv import reader
import numpy as np
from data_preprocessor import Data_preprocessor

class Data_reader(object):
    """docstring for Data_reader"""
    def __init__(self, img_cnt=987, img_width=40, img_height=40):
        self.dp = Data_preprocessor()
        self.img_cnt = img_cnt
        self.img_width = img_width
        self.img_height = img_height
        return

    def read_img(self, path):
        X = np.zeros((self.img_cnt, self.img_width, self.img_height, 3))
        for i in range(self.img_cnt):
            X[i] = self.dp.dec_noise(self.dp.load_img(path + str(i) + ".png"), 0.6)
        return X


    def read_label(self, path):
        _, data = self.read_csv(path)
        y = data[:, 2]
        note = []
        pitch = []
        duration = []
        for i in range(len(y)):
            tmp = eval(y[i])
            note.append(self.num_note(tmp["note"]))
            pitch.append(self.num_pitch(tmp["pitch"]))
            duration.append(self.num_duration(tmp["duration"]))
        return np.array(note), np.array(pitch), np.array(duration)


    def read_csv(self, path):
        with open(path, 'rt', encoding='UTF-8') as raw_data:
            readers = reader(raw_data,delimiter=',')
            x = list(readers)
            data = np.array(x)
        return data[0], data[1:]


    # def cnt_labels_rate(self, y):
    # cnt = []
    # for i in range(len(set(y))):
    #     cnt.append((y == i).sum() / y.shape[0])
    # return cnt


    def num_note(self, note):
        if note < "8" and note >= "0":
            return eval(note)
        elif note == "|":
            return 8
        elif note == "dot":
            return 9
        elif note == "line":
            return 10
        
    def num_pitch(self, pitch):
        if pitch == "high":
            return 0
        elif pitch == "normal":
            return 1
        elif pitch == "low":
            return 2
        
    def num_duration(self, duration):
        if duration == "0":
            return 0
        elif duration == "4":
            return 1
        elif duration == "8":
            return 2
        elif duration == "16":
            return 3