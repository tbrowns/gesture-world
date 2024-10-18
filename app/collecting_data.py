import os
import cv2
import tkinter as tk
from tkinter import simpledialog
import time

# Define the directory where the data will be stored
DATA_DIR = './data'

# Check if the data directory exists, if not, create it
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Define the number of classes and the size of the dataset for each class
number_of_classes = 5
dataset_size = 100

# Initialize the video capture object to capture video from the default camera (usually the first camera)
cap = cv2.VideoCapture(0)

# Initialize the Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Loop over the number of classes
for j in range(number_of_classes):
    # Prompt the user to enter the name of the subdirectory
    class_name = simpledialog.askstring("Input", f"Enter the name for class {j+1}:")

    # Create a subdirectory for each class if it doesn't already exist
    class_dir = os.path.join(DATA_DIR, class_name)
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print(f'Collecting data for class {class_name}')

    # Flag to indicate when data collection for the current class is done
    done = False

    # Loop to wait for the user to be ready to start collecting data
    while True:
        # Capture a frame from the video stream
        ret, frame = cap.read()

        # Add a text overlay to the frame to prompt the user
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        # Display the frame in a window named 'frame'
        cv2.imshow('frame', frame)

        # Wait for the user to press the 'q' key to start collecting data
        if cv2.waitKey(25) == ord('q'):
            break

    # Wait for 3 seconds before starting to collect data
    print("Starting data collection in 3 seconds...")
    time.sleep(3)

    # Counter to keep track of the number of images collected for the current class
    counter = 0

    # Loop to collect the specified number of images for the current class
    while counter < dataset_size:
        # Capture a frame from the video stream
        ret, frame = cap.read()

        # Display the frame in a window named 'frame'
        cv2.imshow('frame', frame)

        # Wait for 100 milliseconds before capturing the next frame
        cv2.waitKey(100)

        # Save the captured frame as an image file in the class directory
        cv2.imwrite(os.path.join(class_dir, '{}.jpg'.format(counter)), frame)

        # Increment the counter
        counter += 1

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()