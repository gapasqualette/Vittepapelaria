import streamlit as st

def page_home():
    st.header('Seja bem-vindo a Vitté Papelaria!', anchor=False, divider=True)

    if 'foto' not in st.session_state:
        st.session_state.foto = 0

    fotosVitrine = [
        {"nome": "Welcome", 'descricao': 'É muito bom ter você nos visitando!', 'id': 1, 'imagem': "assets/Welcome.jpeg"},
        {'nome': "Personalizados", 'descricao': 'Fazemos os personalizados do seu jeitinho e do tema que desejar!', "id": 2, "imagem": "assets/Personalizados.jpeg"},
        {'nome': "Pagamento", 'descricao': 'Aceitamos diversas formas de pagamento!', 'id': 3, "imagem": 'assets/Pagamento.jpeg'},
        {"nome": "Atendimento", 'descricao': 'Fique à vontade para tirar dúvidas conosco!', "id": 4, "imagem": "assets/Atendimento.jpeg"},
        {'nome': 'Contato', 'descricao': 'Só apontar o celular para QRCode ou pressione os botões de nossas redes sociais!', 'id': 5, 'imagem': 'assets/Contato.jpeg'}
    ]
    
    cols = st.columns([20,60,20])
    with cols[1]:
        foto = fotosVitrine[st.session_state.foto]
        st.image(foto['imagem'], caption=foto['descricao'],use_container_width=True)
    
    btncols = st.columns([35,15,15,35])
    with btncols[1]:
        if st.session_state.foto > 0:
            if st.button('', icon=':material/arrow_back_ios_new:', use_container_width=True, key='btnBack', type='primary'):
                st.session_state.foto = st.session_state.foto - 1
                with st.spinner():
                    st.rerun()

    with btncols[2]:
        if st.session_state.foto < len(fotosVitrine) - 1:
            if st.button('', icon=':material/arrow_forward_ios:', use_container_width=True, key='btnNext', type='primary'):
                st.session_state.foto = st.session_state.foto + 1           
                with st.spinner():    
                    st.rerun()
    