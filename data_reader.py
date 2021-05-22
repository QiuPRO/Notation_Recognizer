from csv import reader
import numpy as np
from data_preprocessor import Data_preprocessor

class Data_reader(object):
    """docstring for Data_reader"""
    def __init__(self, arg):
        dp = Data_preprocessor()

    def read_img(self, path):
        for i in range(len(res)):
            X[i] = dp.load_img(path + str(i) + ".png")


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