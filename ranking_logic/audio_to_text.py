import speech_recognition as sr


def to_text(file):
    r = sr.Recognizer()

    try:
        with sr.AudioFile(file) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            return text
    except Exception as e:
        print(f'error: {e}')
