import streamlit as st
import sqlite3, time
from datetime import datetime, timedelta
def page_cart():

    tel = st.secrets["tel"]
    dataNow = datetime.today()
    freteDict = {
            'Braga - Retirada': 0,
            'Peró': 12,
            'Jardim Esperança': 15,
            'Gamboa': 10,
            'São Cristóvão': 7,
            'Parque Burle': 7,
            'Jardim Caiçara': 7,
            'Guarani': 7,
            'Passagem': 7,
            'Braga': 7,
            'Centro': 7,
            'Arraial do Cabo': 20,
            'Búzios': 35,
            'São Pedro da Aldeia': 20
    }

    if "pedidos" not in st.session_state:
        st.session_state.pedidos = []

    if 'form' not in st.session_state:
        st.session_state.form = {}

    if 'confirmed' not in st.session_state:
        st.session_state.confirmed = False
    
    cols = st.columns([60,10,10,10,10])

    with cols[0]:
        prod = st.selectbox('Produtos Disponíveis', listar_produtos(), placeholder='Selecione um produto',label_visibility='collapsed')

    with cols[1]:
        qtd = st.number_input('Quantidade', step=1, min_value=1, value=1, label_visibility='collapsed')

    with cols[2]:
        if prod:
            price = search_price(prod)
            total = qtd * price
            st.text_input('a', value=f'Valor: R${total:.2f}', disabled=True, label_visibility='collapsed')

    with cols[3]:
        cart_btn = st.button('', use_container_width=True, icon=':material/add_shopping_cart:', type='primary')

    with cols[4]:
        if st.button('', use_container_width=True, icon=':material/shopping_cart_off:', type='primary'):
            if st.session_state.pedidos:
                st.session_state.pedidos = []
                st.toast('Carrinho esvaziado!', icon=':material/shopping_cart:')
            else:
                st.toast('Carrinho já vazio!', icon=':material/shopping_cart:')
    
    if st.session_state.pedidos:
        st.subheader(f'Itens - Quantidade: {total_qtd_cart()}', anchor=False)

    if cart_btn:
        add_to_cart(prod, qtd)
        st.toast('Produto no carrinho!', icon=':material/shopping_cart:')
        st.rerun()

    cols2 = st.columns([50,10,25])
    if st.session_state.pedidos:
        st.caption('Clique no pedido se deseja remover do carrinho!')
        for i, pedido in enumerate(st.session_state.pedidos):
            with cols2[0]:
                if st.button(f'Item {i+1} -> {pedido['quantidade']} x {pedido['produto']} - R${pedido['total']:,.2f} '':material/delete:''', key=f'prod{i}', use_container_width=True, type='primary'):
                    del st.session_state.pedidos[i]
                    st.rerun()

    with cols2[1]:
        if st.session_state.pedidos:
            altura = len(st.session_state.pedidos) * 55
            st.markdown(
            f"""
            <style>
            .vl {{
                border-left: 3px solid purple;
                height: {altura}px; /* Altura da linha */
                position: absolute;
                left: 50%; /* Alinhamento horizontal */
                margin-left: -1px; /* Centralização */
                top: 15;
            }}
            </style>
            """,
            unsafe_allow_html=True,
    )
            st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)

    with cols2[2]:
        if len(st.session_state.pedidos) > 0:
            total_pedido = total_cart()
            st.markdown(f'''<h1 style = "font-size: 30px; vertical-align: botton; height: 50px"> <center>Total: R${total_pedido: .2f}</center></h1>''', unsafe_allow_html=True)
            st.divider()    
            if st.button('Confirmar Pedido', type='primary', icon=':material/task_alt:', use_container_width=True):
                confirm_order()
        
    if st.session_state.confirmed: 
        if st.session_state.pedidos:           
            st.divider()
            colsForm = st.columns([50,10,50,10,50], gap='medium')
            with colsForm[0]:
                nomeResponsável = st.text_input('Nome do Cliente *')
                nome = st.text_input('Nome do Aniversariante *')
                idade = st.text_input('Idade Aniversariante *', placeholder='8 anos | 8 meses')
                frete = st.selectbox('Frete *', freteDict.keys(), index=0)
                valor_frete = freteDict.get(frete)

                if total_qtd_cart() <= 3 and total_qtd_cart() >= 0:
                    dataPrev = dataNow + timedelta(days=5)
                elif total_qtd_cart() <=10:
                    dataPrev = dataNow + timedelta(days=10)
                else:
                    dataPrev = dataNow + timedelta(days=15)

            with colsForm[2]:
                telefone = st.text_input('Celular (Somente Números com DDD) *', max_chars=11, placeholder='22123456789')
                data_festa = st.date_input(f'''Data da Festa **(Prazo mínimo de confecção - 5 dias úteis)***''',format='DD/MM/YYYY', value=dataPrev + timedelta(days=5), min_value=dataPrev + timedelta(days=5))
                tema = st.text_input('Tema do Pedido *')
                obs = st.text_area('Observações do pedido', placeholder='''- Caso queira antecipar o pedido (Urgência), favor mencionar a data.\n- Caso queira envio via Correios, digitar o CEP.''', height=70)
                
                if not obs:
                    obs = "Sem Observação"
                    
                if not nomeResponsável or not telefone.isnumeric() or not tema or not nome or not idade or not frete or not data_festa:
                    st.error('Preencher os dados obrigatórios!', icon=':material/warning:')
                else:
                    pedidos_formatados = "\n".join([f"  - {pedido['produto']} x {pedido['quantidade']} = Total: R${pedido['total']:.2f}" for pedido in st.session_state.pedidos])
                        
                    msg = ("Oi, gostaria de confirmar o meu pedido com a Vitté Papelaria\n"
                            
                        f"- Nome Cliente: {nomeResponsável}\n"
                        f"- Nome Aniversariante: {nome}\n"
                        f"- Idade Aniversariante: {idade}\n"
                        f"- Tema: {tema}\n"
                        f"- Data da Festa: {data_festa.strftime('%d/%m/%Y')}\n"
                        f"- Valor Total com Frete: R$ {total_cart() + valor_frete:.2f}\n"
                        f"- Observação: {obs}\n\n"
                        f"***\tItens do Pedido\t***\n\n"
                        f"{pedidos_formatados}")
                    
                    msg_codificada = msg.replace("\n", "%0A")
                    linkwpp = f'https://wa.me/{tel}?text={msg_codificada}'
            
            with colsForm[4]:
                st.markdown(f"""
                    ### Detalhes do Pedido:
                    - **Data de Entrega (Estipulada): {dataPrev.strftime('%d/%m/%Y') if len(st.session_state.pedidos) > 0 else "Faça antes seu pedido!"}**
                    - **Pedido: R$ {total_cart():.2f}**
                    - **Frete: R$ {valor_frete:.2f}**
                    - **Total:** **R$ {total_cart() + valor_frete:.2f}**
                    """)
                
                if nomeResponsável and telefone.isnumeric() and tema and nome and idade and frete and data_festa and st.session_state.pedidos:
                    st.divider()
                    st.link_button('Confirmar Pedido', url=linkwpp, icon=':material/shopping_cart:', type='primary', use_container_width=True)

def add_to_cart(product: str, qtd: int):
    price = search_price(product)
    total = qtd * price
    st.session_state.pedidos.append({"produto": product, "quantidade": qtd , "total": total})

def carregar_produtos(): # DB dos produtos
    try:
        return sqlite3.connect('produtos.db')
    except:
        st.error('Erro no carregamento do catálogo de fotos')

def listar_produtos():
    con = carregar_produtos()
    cursor = con.cursor()

    cursor.execute('SELECT nome FROM produtos ORDER BY nome')
    try:
        nomes = [linha[0] for linha in cursor.fetchall()]
    
        return nomes
    except:
        cursor.close()
        con.close()

def search_price(prod: str):
    con = carregar_produtos()
    cursor = con.cursor()

    try:
        cursor.execute('SELECT price FROM produtos WHERE nome = ?', (prod,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            st.error(f'Não foi achado o preço do produto {prod}')
    
    except:
        st.error('Erro na busca!')

    finally:
        cursor.close()
        con.close()

def total_cart():
    return sum(pedido['total'] for pedido in st.session_state.pedidos)

def total_qtd_cart():
    return sum(pedido['quantidade'] for pedido in st.session_state.pedidos)

def confirm_order():
    st.session_state.confirmed = True
    st.rerun()