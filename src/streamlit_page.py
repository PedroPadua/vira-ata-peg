import streamlit as st
import openai
from dotenv import load_dotenv, find_dotenv
from atacreator import AtaCreator
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from pathlib import Path
from datetime import datetime
import time
import queue
import pydub


_= load_dotenv(find_dotenv())
client = openai.OpenAI()
ac = AtaCreator()


def tab_gravar_reuniao():
    webrtx_ctx = webrtc_streamer(
        key = 'recebe_audio',
        mode = WebRtcMode.SENDONLY,
        audio_receiver_size= 1024,
        media_stream_constraints= {'video': False, 'audio': True}
    )

    if not webrtx_ctx.state.playing:
        st.markdown('Gravação não iniciada')
        return 
    
    PASTA_ARQUIVOS = Path(__file__).parent / 'aud_files'
    PASTA_ARQUIVOS.mkdir(exist_ok=True)


    container = st.empty()
    container.markdown('Comece a falar.')
    pasta_reuniao = PASTA_ARQUIVOS / datetime.now().strftime('_%d_%m_%Y_%H-%M')
    pasta_reuniao.mkdir(exist_ok=True)


    last_transcript = time.time()
    audio_chunck = pydub.AudioSegment.empty()
    audio_completo = pydub.AudioSegment.empty()



    while True:
        if webrtx_ctx.audio_receiver:
            container.markdown('Audio sendo coletado')
            try:
                frames = webrtx_ctx.audio_receiver.get_frames(timeout=1)

            except queue.Empty:
                time.sleep(0.1)
                continue
            for frame in frames:
                sound = pydub.AudioSegment(
                    data = frame.to_ndarray().tobytes(),
                    sample_width = frame.format.bytes,
                    frame_rate = frame.sample_rate,
                    channels = len(frame.layout.channels)
                )
                audio_chunck += sound
                audio_completo  += sound

            if len(audio_completo) > 0:
                audio_completo.export(pasta_reuniao / 'aud.mp3')
                now = time.time()
                if now - last_transcript > 15:
                    last_transcript = now
                    audio_chunck.export(pasta_reuniao / 'aud_temp.mp3')

        else:
            break
def tab_transcricoes():
    st.markdown('tab_trans')

def tab_selecao_atas():
    st.markdown('tab_selecao')
    

def main():
    st.header('Bem-Vindo ao Vira.Ata Peixoto e Gomes🎤', divider = True)
    tab_gravar, tab_trans,tab_selecao  = st.tabs(['Gravar Reunião', 'Importar Transcrição', 'Ver Atas'])

    with tab_gravar:
        tab_gravar_reuniao()
    with tab_trans:
        tab_transcricoes()
    with tab_selecao:
        tab_selecao_atas


if __name__ == '__main__':
    main()