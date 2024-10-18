# Sign Language Detection and Speech Synthesis

This project aims to create a system that can detect sign language gestures using a webcam, convert them into text, and optionally synthesize speech from the detected text using Azure Cognitive Services. The project is divided into several components, each responsible for a specific part of the workflow.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Components](#components)
  - [Main Application](#main-application)
  - [Training the Model](#training-the-model)
  - [Collecting Data](#collecting-data)
  - [Speech Services](#speech-services)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**
   `sh
    git clone https://github.com/yourusername/sign-language-detection.git
    cd sign-language-detection
    `

2. **Install the required dependencies:**
   `sh
    pip install -r requirements.txt
    `

3. **Set up Azure Cognitive Services:** - Create an Azure account and set up a Speech service. - Replace the `speech_key` and `service_region` in `main.py` and `speech_services.py` with your Azure credentials.

## Usage

1.  **Collect Data:** - Run `collecting_data.py` to collect images for different sign language gestures. - Follow the prompts to enter class names and capture images.

        ```sh
        python collecting_data.py
        ```

2.  **Train the Model:** - Run `training_model.py` to train a RandomForest model on the collected data.

        ```sh
        python training_model.py
        ```

3.  **Run the Main Application:** - Run `main.py` to start the Streamlit application for real-time sign language detection and speech synthesis.

        ```sh
        streamlit run main.py
        ```

## Components

### Main Application

**File:** `main.py`

This is the main application file that uses Streamlit to create a web interface for real-time sign language detection and speech synthesis. It captures video input, processes it to detect hand landmarks using MediaPipe, and uses a pre-trained model to predict the sign language gesture. The detected gesture can be converted to speech using Azure Cognitive Services.

### Training the Model

**File:** `training_model.py`

This script is used to train a RandomForest model on the collected sign language gesture data. It processes the images to extract hand landmarks using MediaPipe, normalizes the landmarks, and trains the model. The trained model is saved as a pickle file for later use.

### Collecting Data

**File:** `collecting_data.py`

This script is used to collect images for different sign language gestures. It captures images from the webcam and saves them in a specified directory. The user is prompted to enter class names for each gesture, and the images are saved in corresponding subdirectories.

### Speech Services

**File:** `speech_services.py`

This module contains the `AzureSpeechSynthesizer` class, which uses Azure Cognitive Services to convert text to speech. It initializes the Azure Speech SDK with the provided credentials and synthesizes speech from input text.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
