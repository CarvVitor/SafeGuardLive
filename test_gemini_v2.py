import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path
import time

# Carrega API key
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ ERRO: API key não encontrada")
    exit()

genai.configure(api_key=api_key)

print("🚀 SafeGuard Live - Teste Inicial\n")
print("="*50)

# Pega primeiro vídeo
dataset_path = Path("dataset")
videos = list(dataset_path.glob("*.mp4"))

if not videos:
    print("❌ ERRO: Nenhum vídeo encontrado")
    exit()

video_path = videos[0]
print(f"📹 Analisando: {video_path.name}\n")

# Upload do vídeo
print("⏳ Fazendo upload do vídeo...")

video_file = genai.upload_file(path=str(video_path))

# Espera processar
while video_file.state.name == "PROCESSING":
    print("⏳ Processando...")
    time.sleep(3)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
    print("❌ ERRO: Falha no upload")
    exit()

print("✅ Upload completo!\n")

# Prompt
prompt = """
Analise este vídeo de ambiente industrial/construção e identifique riscos de segurança.

Procure por:
1. Pessoas sem equipamentos de proteção (capacete, colete, luvas)
2. Comportamentos de risco (perto de máquinas, altura sem proteção)
3. Violações de segurança

Para cada risco:
- Tipo de risco
- Timestamp aproximado
- Severidade (baixa/média/alta)
- Descrição breve
"""

print("🧠 Gemini analisando vídeo...\n")

model = genai.GenerativeModel('models/gemini-2.5-flash')
response = model.generate_content([prompt, video_file])

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

