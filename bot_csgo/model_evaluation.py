from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

accuracy = []


def create_model() -> DecisionTreeRegressor:
    data = pd.read_csv('suren2.csv')
    y = data.win
    features = ['teamA', 'teamB', 'kefA', 'kefb']
    X = data[features]
    train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=1, random_state=1)
    model = DecisionTreeRegressor(random_state=1)
    model.fit(train_X, train_y)
    for i in val_X.iterrows():
        for jz in val_y:
            if model.predict([[int(i[1][0]), int(i[1][1]), float(i[1][2]), float(i[1][3])]]) == jz:
                accuracy.append(1)
            else:
                accuracy.append(0)
            break
    print(f'{round(accuracy.count(1) / len(accuracy) * 100)}% winrate SurenNET by VORONBETS OAO')


create_model()
