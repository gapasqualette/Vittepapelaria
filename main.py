import streamlit as st
import streamlit_option_menu as sto
import base64

from streamlit import sidebar as sd
from pageFiles.pics import page_pics
from pageFiles.cart import page_cart
from pageFiles.manager import page_manager
from pageFiles.home import page_home

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

instalUrl = st.secrets["instaUrl"]
wppUrl  = st.secrets["wppUrl"]    

st.set_page_config(layout='wide')
imagePath = 'assets/bgVitte3.jpg'
base64_image = get_base64_of_bin_file(imagePath)

page_bg_img = f'''
    <style>
    [data-testid="stApp"] {{
        background: rgb(230,138,247);
        background: linear-gradient(180deg, rgba(230,138,247,0.8547794117647058) 14%, rgba(255,200,87,0.700717787114846) 41%, rgba(255,200,87,0.7) 62%, rgba(56,202,232,0.8519782913165266) 93%);
    }}
    [data-testid="stHeader"] {{
        background: rgba(0, 0, 0, 0);
    }}
    [data-testid="stSidebar"] {{
        background: rgb(255,255,255,1)
    }}
    </style>
    '''

st.markdown(page_bg_img, unsafe_allow_html=True)

st.logo('assets/LOGO.png', size='large')
sd.subheader('''Vitté Papelaria Criativa
- Por Esther | Desde 2015
- Papelaria Personalizada 📦🌍💕
- Design Gráfico 💻
- Cabo Frio - RJ 📍
- Enviamos para todo o Brasil ✈️''')

sd.divider()
sd.link_button('Whatsapp', url= wppUrl, icon=':material/call:',use_container_width=True,type='primary')
sd.link_button('Instagram', url= instalUrl, icon=':material/photo_camera:',use_container_width=True, type='primary')

#sd.subheader('Feito por Guilherme Pasqualette')

sd.markdown("""
    <style>
    /* Configura a posição do conteúdo no fundo da sidebar */
    .sidebar-footer {
        position: absolute;
        bottom: -425px; /* Ajuste conforme necessário */
        width: 100%;
        text-align: center;
        font-size: 0.85rem;
        color: gray;
    }
    </style>
""", unsafe_allow_html=True)

sd.markdown('<div class = "sidebar-footer">Feito por Guilherme Pasqualette </div>', unsafe_allow_html=True)

page = sto.option_menu(None, 
    options=['Home', 'Mostruário', 'Orçamento | Pedido', 'Administrador'], 
    orientation='horizontal', 
    menu_icon='None', 
    icons=['house', 'camera', 'cart', 'lock']
    )

if page == 'Home':
    page_home()

elif page == 'Mostruário':
    page_pics()

elif page == 'Orçamento | Pedido':
    st.header('Faça seu orçamento conosco!', anchor=False, divider=True)
    page_cart()

elif page == 'Administrador':
    page_manager()