from sklearn.base import BaseEstimator


class CustomEncoder(BaseEstimator):
    def __init__(self):
        pass

    def fit(self, documents, y=None):
        return self

    def transform(self, x_dataset):
        # nb_of_runs
        x_dataset["Unpopular"] = x_dataset["nb_of_runs"].apply(
            lambda x: 1 if x <= 3 else 0
        )
        x_dataset["Somehow_Popular"] = x_dataset["nb_of_runs"].apply(
            lambda x: 1 if x > 3 and x <= 7 else 0
        )
        x_dataset["Popular"] = x_dataset["nb_of_runs"].apply(
            lambda x: 1 if x > 7 and x <= 19 else 0
        )
        x_dataset["Very_Popular"] = x_dataset["nb_of_runs"].apply(
            lambda x: 1 if x > 19 else 0
        )

        # age
        x_dataset["Young"] = x_dataset["age"].apply(lambda x: 1 if x <= 21 else 0)
        x_dataset["Somehow_Old"] = x_dataset["age"].apply(
            lambda x: 1 if x > 21 and x <= 28 else 0
        )
        x_dataset["Old"] = x_dataset["age"].apply(
            lambda x: 1 if x > 28 and x <= 31 else 0
        )
        x_dataset["Very_Old"] = x_dataset["age"].apply(lambda x: 1 if x > 31 else 0)

        # coding time to a categorical variable
        x_dataset["Short"] = x_dataset["time"].apply(lambda x: 1 if x <= 664.833 else 0)
        x_dataset["Somehow_Long"] = x_dataset["time"].apply(
            lambda x: 1 if x > 664.833 and x <= 1226 else 0
        )
        x_dataset["Long"] = x_dataset["time"].apply(
            lambda x: 1 if x > 1226 and x <= 2315 else 0
        )
        x_dataset["Very_Long"] = x_dataset["time"].apply(lambda x: 1 if x > 2315 else 0)

        return x_dataset
