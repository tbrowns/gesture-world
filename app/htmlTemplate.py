css = '''
<style>
.audio-container{
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f4f4f9;
    margin: 0;
    padding:20px auto;
    font-family: Arial, sans-serif;
}

.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}

.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}

.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}

.pulsate {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 100px;
    background-color: #ff5555;
    border-radius: 50%;
    box-shadow: 0 0 0 rgba(255, 85, 85, 0.7);
    animation: pulse 1.5s infinite;


@keyframes pulse {
    0% {
        transform: scale(0.9);
        box-shadow: 0 0 0 0 rgba(255, 85, 85, 0.7);
    }
    70% {
        transform: scale(1.1);
        box-shadow: 0 0 0 40px rgba(255, 85, 85, 0);
    }
    100% {
        transform: scale(0.9);
        box-shadow: 0 0 0 0 rgba(255, 85, 85, 0);
    }

.recording-text {
        z-index: 9;
        font-size: 16px;
        color: white;
}
'''

other_user_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="../icons/voice-message.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="../icons/hand-gesture.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

audio_animation = '''
<div class = "audio-container">
    <div class="pulsate"><p class="recording-text">Listening</p></div>

</div>
'''