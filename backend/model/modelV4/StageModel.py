from ML import ML

# * Stage Model Information
# This model builds on the previously deployed model by grouping data into crop growing stages (sowing, tillering, heading, etc.) and then predicts the sequence in the given timeframe.

# Known disadvantages: cumulative variables are low at the start of a stage, causing concerningly low predictions from a farmer's perspective.

class StageModel(ML):
    def train(self):
        pass

    def predict(self, data):
        pass

    def prepare(self):
        pass

    def evaluate(self):
        pass

if __name__ == '__main__':
    fm = StageModel()