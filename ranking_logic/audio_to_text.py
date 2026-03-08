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
                try:
                    chunk_text = r.recognize_google(audio,language='he-IL')
                    all_text.append(chunk_text)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(e)
                    break

                offset += 60

        return ' '.join(all_text)
    except Exception as e:
        print(f'error: {e}')

    return r.recognize_google(audio)
