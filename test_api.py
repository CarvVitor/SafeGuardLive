from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print(f"🔑 API Key encontrada: {api_key[:20] if api_key else 'NENHUMA'}...")

if not api_key:
    print("❌ ERRO: .env não tem a chave!")
    exit()

try:
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents='Diga apenas: funcionou!'
    )
    
    print(f"✅ API funcionando! Resposta: {response.text}")
    
except Exception as e:
    print(f"❌ Erro na API: {e}")

