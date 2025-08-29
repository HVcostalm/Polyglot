# 🧠 Polyglot - Assistente de Transcrição & Tradução

O **Polyglot** é um aplicativo interativo que utiliza IA local para transcrever áudios/vídeos, identificar palavras e expressões idiomáticas, e traduzir conteúdos para o português de forma clara e acessível.  
O objetivo do projeto é auxiliar no aprendizado de idiomas e facilitar a compreensão de conteúdos em inglês.

---

## 🚀 Funcionalidades

- 🎧 **Upload de áudio ou vídeo** (MP3, WAV, MP4, MKV)  
- 📝 **Transcrição automática** com o modelo **Whisper**  
- 🔍 **Identificação de palavras e expressões idiomáticas** com seus significados  
- 🌎 **Tradução para PT-BR** feita via modelo de linguagem local 
- 📊 **Interface amigável** construída com **Streamlit**  
- 🤖 Integração com **LM Studio**, permitindo escolha entre diferentes modelos de IA  

---

## 🛠️ Tecnologias & Bibliotecas

- **[Python 3.10+](https://www.python.org/)** → Linguagem principal do projeto  
- **[Streamlit](https://streamlit.io/)** → Criação da interface web interativa  
- **[Faster-Whisper](https://github.com/guillaumekln/faster-whisper)** → Transcrição de áudio/vídeo com modelos Whisper otimizados  
- **[LM Studio](https://lmstudio.ai/)** → Execução local do modelo  
- **[Requests](https://requests.readthedocs.io/)** → Comunicação HTTP com a API do LM Studio  
- **[FFmpeg](https://ffmpeg.org/)** → Extração de áudio de vídeos (via função utilitária `extrair_audio`)  
- **[MoviePy](https://zulko.github.io/moviepy/?utm_source=chatgpt.com)** → Manipulação de arquivos de vídeo e suporte ao processamento de mídia

---

## ⚙️ Como funciona

1. O usuário envia um arquivo de áudio ou vídeo  
2. O **Polyglot** extrai o áudio (se for vídeo) e o transcreve com o **Whisper**  
3. O texto transcrito é enviado para um modelo local rodando no **LM Studio**  
4. O modelo identifica **palavras e expressões idiomáticas** e gera uma **tradução para PT-BR**  
5. O resultado é exibido em uma interface com abas:  
   - Transcrição em inglês  
   - Lista de palavras e expressões com seus significados  
   - Tradução para português  

---

## 🎯 Objetivo

O **Polyglot** foi criado para ser um assistente de idiomas que vai além da simples tradução.  
Ele ajuda estudantes, professores e curiosos a entenderem palavras e expressões idiomáticas, melhorando a compreensão de conteúdos em inglês e tornando o aprendizado mais eficiente.

---

## 📌 Próximos Passos (Roadmap)

- ⏳ Seleção de diferentes modelos LM Studio na interface  
- ⏳ Suporte a múltiplos idiomas além do inglês  
- ⏳ Histórico de transcrições e traduções  
- ⏳ Modo “chat com o Polyglot” para prática de conversação  

---

## 🖥️ Execução do Projeto

```bash
# Clone o repositório
git clone https://github.com/HVcostalm/polyglot.git
cd polyglot

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instale as dependências

# Instalar Whisper
pip install faster-whisper

# Instalar ffmpeg (Fora do Python. Execute pelo prompt de comando)
winget install Gyan.FFmpeg ou choco install ffmpeg # Windows 
sudo apt update && sudo apt install ffmpeg # Linux
brew install ffmpeg # MacOs

# Instalar Moviepy 

pip install moviepy

# Instalar Requests

pip install requests

# Instalar Streamlit 

pip install streamlit

# LMStudio
- Baixe e instale o LM Studio
- Carregue o modelo desejado (ex: mistralai_-_mistral-7b-instruct-v0.2)
- Ative a API local no LM Studio (porta padrão: 1234)

# Execute a aplicação
streamlit run app.py
