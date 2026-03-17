import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split

def preprocess_data(path):

    df = pd.read_csv(path)

    df = df.dropna()

    label_cols = [
        "Smoking",
        "Alcohol",
        "Stroke",
        "Sex",
        "Diabetic",
        "PhysicalActivity",
        "Age_Category"
    ]

    le = LabelEncoder()

    for col in label_cols:
        df[col] = le.fit_transform(df[col])

    X = df.drop("Attack_Label", axis=1)
    y = df["Attack_Label"]

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    X_scaled = X_scaled.reshape(
        X_scaled.shape[0],
        1,
        X_scaled.shape[1]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.2,
        random_state=42
    )

    return X_train, X_test, y_train, y_test