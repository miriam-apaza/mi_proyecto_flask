import requests
import json

API_KEY = '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'

def consultar_ia(prompt_contexto):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt_contexto
                    }
                ]
            }),
            timeout=15
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Análisis no disponible temporalmente. Motivo: {str(e)}"