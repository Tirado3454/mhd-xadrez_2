streamlit as st
import pandas as pd
import chess
import chess.svg

# Configura��o inicial da interface
st.set_page_config(page_title="Modelo Hipot�tico-Dedutivo no Xadrez", layout="centered")
st.markdown("""<h1 style='font-size:32px; display: flex; align-items: center;'>
<img src='data:image/png;base64,<insira_o_base64_gerado_da_logo_aqui>' style='height:50px; margin-right:10px;'> Modelo Hipot�tico-Dedutivo no Xadrez
</h1>""", unsafe_allow_html=True)
st.write("Configure e salve posi��es personalizadas no tabuleiro.")

# Inicializa��o da tabela de dados
if "mhd_data" not in st.session_state:
    st.session_state.mhd_data = pd.DataFrame(columns=["Etapa", "Descri��o", "FEN"])

# Inicializa��o do tabuleiro
if "current_board" not in st.session_state:
    st.session_state.current_board = chess.Board()

# Perguntas norteadoras para cada etapa do MHD
perguntas = {
    "Base Te�rica": "Qual � a base de conhecimento ou estrat�gia que ser� usada como refer�ncia?",
    "Hip�tese": "O que voc� espera alcan�ar com uma jogada ou sequ�ncia de jogadas?",
    "Consequ�ncias": "Quais rea��es ou respostas voc� espera do advers�rio?",
    "Experimento": "Qual jogada ou sequ�ncia ser� aplicada para testar sua hip�tese?",
    "Observa��es": "O que aconteceu ap�s a jogada? O resultado foi o esperado?",
    "Avalia��o": "A hip�tese inicial foi confirmada, ajustada ou refutada? Por qu�?"
}

# Fun��o para renderizar o tabuleiro com estilo customizado
def render_tabuleiro_customizado(board):
    return chess.svg.board(
        board=board, 
        size=320,  # Reduzindo o tamanho do tabuleiro (20% menor)
        style="""
            .square.light { fill: #ffffff; }  /* Casas claras em branco */
            .square.dark { fill: #8FBC8F; }  /* Casas escuras em verde */
        """
    )

# Configura��o do tabuleiro com FEN
st.markdown("### Configura��o do Tabuleiro")
fen_input = st.text_input(
    "Insira a nota��o FEN para configurar o tabuleiro:", 
    value=st.session_state.current_board.fen()
)

if st.button("Atualizar Tabuleiro com FEN"):
    try:
        st.session_state.current_board.set_fen(fen_input)
        st.success("Tabuleiro atualizado com sucesso!")
    except ValueError:
        st.error("Nota��o FEN inv�lida. Por favor, insira uma nota��o correta.")

# Formul�rio para entrada dos dados
st.markdown("### Adicionar Nova Etapa")
with st.form("mhd_form"):
    etapa = st.selectbox("Selecione a Etapa", list(perguntas.keys()))
    st.markdown(f"**Dica:** {perguntas[etapa]}")  # Atualiza a dica dinamicamente com base na sele��o
    descricao = st.text_area("Descreva a etapa:", height=100)

    # Visualizar tabuleiro configurado
    st.markdown("### Tabuleiro Atual")
    st.image(render_tabuleiro_customizado(st.session_state.current_board), use_container_width=True)

    submitted = st.form_submit_button("Adicionar Etapa")
    if submitted:
        if descricao.strip():
            nova_entrada = pd.DataFrame({
                "Etapa": [etapa],
                "Descri��o": [descricao],
                "FEN": [st.session_state.current_board.fen()]
            })
            st.session_state.mhd_data = pd.concat([st.session_state.mhd_data, nova_entrada], ignore_index=True)
            st.success(f"Etapa '{etapa}' adicionada com sucesso!")
        else:
            st.error("A descri��o n�o pode estar vazia!")

# Exibi��o da tabela din�mica
st.subheader("Tabela do Modelo Hipot�tico-Dedutivo")
if not st.session_state.mhd_data.empty:
    for index, row in st.session_state.mhd_data.iterrows():
        st.markdown(f"**Etapa:** {row['Etapa']}")
        st.markdown(f"**Descri��o:** {row['Descri��o']}")
        st.image(render_tabuleiro_customizado(chess.Board(row['FEN'])), use_column_width=True)
else:
    st.info("Nenhuma etapa adicionada ainda.")

# Exportar a tabela para CSV
st.markdown("### Exporta��o de Dados")
if not st.session_state.mhd_data.empty:
    csv_data = st.session_state.mhd_data.to_csv(index=False)
    st.download_button(
        label="Baixar Tabela como CSV",
        data=csv_data,
        file_name="mhd_xadrez.csv",
        mime="text/csv"
    )
else:
    st.info("Nenhum dado dispon�vel para exporta��o.")