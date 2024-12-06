import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial da página
st.set_page_config(
    page_title="Dashboard de Algoritmos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #000000;
            color: #ffffff;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
            color: #ffffff;
        }
        h1, h2, h3 {
            font-family: 'Arial Black', sans-serif;
            color: #000000;
        }
        .box {
            border: 2px solid #333333;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #ffffff;
            text-align: center;
        }
        .participant-box {
            background-color: #E0F7FA;
            border: 1px solid #B3E5FC;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            text-align: center;
            font-family: 'Arial', sans-serif;
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

# Dados simulados
@st.cache_data
def load_data():
    data = {
        "Notebook": ["Notebook 1", "Notebook 2", "Notebook 3", "Notebook 4"] * 12,
        "Cenário": ["Crescente", "Decrescente", "Aleatório", "Strings Aleatórias"] * 12,
        "Algoritmo": ["Bubble Sort", "Quick Sort", "Merge Sort", "Shell Sort"] * 12,
        "Tempo (ms)": [1.5, 2.3, 3.0, 4.5, 1.2, 2.0, 3.5, 4.0, 1.8, 2.1, 2.9, 3.3] * 4,
        "Tamanho do Vetor": [10000, 100000, 500000] * 16
    }
    return pd.DataFrame(data)

df = load_data()

# Layout inicial: Título e imagens dos notebooks
st.markdown("<h1>Comparação de Algoritmos de Ordenação</h1>", unsafe_allow_html=True)
st.markdown("### Hardware: Poder Computacional de Cada Notebook")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="box">
            <img src="https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/g-series/g15-5520/media-gallery/g15-5520-bk-coralkb/notebook-g-15-5520-gallery-9.psd?fmt=pjpg&pscan=auto&scl=1&wid=5000&hei=5000&qlt=100,1&resMode=sharp2&size=5000,5000&chrss=full&imwidth=5000" alt="Notebook 1">
            <p>Notebook 1: Dell G15 5520<br>Processador: i5 12ª Geração<br>Memória: 8GB RAM<br>Armazenamento: SSD 512GB</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="box">
            <img src="https://m.media-amazon.com/images/I/61124nnv87L.AC_SL1500.jpg" alt="Notebook 2">
            <p>Notebook 2: Legion 5i<br>Processador: Ryzen 7 5000<br>Memória: 4GB RAM<br>Armazenamento: SSD 256GB</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="box">
            <img src="https://down-id.img.susercontent.com/file/sg-11134201-22100-gxatyb37rbjvb7" alt="Notebook 3">
            <p>Notebook 3: Ideapad 3I Gaming<br>Processador: i5 11ª Geração<br>Memória: 16GB RAM<br>Armazenamento: SSD 512GB</p>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="box">
            <img src="https://s2-techtudo.glbimg.com/qPgH_oQBUw8Vj9pePfLbEDTpRUM=/0x0:695x473/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2021/v/e/rocTlgS6C3OtCNiggYkA/2015-06-10-laptop-xuxa-usar.jpg" alt="Notebook 4">
            <p>Notebook 4: TUF Gaming B550M<br>Processador: Ryzen 7 5700G<br>Memória: 16GB RAM<br>Armazenamento: SSD 1TB</p>
        </div>
    """, unsafe_allow_html=True)
# Barra lateral para filtros interativos
st.sidebar.header("Configurações de Comparação")
dispositivos = st.sidebar.multiselect("💻 Dispositivos", df["Notebook"].unique(), default=df["Notebook"].unique())
algoritmos = st.sidebar.multiselect("📂 Algoritmos", df["Algoritmo"].unique(), default=df["Algoritmo"].unique())
cenarios = st.sidebar.multiselect("🔍 Cenários", df["Cenário"].unique(), default=df["Cenário"].unique())
tamanhos = st.sidebar.multiselect("📏 Tamanhos de Vetor", df["Tamanho do Vetor"].unique(), default=df["Tamanho do Vetor"].unique())

# Filtro de dados
filtered_df = df[
    (df["Notebook"].isin(dispositivos)) &
    (df["Algoritmo"].isin(algoritmos)) &
    (df["Cenário"].isin(cenarios)) &
    (df["Tamanho do Vetor"].isin(tamanhos))
]

# Verificação se há dados filtrados
if filtered_df.empty:
    st.warning("Nenhum dado disponível para os filtros selecionados.")
else:
      # Gráficos separados por notebook
    st.markdown(f"### Gráficos de Desempenho nos Cenários Selecionados")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Mapear paletas distintas para cada notebook
    notebook_color_palettes = {
        "Notebook 1": px.colors.qualitative.Pastel,
        "Notebook 2": px.colors.qualitative.Vivid,
        "Notebook 3": px.colors.qualitative.Set3,
        "Notebook 4": px.colors.qualitative.Bold
    }

    for i, notebook in enumerate(["Notebook 1", "Notebook 2", "Notebook 3", "Notebook 4"]):
        notebook_data = filtered_df[filtered_df["Notebook"] == notebook]

        if not notebook_data.empty:
            fig = px.bar(
                notebook_data,
                x="Tamanho do Vetor",
                y="Tempo (ms)",
                color="Algoritmo",
                barmode="group",
                title=f"{notebook}",
                labels={"Tamanho do Vetor": "Tamanho do Vetor", "Tempo (ms)": "Tempo de Execução (ms)"},
                color_discrete_sequence=notebook_color_palettes[notebook]  # Paleta distinta para cada notebook
            )

            # Adicionar os gráficos nas colunas
            if i == 0:
                col1.plotly_chart(fig, use_container_width=True)
            elif i == 1:
                col2.plotly_chart(fig, use_container_width=True)
            elif i == 2:
                col3.plotly_chart(fig, use_container_width=True)
            elif i == 3:
                col4.plotly_chart(fig, use_container_width=True)


# Gráfico de desempenho geral com destaque para tamanhos de vetores
if not filtered_df.empty:
    # Obtendo os tamanhos únicos de vetor filtrados
    tamanhos_selecionados = ", ".join(map(str, sorted(filtered_df["Tamanho do Vetor"].unique())))
    
    st.markdown(f"### Qual notebook apresentou melhor desempenho? (Vetores: {tamanhos_selecionados})")
    
    # Agrupando dados para o gráfico geral
    desempenho_geral = filtered_df.groupby("Notebook").agg(
        media_tempo=("Tempo (ms)", "mean"),
        vetor_info=("Tamanho do Vetor", lambda x: ', '.join(map(str, sorted(x.unique()))))
    ).reset_index()
    
    fig2 = px.bar(
        desempenho_geral,
        x="Notebook",
        y="media_tempo",
        title=f"Média de Desempenho por Notebook (Vetores: {tamanhos_selecionados})",
        labels={"media_tempo": "Média de Tempo (ms)", "Notebook": "Notebooks"},
        color="Notebook",  # Cor para diferenciar os notebooks
        text="vetor_info"  # Adiciona a informação dos vetores como rótulo
    )
    
    # Ajustando layout do gráfico
    fig2.update_traces(textposition="outside")  # Exibe rótulos fora das barras
    fig2.update_layout(showlegend=False)  # Remove legenda desnecessária
    st.plotly_chart(fig2, use_container_width=True)


# Tabela de estatísticas descritivas
st.markdown("### Estatísticas dos Resultados Adquiridos")
stats = df.groupby(["Notebook", "Algoritmo", "Tamanho do Vetor"]).agg(
    média=("Tempo (ms)", "mean"),
    desvio=("Tempo (ms)", "std"),
    máximo=("Tempo (ms)", "max"),
    mínimo=("Tempo (ms)", "min")
).reset_index()
st.dataframe(stats, use_container_width=True)

st.markdown("### Participantes do Grupo")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="participant-box">
            <p><strong>Adler Augustus</strong></p>
            <p>Email: adler23300004@aluno.cesupa.br</p>
            <p>GitHub: <a href="https://github.com" target="_blank">AdlerGit</a></p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="participant-box">
            <p><strong>Elissandra Bernadett</strong></p>
            <p>Email: elissandra23300025@aluno.cesupa.br</p>
            <p>GitHub: <a href="https://github.com" target="_blank">ElissandraGit</a></p>
        </div>
    """, unsafe_allow_html=True)
with col1:
    st.markdown("""
        <div class="participant-box">
            <p><strong>Luiz Eduardo</strong></p>
            <p>Email: luiz23300032@aluno.cesupa.br</p>
            <p>GitHub: <a href="https://github.com" target="_blank">LuizGit</a></p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="participant-box">
            <p><strong>Renan Abreu</strong></p>
            <p>Email: renan23300025@aluno.cesupa.br</p>
            <p>GitHub: <a href="https://github.com" target="_blank">RenanGit</a></p>
        </div>
    """, unsafe_allow_html=True)
# Rodapé
st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <p>© Projeto Interdisciplinar - EC4MA | 2024</p>
    </div>
""", unsafe_allow_html=True)