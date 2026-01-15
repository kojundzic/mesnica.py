import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Postavke aplikacije za 2026.
st.set_page_config(page_title="Kojundžić Mesnica | Premium Selection", page_icon="🥩", layout="wide")

@st.cache_data
def load_image(url):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# --- MODERNI VIZUALNI IDENTITET ---
st.markdown(
    """
    <style>
    .stApp { background: #fdfdfd; }
    
    /* Hero sekcija s prirodom */
    .hero-section {
        background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
        url('images.unsplash.com');
        background-size: cover; background-position: center;
        padding: 80px; border-radius: 30px; text-align: center; color: white; margin-bottom: 40px;
    }
    
    .product-card {
        background: white; border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #eee;
        transition: all 0.3s ease; margin-bottom: 20px;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(139,0,0,0.1); }
    
    .stButton>button {
        background: #8B0000; color: white !important; border-radius: 50px;
        border: none; font-weight: 700; width: 100%;
    }
    .sidebar-cart {
        background: white; padding: 20px; border-radius: 20px;
        border: 1px solid #ddd; position: sticky; top: 10px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- PODACI O PROIZVODIMA ---
proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50, "slika": "images.unsplash.com"},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50, "slika": "images.unsplash.com"},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.20, "slika": "images.unsplash.com"},
    {"id": 4, "ime": "Premium Buđola", "cijena": 19.50, "slika": "images.unsplash.com"},
    {"id": 5, "ime": "Dimljeni vrat", "cijena": 15.00, "slika": "images.unsplash.com"},
    {"id": 6, "ime": "Slavonska kobasica", "cijena": 14.50, "slika": "images.unsplash.com"},
]

# --- NAVIGACIJA ---
with st.sidebar:
    st.markdown("## 🥩 KOJUNDŽIĆ")
    izbor = st.radio("NAVIGACIJA", ["🛍️ TRGOVINA", "🚜 DOBAVLJAČI", "🧼 HACCP", "ℹ️ KONTAKT"])
    st.write("---")
    st.caption("Sisak | 2026")

# --- TRGOVINA ---
if izbor == "🛍️ TRGOVINA":
    st.markdown('<div class="hero-section"><h1>Okusi prirode Banovine i Posavine</h1><p>Domaća prerada mesa s pašnjaka Lonjskog polja</p></div>', unsafe_allow_html=True)

    col_main, col_cart = st.columns([2.5, 1])

    with col_main:
        st.subheader("Ponuda tjedna")
        prod_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with prod_cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                img = load_image(p["slika"])
                if img: st.image(img, use_container_width=True)
                st.markdown(f"### {p['ime']}")
                st.markdown(f"#### {p['cijena']:.2f} €/kg")
                qty = st.number_input(f"Kg", 1.0, 30.0, 1.0, 0.5, key=f"q_{p['id']}")
                if st.button("DODAJ", key=f"b_{p['id']}"):
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    with col_cart:
        st.markdown('<div class="sidebar-cart">', unsafe_allow_html=True)
        st.subheader("🛒 Košarica")
        if not st.session_state.cart:
            st.write("Prazna je.")
        else:
            ukupno = sum(item['price'] for item in st.session_state.cart)
            email_lista = ""
            for item in st.session_state.cart:
                st.write(f"**{item['ime']}** ({item['qty']}kg)")
                email_lista += f"- {item['ime']}: {item['qty']}kg%0D%0A"
            st.write("---")
            st.markdown(f"### Ukupno: {ukupno:.2f} €")
            if st.button("🗑️ ISPRAZNI"):
                st.session_state.cart = []
                st.rerun()
            
            st.write("---")
            ime = st.text_input("Ime*")
            mob = st.text_input("Mob*")
            adr = st.text_input("Adresa*")
            if st.button("✅ POŠALJI NARUDŽBU"):
                if ime and mob and adr:
                    body = f"KUPAC: {ime}%0D%0AMOB: {mob}%0D%0AADRESA: {adr}%0D%0A%0D%0AARTIKLI:%0D%0A{email_lista}%0D%0AUKUPNO: {ukupno:.2f} EUR"
                    mail_link = f"mailto:tomislavtomi90@gmail.com_{ime}&body={body}"
                    st.markdown(f'<a href="{mail_link}"><button style="background:#D44638; color:white; border:none; padding:12px; border-radius:8px; width:100%;">OTVORI E-MAIL</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- DOBAVLJAČI ---
elif izbor == "🚜 DOBAVLJAČI":
    st.title("🚜 Naši pašnjaci i OPG-ovi")
    # Slika krava u prirodi
    st.image("images.unsplash.com", caption="Slobodna ispaša u Lonjskom polju", use_container_width=True)
    st.markdown("""
    ### Prirodni uzgoj Banovine, Posavine i Lonjskog polja
    Naša filozofija temelji se na suradnji s prirodom. Svu stoku nabavljamo od malih OPG-ova s područja:
    *   **Banovine:** Gdje brežuljci i čist zrak jamče zdrav uzgoj.
    *   **Posavine:** Kraja duge stočarske tradicije.
    *   **Parka prirode Lonjsko polje:** Gdje životinje žive na otvorenim pašnjacima u srcu zaštićene prirode.
    """)
    st.image("images.unsplash.com", caption="Tradicija domaćeg uzgoja", use_container_width=True)

# --- HACCP ---
elif izbor == "🧼 HACCP":
    st.title("Sigurnost i Čistoća")
    st.success("Registracijski broj pogona: 2686")
    st.markdown("""
    Primjenjujemo najviše standarde **HACCP sustava** kontrole hrane u 2026. godini. 
    Svaki komad mesa koji naručite je pod strogim sanitarnim nadzorom od trenutka otkupa do pakiranja.
    """)

# --- KONTAKT ---
elif izbor == "ℹ️ KONTAKT":
    st.title("Posjetite nas u Sisku")
    st.write("📍 **Adresa:** Trg Josipa Mađerića 1, 44000 Sisak")
    st.write("📧 **E-mail:** tomislavtomi90@gmail.com")
    sisak_map = pd.DataFrame({'lat': [45.4832], 'lon': [16.3761]})
    st.map(sisak_map)
