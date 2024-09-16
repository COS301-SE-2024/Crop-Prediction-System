from ML import ML

# * Fusion Model Information
# This model aims to fuse a few models together by bringing in different models and ensembling them together. This is the "final model" in the range of models that aims to take the best of each model and merge it into one consistent model that can evaluate, train, and predict on demand. Some features of this evaluation include rejecting values that are outside a confidence level to ensure consistency in the data.

# Later on with the sensor, additional models can be "fused" onto this model to make sensor-specific predictions.

class FusionModel(ML):
    def train(self):
        pass

    def predict(self, data):
        pass

    def prepare(self):
        pass

    def evaluate(self):
        pass

if __name__ == '__main__':
    fm = FusionModel()