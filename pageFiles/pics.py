import streamlit as st
import sqlite3, io
from PIL import Image

def page_pics():
    criar_tabela()

    st.header('Dê uma olhada em nossos produtos!', anchor=False, divider=True)
    
    cols1, cols2 = st.columns([15,35])
    with cols1:
        st.subheader('Selecione por categoria: ', anchor=False)
    with cols2:
        cat_selected = st.pills('a', ['Todos'] + listar_categorias(), label_visibility='collapsed')

    if cat_selected == 'Todos': 
        for cat in listar_categorias():
            listar_produtos_categoria(cat)  
            st.divider() 
    elif not cat_selected:
        pass
    
    else:
        listar_produtos_categoria(cat_selected)  
        st.divider()  

    # else para todas as categorias
        
def carregar_produtos():
    try:
        return sqlite3.connect('produtos.db')
    except:
        st.error('Não conectou ao BD')

def criar_tabela(): # Criação da Tabela de Produtos
    con = carregar_produtos()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            price REAL,
            dados BLOB 
        )
    """
    )

    con.commit()
    cursor.close()
    con.close()

def listar_produtos():
    con = carregar_produtos()
    cursor = con.cursor()

    cursor.execute('SELECT nome FROM produtos')
    try:
        nomes = [linha[0] for linha in cursor.fetchall()]
    
        return nomes
    except:
        cursor.close()
        con.close()

def listar_produtos_categoria(categoria: str):
    con = carregar_produtos()
    cursor = con.cursor()

    cursor.execute("SELECT nome, price, imagem FROM produtos WHERE categoria = ? AND imagem IS NOT NULL", (categoria,))
    results = cursor.fetchall()

    if results:
            prod_page = 5
            total_paginas = (len(results) - 1) // prod_page + 1

            cols = st.columns([90,10])
            with cols[0]:
                st.subheader(f'{categoria.upper()} - {len(results)} Itens' if len(results) > 1 else f'{categoria.upper()} - 1 Item', anchor=False)
            with cols[1]:
                pagina = st.number_input(f'Página 1 a {total_paginas}', max_value=total_paginas, step=1, min_value=1, value=1, key=f'numInp{categoria}', label_visibility='collapsed')
            
            inicio = (pagina - 1) * prod_page
            fim = inicio + prod_page
            prod_pagina = results[inicio:fim]

            colunas = st.columns(5)  # Cria 5 colunas
            for idx, (nome, preco, imagem_blob) in enumerate(prod_pagina):
                imagem = redimensionar_imagem(imagem_blob)
                with colunas[idx % 5]:  # Posiciona o produto na coluna correspondente
                    st.image(imagem, caption=f"{nome} - R${preco:.2f}", use_container_width=True)
    else:
        st.warning(f"Nenhum produto com foto encontrado para a categoria '{categoria}'.")

    cursor.close()
    con.close()

def listar_categorias():
    con = carregar_produtos()
    cursor = con.cursor()

    cursor.execute('''SELECT DISTINCT categoria 
                   FROM produtos
                   WHERE categoria IN(
                   SELECT DISTINCT categoria
                   FROM produtos
                   WHERE imagem IS NOT NULL
                   ) 
                   ORDER BY categoria''')
    try:
        cats = [linha[0] for linha in cursor.fetchall()]
    
        return cats
    except:
        cursor.close()
        con.close()

def atualizar_imagem(produto, imagem_binaria):
    con = carregar_produtos()
    cursor = con.cursor()
    try:
        # Atualizar a coluna 'imagem' do produto
        cursor.execute(
            "UPDATE produtos SET imagem = ? WHERE nome = ?",
            (imagem_binaria, produto),
        )
        con.commit()
        st.success("Imagem adicionada com sucesso ao produto!")
    except sqlite3.Error as e:
        st.error(f"Erro ao atualizar a imagem no banco de dados: {e}")
    finally:
        cursor.close()
        con.close()
        st.rerun()
    
def redimensionar_imagem(imagem_blob, altura_padrao=310):
    imagem = Image.open(io.BytesIO(imagem_blob))
    proporcao = altura_padrao / imagem.height
    imagem_redimensionada = imagem.resize((325, altura_padrao))
    return imagem_redimensionada