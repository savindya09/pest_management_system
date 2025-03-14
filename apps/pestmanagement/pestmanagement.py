import cv2 as cv
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

# Load Pest Detection Model
model = tf.keras.models.load_model('apps/pestmanagement/artifacts/pests.h5')

model.compile(
    optimizer='Adam',
    loss='categorical_crossentropy',
    metrics=[
        tf.keras.metrics.CategoricalAccuracy(name='accuracy'),
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall'),
        tf.keras.metrics.AUC(name='auc')
    ]
)

def preprocessing_function(img):
    """
    Preprocess an image for the pest detection model.
    """
    return tf.keras.applications.xception.preprocess_input(img)

import os
import pandas as pd

def get_remedies(pest):
    """
    Retrieve pest-specific harms and remedies from an Excel sheet.
    """
    # Dynamically locate the 'data' folder inside your project
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current directory
    remedies_path = os.path.join(base_dir, '..', 'pestmanagement', 'data', 'pest management.xlsx')

    # Ensure the file exists before attempting to read
    if not os.path.exists(remedies_path):
        return {"error": "Remedies file not found", "file_path": remedies_path}

    try:
        # Load the Excel file using openpyxl (ensure you have openpyxl installed)
        df = pd.read_excel(remedies_path, engine='openpyxl')
        
        # Drop empty rows (if any)
        df.dropna(how='all', inplace=True)

        # Ensure 'Pests' column exists
        if 'Pests' not in df.columns:
            return {"error": "Invalid file format - 'Pests' column missing"}

        # Fill missing pest names (forward fill)
        df['Pests'].fillna(method='ffill', inplace=True)
        df['Pests'] = df['Pests'].astype(str).str.lower().str.strip()

        # Find the remedies for the specified pest
        pest_data = df[df['Pests'] == pest.lower().strip()]

        # Ensure 'Harms' and 'Solution' columns exist
        if 'Harms' not in df.columns or 'Solution' not in df.columns:
            return {"error": "Invalid file format - Required columns missing"}

        return {
            "pest": pest,
            "harms": pest_data['Harms'].dropna().tolist(),
            "remedies": pest_data['Solution'].dropna().tolist()
        }

    except Exception as e:
        return {"error": f"Failed to read Excel file: {str(e)}"}

def inference_pests(image_path):
    """
    Detects the pest from an image and returns pest name, probability, harms, and remedies.
    """
    pest_dict = {
        0: 'ants', 1: 'bees', 2: 'beetle', 3: 'catterpillar',
        4: 'earthworms', 5: 'earwig', 6: 'grasshopper', 7: 'moth',
        8: 'slug', 9: 'snail', 10: 'wasp', 11: 'weevil'
    }
    
    # Read and preprocess image
    image = cv.imread(image_path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = cv.resize(image, (299, 299))
    image = np.expand_dims(image, axis=0)
    image = preprocessing_function(image)
    
    # Make prediction
    prediction = model.predict(image)
    prob = f"{np.max(prediction) * 100:.2f} %"
    label = pest_dict[np.argmax(prediction)]
    
    # Get remedies
    remedies = get_remedies(label)
    remedies["probability"] = prob
    return remedies
