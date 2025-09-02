# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

st.set_page_config(
    page_title="Gerador de HQ de Notícias",
    page_icon="📰",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
    .quadro {
        border: 3px solid #333;
        padding: 15px;
        margin: 10px;
        background: white;
        box-shadow: 5px 5px 10px rgba(0,0,0,0.2);
    }
    .legenda {
        background: #fffacd;
        padding: 10px;
        border-left: 3px solid #ffd700;
        margin-top: 10px;
    }
    .prompt-box {
        background: #f0f0f0;
        padding: 10px;
        border: 1px dashed #999;
        font-size: 12px;
        color: #666;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def extrair_noticia_g1():
    """Extrai primeira notícia do G1"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://g1.globo.com', headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar primeira notícia
        noticia = soup.find('a', class_='feed-post-link')
        if noticia:
            return {
                'titulo': noticia.text.strip(),
                'link': noticia.get('href'),
                'fonte': 'G1'
            }
    except:
        return None

def gerar_roteiro_simples(titulo):
    """Gera roteiro sem API (versão demo)"""
    # Simulação de geração de roteiro
    quadros = []
    
    # Templates de narrativa baseados no título
    if "tecnologia" in titulo.lower():
        narrativa = [
            "Cientistas fazem descoberta revolucionária em laboratório",
            "A nova tecnologia promete transformar o cotidiano",
            "Primeiros testes mostram resultados impressionantes",
            "Especialistas debatem os impactos da inovação",
            "Empresas já demonstram interesse na novidade",
            "O futuro pode estar mais próximo do que imaginamos"
        ]
    elif "política" in titulo.lower():
        narrativa = [
            "Autoridades se reúnem para importante decisão",
            "Discussões intensas marcam o encontro",
            "Propostas são apresentadas e debatidas",
            "População acompanha atentamente os desdobramentos",
            "Votação define os rumos da questão",
            "Resultados geram reações diversas na sociedade"
        ]
    else:
        narrativa = [
            "O dia começa com uma notícia surpreendente",
            "Detalhes começam a emergir sobre o acontecimento",
            "Testemunhas relatam o que presenciaram",
            "Autoridades investigam a situação",
            "Especialistas analisam as implicações",
            "A história continua a se desenvolver"
        ]
    
    prompts = [
        "Wide establishing shot of the main scene, comic book style, dramatic lighting",
        "Close-up of key elements, detailed illustration, dynamic angle",
        "Action scene showing the main event, energetic composition",
        "Group of people reacting, varied expressions, comic art style",
        "Dramatic moment of revelation, intense atmosphere",
        "Final scene suggesting future implications, hopeful or mysterious tone"
    ]
    
    for i in range(6):
        quadros.append({
            'numero': i + 1,
            'legenda': narrativa[i],
            'prompt': prompts[i]
        })
    
    return quadros

# Interface principal
st.title("📰 Gerador de HQ de Notícias")
st.markdown("Transforme notícias em histórias em quadrinhos!")

# Sidebar com opções
with st.sidebar:
    st.header("⚙️ Configurações")
    
    fonte_noticia = st.selectbox(
        "Fonte da Notícia",
        ["G1 (Automático)", "URL Personalizada", "Texto Manual"]
    )
    
    if fonte_noticia == "URL Personalizada":
        url_custom = st.text_input("Cole a URL da notícia")
    elif fonte_noticia == "Texto Manual":
        titulo_manual = st.text_input("Título da Notícia")
        link_manual = st.text_input("Link (opcional)")
    
    st.markdown("---")
    
    usar_ia = st.checkbox("Usar IA para roteiro (necessita API Key)")
    
    if usar_ia:
        api_key = st.text_input("OpenAI API Key", type="password")

# Área principal
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📥 Entrada")
    
    if st.button("🎬 Gerar HQ", type="primary"):
        with st.spinner("Processando..."):
            
            # Obter notícia
            if fonte_noticia == "G1 (Automático)":
                noticia = extrair_noticia_g1()
                if noticia:
                    st.success(f"✅ Notícia extraída: {noticia['titulo'][:50]}...")
                else:
                    st.error("❌ Erro ao extrair notícia do G1")
                    noticia = {
                        'titulo': 'Exemplo: Nova descoberta científica surpreende pesquisadores',
                        'link': '#',
                        'fonte': 'Demo'
                    }
            elif fonte_noticia == "Texto Manual":
                noticia = {
                    'titulo': titulo_manual,
                    'link': link_manual or '#',
                    'fonte': 'Manual'
                }
            
            # Gerar roteiro
            time.sleep(1)  # Simular processamento
            
            if usar_ia and api_key:
                st.info("🤖 Gerando roteiro com IA...")
                # Aqui você implementaria a chamada real à API
                quadros = gerar_roteiro_simples(noticia['titulo'])
            else:
                quadros = gerar_roteiro_simples(noticia['titulo'])
            
            # Salvar no session state
            st.session_state['noticia'] = noticia
            st.session_state['quadros'] = quadros
            st.session_state['titulo_hq'] = f"📚 {noticia['titulo'][:50]}..."

with col2:
    st.header("🎨 História em Quadrinhos")
    
    if 'quadros' in st.session_state:
        st.subheader(st.session_state['titulo_hq'])
        
        # Exibir quadros em grade 2x3
        for row in range(3):
            cols = st.columns(2)
            for col in range(2):
                idx = row * 2 + col
                if idx < 6:
                    with cols[col]:
                        quadro = st.session_state['quadros'][idx]
                        
                        st.markdown(f"""
                        <div class="quadro">
                            <h4>Quadro {quadro['numero']}</h4>
                            <div class="prompt-box">
                                <b>Prompt para imagem:</b><br>
                                {quadro['prompt']}
                            </div>
                            <div class="legenda">
                                {quadro['legenda']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Informações da fonte
        st.markdown("---")
        st.info(f"""
        **📌 Fonte:** {st.session_state['noticia']['fonte']}  
        **🔗 Link:** {st.session_state['noticia']['link']}  
        **📅 Gerado em:** {datetime.now().strftime("%d/%m/%Y %H:%M")}
        """)
        
        # Botão para baixar
        if st.button("💾 Baixar HTML"):
            # Gerar HTML para download
            html_content = gerar_html_completo(
                st.session_state['titulo_hq'],
                st.session_state['quadros'],
                st.session_state['noticia']
            )
            st.download_button(
                label="📥 Clique para baixar",
                data=html_content,
                file_name="hq_noticia.html",
                mime="text/html"
            )

def gerar_html_completo(titulo, quadros, noticia):
    """Gera HTML completo da HQ"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{titulo}</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }}
            .quadro {{ border: 3px solid #333; padding: 15px; background: white; }}
            .legenda {{ background: #fffacd; padding: 10px; margin-top: 10px; }}
            .prompt {{ background: #f0f0f0; padding: 10px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <h1>{titulo}</h1>
        <div class="grid">
    """
    
    for quadro in quadros:
        html += f"""
            <div class="quadro">
                <h3>Quadro {quadro['numero']}</h3>
                <div class="prompt">{quadro['prompt']}</div>
                <div class="legenda">{quadro['legenda']}</div>
            </div>
        """
    
    html += f"""
        </div>
        <hr>
        <p>Fonte: {noticia['fonte']} - <a href="{noticia['link']}">{noticia['link']}</a></p>
    </body>
    </html>
    """
    
    return html

# Rodapé
st.markdown("---")
st.markdown("Feito com ❤️ usando Streamlit")
