import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import pickle

# Load the dataset
df = pd.read_csv('crop_data.csv')

# Define features and target
X = df[['temperature', 'rainfall', 'ph', 'nitrogen', 'phosphorus', 'potassium', 'soil_type', 'season']]
y = df['crop']

# Create a preprocessor to handle categorical features
# 'soil_type' and 'season' are categorical. The rest are numerical.
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['soil_type', 'season'])
    ],
    remainder='passthrough' # Keep the numerical columns as they are
)

# Create the model pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
model_pipeline.fit(X, y)

# Save the trained model pipeline
with open('crop_model.pkl', 'wb') as f:
    pickle.dump(model_pipeline, f)

print("Model trained with soil_type and season, and saved as crop_model.pkl")
