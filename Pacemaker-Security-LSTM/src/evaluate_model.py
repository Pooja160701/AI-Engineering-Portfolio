import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import load_model
from preprocessing import preprocess_data
import numpy as np

X_train, X_test, y_train, y_test = preprocess_data("../data/pacemaker_dataset.csv")

model = load_model("../models/pacemaker_lstm_model.h5")

pred = model.predict(X_test)

pred = np.argmax(pred, axis=1)

cm = confusion_matrix(y_test, pred)

sns.heatmap(cm, annot=True)

plt.savefig("../results/confusion_matrix.png")

print(classification_report(y_test, pred))