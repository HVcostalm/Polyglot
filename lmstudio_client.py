import requests
import json

# URL do LMStudio
LMSTUDIO_URL = "http://127.0.0.1:1234"

def processar_transcricao(texto_ingles, model_name):
    """
    Retorna dicionário com:
    - palavras_explicadas
    - traducao_pt
    """

    prompt = f"""
ATENÇÃO: Responda APENAS em JSON válido, sem comentários, sem texto extra.
Estrutura obrigatória:
{{
   "palavras_explicadas": [
       {{ "expressao": "string", "significado": "string (em português)" }}
   ],
   "traducao_pt": "string"
}}

Regras:
1. "palavras_explicadas" → Liste TODAS as expressões idiomáticas, palavras incomuns e gírias.
2. "traducao_pt" → Traduza o texto original para português, mantendo:
   - Coesão textual e fluência natural
   - Contexto adequado para expressões idiomáticas
   - Registro linguístico equivalente ao original
   - Naturalidade na língua portuguesa
3. Adapte culturalmente as expressões quando necessário.
4. Não adicione campos extras.
5. Não use caracteres de formatação fora do JSON.

Texto original:
{texto_ingles}
"""

    # Detecta se é modelo chat-style ou instruct
    if "instruct" in model_name.lower():
        # GGUF instruct → /v1/completions com prompt
        url = f"{LMSTUDIO_URL}/v1/completions"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "temperature": 0.3,
            "max_tokens": 2000
        }
    else:
        # Chat-style → /v1/chat/completions com messages
        url = f"{LMSTUDIO_URL}/v1/chat/completions"
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "Você é um professor de inglês fluente em português."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()

        data = response.json()

        # Extrair resposta de acordo com o tipo
        if "choices" in data and len(data["choices"]) > 0:
            if "message" in data["choices"][0]:
                # chat-style
                resposta_texto = data["choices"][0]["message"]["content"]
            else:
                # instruct-style
                resposta_texto = data["choices"][0]["text"]
        else:
            print("\n[ERRO] Nenhuma escolha retornada pelo modelo.")
            return {"erro": "Nenhuma escolha retornada", "resposta": data}

        try:
            return json.loads(resposta_texto)
        except json.JSONDecodeError:
            # Tenta extrair trecho JSON mais "limpo"
            inicio = resposta_texto.find("{")
            fim = resposta_texto.rfind("}") + 1
            if inicio != -1 and fim != -1:
                trecho = resposta_texto[inicio:fim]
                try:
                    return json.loads(trecho)
                except json.JSONDecodeError:
                    pass

            print("\n[ERRO JSON] O modelo respondeu, mas o JSON está mal formatado.")
            print("Resposta recebida:\n", resposta_texto)
            with open("resposta_invalida.json", "w", encoding="utf-8") as f:
                f.write(resposta_texto)
            return {"erro": "JSON inválido", "resposta": resposta_texto}

    except requests.exceptions.RequestException as e:
        print("\n[ERRO HTTP] Não foi possível se comunicar com o LM Studio.")
        print("Detalhes:", e)
        return {"erro": "Falha na comunicação com LM Studio", "detalhes": str(e)}
