from dotenv import load_dotenv, find_dotenv
import openai
_= load_dotenv(find_dotenv())
client = openai.OpenAI()

class AtaCreator:

    def __init__(self):
        
        self.client = client
        self.language = 'pt'
        self.response_format = 'text'
        self.audio_model = 'whisper-1'

    def trancription(self, path_audio):

        with open(path_audio, 'rb') as aud:
            text = self.client.audio.transcriptions.create(
                model = self.audio_model,
                language= self.language,
                response_format= self.response_format,
                file = aud
            )
        return text