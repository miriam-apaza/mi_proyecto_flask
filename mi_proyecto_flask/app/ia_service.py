import requests
import json

def consultar_ia(prompt: str) -> str:
    """
    Realiza una petición directa a OpenRouter utilizando el modelo gratuito de Gemini
    para evitar errores de falta de pago (402).
    """
    # Cambia esto por tu API Key real de OpenRouter si no usas variables de entorno
    api_key = "TU_API_KEY_DE_OPENROUTER" 
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/gemini-2.5-flash:free",  # Modelo gratuito que no pide créditos
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        # Si la respuesta es exitosa, extraemos el contenido
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            # Si da 402, 404 u otro error, levantamos una excepción para activar el plan B
            raise Exception(f"HTTP Error {response.status_code}")
            
    except Exception as e:
        # Retornamos una cadena vacía o indicativo para que el backend use el respaldo local
        return ""