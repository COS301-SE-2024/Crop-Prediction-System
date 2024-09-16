from ML import ML

# * Yield Only Model Information
# This model aims to predict yield purely by means of historic yield data, and doesn't take into account any weather or crop-specific data. The aim of this model is for pure evaluation and prevention of inaccurate predictions. The fusion model will use the confidence level of the Yield Only Model to determine if other model predictions in the ensemble were sound or not.

class YieldOnlyModel(ML):
    def train(self):
        pass

    def predict(self, data):
        pass

    def prepare(self):
        pass

    def evaluate(self):
        pass

if __name__ == '__main__':
    fm = YieldOnlyModel()