import numpy as np
from keras.models import load_model
from cancers.cancer import BaseCancer


class BrainCancer(BaseCancer):
    def __init__(self):
        self.model = load_model("models/Brain_Tumor.h5")
        print("Brain cancer Model loaded!")

    def get_classes(self) -> list[str]:
        return ["Glioma Tumor","The model predicts that there is no tumor","Meningioma Tumor","Pituitary Tumor"]

    def get_model(self):
        return self.model;

    def preprocess_image(self, img):
        return img.reshape(1,150,150,3)

    def predict(self, img):
        processed_image = self.preprocess_image(img)
        return self.get_classes()[np.argmax(self.model.predict(processed_image), axis=1)[0]]

    def get_target_size(self):
        return (150,150)
