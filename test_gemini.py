from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from pathlib import Path
import time

# Carrega API key
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ ERRO: API key não encontrada no arquivo .env")
    exit()

client = genai.Client(api_key=api_key)

print("🚀 SafeGuard Live - Teste Inicial\n")
print("="*50)

# Pega primeiro vídeo da pasta dataset/
dataset_path = Path("dataset")
videos = list(dataset_path.glob("*.mp4"))

if not videos:
    print("❌ ERRO: Nenhum vídeo .mp4 encontrado na pasta dataset/")
    exit()

video_path = videos[0]
print(f"📹 Analisando: {video_path.name}\n")

# Upload do vídeo pro Gemini
print("⏳ Fazendo upload do vídeo... (30s-2min)")

try:
    with open(video_path, 'rb') as f:
        video_file = client.files.upload(
            file=f,
            config={'mime_type': 'video/mp4'}
        )
    
    print(f"✅ Upload completo! File URI: {video_file.name}\n")
    
    # Prompt de análise
    prompt = """
Analise este vídeo de ambiente industrial/construção e identifique riscos de segurança.

Procure por:
1. Pessoas sem equipamentos de proteção (capacete, colete, luvas, óculos)
2. Comportamentos de risco (correndo, perto de máquinas, altura sem proteção)
3. Violações de segurança (saídas bloqueadas, equipamentos sem trava)

Para cada risco encontrado, forneça:
- Tipo de risco
- Timestamp aproximado (segundos ou minutos)
- Severidade (baixa/média/alta)
- Descrição breve

Seja específico e técnico.
"""
    
    print("🧠 Gemini analisando vídeo...\n")
    
    response = client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=[
            prompt,
            types.Part.from_uri(
                file_uri=video_file.uri,
                mime_type=video_file.mime_type
            )
        ]
    )
    
    print("="*50)
    print("📊 RESULTADO DA ANÁLISE:\n")
    print(response.text)
    print("="*50)
    
    # Salva resultado
    output_file = Path("output") / f"analise_{video_path.stem}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Análise de: {video_path.name}\n")
        f.write("="*50 + "\n\n")
        f.write(response.text)
    
    print(f"\n✅ Resultado salvo em: {output_file}")
    print("\n🎉 Teste concluído com sucesso!")

except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()

