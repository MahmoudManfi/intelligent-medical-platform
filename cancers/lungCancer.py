import numpy as np
from tensorflow.keras.preprocessing import image
from keras.models import load_model
from cancers.cancer import BaseCancer


class LungCancer(BaseCancer):
    def __init__(self):
        self.model = load_model("models/modelcancerlung.h5", compile=False)
        print("lung cancer Model loaded!")

    def get_classes(self) -> list[str]:
        return ["AdenocarcinomaChest Lung Cancer ","Large cell carcinoma Lung Cancer" , "NO Lung Cancer/ NORMAL" , "Squamous cell carcinoma Lung Cancer"]

    def get_model(self):
        return self.model;

    def preprocess_image(self, img):
        x = image.img_to_array(img)
        x=x/255
        x=np.expand_dims(x,axis=0)
        return x

    def predict(self, img):
        processed_image = self.preprocess_image(img)
        return self.get_classes()[np.argmax(self.get_model().predict(processed_image))]

    def get_target_size(self):
        return (224,224)
