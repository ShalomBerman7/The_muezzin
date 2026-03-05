import speech_recognition as sr


def to_text(file):
    r = sr.Recognizer()

    with sr.AudioFile(str(file)) as source:
        audio = r.record(source)

    return r.recognize_google(audio, language='he-IL')
