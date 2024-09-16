from ML import ML

# * Multi-Scale Model Information
# This model aims to experiment with the same data on different frequencies (i.e. daily, monthly, yearly) and then let the models act as an ensemble model by taking the average output between n models.

class MultiScaleModel(ML):
    def train(self):
        pass

    def predict(self, data):
        pass

    def prepare(self):
        pass

    def evaluate(self):
        pass

if __name__ == '__main__':
    fm = MultiScaleModel()