from gtts import gTTS


def convert_text_to_mp3(text: str, target_language_code: str) -> None:
    """Convert the given text to mp3 formatted audio

    :type text: str
    :param text: Text to convert to audio
    :type target_language_code: str
    :param target_language_code: Language code
    """

    tts = gTTS(text, lang=target_language_code, lang_check=True)

    with open("translation.mp3", "wb") as mp3_file:
        tts.write_to_fp(mp3_file)