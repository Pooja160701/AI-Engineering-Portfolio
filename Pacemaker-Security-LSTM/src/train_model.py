from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from preprocessing import preprocess_data

X_train, X_test, y_train, y_test = preprocess_data("../data/pacemaker_dataset.csv")

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

model = Sequential()

model.add(LSTM(100, return_sequences=True, input_shape=(1, X_train.shape[2])))
model.add(Dropout(0.2))

model.add(LSTM(50))
model.add(Dropout(0.2))

model.add(Dense(32, activation='relu'))

model.add(Dense(4, activation='softmax'))

model.compile(
    loss="categorical_crossentropy",
    optimizer="adam",
    metrics=["accuracy"]
)

history = model.fit(
    X_train,
    y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2
)

model.save("../models/pacemaker_lstm_model.h5")