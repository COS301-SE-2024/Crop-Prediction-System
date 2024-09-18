from backend.model.ML import ML
from backend.model.MultiScaleModel import MultiScaleModel
from backend.model.StageModel import StageModel
from backend.model.YieldOnlyModel import YieldOnlyModel
from backend.definitions.crop import Crop
import numpy as np

# import timer
import time

# * Fusion Model Information
# This model aims to fuse a few models together by bringing in different models and ensembling them together. This is the "final model" in the range of models that aims to take the best of each model and merge it into one consistent model that can evaluate, train, and predict on demand. Some features of this evaluation include rejecting values that are outside a confidence level to ensure consistency in the data.

# Later on with the sensor, additional models can be "fused" onto this model to make sensor-specific predictions.

class FusionModel(ML):
    def __init__(self, X, y, c):
        super().__init__(X, y)
        self.X = self.historical_data
        self.y = self.yield_data
        self.crop = c

        self.msm = MultiScaleModel(self.X, self.y)
        self.sm = StageModel(self.X, self.y, self.crop)
        self.yom = YieldOnlyModel(self.y)

        self.bestModel = None

        self.inStage = True

    def train(self):
        # Train each model in the ensemble
        start = time.time()

        msm_rmse = self.msm.train()
        sm_rmse = self.sm.train()
        yom_rmse = self.yom.train()

        end = time.time()

        if sm_rmse is None:
            self.inStage = False

        duration = end - start

        prediction = self.predict()

        return {
            "MultiScaleModel": msm_rmse,
            "StageModel": sm_rmse,
            "YieldOnlyModel": yom_rmse,
            "duration": str(duration) + " seconds",
            "prediction": prediction
        }

    def predict(self):
        # Perform ensemble prediction by averaging the predictions of the models
        # Reject if the prediction is outside a confidence level of the YieldOnlyModel
        msm_pred = self.msm.predict()
        yom_pred = self.yom.predict()

        # Average the predictions
        predictions = []
        for p in msm_pred:
            predictions.append(p)
        
        if self.inStage:
            sm_pred = self.sm.predict()
            predictions.append(sm_pred)

        # This year prediction
        latestPredictions = []
        for p in predictions:
            latestPredictions.append(p[-1])

        avg_pred = np.mean(latestPredictions)

        # Get the average of the last 5 years
        yom_last_5_years = yom_pred[-5:]

        # Compute confidence interval
        confidence_level = 0.95
        confidence_interval = 1.96 * np.std(yom_last_5_years) / np.sqrt(5)
        ci_upper = avg_pred + confidence_interval
        ci_lower = avg_pred - confidence_interval

        if avg_pred < ci_lower or avg_pred > ci_upper:
            avg_pred = yom_pred # pick the YieldOnlyModel prediction if the ensemble prediction is outside the confidence level
        
        return avg_pred

    def prepare(self):
        pass

    def evaluate(self):
        pass

# if __name__ == '__main__':
#     # Define some crop
#     c = Crop(
#         name="wheat",
#         t_base=5.0, 
#         stages={
#             "sowing": {"day": 111},
#             "germination": {"day": 151},
#             "tillering": {"day": 182},
#             "heading": {"day": 243},
#             "maturity": {"day": 304}
#         }
#     )

#     fm = FusionModel(c)
#     fm.train()
    