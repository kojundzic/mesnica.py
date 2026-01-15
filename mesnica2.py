import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Postavke aplikacije
st.set_page_config(page_title="Kojundžić Mesnica | Premium Selekcija", page_icon="🥩", layout="wide")

# Funkcija za sigurno učitavanje slika
@st.cache_data
def load_image(url):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# --- DIZAJN I MARKETINŠKA STILIZACIJA ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .brand-name {
        color: #8B0000; font-size: 70px; font-weight: 900; text-align: center;
        margin-bottom: 0px; text-transform: uppercase; letter-spacing: 5px; line-height: 1;
    }
    .brand-sub {
        color: #333; font-size: 28px; text-align: center; margin-top: 0px;
        margin-bottom: 30px; font-weight: 600; letter-spacing: 2px;
    }
    /* Kartica proizvoda s marketinškim efektom */
    .product-card {
        background-color: white; border-radius: 20px; padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #efefef;
        margin-bottom: 25px; text-align: center; transition: all 0.3s ease;
    }
    .product-card:hover { transform: translateY(-10px); box-shadow: 0 15px 40px rgba(139,0,0,0.15); }
    
    .price-tag { color: #8B0000; font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    
    .stButton>button {
        background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%);
        color: white !important; border-radius: 50px; width: 100%; font-weight: bold; height: 3em;
    }
    /* Oznake za psihološki utjecaj */
    .badge-bestseller { background-color: #FFD700; color: black; padding: 5px 15px; border-radius: 50px; font-size: 12px; font-weight: bold; }
    .badge-limited { background-color: #FF4B4B; color: white; padding: 5px 15px; border-radius: 50px; font-size: 12px; font-weight: bold; }
    
    .sidebar-cart {
        background-color: #ffffff; padding: 25px; border-radius: 20px;
        border: 1px solid #eee; box-shadow: 0 5px 20px rgba(0,0,0,0.05); position: sticky; top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- ARTIKLI S MARKETINŠKIM OZNAKAMA ---
proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50, "oznaka": "NAJPRODAVANIJE", "slika": "cdn.pixabay.com"},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50, "oznaka": "PREPORUKA MESARA", "slika": "cdn.pixabay.com"},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.20, "oznaka": "DANAŠNJA PONUDA", "slika": "cdn.pixabay.com"},
    {"id": 4, "ime": "Premium Buđola", "cijena": 19.50, "oznaka": "EKSKLUZIVNO", "slika": "cdn.pixabay.com"},
    {"id": 5, "ime": "Dimljeni vrat", "cijena": 15.00, "oznaka": "TRADICIONALNO", "slika": "cdn.pixabay.com"},
    {"id": 6, "ime": "Slavonska kobasica", "cijena": 14.50, "oznaka": "DOMAĆI RECEPT", "slika": "cdn.pixabay.com"},
]

# --- NAVIGACIJA ---
with st.sidebar:
    st.markdown("## 🥩 IZBORNIK")
    izbor = st.radio("NAVIGACIJA", ["🛍️ TRGOVINA", "🚜 DOBAVLJAČI", "🧼 HACCP", "ℹ️ O NAMA"])
    st.write("---")
    st.caption("Sisak, 15. siječanj 2026.")

# --- TRGOVINA ---
if izbor == "🛍️ TRGOVINA":
    st.markdown('<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-sub">MESNICA I PRERADA MESA</p>', unsafe_allow_html=True)

    # Psihološki okidač na vrhu
    st.warning("🔥 **Danas svježe iz pušnice:** Ograničene količine domaće dimljene češnjovke!")

    col_trgovina, col_kosarica = st.columns([3, 1])

    with col_trgovina:
        prod_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with prod_cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                # Prikaz oznake ovisno o tipu
                st.markdown(f'<span class="badge-bestseller">{p["oznaka"]}</span>', unsafe_allow_html=True)
                
                img = load_image(p["slika"])
                if img: st.image(img, use_container_width=True)
                
                st.markdown(f"### {p['ime']}")
                st.markdown(f"<div class='price-tag'>{p['cijena']:.2f} €/kg</div>", unsafe_allow_html=True)
                
                qty = st.number_input(f"Odaberite kg za {p['ime']}", 1.0, 50.0, 1.0, 0.5, key=f"q_{p['id']}")
                
                if st.button("DODAJ U KOŠARICU", key=f"b_{p['id']}"):
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.balloons() # Vizualna nagrada za kupnju
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    with col_kosarica:
        st.markdown('<div class="sidebar-cart">', unsafe_allow_html=True)
        st.subheader("🛒 Vaša Narudžba")
        if not st.session_state.cart:
            st.write("Vaša košarica je prazna. Odaberite najbolje od domaćeg mesa!")
        else:
            ukupno = sum(item['price'] for item in st.session_state.cart)
            email_lista = ""
            for item in st.session_state.cart:
                st.write(f"**{item['ime']}**")
                st.caption(f"{item['qty']}kg = {item['price']:.2f}€")
                email_lista += f"- {item['ime']}: {item['qty']}kg%0D%0A"
            
            st.write("---")
            st.markdown(f"### Ukupno: {ukupno:.2f} €")
            
            if st.button("🗑️ Isprazni košaricu"):
                st.session_state.cart = []
                st.rerun()
            
            st.write("---")
            ime_prezime = st.text_input("Ime i Prezime*")
            mob = st.text_input("Broj mobitela*")
            grad = st.text_input("Grad*")
            ptt = st.text_input("Poštanski broj*")
            adr = st.text_input("Adresa*")
            drzava = st.text_input("Država*", value="Hrvatska")
            
            st.markdown('<p style="font-size: 11px; color: gray;">🚚 Dostavu plaćate kuriru pri preuzimanju.</p>', unsafe_allow_html=True)
            
            if st.button("✅ POTVRDI NARUDŽBU"):
                if ime_prezime and mob and grad and ptt and adr:
                    body = f"NARUDŽBA MESA%0D%0A%0D%0AKUPAC: {ime_prezime}%0D%0AMOB: {mob}%0D%0AADRESA: {adr}%0D%0AGRAD: {ptt} {grad}%0D%0ADRŽAVA: {drzava}%0D%0A%0D%0AARTIKLI:%0D%0A{email_lista}%0D%0AUKUPNO: cca {ukupno:.2f} EUR"
                    mail_link = f"mailto:tomislavtomi90@gmail.com_{ime_prezime}&body={body}"
                    st.markdown(f'<a href="{mail_link}"><button style="background:#D44638; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">📧 POŠALJI E-MAIL</button></a>', unsafe_allow_html=True)
                else:
                    st.error("Ispunite sva polja!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- OSTALE STRANICE (Dobavljači, HACCP, O nama) ---
elif izbor == "🚜 DOBAVLJAČI":
    st.title("🚜 Naši Dobavljači")
    img_priroda = load_image("cdn.pixabay.com")
    if img_priroda: st.image(img_priroda, caption="Slobodna ispaša - Lonjsko polje", use_container_width=True)
    st.markdown("""
    Sva stoka se kupuje u **okolici Siska** (Banovina, Posavina, Park prirode Lonjsko polje) 
    isključivo od malih proizvođača i OPG-ova koji jamče prirodan uzgoj.
    """)

elif izbor == "🧼 HACCP":
    st.title("🧼 Higijena & HACCP")
    st.write("Pogon registriran pod brojem: **2686**")
    st.info("Najviši standardi sigurnosti hrane u 2026. godini.")

elif izbor == "ℹ️ O NAMA":
    st.title("ℹ️ O nama")
    st.write("Mala obiteljska tvrtka bazirana na tradicionalnoj proizvodnji još od 1990-ih.")
    st.write("📍 **Trg Josipa Mađerića 1, Sisak**")
    st.map(pd.DataFrame({'lat': [45.4832], 'lon': [16.3761]}))
