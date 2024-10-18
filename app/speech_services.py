import azure.cognitiveservices.speech as speechsdk

class AzureSpeechSynthesizer:
    def __init__(self, speech_key: str, service_region: str, voice_name: str = "en-US-DustinMultilingualNeural"):
        """
        Initializes the AzureSpeechSynthesizer with a subscription key, service region, and optional voice name.
        :param speech_key: Azure Cognitive Services speech key.
        :param service_region: Azure Cognitive Services service region.
        :param voice_name: The voice to use for speech synthesis (default is 'en-US-DustinMultilingualNeural').
        """
        self.speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        self.speech_config.speech_synthesis_voice_name = voice_name
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

    def synthesize_text(self, text: str):
        """
        Synthesizes speech from the input text.
        :param text: The text to be converted to speech.
        :return: Synthesis result, either success or error details.
        """
        result = self.synthesizer.speak_text_async(text).get()

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized for text: {text}")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")

        return result

# Example usage
if __name__ == "__main__":
    speech_key = "a79116e8718442e789ae06265b937ec8"
    service_region = "eastus"
    text = "Hi, this is Dustin Multilingual"

    # Create an instance of the AzureSpeechSynthesizer class
    synthesizer = AzureSpeechSynthesizer(speech_key, service_region)

    # Synthesize speech from text
    synthesizer.synthesize_text(text)
