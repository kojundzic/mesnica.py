import streamlit as st
import pandas as pd

# Postavke aplikacije za siječanj 2026.
st.set_page_config(page_title="Kojundžić Mesnica", page_icon="🥩", layout="wide")

# --- MODERNI PREMIUM DIZAJN ---
# Ispravljen parametar unsafe_allow_html=True
st.markdown(
    """
    <style>
    .stApp { background-color: #f8f9fa; }
    .product-card {
        background-color: white; border-radius: 20px; padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #efefef;
        transition: transform 0.3s ease; margin-bottom: 25px; text-align: center;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
    .stButton>button {
        background: linear-gradient(135deg, #8B0000 0%, #5d0000 100%);
        color: white !important; border-radius: 12px; border: none;
        font-weight: 600; width: 100%; height: 3.5em;
    }
    h1, h2, h3 { color: #1a1a1a; font-weight: 800 !important; }
    [data-testid="stSidebar"] { background-color: #1a1a1a; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

# --- LOGIKA KOŠARICE ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- POPIS PROIZVODA ---
proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50, "slika": "images.unsplash.com"},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50, "slika": "images.unsplash.com"},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.20, "slika": "images.unsplash.com"},
    {"id": 4, "ime": "Buđola", "cijena": 19.50, "slika": "images.unsplash.com"},
    {"id": 5, "ime": "Dimljeni vrat", "cijena": 15.00, "slika": "images.unsplash.com"},
    {"id": 6, "ime": "Slavonska kobasica", "cijena": 14.50, "slika": "images.unsplash.com"},
    {"id": 7, "ime": "Domaća salama", "cijena": 16.00, "slika": "images.unsplash.com"},
    {"id": 8, "ime": "Čvarci", "cijena": 22.00, "slika": "images.unsplash.com"},
    {"id": 9, "ime": "Dimljene kosti", "cijena": 4.50, "slika": "images.unsplash.com"},
    {"id": 10, "ime": "Dimljeni hamburger", "cijena": 12.80, "slika": "images.unsplash.com"},
]

# --- IZBORNIK ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🥩 KOJUNDŽIĆ</h2>", unsafe_allow_html=True)
    izbor = st.sidebar.radio("NAVIGACIJA", ["🛍️ TRGOVINA", "🛒 KOŠARICA", "ℹ️ O NAMA"])
    st.write("---")
    st.caption("Sisak, Hrvatska | 2026")

# --- STRANICA: TRGOVINA ---
if izbor == "🛍️ TRGOVINA":
    st.title("Domaća Ponuda")
    st.info("ℹ️ **Informacija:** Točan iznos računa znat će se nakon vaganja proizvoda.")
    
    cols = st.columns(2)
    for i, p in enumerate(proizvodi):
        with cols[i % 2]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.image(p["slika"], use_container_width=True)
            st.markdown(f"### {p['ime']}")
            st.markdown(f"<p style='color: #8B0000; font-size: 20px; font-weight: bold;'>{p['cijena']:.2f} € / kg</p>", unsafe_allow_html=True)
            
            qty = st.number_input(f"Količina (kg)", min_value=0.0, step=0.5, key=f"q_{p['id']}", format="%.1f")
            
            if st.button("DODAJ U KOŠARICU", key=f"b_{p['id']}"):
                if qty >= 0.5:
                    postoji = False
                    for stavka in st.session_state.cart:
                        if stavka['ime'] == p['ime']:
                            stavka['qty'] += qty
                            stavka['price'] = stavka['qty'] * p['cijena']
                            postoji = True
                            break
                    if not postoji:
                        st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.toast(f"Dodan {p['ime']}!", icon="✅")
                else:
                    st.error("Minimalna količina je 0.5 kg.")
            st.markdown('</div>', unsafe_allow_html=True)

# --- STRANICA: KOŠARICA ---
elif izbor == "🛒 KOŠARICA":
    st.title("Vaša Narudžba")
    
    if not st.session_state.cart:
        st.info("Vaša košarica je prazna.")
    else:
        if st.button("🗑️ Isprazni košaricu"):
            st.session_state.cart = []
            st.rerun()

        st.write("---")
        ukupno_euro = 0
        email_stavke = ""
        
        for s in st.session_state.cart:
            c1, c2 = st.columns()
            c1.write(f"**{s['ime']}**")
            c2.write(f"{s['qty']} kg = {s['price']:.2f} €")
            ukupno_euro += s['price']
            email_stavke += f"- {s['ime']}: {s['qty']} kg ({s['price']:.2f} EUR)%0D%0A"
        
        st.markdown("---")
        st.markdown(f"<h2 style='text-align: right;'>Informativni iznos: {ukupno_euro:.2f} €</h2>", unsafe_allow_html=True)

        with st.form("forma_narudzbe"):
            st.markdown("### 🚚 Podaci za dostavu")
            ime = st.text_input("Ime i Prezime primatelja*")
            mob = st.text_input("Kontakt telefon (npr. +385...)*")
            adr = st.text_input("Ulica i kućni broj*")
            grad_ptt = st.text_input("Poštanski broj i Grad*")
            
            regija = st.selectbox("Regija dostave", ["Hrvatska", "Inozemstvo (EU)"])
            drzava = "Hrvatska"
            email_kupca = ""
            
            if regija == "Inozemstvo (EU)":
                st.warning("Za EU dostavu kuriri zahtijevaju E-mail i Državu.")
                drzava = st.text_input("Država*")
                email_kupca = st.text_input("E-mail adresa kupca*")
            
            if st.form_submit_button("GENERIRAJ NARUDŽBU ZA E-MAIL"):
                uvjet_inozemstvo = True if regija == "Hrvatska" else (drzava and email_kupca)
                
                if ime and adr and grad_ptt and mob and uvjet_inozemstvo:
                    MOJ_GMAIL = "tomislavtomi90@gmail.com"
                    subjekt = f"Narudzba_{regija}_{ime}"
                    
                    tijelo = f"NARUDŽBA MESA%0D%0A-----------------%0D%0A{email_stavke}"
                    tijelo += f"%0D%0AUKUPNO: cca {ukupno_euro:.2f} EUR%0D%0A-----------------%0D%0APRIMATELJ: {ime}"
                    tijelo += f"%0D%0AADRESA: {adr}, {grad_ptt}, {drzava}%0D%0AMOBITEL: {mob}"
                    if email_kupca:
                        tijelo += f"%0D%0AEMAIL: {email_kupca}"
                    
                    mail_link = f"mailto:{MOJ_GMAIL}?subject={subjekt}&body={tijelo}"
                    
                    st.success("✅ Narudžba generirana!")
                    st.markdown(f"""
                        <a href="{mail_link}">
                            <button style="background-color: #D44638; color: white; padding: 20px; border-radius: 12px; width: 100%; border: none; font-size: 18px; font-weight: bold; cursor: pointer;">
                                📧 POŠALJI NARUDŽBU E-MAILOM
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Ispunite obavezna polja (*).")

# --- STRANICA: O NAMA ---
elif izbor == "ℹ️ O NAMA":
    st.title("Mesnica Kojundžić Sisak")
    st.write("Tradicija i kvaliteta domaće prerade mesa iz Siska.")
    st.divider()
    st.subheader("📍 Lokacija")
    st.write("Trg Josipa Mađerića 1, 44000 Sisak")
    map_data = pd.DataFrame({'lat': [45.4832], 'lon': [16.3761]})
    st.map(map_data)
