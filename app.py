import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path
import time
import tempfile

st.set_page_config(page_title="SafeGuard Live", page_icon="🦺", layout="wide")

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

st.markdown("# 🦺 SafeGuard Live")
st.markdown("### IA que previne acidentes industriais")
st.markdown("---")

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/hard-hat.png", width=80)
    st.title("Configurações")
    model = st.selectbox("Modelo", ["models/gemini-2.5-flash"])
    st.markdown("---")
    st.info("Análise multi-turn de vídeos industriais")

tab1, tab2, tab3 = st.tabs(["📹 Análise", "📊 Resultados", "ℹ️ Info"])

with tab1:
    st.header("Upload de Vídeo")
    uploaded = st.file_uploader("Vídeo industrial", type=['mp4', 'mov', 'avi'])
    
    if uploaded:
        st.success(f"✅ {uploaded.name}")
        st.video(uploaded)
        
        if st.button("🚀 Iniciar Análise", type="primary", use_container_width=True):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                tmp.write(uploaded.read())
                video_path = tmp.name
            
            prog = st.progress(0)
            status = st.empty()
            
            try:
                status.text("⏳ Upload...")
                prog.progress(10)
                vf = genai.upload_file(path=video_path)
                
                while vf.state.name == "PROCESSING":
                    time.sleep(2)
                    vf = genai.get_file(vf.name)
                
                if vf.state.name == "FAILED":
                    st.error("❌ Falha")
                    st.stop()
                
                prog.progress(25)
                m = genai.GenerativeModel(model)
                
                status.text("🧠 Turn 1/4...")
                prog.progress(30)
                r1 = m.generate_content(["Analise este vídeo industrial: 1. Pessoas? 2. Ambiente? 3. Equipamentos? 4. Atividades?", vf])
                t1 = r1.text
                prog.progress(45)
                
                status.text("🧠 Turn 2/4...")
                r2 = m.generate_content([f"Baseado em: {t1}\n\nPara cada pessoa, verifique EPIs: Capacete? Colete? Óculos? Luvas? Calçado?", vf])
                t2 = r2.text
                prog.progress(65)
                
                status.text("🧠 Turn 3/4...")
                r3 = m.generate_content([f"Contexto: {t1}\nEPIs: {t2}\n\nIdentifique riscos com timestamp, severidade (BAIXA/MÉDIA/ALTA) e descrição.", vf])
                t3 = r3.text
                prog.progress(85)
                
                status.text("🧠 Turn 4/4...")
                r4 = m.generate_content([f"Análise: {t1}\n{t2}\n{t3}\n\nForneça: 1. Score 0-100 2. Top 3 riscos 3. Ações imediatas 4. Recomendações", vf])
                t4 = r4.text
                prog.progress(100)
                
                status.text("✅ Concluído!")
                
                score = 20
                try:
                    import re
                    for line in t4.split('\n'):
                        if 'score' in line.lower():
                            match = re.search(r':\s*(\d{1,2})\b', line)
                            if match:
                                score = int(match.group(1))
                                break
                except:
                    pass
                
                st.success("🎉 Análise concluída!")
                st.balloons()
                
                st.markdown("---")
                st.header("Resultados")
                
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    if score < 30:
                        emoji = "🔴"
                        nivel = "CRÍTICO"
                    elif score < 60:
                        emoji = "🟠"
                        nivel = "ATENÇÃO"
                    else:
                        emoji = "🟢"
                        nivel = "OK"
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 30px; border-radius: 15px; text-align: center;">
                    <h1 style="margin: 0;">{emoji} {score}/100</h1>
                    <h3 style="margin: 10px 0 0 0;">{nivel}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("")
                
                rt1, rt2, rt3, rt4 = st.tabs(["🧠 Contexto", "🦺 EPIs", "⚠️ Riscos", "📊 Relatório"])
                
                with rt1:
                    st.markdown(t1)
                with rt2:
                    st.markdown(t2)
                with rt3:
                    st.markdown(t3)
                with rt4:
                    st.markdown(t4)
                
                report = f"""SafeGuard Live - Relatório
Vídeo: {uploaded.name}
Score: {score}/100
{"="*70}

TURN 1 - CONTEXTO
{t1}

TURN 2 - EPIs
{t2}

TURN 3 - RISCOS
{t3}

TURN 4 - RELATÓRIO
{t4}
"""
                
                st.download_button("📥 Baixar Relatório", data=report, 
                                 file_name=f"safeguard_{uploaded.name}.txt", 
                                 mime="text/plain", use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Erro: {e}")
            finally:
                if os.path.exists(video_path):
                    os.unlink(video_path)

with tab2:
    st.header("Análises Anteriores")
    st.info("Histórico em desenvolvimento")

with tab3:
    st.header("Como Funciona")
    st.markdown("""
    ### 🧠 Multi-Turn Analysis
    
    **Turn 1:** Contexto (pessoas, ambiente, equipamentos)  
    **Turn 2:** Análise de EPIs por pessoa  
    **Turn 3:** Comportamentos de risco com severidade  
    **Turn 4:** Relatório final com score e ações  
    
    ### 🎯 Diferencial
    - Thought Signatures (contexto entre turns)
    - Spatial-Temporal Understanding
    - 1M Context Window
    
    ### 📈 Aplicações
    - Auditorias de segurança
    - Treinamento de equipes
    - Prevenção de acidentes
    - Relatórios para CIPA
    """)

