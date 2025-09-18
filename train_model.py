import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the dataset
df = pd.read_csv('crop_data.csv')

# Prepare the data
X = df[['temperature', 'rainfall', 'ph', 'nitrogen', 'phosphorus', 'potassium']]
y = df['crop']

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the trained model
with open('crop_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as crop_model.pkl")
