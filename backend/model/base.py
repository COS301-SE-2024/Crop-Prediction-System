from backend.model.predict import predict
from backend.model.cropHealth import calculateHealth

class MLModel:
    def __init__(self):
        pass

    def predict(self, data, crop, hectare):
        return predict(data, crop, hectare)
    
    def calculateHealth(self, crop, n):
        return calculateHealth(None, crop, n)

