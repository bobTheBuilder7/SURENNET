import pandas as pd
from sklearn.tree import DecisionTreeRegressor


def create_model() -> DecisionTreeRegressor:
    data = pd.read_csv('suren2.csv')
    y = data.win
    features = ['teamA', 'teamB', 'kefA', 'kefb']
    X = data[features]
    model = DecisionTreeRegressor()
    model.fit(X, y)
    return model
