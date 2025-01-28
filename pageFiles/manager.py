import streamlit as st
import sqlite3, yaml
import streamlit_authenticator as auth

from yaml.loader import SafeLoader
from streamlit import sidebar as sd
def page_manager():
    if 'act' not in st.session_state:
        st.session_state.act = 'Inicio'

    if 'sub_act' not in st.session_state:
        st.session_state.sub_act = None
    
    if 'produto' not in st.session_state:
        st.session_state.produto = None

    if 'logged' not in st.session_state:
        st.session_state.logged = False
     
    st.markdown(
        """
        <style>
        .vl {
            border-left: 3px solid purple;
            height: 600px; /* Altura da linha */
            position: absolute;
            left: 50%; /* Alinhamento horizontal */
            margin-left: -1px; /* Centralização */
            top: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
    """
    <style>
    hr.solid {
        border-top: 2px solid #bbb;
        border-color: #8e57ff
    }
    </style>
    """,
    unsafe_allow_html=True
) 
    if not st.session_state.logged:
        st.header('Login - Admin', anchor=False, divider=True)
        logincols = st.columns([40,40,20])
        with logincols[0]:
            username = st.text_input('a', placeholder='Username', label_visibility='collapsed')
        with logincols[1]:
            password = st.text_input('a', placeholder='Password', label_visibility='collapsed', type='password')
        with logincols[2]:
            login_btn = st.button('', icon=':material/login:', type='primary', use_container_width=True)
        if username and password and login_btn:
            nameAdmin = check_auth(username, password)
            if nameAdmin:
                st.session_state.logged = True
                st.rerun()

    if st.session_state.logged:
        st.header(f'Página do administrador', anchor=False, divider=True)
        cols = st.columns([25,10,75])
        listProd = ['Adicionar Produtos', 'Editar Produto', 'Remover Produto']
        listCliente = ['Adicionar Cliente', 'Editar Cliente', 'Apagar Cliente','Alterar Status de Pedidos', 'Dashboard']

        with cols[0]:
            st.subheader('Produtos', anchor=False, divider=True)
            if st.button(listProd[0], type='primary', use_container_width=True, key='btnAddProd', icon=':material/add:'):
                st.session_state.sub_act = listProd[0]
            if st.button(listProd[1], type='primary', use_container_width=True, key='btnEdtProd', icon=':material/edit:'):
                st.session_state.sub_act = listProd[1]
            if st.button(listProd[2], type='primary', use_container_width=True, key='btnRmvProd', icon=':material/delete_forever:'):
                st.session_state.sub_act = listProd[2]

            st.subheader('Clientes | Pedidos', anchor=False, divider=True) 
            if st.button(listCliente[0], type='primary', icon=':material/person_add:', use_container_width=True):
                st.session_state.sub_act = listCliente[0] 
            if st.button(listCliente[1], type='primary', icon=':material/border_color:', use_container_width=True):
                st.session_state.sub_act = listCliente[1] 
            if st.button(listCliente[2], type='primary', icon=':material/person_remove:', use_container_width=True):
                st.session_state.sub_act = listCliente[2] 
            if st.button(listCliente[3], type='primary', icon=':material/edit_document:', use_container_width=True):
                st.session_state.sub_act = listCliente[3] 
            if st.button(listCliente[4], type='primary', icon=':material/monitoring:', use_container_width=True):
                st.session_state.sub_act = listCliente[4] 
        
        with cols[1]:
            st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)

        with cols[2]:
            st.header(f'{'Gerenciamento Vitté Papelaria' if st.session_state.sub_act == None else 'Gerenciamento Vitté Papelaria - ' + st.session_state.sub_act}')
            st.markdown('<hr class = "solid" </hr>', unsafe_allow_html=True)
            
            ########### Adicionar Produto ############
            if st.session_state.sub_act == listProd[0]:
                colsAdd = st.columns([30,30,30,10], gap='medium')
                with colsAdd[0]:
                    nomeNew = st.text_input('a', placeholder='Nome do Produto', label_visibility='collapsed')
                with colsAdd[1]:
                    precoNew = st.text_input('b', placeholder='Preço do Produto', label_visibility='collapsed')
                with colsAdd[2]:
                    catNew = st.text_input('c', placeholder='Categoria do Produto', label_visibility='collapsed')                   
                
                imageNew = st.file_uploader(label=f'Nova Imagem para {nomeNew.upper()}', type=['png', 'jpeg', 'jpg'], accept_multiple_files=False, label_visibility='collapsed')
                
                with colsAdd[3]:
                    if nomeNew and precoNew and catNew and imageNew:
                        if st.button('', type='primary', icon=':material/add:', use_container_width=True):
                            add_product(nomeNew.upper(), precoNew, catNew, imageNew)
                            sort_name_produto()
                            reload_page()

            ############# Edição Produtos ##############
            elif st.session_state.sub_act == listProd[1]:
                prod = st.selectbox('A', listar_produtos(), placeholder='Pesquise o produto desejado', label_visibility='collapsed', key=f'editProd')
                searchprod = buscar_produto_nome(prod)
                if searchprod:
                    nome, preco, categoria, imagem_bin = searchprod
                    st.divider()
                    colsEd = st.columns([35,10,25,30], gap='medium')
                    with colsEd[0]:    
                        nomeEdit = st.text_input('q', nome, placeholder='Produto', label_visibility='collapsed')
                    with colsEd[1]:
                        precoEdit = st.text_input('w', preco, placeholder='Preço do Produto', label_visibility='collapsed')
                    with colsEd[2]:
                        catEdit = st.text_input('e',categoria, placeholder='Categoria do Produto', label_visibility='collapsed')
                    with colsEd[3]:
                        if nomeEdit and precoEdit and catEdit:    
                            if st.button('Editar Informações Básicas', type='primary', icon=':material/edit:', use_container_width=True):
                                edit_product(nomeEdit.upper(), precoEdit, catEdit, nome)
                                sort_name_produto()
                                reload_page()                  

                    colsEd2 = st.columns([30,10,60])        
                    if imagem_bin:
                        with colsEd2[0]:
                            st.image(imagem_bin, caption=f'Imagem atual: {nome} - R${preco: .2f}', width=200)
                        with colsEd2[2]:
                            imageEdit = st.file_uploader(f'Nova Imagem para {nome}', type=['png', 'jpeg', 'jpg'], accept_multiple_files=False)
                            if imageEdit:
                                if st.button('Editar Foto do Produto', type='primary', icon=':material/add_a_photo:'):
                                    atualizar_imagem(nome, imageEdit)
                                    reload_page()

            ############## Remoção Produto ##############
            elif st.session_state.sub_act == listProd[2]:
                colsDel = st.columns([80,10], gap='medium')
                with colsDel[0]:
                    prod = st.selectbox('A', listar_produtos(), placeholder='Pesquise o produto desejado', label_visibility='collapsed', key=f'delProd')
                with colsDel[1]:
                    if st.button('', type='primary', icon=':material/delete_forever:', use_container_width=True):
                        delete_product(prod)
                        sort_name_produto()
                        reload_page()
            
            elif st.session_state.sub_act == listCliente[0]:
                colsAddClnt = st.columns([75,25]) # Nome e Celular
                with colsAddClnt[0]:
                    nomeNewClnt = st.text_input('Nome Completo do Cliente *')
                with colsAddClnt[1]:
                    telNewClnt = st.text_input('Telefone (Somente Números) *', max_chars=11)

                endNewClnt = st.text_input('Endereço c/Complemento *')        
                colsAddClnt2 = st.columns([40,40,15]) # Bairro, Cidade e Estado (Sigla)
                with colsAddClnt2[0]:
                    bairroNewClnt = st.text_input('Bairro *')
                with colsAddClnt2[1]:
                    CityNewClnt = st.text_input('Cidade *')
                with colsAddClnt2[2]:
                    StNewClnt = st.text_input('Estado (Sigla) *', max_chars=2)
                    if st.button('', icon=':material/person_add:', type='primary', use_container_width=True):
                        add_client(nomeNewClnt, telNewClnt, endNewClnt, bairroNewClnt, CityNewClnt, StNewClnt)
                        sort_name_client()
                        reload_page()
            
            elif st.session_state.sub_act == listCliente[1]:
                cliente = st.selectbox('a', listar_clients(), label_visibility='collapsed')
                searchClnt = buscar_cliente_nome(cliente)
                if searchClnt:
                    nome, telefone, endereço, bairro, cidade, estado = searchClnt
                    st.divider()
                    colsEdClnt = st.columns([75,25]) # Nome e Celular
                    with colsEdClnt[0]:
                        nomeEdClnt = st.text_input('Nome Completo do Cliente *', nome)
                    with colsEdClnt[1]:
                        telEdClnt = st.text_input('Telefone (Somente Números) *', telefone, max_chars=11)

                    endEdClnt = st.text_input('Endereço c/Complemento *', endereço)        
                    colsEdClnt2 = st.columns([40,40,15]) # Bairro, Cidade e Estado (Sigla)
                    with colsEdClnt2[0]:
                        bairroEdClnt = st.text_input('Bairro *', bairro)
                    with colsEdClnt2[1]:
                        CityEdClnt = st.text_input('Cidade *', cidade)
                    with colsEdClnt2[2]:
                        StEdClnt = st.text_input('Estado (Sigla) *', estado, max_chars=2)
                        if st.button('', icon=':material/edit:', type='primary', use_container_width=True):
                            edit_client(nomeEdClnt, telEdClnt, endEdClnt, bairroEdClnt, CityEdClnt, StEdClnt, cliente)
                            sort_name_client()
                            reload_page()
            
            elif st.session_state.sub_act == listCliente[2]:
                colsDelClnt = st.columns([80,10], gap='medium')
                with colsDelClnt[0]:
                    clnt = st.selectbox('A', listar_clients(), placeholder='Pesquise o cliente desejado', label_visibility='collapsed')
                with colsDelClnt[1]:
                    if st.button('', type='primary', icon=':material/delete_forever:', use_container_width=True):
                        delete_client(clnt)
                        sort_name_client()
                        reload_page()
            
#### Funções Carregamento DBs ####
def carregar_produtos():
    try:
        return sqlite3.connect('produtos.db')
    except:
        st.error('Não conectou ao BD')

def carregar_clients():
    try:
        return sqlite3.connect('clientes.db')
    except:
        st.error('Sem conexão a Clientes DB')

#### Funções Listagem Nomes ####
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

def listar_clients():
    con = carregar_clients()
    cursor = con.cursor()

    try:
        cursor.execute('SELECT nome FROM clientes ORDER BY nome')
        nomes = [linha[0] for linha in cursor.fetchall()]
        return nomes
    except sqlite3.Error as e:
        st.error(f'Erro ao listar os clientes: {e}')
    finally:
        cursor.close()
        con.close()

#### Fuções Busca por Nome ####
def buscar_produto_nome(nome: str):
    con = carregar_produtos()
    cursor = con.cursor()

    cursor.execute('SELECT nome, price, categoria, imagem FROM produtos WHERE nome = ?', (nome,))
    try:
        prod = cursor.fetchone()
        return prod
    except:
        cursor.close()
        con.close()

def buscar_cliente_nome(nome:str):
    con = carregar_clients()
    cursor = con.cursor()

    cursor.execute('SELECT nome, telefone, endereço, bairro, cidade, estado FROM clientes WHERE nome = ?', (nome,))
    try:
        clnt = cursor.fetchone()
        return clnt
    except sqlite3.Error as e:
        st.error(f'Erro na busca do cliente {e}')
    finally:
        cursor.close()
        con.close()

#### Funções Remoção ####
def delete_product(name: str):
    con = carregar_produtos()
    cursor = con.cursor()
    try:
        cursor.execute('DELETE FROM produtos WHERE nome = ?', (name,))
        st.toast(f'{name.upper()} apagado com sucesso!', icon=':material/check:')
    except sqlite3.Error as e:
        st.error(f"Erro ao apagar o produto do banco de dados: {e}")
    finally:
        con.commit()
        cursor.close()
        con.close()

def delete_client(name: str):
    con = carregar_clients()
    cursor = con.cursor()
    try:
        cursor.execute('DELETE FROM clientes WHERE nome = ?', (name,))
        st.toast(f'Cliente {name} removido com sucesso', icon=':material/check:')
    except sqlite3.Error as e:
        st.error(f'Erro ao remover o cliente: {e}')
    finally:
        con.commit()
        cursor.close()
        con.close()

#### Funções Edição ####
def edit_product(new_name: str, preco: str, categoria: str, produto:str):
    con = carregar_produtos()
    cursor = con.cursor()
    try:
        # Atualizar a coluna 'imagem' do produto
        cursor.execute(
            "UPDATE produtos SET nome = ?, price = ?, categoria = ? WHERE nome = ?",
            (new_name, preco, categoria, produto),
        )
        con.commit()
        st.toast(f"Informações do produto {new_name} atualizadas com sucesso ao produto!", icon=':material/check:')
    except sqlite3.Error as e:
        st.error(f"Erro ao atualizar a imagem no banco de dados: {e}")
    finally:
        cursor.close()
        con.close()

def edit_client(new_name: str, tel: str, endereco: str, bairro: str, cidade: str, estado: str, name:str):
    con = carregar_clients()
    cursor = con.cursor()
    try:
        # Atualizar a coluna 'imagem' do produto
        cursor.execute(
            "UPDATE clientes SET nome = ?, telefone = ?, endereço = ?, bairro = ?, cidade = ?, estado = ? WHERE nome = ?",
            (new_name, tel, endereco, bairro, cidade, estado, name),
        )
        con.commit()
        st.toast(f"Informações do cliente {new_name} atualizadas com sucesso ao produto!", icon=':material/check:')
    except sqlite3.Error as e:
        st.error(f"Erro ao atualizar a imagem no banco de dados: {e}")
    finally:
        cursor.close()
        con.close()

#### Funções Adicionar ####
def add_product(nome: str, preco: float, cat: str, image):
    con = carregar_produtos()
    cursor = con.cursor()
    imageBin = image.read()
    
    if nome.upper() in listar_produtos():
        st.toast('Produto já relacionado', icon=':material/warning:')
        cursor.close()
        con.close()
    else:    
        try:
            cursor.execute('INSERT INTO produtos (nome, price, categoria, imagem) VALUES (?, ?, ?, ?)', (nome, preco, cat, imageBin))
            st.toast(f'Produto {nome} adicionado com sucesso!', icon=':material/check:')
        except sqlite3.Error as e:
            st.error(f'Erro ao inserir o produto: {e}')
        finally:
            con.commit()
            cursor.close()
            con.close()

def add_client(nome: str, tel: str, endereço: str, bairro: str, cidade: str, estado: str):
    con = carregar_clients()
    cursor = con.cursor()

    if nome in listar_produtos():
        st.toast('Cliente já relacionado', icon=':material/warning:')
        cursor.close()
        con.close()
    else:   
        try:
            cursor.execute('INSERT INTO clientes (nome, telefone, endereço, bairro, cidade, estado) VALUES (?, ?, ?, ?, ?, ?)', (nome, tel, endereço, bairro, cidade, estado))
            st.toast(f'Cliente {nome} adicionado com sucesso!', icon=':material/check:')
        except sqlite3.Error as e:
            st.error(f'Erro ao inserir o cliente: {e}')
        finally:
            con.commit()
            cursor.close()
            con.close()

#### Ordenação ####
def sort_name_produto():
    con = carregar_produtos()
    cursor = con.cursor()

    try:
        cursor.execute('SELECT * FROM produtos ORDER BY nome')
    except sqlite3.Error as e:
        st.error(f'Erro na ordenação: {e}')
    finally:
        con.commit()
        cursor.close()
        con.close()

def sort_name_client():
    con = carregar_clients()
    cursor = con.cursor()

    try:
        cursor.execute('SELECT * FROM clientes ORDER BY nome')
    except sqlite3.Error as e:
        st.error(f'Erro na ordenação: {e}')
    finally:
        con.commit()
        cursor.close()
        con.close()

def atualizar_imagem(produto: str, imagem_binaria):
    con = carregar_produtos()
    cursor = con.cursor()
    imageBin = imagem_binaria.read()
    try:
        # Atualizar a coluna 'imagem' do produto
        cursor.execute(
            "UPDATE produtos SET imagem = ? WHERE nome = ?",
            (imageBin, produto),
        )
        con.commit()
        st.toast("Imagem adicionada com sucesso ao produto!")
    except sqlite3.Error as e:
        st.error(f"Erro ao atualizar a imagem no banco de dados: {e}")
    finally:
        cursor.close()
        con.close()


def listar_categorias():
    con = carregar_produtos()
    cursor = con.cursor()

    cursor.execute('''SELECT DISTINCT categoria 
                   FROM produtos ''')
    try:
        cats = [linha[0] for linha in cursor.fetchall()]
        return cats
    except:
        cursor.close()
        con.close()

def reload_page():
    st.session_state.sub_act = None
    st.rerun()

def check_auth(username, password):
    admin_credentials = st.secrets["admin_credentials"]
    if username in admin_credentials and admin_credentials[username]["password"] == password:
        return admin_credentials[username]["name"]
    return None