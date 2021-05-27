## Notation Recognizer

### 1. Intro

In this project, I realized a way to separate a notation into figures of notes then use models to "sing".

### 2. To Run

#### 2.1 Recognizing

First, you need ensure your recognizing picture's file format is ".png". Second, import class Predictor and pass your picture to function predict. A typical use of this class is shown as below:

```python
from predictor import Predictor
predictor = Predictor()
predictor.predict("path/name.png")
```

The function predict offers 5 adjustable arguments:

```python
path                                         # path of the picture to deal with
path_save='[乐谱播放]\\MusicPlayer\\sheet\\'  # path of output 
file_name="new"								 # output file's name
contrast_rate=0.5							# adjustable arg decided by environment light situation
line_rate=0.2								# adjustable arg for tie line height.
```

After calling the function, you will get a file end with 't', composed by each note's pitch and duration. You can use the vs solution in MusicPlayer.zip to listen the music produced by my models.

#### 2.2 Retrain a model

If you are not satisfied in using my models, you can also train your own models. 

Firstly,  use data_preprocessor to cut whole notation into many notes then label your data, as I have uploaded my training data, you can also use it to train.

Secondly, I uploaded a effective tool named "data_splitter", which could separate the input data set and it's labels into specified scale training set, valid set and test set, and guaranteed the valid set and test have the same distribution as the whole data set.

Then use Tensorflow or Pytorch or any frame you are familiar to train a better model.