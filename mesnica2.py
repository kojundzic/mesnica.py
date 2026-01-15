import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Postavke aplikacije
st.set_page_config(page_title="Kojundžić Mesnica", page_icon="🥩", layout="wide")

# Funkcija za sigurno učitavanje slika
def load_image(url):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# --- DIZAJN I STIL ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .brand-name {
        color: #8B0000; font-size: 70px; font-weight: 900; text-align: center;
        margin-bottom: 0px; text-transform: uppercase; letter-spacing: 5px;
        line-height: 1;
    }
    .brand-sub {
        color: #333; font-size: 30px; text-align: center; margin-top: 0px;
        margin-bottom: 40px; font-weight: 600; letter-spacing: 2px;
    }
    .product-card {
        background-color: white; border-radius: 15px; padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #efefef;
        margin-bottom: 20px; text-align: center;
    }
    .price-tag { color: #8B0000; font-size: 18px; font-weight: bold; }
    .sidebar-cart {
        background-color: #ffffff; padding: 20px; border-radius: 15px;
        border: 1px solid #ddd; position: sticky; top: 20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%);
        color: white !important; border-radius: 10px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- POPIS ARTIKALA ---
proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50, "slika": "cdn.pixabay.com"},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50, "slika": "cdn.pixabay.com"},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.20, "slika": "cdn.pixabay.com"},
    {"id": 4, "ime": "Premium Buđola", "cijena": 19.50, "slika": "cdn.pixabay.com"},
    {"id": 5, "ime": "Dimljeni vrat", "cijena": 15.00, "slika": "cdn.pixabay.com"},
    {"id": 6, "ime": "Slavonska kobasica", "cijena": 14.50, "slika": "cdn.pixabay.com"},
    {"id": 7, "ime": "Domaća salama", "cijena": 16.00, "slika": "cdn.pixabay.com"},
    {"id": 8, "ime": "Hrskavi Čvarci", "cijena": 22.00, "slika": "cdn.pixabay.com"},
]

# --- NAVIGACIJA ---
with st.sidebar:
    st.markdown("## 🥩 IZBORNIK")
    izbor = st.radio("NAVIGACIJA", ["🛍️ TRGOVINA", "🧼 HIGIJENA & HACCP", "🚜 DOBAVLJAČI", "ℹ️ O NAMA"])
    st.write("---")
    st.caption("Sisak, siječanj 2026.")

# --- STRANICA: TRGOVINA ---
if izbor == "🛍️ TRGOVINA":
    # --- ISTAKNUTI NASLOV ---
    st.markdown('<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-sub">MESNICA I PRERADA MESA</p>', unsafe_allow_html=True)

    col_trgovina, col_kosarica = st.columns([3, 1])

    with col_trgovina:
        st.info("📢 Dostavu plaćate kuriru pri preuzimanju pošiljke.")
        prod_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with prod_cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                img = load_image(p["slika"])
                if img: st.image(img, use_container_width=True)
                st.markdown(f"**{p['ime']}**")
                st.markdown(f"<div class='price-tag'>{p['cijena']:.2f} €/kg</div>", unsafe_allow_html=True)
                qty = st.number_input(f"Kg", 1.0, 50.0, 1.0, 0.5, key=f"q_{p['id']}")
                if st.button("DODAJ", key=f"b_{p['id']}"):
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    with col_kosarica:
        st.markdown('<div class="sidebar-cart">', unsafe_allow_html=True)
        st.subheader("🛒 Košarica")
        if not st.session_state.cart:
            st.write("Prazna je.")
        else:
            ukupno = 0
            email_lista = ""
            for item in st.session_state.cart:
                st.write(f"**{item['ime']}** ({item['qty']}kg)")
                ukupno += item['price']
                email_lista += f"- {item['ime']}: {item['qty']}kg%0D%0A"
            st.write("---")
            st.write(f"### Ukupno: {ukupno:.2f} €")
            if st.button("🗑️ Isprazni"):
                st.session_state.cart = []
                st.rerun()
            st.write("---")
            ime_prezime = st.text_input("Ime i Prezime*")
            mob = st.text_input("Broj mobitela*")
            drzava = st.text_input("Država*", value="Hrvatska")
            grad = st.text_input("Grad*")
            ptt = st.text_input("Poštanski broj*")
            adr = st.text_input("Ulica i kućni broj*")
            
            if st.button("✅ NARUČI"):
                if ime_prezime and mob and grad and ptt and adr:
                    body = f"NARUDŽBA MESA%0D%0A%0D%0AKUPAC: {ime_prezime}%0D%0AMOB: {mob}%0D%0AADRESA: {adr}%0D%0AGRAD: {ptt} {grad}%0D%0ADRŽAVA: {drzava}%0D%0A%0D%0AARTIKLI:%0D%0A{email_lista}%0D%0AUKUPNO: {ukupno:.2f} EUR"
                    mail_link = f"mailto:tomislavtomi90@gmail.com_{ime_prezime}&body={body}"
                    st.markdown(f'<a href="{mail_link}"><button style="background:#D44638; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">POŠALJI MAIL</button></a>', unsafe_allow_html=True)
                else:
                    st.error("Ispunite sva polja!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- STRANICA: DOBAVLJAČI ---
elif izbor == "🚜 DOBAVLJAČI":
    st.title("🚜 Naši Dobavljači")
    # Slika životinja u prirodi (Lonjsko polje)
    img_priroda = load_image("cdn.pixabay.com")
    if img_priroda: st.image(img_priroda, caption="Slobodna ispaša - Park prirode Lonjsko polje", use_container_width=True)
    
    st.markdown("""
    Sva stoka se kupuje u **okolici Siska** od malih proizvođača i OPG-ova s područja:
    * **Banovine**
    * **Posavine**
    * **Parka prirode Lonjsko polje**
    
    Naši dobavljači jamče tradicionalan uzgoj u skladu s prirodom.
    """)

# --- STRANICA: HIGIJENA ---
elif izbor == "🧼 HIGIJENA & HACCP":
    st.title("🧼 Higijena & HACCP")
    st.write("Pogon registriran pod brojem: **2686**")
    st.info("Svi procesi su u skladu s najvišim standardima sigurnosti hrane u 2026. godini.")

# --- O NAMA ---
elif izbor == "ℹ️ O NAMA":
    st.title("ℹ️ O Mesnici Kojundžić")
    st.write("Poslujemo još od 1990-ih godina.")
    st.write("Posjetite nas u mesnici: **Trg Josipa Mađerića 1, Sisak**")
    st.write("Pogon za preradu mesa registriran pod brojem: **2686**")
    sisak_map = pd.DataFrame({'lat': [45.4832], 'lon': [16.3761]})
    st.map(sisak_map)
