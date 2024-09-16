from ML import ML

# * BiWeekToDate Model Information
# This model aims to develop a sequence of data from biweekly averages and cumulations from the start of the year to the given timeframe in a biweekly dataset. This way the model can sense the current progress to either a good or a bad season - and consequently a good or a bad harvest.

# Straight up disadvantages: the model might be ineffective towards the start of the year, but can perform later in the year as it accumulates new data.

class BiWeekToDateModel(ML):
    def train(self):
        pass

    def predict(self, data):
        pass

    def prepare(self):
        pass

    def evaluate(self):
        pass

if __name__ == '__main__':
    fm = BiWeekToDateModel()