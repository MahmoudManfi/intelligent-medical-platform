class BaseCancer:
    def get_classes(self) -> list[str]:
        pass

    def get_model(self):
        pass

    def preprocess_image(self, img):
        pass

    def predict(self, img):
        pass

    def get_target_size(self):
        pass