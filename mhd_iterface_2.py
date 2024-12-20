import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial da interface
st.set_page_config(page_title="Modelo Hipotético-Dedutivo no Xadrez", layout="centered")
st.title("♟️ Modelo Hipotético-Dedutivo no Xadrez")
st.write("Preencha as etapas do método para organizar suas jogadas e estratégias.")

# Inicialização da tabela de dados
if "mhd_data" not in st.session_state:
    st.session_state.mhd_data = pd.DataFrame(columns=["Etapa", "Descrição"])

# Perguntas norteadoras para cada etapa
perguntas = {
    "Base Teórica": "Qual é a base de conhecimento ou estratégia que será usada como referência?",
    "Hipótese": "O que você espera alcançar com uma jogada ou sequência de jogadas?",
    "Consequências": "Quais reações ou respostas você espera do adversário?",
    "Experimento": "Qual jogada ou sequência será aplicada para testar sua hipótese?",
    "Observações": "O que aconteceu após a jogada? O resultado foi o esperado?",
    "Avaliação": "A hipótese inicial foi confirmada, ajustada ou refutada? Por quê?"
}

# Formulário para entrada dos dados
with st.form("mhd_form"):
    etapa = st.selectbox("Selecione a Etapa", list(perguntas.keys()))
    descricao = st.text_area("Responda:", perguntas[etapa], height=100)
    submitted = st.form_submit_button("Adicionar Etapa")

    if submitted:
        if descricao.strip():
            nova_entrada = pd.DataFrame({"Etapa": [etapa], "Descrição": [descricao]})
            st.session_state.mhd_data = pd.concat([st.session_state.mhd_data, nova_entrada], ignore_index=True)
            st.success(f"Etapa '{etapa}' adicionada com sucesso!")
        else:
            st.error("A descrição não pode estar vazia!")

# Filtros para exibição da tabela
st.subheader("Tabela do Modelo Hipotético-Dedutivo")
col1, col2 = st.columns(2)

with col1:
    filtro_etapa = st.selectbox("Filtrar por Etapa", ["Todas"] + list(st.session_state.mhd_data["Etapa"].unique()))
    tabela_filtrada = (
        st.session_state.mhd_data if filtro_etapa == "Todas" else st.session_state.mhd_data[st.session_state.mhd_data["Etapa"] == filtro_etapa]
    )

with col2:
    ordenar_por = st.selectbox("Ordenar por", ["Etapa", "Descrição"])
    tabela_filtrada = tabela_filtrada.sort_values(by=ordenar_por, ignore_index=True)

# Exibição da tabela dinâmica
st.dataframe(tabela_filtrada, use_container_width=True)

# Edição da tabela
st.markdown("### Editar Entradas")
if not st.session_state.mhd_data.empty:
    max_index = len(st.session_state.mhd_data) - 1
else:
    max_index = 0

linha_para_editar = st.number_input(
    "Selecione a linha para editar (índice)",
    min_value=0,
    max_value=max_index,
    step=1
)

texto_editado = st.text_area("Novo texto para a descrição", st.session_state.mhd_data.iloc[linha_para_editar, 1] if not st.session_state.mhd_data.empty else "")
if st.button("Salvar Alteração"):
    st.session_state.mhd_data.iloc[linha_para_editar, 1] = texto_editado
    st.success("Alteração salva com sucesso!")

# Opção para limpar a tabela
if st.button("Limpar Tabela"):
    st.session_state.mhd_data = pd.DataFrame(columns=["Etapa", "Descrição"])
    st.success("Tabela limpa com sucesso!")

# Visualização em gráfico
if not st.session_state.mhd_data.empty:
    st.subheader("Análise Visual das Etapas")
    grafico = px.histogram(st.session_state.mhd_data, x="Etapa", title="Distribuição de Etapas", text_auto=True)
    st.plotly_chart(grafico, use_container_width=True)

# Exportar a tabela para CSV
st.download_button(
    label="Baixar Tabela como CSV",
    data=st.session_state.mhd_data.to_csv(index=False),
    file_name="mhd_xadrez.csv",
    mime="text/csv"
)
