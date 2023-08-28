import streamlit as st
import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('metas.db')
cursor = conn.cursor()

# Criar tabela se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY,
        titulo TEXT,
        descricao TEXT,
        data_limite DATE,
        progresso INTEGER,
        categoria TEXT
    )
''')
conn.commit()

# Função para adicionar uma nova meta
def adicionar_meta(titulo, descricao, data_limite, categoria):
    cursor.execute('INSERT INTO metas (titulo, descricao, data_limite, progresso, categoria) VALUES (?, ?, ?, ?, ?)',
                   (titulo, descricao, data_limite, 0, categoria))
    conn.commit()

# Função para atualizar o progresso de uma meta
def atualizar_progresso(meta_id, novo_progresso):
    cursor.execute('UPDATE metas SET progresso = ? WHERE id = ?', (novo_progresso, meta_id))
    conn.commit()

# Função para excluir uma meta
def excluir_meta(meta_id):
    cursor.execute('DELETE FROM metas WHERE id = ?', (meta_id,))
    conn.commit()

# Função para buscar todas as metas
def buscar_metas(categoria=None):
    if categoria:
        cursor.execute('SELECT id, titulo, descricao, data_limite, progresso FROM metas WHERE categoria = ?', (categoria,))
    else:
        cursor.execute('SELECT id, titulo, descricao, data_limite, progresso FROM metas')
    return cursor.fetchall()

def main():
    st.title("Aplicativo de Definição de Metas")

    # Definindo novas metas
    st.subheader("Definir Nova Meta")
    novo_titulo = st.text_input("Título da Meta")
    novo_descricao = st.text_area("Descrição da Meta")
    novo_data_limite = st.date_input("Data Limite")
    categoria = st.selectbox("Categoria da Meta", ["Pessoal", "Profissional", "Familiar"])

    if st.button("Adicionar Meta"):
        adicionar_meta(novo_titulo, novo_descricao, novo_data_limite, categoria)
        st.success("Meta adicionada com sucesso!")

    # Listando metas
    st.subheader("Metas Definidas")
    categorias = {
        "Pessoal": "blue",
        "Profissional": "green",
        "Familiar": "orange"
    }
    for cat, cor in categorias.items():
        st.write(f"## {cat}", f"Categoria: {cat}", key=f"header_{cat}")
        metas = buscar_metas(cat)
        if metas:
            for meta in metas:
                meta_id, titulo, descricao, data_limite, progresso = meta

                with st.expander(titulo, key=f"expander_{meta_id}", expanded=True):
                    st.text(f"Descrição: {descricao}")
                    st.text(f"Data Limite: {data_limite}")
                    st.progress(progresso, f"Progresso: {progresso}%")
                    novo_progresso = st.slider(f"Atualizar Progresso (%)", 0, 100, progresso)
                    if st.button(f"Atualizar Progresso##{meta_id}"):
                        atualizar_progresso(meta_id, novo_progresso)
                        st.success("Progresso atualizado com sucesso!")
                    
                    st.button(f"Excluir Meta##{meta_id}", key=f"delete_{meta_id}", help=f"Excluir a meta '{titulo}'")
                    if st.button(f"Excluir Meta##{meta_id}", key=f"delete_{meta_id}"):
                        excluir_meta(meta_id)
                        st.success("Meta excluída com sucesso!")

if __name__ == "__main__":
    main()
