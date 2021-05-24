from tensorflow import keras
from data_preprocessor import Data_preprocessor
from data_reader import Data_reader
import numpy as np
import os

class Predictor(object):
    """docstring for Predictor"""
    def __init__(self):
        self.model_note = keras.models.load_model("model/note.h5")
        self.model_pitch = keras.models.load_model("model/pitch.h5")
        self.model_duration = keras.models.load_model("model/duration.h5")
        self.dp = Data_preprocessor()
        # self.dr = Data_reader()
        return


    def load_data(self, path, contrast_rate, line_rate):
        res = self.dp.data_preprocess(self.dp.load_img(path), contrast_rate, line_rate) #
        print(len(res))
        data = np.zeros((len(res), 40, 40, 3))
        for i in range(len(res)):
            data[i] = self.dp.constrain_img_size(res[i])
        return data


    def predict(self, path, path_save='[乐谱播放]\\MusicPlayer\\sheet\\', file_name="new", contrast_rate=0.5, line_rate=0.2):
        data = self.load_data(path, contrast_rate, line_rate)
        print(data.shape)
        if len(data.shape) < 4:
            data.reshape((1, 40, 40, 3))
        y_note = np.argmax(self.model_note.predict(data), 1)
        y_pitch = np.argmax(self.model_pitch.predict(data), 1)
        y_duration = np.argmax(self.model_duration.predict(data), 1)
        result = self.generate_result(y_note, y_pitch, y_duration)
        file = open(path_save + file_name + '.sht', 'w')
        file.write("D 4 4 144\n")
        file.write(result)
        file.close()

        return result



    def generate_result(self, note, pitch, duration):
        res = ""
        for i in range(len(note)):
            res += self.parse_note(note[i])
            if note[i] < 8:
                res += self.parse_pitch(pitch[i])
            res += self.parse_duration(duration[i])
        return res


    def parse_note(self, note):
        if (note <= 7 and note >= 0):
            return " " + str(note)
        elif note == 8:
            return " |"
        elif note == 9:
            return "."
        elif note == 10:
            return "-"


    def parse_duration(self, duration):
        if duration <= 1:
            return ""
        else:
            return (duration - 1) * "_"


    def parse_pitch(self, pitch):
        return str(5 - pitch)
