import speech_recognition as sr

def transcribe_speech(logger, audio_file):
    print("Starting processing of speech file...")
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        logger.info("Transcription: " + text)
        return text
    except sr.UnknownValueError:
        logger.info("Speech recognition could not understand audio")
    except sr.RequestError as e:
        logger.info("Could not request results from Google Speech Recognition service; {0}".format(e))