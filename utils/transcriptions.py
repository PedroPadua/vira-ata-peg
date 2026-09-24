from dotenv import load_dotenv, find_dotenv
import openai
_= load_dotenv(find_dotenv())

client = openai.OpenAI()

def transcription(path_audio, language = 'pt', response_format = 'text'):
    with open(path_audio, 'rb') as aud:
        text= client.audio.transcriptions.create(
            model ='whisper-1',
            language =language,
            response_format = response_format,
            file = aud
        )
    return text
texto = (transcription('audio_urgente.mp3'))

with open("transcricao2.txt", "w", encoding="utf-8") as f:
    f.write(texto)

