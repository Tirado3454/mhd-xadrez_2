import streamlit as st
import chess
import chess.svg

# Configuração inicial da interface
st.set_page_config(page_title="Editor de Tabuleiro de Xadrez", layout="centered")
st.markdown(
    """
    <h1 style='font-size:32px; display: flex; align-items: center;'>
    <img src='data:image/png;base64,<insira_o_base64_gerado_da_logo_aqui>' style='height:50px; margin-right:10px;'> Editor de Tabuleiro de Xadrez
    </h1>
    """,
    unsafe_allow_html=True
)
st.write("Configure e visualize posições personalizadas no tabuleiro de xadrez.")

# Inicialização do tabuleiro
if "current_board" not in st.session_state:
    st.session_state.current_board = chess.Board()

# Função para renderizar o tabuleiro com estilo customizado
def render_tabuleiro_customizado(board):
    return chess.svg.board(
        board=board, 
        size=320,  # Reduzindo o tamanho do tabuleiro
        style="""
            .square.light { fill: #ffffff; }  /* Casas claras em branco */
            .square.dark { fill: #8FBC8F; }  /* Casas escuras em verde */
        """
    )

# Configuração do tabuleiro com FEN
st.markdown("### Configuração do Tabuleiro")
fen_input = st.text_input(
    "Insira a notação FEN para configurar o tabuleiro:", 
    value=st.session_state.current_board.fen()
)

if st.button("Atualizar Tabuleiro com FEN"):
    try:
        st.session_state.current_board.set_fen(fen_input)
        st.success("Tabuleiro atualizado com sucesso!")
    except ValueError:
        st.error("Notação FEN inválida. Por favor, insira uma notação correta.")

# Visualizar tabuleiro configurado
st.markdown("### Tabuleiro Atual")
st.image(render_tabuleiro_customizado(st.session_state.current_board), use_container_width=True)

