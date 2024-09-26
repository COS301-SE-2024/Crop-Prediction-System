from backend.model.ML import ML
from backend.model.MultiScaleModel import MultiScaleModel
from backend.model.StageModel import StageModel
from backend.model.YieldOnlyModel import YieldOnlyModel
from backend.definitions.crop import Crop
import numpy as np
import copy
import time
import matplotlib.pyplot as plt

# * Fusion Model Information
# This model aims to fuse a few models together by bringing in different models and ensembling them together. This is the "final model" in the range of models that aims to take the best of each model and merge it into one consistent model that can evaluate, train, and predict on demand. Some features of this evaluation include rejecting values that are outside a confidence level to ensure consistency in the data.

# Later on with the sensor, additional models can be "fused" onto this model to make sensor-specific final_predictions.

class FusionModel(ML):
    def __init__(self, X, y, c, field_id = None):
        super().__init__(X, y)
        self.X = self.historical_data
        self.y = self.yield_data
        self.crop = c

        self.msm = MultiScaleModel(copy.deepcopy(self.X), self.y)
        self.sm = StageModel(copy.deepcopy(self.X), self.y, self.crop)
        self.yom = YieldOnlyModel(copy.deepcopy(self.y))

        self.bestModel = None

        self.inStage = True

    def train(self) -> dict:
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
            "training_time_s": str(duration),
            "prediction": prediction
        }

    def predict(self):
        # Perform ensemble prediction by averaging the final_predictions of the models
        # Reject if the prediction is outside a confidence level of the YieldOnlyModel
        msm_pred = self.msm.predict()
        yom_pred = self.yom.predict()

        # Average the predictions
        predictions = []
        for p in msm_pred:
            predictions.append(p)

        final_predictions = []
        # average final_predictions in i
        for i in range(len(predictions[0])):
            sum = 0
            for j in range(len(predictions)):
                sum += predictions[j][i]
            final_predictions.append(sum / len(predictions))
        
        sm_pred = None
        if self.inStage:
            sm_pred = self.sm.predict()[0]

        # Get the average of the last 10 years
        yom_last_5_years = yom_pred[-10:]
        mean = np.mean(yom_last_5_years)

        # Compute confidence interval
        # confidence_level = 0.99
        confidence_interval = 2.575 * np.std(yom_last_5_years) / np.sqrt(5)
        ci_upper = mean + confidence_interval
        ci_lower = mean - confidence_interval

        for i in range(len(final_predictions)):
            if final_predictions[i] > ci_upper or final_predictions[i] < ci_lower:
                if sm_pred is not None and (sm_pred <= ci_upper and sm_pred >= ci_lower):
                    final_predictions[i] = sm_pred
                else:
                    final_predictions[i] = mean
            else:
                if sm_pred is not None:
                    final_predictions[i] = (final_predictions[i] + sm_pred) / 2
                else:
                    final_predictions[i] = (final_predictions[i] + mean) / 2

        # Plot
        # plt.figure(figsize=(10, 6))
        # plt.plot(final_predictions, label='Prediction', color='red', linestyle='dashed')
        # plt.xlabel('Index')
        # plt.ylabel('Value')
        # plt.title('Model final_predictions vs Actual Values')
        # plt.legend()
        # plt.show()

        return final_predictions

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
    