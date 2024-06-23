from model.predict import predict
from model.cropHealth import calculateHealth

class MLModel:
    def __init__(self):
        pass

    def predict(self, data, crop, hectare):
        val = predict(data, crop, hectare)
        print(val)
        return val
    
    def calculateHealth(self, crop, n):
        val = calculateHealth(None, crop, n)

        print(val)
        
        # Change all "" to '' for JSON compatibility
        val = str(val).replace('"', "'")

        # Convert to dictionary
        val = eval(val)

        return val

