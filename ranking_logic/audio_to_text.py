import speech_recognition as sr


def to_text(file):
    r = sr.Recognizer()
    all_text = []

    try:
        with sr.AudioFile(str(file)) as source:
            duration = source.DURATION
            offset = 0
            while offset < duration:
                audio = r.record(source, duration=60)
                all_text.append(audio)
                offset += 60
        return ' '.join(all_text)
    except Exception as e:
        print(f'error: {e}')

    return r.recognize_google(audio)
