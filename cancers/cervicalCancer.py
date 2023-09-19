import numpy as np
from tensorflow.keras.preprocessing import image
from keras.models import load_model
from cancers.cancer import BaseCancer


class CervicalCancer(BaseCancer):
    def __init__(self):
        self.model = load_model("models/cervical_cancer_best_model.hdf5", compile=False)
        print("cervical cancer Model loaded!")

    def get_classes(self) -> list[str]:
        return ["Dyskeratotic","Koilocytotic","Metaplastic","Parabasal","Superficial-Intermediate"]

    def get_model(self):
        return self.model;

    def preprocess_image(self, img):
        norm_img = image.img_to_array(img)/255
        return np.array([norm_img])

    def predict(self, img):
        processed_image = self.preprocess_image(img)
        return self.get_classes()[np.argmax(self.model.predict(processed_image))]

    def get_target_size(self):
        return (64,64)
