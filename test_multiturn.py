import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path
import time
import json

# Carrega API key
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

print("🚀 SafeGuard Live - Análise Multi-Turn com Thought Signatures\n")
print("="*70)

# Pega primeiro vídeo
dataset_path = Path("dataset")
videos = list(dataset_path.glob("*.mp4"))
video_path = videos[0]

print(f"📹 Analisando: {video_path.name}\n")

# Upload do vídeo
print("⏳ Fazendo upload do vídeo...")
video_file = genai.upload_file(path=str(video_path))

while video_file.state.name == "PROCESSING":
    print("⏳ Processando...")
    time.sleep(3)
    video_file = genai.get_file(video_file.name)

print("✅ Upload completo!\n")

# Modelo
model = genai.GenerativeModel('models/gemini-2.5-flash')

# TURN 1: Análise geral da cena
print("🧠 TURN 1: Analisando cena geral...")
prompt1 = """
Analise este vídeo de ambiente industrial/construção.

Descreva:
1. Quantas pessoas aparecem?
2. Que tipo de ambiente é? (construção, fábrica, armazém, etc)
3. Que equipamentos/máquinas estão presentes?
4. Que atividades estão sendo realizadas?

Seja breve e objetivo.
"""

response1 = model.generate_content([prompt1, video_file])
print("\n" + "="*70)
print("📋 CONTEXTO GERAL:")
print(response1.text)
print("="*70 + "\n")

# Salva Turn 1
turn1_result = response1.text

# TURN 2: Análise de EPIs (usando contexto do Turn 1)
print("🧠 TURN 2: Analisando EPIs com base no contexto anterior...")
time.sleep(2)  # Evita rate limit

prompt2 = f"""
Baseado na análise anterior:
{turn1_result}

Agora, para CADA pessoa identificada, verifique:
- Está usando capacete de segurança?
- Está usando colete/colete refletivo?
- Está usando óculos de segurança?
- Está usando luvas?
- Está usando calçado de segurança?

Liste timestamp e o que está faltando para cada pessoa.
"""

response2 = model.generate_content([prompt2, video_file])
print("\n" + "="*70)
print("🦺 ANÁLISE DE EPIs:")
print(response2.text)
print("="*70 + "\n")

turn2_result = response2.text

# TURN 3: Análise de riscos comportamentais (usando contexto Turn 1 + Turn 2)
print("🧠 TURN 3: Analisando comportamentos de risco...")
time.sleep(2)

prompt3 = f"""
Contexto da cena:
{turn1_result}

Status de EPIs:
{turn2_result}

Agora identifique COMPORTAMENTOS DE RISCO:
- Pessoas trabalhando em altura sem proteção contra quedas?
- Pessoas próximas (<2m) de máquinas em movimento?
- Pessoas em zonas perigosas (abaixo de cargas suspensas, perto de veículos)?
- Distrações (celular, conversando enquanto opera máquina)?
- Procedimentos inseguros (lockout/tagout não seguido)?

Para cada risco:
- Timestamp
- Severidade (BAIXA/MÉDIA/ALTA)
- Descrição detalhada
- Consequência potencial
"""

response3 = model.generate_content([prompt3, video_file])
print("\n" + "="*70)
print("⚠️ RISCOS COMPORTAMENTAIS:")
print(response3.text)
print("="*70 + "\n")

# TURN 4: Score final e recomendações
print("🧠 TURN 4: Calculando score e recomendações...")
time.sleep(2)

prompt4 = f"""
Com base em toda a análise:

Contexto: {turn1_result}
EPIs: {turn2_result}
Riscos: {response3.text}

Forneça:
1. **Score de Segurança (0-100)**: Quanto menor o score, mais perigoso
2. **Top 3 Riscos Críticos**: Priorizados por severidade
3. **Ações Corretivas Imediatas**: O que fazer AGORA
4. **Recomendações de Longo Prazo**: Melhorias no processo

Seja objetivo e direto ao ponto.
"""

response4 = model.generate_content([prompt4, video_file])
print("\n" + "="*70)
print("📊 RELATÓRIO FINAL:")
print(response4.text)
print("="*70 + "\n")

# Salva relatório completo
output_file = Path("output") / f"analise_multiturn_{video_path.stem}.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"SafeGuard Live - Análise Multi-Turn\n")
    f.write(f"Vídeo: {video_path.name}\n")
    f.write("="*70 + "\n\n")
    
    f.write("🧠 TURN 1 - CONTEXTO GERAL\n")
    f.write("="*70 + "\n")
    f.write(turn1_result + "\n\n")
    
    f.write("🦺 TURN 2 - ANÁLISE DE EPIs\n")
    f.write("="*70 + "\n")
    f.write(turn2_result + "\n\n")
    
    f.write("⚠️ TURN 3 - RISCOS COMPORTAMENTAIS\n")
    f.write("="*70 + "\n")
    f.write(response3.text + "\n\n")
    
    f.write("📊 TURN 4 - RELATÓRIO FINAL\n")
    f.write("="*70 + "\n")
    f.write(response4.text + "\n\n")

print(f"✅ Relatório completo salvo em: {output_file}")
print("\n🎉 Análise Multi-Turn concluída com sucesso!")
print("\n💡 DIFERENCIAL: Cada turn usa contexto do anterior,")
print("   demonstrando raciocínio complexo e multi-step!")

