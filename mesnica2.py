import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Postavke aplikacije za 2026.
st.set_page_config(page_title="Kojundžić Mesnica | Tradicija Siska", page_icon="🥩", layout="wide")

@st.cache_data
def load_image(url):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# --- MODERNI DIZAJN ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; border-radius: 20px; padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #efefef;
        margin-bottom: 25px; text-align: center;
    }
    .price-tag { color: #8B0000; font-size: 22px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%);
        color: white !important; border-radius: 12px; height: 3.5em; width: 100%;
    }
    .info-box {
        background-color: #fff4f4; padding: 15px; border-radius: 12px;
        border-left: 5px solid #8B0000; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- POPIS ARTIKALA ---
proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50, "slika": "images.unsplash.com"},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50, "slika": "images.unsplash.com"},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.20, "slika": "images.unsplash.com"},
    {"id": 4, "ime": "Premium Buđola", "cijena": 19.50, "slika": "images.unsplash.com"},
    {"id": 5, "ime": "Dimljeni vrat", "cijena": 15.00, "slika": "images.unsplash.com"},
    {"id": 6, "ime": "Slavonska kobasica", "cijena": 14.50, "slika": "images.unsplash.com"},
    {"id": 7, "ime": "Domaća salama", "cijena": 16.00, "slika": "images.unsplash.com"},
    {"id": 8, "ime": "Hrskavi Čvarci", "cijena": 22.00, "slika": "images.unsplash.com"},
]

# --- NAVIGACIJA ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🥩 KOJUNDŽIĆ</h2>", unsafe_allow_html=True)
    izbor = st.radio("IZBORNIK", ["🛍️ TRGOVINA", "🛒 KOŠARICA", "🧼 HIGIJENA & HACCP", "🚜 DOBAVLJAČI", "ℹ️ O NAMA"])
    st.write("---")
    st.caption("Sisak 2026 | Domaća Prerada")

# --- STRANICA: TRGOVINA ---
if izbor == "🛍️ TRGOVINA":
    st.title("Ponuda domaćih delicija")
    st.markdown('<div class="info-box">📢 <b>Važno:</b> Trošak dostave nije uključen u cijenu mesa. Dostavu plaćate izravno kuriru prilikom preuzimanja.</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, p in enumerate(proizvodi):
        with cols[i % 2]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            img = load_image(p["slika"])
            if img: st.image(img, use_container_width=True)
            st.markdown(f"### {p['ime']}")
            st.markdown(f"<div class='price-tag'>{p['cijena']:.2f} € / kg</div>", unsafe_allow_html=True)
            
            qty = st.number_input(f"Odaberite kg", 1.0, 50.0, 1.0, 0.5, key=f"q_{p['id']}")
            
            if st.button("DODAJ U KOŠARICU", key=f"b_{p['id']}"):
                st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                st.toast(f"Dodano: {p['ime']} ({qty}kg)")
            st.markdown('</div>', unsafe_allow_html=True)

# --- STRANICA: KOŠARICA ---
elif izbor == "🛒 KOŠARICA":
    st.title("Pregled narudžbe")
    if not st.session_state.cart:
        st.info("Košarica je prazna.")
    else:
        za_meso = 0
        email_lista = ""
        for item in st.session_state.cart:
            st.write(f"✅ {item['ime']} - {item['qty']} kg = **{item['price']:.2f} €**")
            za_meso += item['price']
            email_lista += f"- {item['ime']}: {item['qty']}kg ({item['price']:.2f}€)%0D%0A"
        
        st.divider()
        st.subheader(f"Iznos za meso: {za_meso:.2f} €")
        st.warning("⚠️ Trošak dostave kurirska služba naplaćuje zasebno po preuzimanju pošiljke.")

        if st.button("🗑️ Isprazni košaricu"):
            st.session_state.cart = []
            st.rerun()
            
        with st.form("narudzba"):
            ime = st.text_input("Ime i Prezime*")
            mob = st.text_input("Mobitel*")
            adr = st.text_input("Adresa i Grad*")
            regija = st.selectbox("Regija dostave", ["Hrvatska", "Inozemstvo (EU)"])
            
            if st.form_submit_button("PRIPREMI E-MAIL NARUDŽBU"):
                if ime and mob and adr:
                    body = f"KUPAC: {ime}%0D%0AMOB: {mob}%0D%0AADRESA: {adr}%0D%0AREGIJA: {regija}%0D%0A%0D%0AARTIKLI:%0D%0A{email_lista}%0D%0A-----------------%0D%0ACijena mesa: {za_meso:.2f} EUR%0D%0A(Dostavu placa kupac kuriru pri preuzimanju)"
                    mail_link = f"mailto:tomislavtomi90@gmail.com_{ime}&body={body}"
                    
                    st.success("Narudžba pripremljena!")
                    st.markdown(f'<a href="{mail_link}"><button style="width:100%; height:50px; background:#D44638; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">📧 POŠALJI MAIL</button></a>', unsafe_allow_html=True)
                else:
                    st.error("Ispunite obavezna polja.")

# --- STRANICA: HIGIJENA ---
elif izbor == "🧼 HIGIJENA & HACCP":
    st.title("Sigurnost i Standardi")
    st.markdown("""
    Naša proizvodnja u Sisku strogo prati **HACCP standarde** za 2026. godinu. 
    Higijena je ključ naše tradicije:
    * Svaki komad mesa je pod veterinarskim nadzorom.
    * Koristimo profesionalne rashladne sustave.
    * Pakiranje se vrši neposredno prije slanja kuriru.
    """)

# --- STRANICA: DOBAVLJAČI ---
elif izbor == "🚜 DOBAVLJAČI":
    st.title("Domaća stoka iz Siska")
    st.markdown("""
    Svu stoku kupujemo isključivo u **okolici Siska** od:
    * Malih obiteljskih proizvođača.
    * Provjerenih OPG-ova koji cijene tradiciju.
    
    Time osiguravamo da meso bude svježe, bez nepotrebnog dugog transporta i s poznatim podrijetlom.
    """)

# --- STRANICA: O NAMA ---
elif izbor == "ℹ️ O NAMA":
    st.title("Tradicija Kojundžić")
    st.write("Poslujemo već desetljećima, donoseći okuse domaćeg dima na vaše stolove.")
    st.divider()
    st.write("**Adresa:** Trg Josipa Mađerića 1, 44000 Sisak")
    st.map(pd.DataFrame({'lat': [45.4832], 'lon': [16.3761]}))
