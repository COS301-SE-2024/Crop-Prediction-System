from ML import ML
from MultiScaleModel import MultiScaleModel
from StageModel import StageModel, Crop
from YieldOnlyModel import YieldOnlyModel
import numpy as np

# * Fusion Model Information
# This model aims to fuse a few models together by bringing in different models and ensembling them together. This is the "final model" in the range of models that aims to take the best of each model and merge it into one consistent model that can evaluate, train, and predict on demand. Some features of this evaluation include rejecting values that are outside a confidence level to ensure consistency in the data.

# Later on with the sensor, additional models can be "fused" onto this model to make sensor-specific predictions.

class FusionModel(ML):
    def __init__(self, crop):
        super().__init__()

        self.msm = MultiScaleModel()
        self.sm = StageModel(crop)
        self.yom = YieldOnlyModel()

    def train(self):
        # Train each model in the ensemble
        print(self.msm.train())
        print(self.sm.train())
        print(self.yom.train())

    def predict(self, data):
        # Perform ensemble prediction by averaging the predictions of the models
        # Reject if the prediction is outside a confidence level of the YieldOnlyModel

        msm_pred = self.msm.predict(data)
        sm_pred = self.sm.predict(data)
        yom_pred = self.yom.predict(data)

        # Average the predictions
        predictions = []
        for p in msm_pred:
            predictions.append(p)
        
        predictions.append(sm_pred)

        avg_pred = sum(predictions) / len(predictions)

        # Compute confidence interval
        # confidence_level = 0.95
        confidence_interval = 1.96 * (self.yield_data['yield'].std() / np.sqrt(len(self.yield_data)))
        ci_upper = avg_pred + confidence_interval
        ci_lower = avg_pred - confidence_interval

        if yom_pred < ci_lower or yom_pred > ci_upper:
            avg_pred = yom_pred # pick the YieldOnlyModel prediction if the ensemble prediction is outside the confidence level
        
        return avg_pred

    def prepare(self):
        pass

    def evaluate(self):
        pass

if __name__ == '__main__':
    # Define some crop
    c = Crop(
        name="wheat",
        t_base=5.0, 
        stages={
            "sowing": {"day": 111},
            "germination": {"day": 151},
            "tillering": {"day": 182},
            "heading": {"day": 243},
            "maturity": {"day": 304}
        }
    )

    fm = FusionModel(c)
    fm.train()
    