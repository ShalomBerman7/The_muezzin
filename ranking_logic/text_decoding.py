import base64
import re


def decode_hidden_content(text):
    base64_pattern = r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'

    matches = re.findall(base64_pattern, text)
    decoded_results = []

    for match in matches:
        try:
            decoded_bytes = base64.b64decode(match)
            decoded_text = decoded_bytes.decode('utf-8')

            if decoded_text.isprintable():
                decoded_results.append(decoded_text)
        except Exception:
            continue

    return decoded_results

encod = 'R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT'
encod2 = 'RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=='
Hostile_list = decode_hidden_content(encod)
Less_hostile_list = decode_hidden_content(encod2)
