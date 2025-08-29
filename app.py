import streamlit as st
from lmstudio_client import processar_transcricao
from faster_whisper import WhisperModel
import mimetypes
from utils import extrair_audio
import os

# =============================
# Configuração inicial
# =============================
st.set_page_config(page_title="Polyglot - Transcrição & Tradução", layout="wide")
st.title("🧠 Polyglot - Seu Assistente de Idiomas")

# =============================
# Upload de arquivo
# =============================
uploaded_file = st.file_uploader(
    "Envie um arquivo de áudio ou vídeo para que o Polyglot analise:",
    type=["mp3", "wav", "mp4", "mkv"]
)

col1, col2 = st.columns(2)
with col1:
    model_size = st.selectbox("Qual modelo Whisper o Polyglot deve usar?", ["tiny", "small", "medium", "large"], index=1)
with col2:
    lmstudio_model = st.selectbox(
        "Qual cérebro LMStudio o Polyglot deve ativar?",
        [
            "mistralai_-_mistral-7b-instruct-v0.2"
        ],
        index=0
    )

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    # =============================
    # Salvar temporariamente com extensão
    # =============================
    ext = os.path.splitext(uploaded_file.name)[1]
    caminho = f"temp_input{ext}"
    with open(caminho, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # =============================
    # Extrair áudio se necessário
    # =============================
    tipo_mime, _ = mimetypes.guess_type(caminho)
    if tipo_mime and tipo_mime.startswith("video"):
        st.info("🎬 Polyglot está extraindo o áudio do seu vídeo...")
        caminho_audio = extrair_audio(caminho)
    else:
        caminho_audio = caminho

    # =============================
    # Transcrever
    # =============================
    st.info("📝 Polyglot está transcrevendo seu áudio...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(caminho_audio)
    texto = "".join([seg.text for seg in segments])

    # =============================
    # Processar no LMStudio
    # =============================
    st.info("🤖 Polyglot está pensando e consultando o modelo escolhido...")
    resultado = processar_transcricao(texto, model_name=lmstudio_model)

    # =============================
    # Layout em abas
    # =============================
    aba1, aba2, aba3 = st.tabs(["📝 Transcrição", "📖 Expressões", "🌎 Tradução"])

    with aba1:
        st.subheader("📌 Aqui está a transcrição que o Polyglot preparou")
        st.text_area("Transcrição (Inglês)", value=texto, height=250)

    with aba2:
        st.subheader("🔍 Palavras/Expressões que o Polyglot detectou")
        explicacoes = resultado.get("palavras_explicadas", [])
        if not explicacoes:
            st.warning("Polyglot não encontrou nenhuma expressão idiomática.")
        else:
            for item in explicacoes:
                if isinstance(item, dict):
                    expressao = item.get("expressao") or item.get("expressão") or "???"
                    significado = item.get("significado") or "???"
                elif isinstance(item, str):
                    expressao, significado = item, "não fornecido"
                else:
                    expressao, significado = "???", "???"
                st.write(f"- **{expressao}** → {significado}")

    with aba3:
        st.subheader("🌍 Tradução para PT-BR feita pelo Polyglot")
        traducao = resultado.get("traducao_pt", "")
        if not traducao:
            st.warning("Polyglot não conseguiu gerar a tradução.")
        else:
            st.text_area("Tradução", value=traducao, height=250)

    # =============================
    # Limpeza de arquivos temporários
    # =============================
    try:
        os.remove(caminho)
        if caminho_audio != caminho:  # se foi criado áudio extraído
            os.remove(caminho_audio)
    except Exception:
        pass
