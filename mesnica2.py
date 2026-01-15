import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Postavke aplikacije za siječanj 2026.
st.set_page_config(page_title="Kojundžić Mesnica", page_icon="🥩", layout="wide")

# Funkcija za sigurno učitavanje slika s weba
def load_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# --- MODERNI PREMIUM DIZAJN ---
st.markdown(
    """
    <style>
    .stApp { background-color: #f8f9fa; }
    .product-card {
        background-color: white; border-radius: 20px; padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #efefef;
        margin-bottom: 25px; text-align: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #8B0000 0%, #5d0000 100%);
        color: white !important; border-radius: 12px; border: none;
        font-weight: 600; width: 100%; height: 3.5em;
    }
    [data-testid="stSidebar"] { background-color: #1a1a1a; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'cart' not in st.session_state:
    st.session_state.cart = []

proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50, "slika": "images.unsplash.com"},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50, "slika": "images.unsplash.com"},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.20, "slika": "images.unsplash.com"},
    {"id": 4, "ime": "Buđola", "cijena": 19.50, "slika": "images.unsplash.com"},
    {"id": 5, "ime": "Dimljeni vrat", "cijena": 15.00, "slika": "images.unsplash.com"},
    {"id": 6, "ime": "Slavonska kobasica", "cijena": 14.50, "slika": "images.unsplash.com"},
    {"id": 7, "ime": "Domaća salama", "cijena": 16.00, "slika": "images.unsplash.com"},
    {"id": 8, "ime": "Čvarci", "cijena": 22.00, "slika": "images.unsplash.com"},
]

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🥩 KOJUNDŽIĆ</h2>", unsafe_allow_html=True)
    izbor = st.sidebar.radio("NAVIGACIJA", ["🛍️ TRGOVINA", "🛒 KOŠARICA", "ℹ️ O NAMA"])

if izbor == "🛍️ TRGOVINA":
    st.title("Domaća Ponuda")
    cols = st.columns(2)
    for i, p in enumerate(proizvodi):
        with cols[i % 2]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            # Sigurno učitavanje slike
            slika_obj = load_image(p["slika"])
            if slika_obj:
                st.image(slika_obj, use_container_width=True)
            
            st.markdown(f"### {p['ime']}")
            st.markdown(f"<p style='color: #8B0000; font-size: 20px; font-weight: bold;'>{p['cijena']:.2f} € / kg</p>", unsafe_allow_html=True)
            qty = st.number_input(f"Količina (kg)", min_value=0.0, step=0.5, key=f"q_{p['id']}")
            
            if st.button("DODAJ U KOŠARICU", key=f"b_{p['id']}"):
                if qty >= 0.5:
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.toast(f"Dodan {p['ime']}!")
            st.markdown('</div>', unsafe_allow_html=True)

elif izbor == "🛒 KOŠARICA":
    st.title("Vaša Narudžba")
    if not st.session_state.cart:
        st.info("Košarica je prazna.")
    else:
        ukupno = sum(item['price'] for item in st.session_state.cart)
        email_stavke = "".join([f"- {item['ime']}: {item['qty']} kg%0D%0A" for item in st.session_state.cart])
        
        st.markdown(f"### Ukupno: {ukupno:.2f} €")
        with st.form("forma"):
            ime = st.text_input("Ime i Prezime*")
            mob = st.text_input("Mobitel*")
            adr = st.text_input("Adresa*")
            grad = st.text_input("Grad i Poštanski broj*")
            regija = st.selectbox("Dostava", ["Hrvatska", "Inozemstvo (EU)"])
            
            if st.form_submit_button("POŠALJI"):
                mail_link = f"mailto:tomislavtomi90@gmail.com: {ime}%0D%0AStavke:%0D%0A{email_stavke}"
                st.markdown(f'<a href="{mail_link}"><button style="width:100%; padding:20px; background:#D44638; color:white; border:none; border-radius:10px; cursor:pointer;">📧 KLIKNI ZA SLANJE MAILOM</button></a>', unsafe_allow_html=True)

elif izbor == "ℹ️ O NAMA":
    st.title("Mesnica Kojundžić")
    st.write("Sisak, Trg Josipa Mađerića 1")
    st.map(pd.DataFrame({'lat': [45.4832], 'lon': [16.3761]}))
