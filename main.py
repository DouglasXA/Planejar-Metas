
import streamlit as st

# Lista para armazenar as metas
metas = []


# Função para adicionar uma nova meta
def adicionar_meta(titulo, descricao, data_limite):
    metas.append({
        "Título": titulo,
        "Descrição": descricao,
        "Data Limite": data_limite,
        "Progresso": 0,
        "Imagem": None
    })


# Função para atualizar o progresso de uma meta
def atualizar_progresso(index, novo_progresso):
    metas[index]["Progresso"] = novo_progresso


# Função para adicionar imagem a uma meta
def adicionar_imagem(index, imagem):
    metas[index]["Imagem"] = imagem


# Função principal do aplicativo
def main():
    st.title("Aplicativo de Definição de Metas")

    # Definindo novas metas
    st.subheader("Definir Nova Meta")
    novo_titulo = st.text_input("Título da Meta")
    novo_descricao = st.text_area("Descrição da Meta")
    novo_data_limite = st.date_input("Data Limite")

    if st.button("Adicionar Meta"):
        adicionar_meta(novo_titulo, novo_descricao, novo_data_limite)
        st.success("Meta adicionada com sucesso!")

    # Listando metas
    st.subheader("Metas Definidas")
    for i, meta in enumerate(metas):
        st.write(f"**{meta['Título']}** - {meta['Descrição']} (Data Limite: {meta['Data Limite']})")
        st.progress(meta['Progresso'])

        # Atualizar progresso
        novo_progresso = st.slider(f"Atualizar Progresso para {meta['Título']} (%)", 0, 100, meta['Progresso'])
        if st.button("Atualizar Progresso"):
            atualizar_progresso(i, novo_progresso)
            st.success("Progresso atualizado com sucesso!")

        # Adicionar imagem de realização
        imagem = st.file_uploader(f"Carregar Imagem para {meta['Título']}", type=["jpg", "png"])
        if imagem is not None:
            adicionar_imagem(i, imagem)
            st.success("Imagem adicionada com sucesso!")

        if meta['Imagem'] is not None:
            st.image(meta['Imagem'], caption="Imagem de Realização", use_column_width=True)


# Executando o aplicativo
if __name__ == "__main__":
    main()

