import os
import pickle
import numpy as np

import cv2
import mediapipe as mp

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Initialize MediaPipe Hands solution
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Create a Hands object with static image mode and a minimum detection confidence of 0.3
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Directory where the data is stored
DATA_DIR = './data'

# Initialize lists to hold data and labels
data = []
labels = []

# Loop through each directory in the data directory
for dir_ in os.listdir(DATA_DIR):
    # Loop through each image in the current directory
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        data_aux = []  # Temporary list to hold the landmarks for the current image

        x_ = []  # List to hold x-coordinates of landmarks
        y_ = []  # List to hold y-coordinates of landmarks

        # Read the image using OpenCV
        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        # Convert the image from BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the image to detect hands
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            # Loop through each detected hand
            for hand_landmarks in results.multi_hand_landmarks:
                # Loop through each landmark in the hand
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    # Append the x and y coordinates to their respective lists
                    x_.append(x)
                    y_.append(y)

                # Normalize the landmarks by subtracting the minimum x and y values
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            # Append the normalized landmarks to the data list
            data.append(data_aux)
            # Append the label (directory name) to the labels list
            labels.append(dir_)

# Convert the data and labels lists to numpy arrays
data = np.asarray(data)
labels = np.asarray(labels)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Initialize the RandomForestClassifier
model = RandomForestClassifier()

# Train the model on the training data
model.fit(x_train, y_train)

# Predict the labels for the test data
y_predict = model.predict(x_test)

# Calculate the accuracy of the model
score = accuracy_score(y_predict, y_test)

# Print the accuracy of the model
print('{}% of samples were classified correctly !'.format(score * 100))

# Save the trained model to a file using pickle
f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()