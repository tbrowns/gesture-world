import streamlit as st
import cv2
import numpy as np
import pickle
import mediapipe as mp
import speech_recognition as sr
import asyncio

from app.htmlTemplate import css, other_user_template, user_template, audio_box

# Load the pre-trained model from a pickle file
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Global variable to store chat history
chat_history = []

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Flag variables for stopping the async loops
video_running = False
audio_running = False

# Function to display chat history at the end
def display_chat_history():
    st.subheader("Chat History")
    if chat_history:
        for message in chat_history:
            if message['user'] == 'user':
                st.write(user_template.replace("{{MSG}}", message['text']), unsafe_allow_html=True)
            else:
                st.write(other_user_template.replace("{{MSG}}", message['text']), unsafe_allow_html=True)
    else:
        st.write("No conversation yet.")

# Asynchronous function to process video input for hand detection
async def process_video_input():
    global video_running
    frame_holder = st.empty()  # Placeholder for the video feed
    text_placeholder = st.empty()  # Placeholder for replacing generated text
    cap = cv2.VideoCapture(0)
    
    while video_running:
        ret, frame = cap.read()
        if not ret:
            break
        
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, 
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                data_aux = []
                x_ = [landmark.x for landmark in hand_landmarks.landmark]
                y_ = [landmark.y for landmark in hand_landmarks.landmark]

                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))

                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = prediction[0]
                
                x1, y1 = int(min(x_) * W) - 10, int(min(y_) * H) - 10
                x2, y2 = int(max(x_) * W) - 10, int(max(y_) * H) - 10
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3)

                # Update chat history with the detected sign language
                chat_history.append({'user': 'user', 'text': predicted_character})

                # Replace the previously generated text with the new one
                text_placeholder.write(user_template.replace("{{MSG}}", predicted_character), unsafe_allow_html=True)

        # Display the frame using Streamlit
        frame_holder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
        await asyncio.sleep(0)  # Yield control to the event loop

    cap.release()

# Asynchronous function to process real-time audio input
async def process_audio_input():
    global audio_running
    text_placeholder = st.empty()  # Placeholder for replacing generated audio transcription
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  
        while audio_running:
            audio = recognizer.listen(source, timeout=30, phrase_time_limit=6)
            try:
                text = recognizer.recognize_google(audio)
                chat_history.append({'user': 'other_user', 'text': text})

                # Replace the previously generated text with the new one
                text_placeholder.write(other_user_template.replace("{{MSG}}", text), unsafe_allow_html=True)
                
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
            await asyncio.sleep(0)  # Yield control to the event loop

# Streamlit UI
st.title("Sign Language Detection")

# Layout: two checkboxes for video and audio input
st.write(css, unsafe_allow_html=True)

video_container, audio_container = st.columns(2)

# Video capture section
with video_container:
    start_loading_video = st.checkbox("Start Video Capture")
    if start_loading_video:
        if not video_running:
            video_running = True
            asyncio.run(process_video_input())
    else:
        video_running = False

# Audio transcription section
with audio_container:
    start_loading_audio = st.checkbox("Start Audio Transcription")
    if start_loading_audio:
        if not audio_running:
            audio_running = True
            asyncio.run(process_audio_input())
    else:
        audio_running = False

# Display the entire chat history after processing is stopped
if not (video_running or audio_running):
    display_chat_history()
