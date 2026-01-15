import streamlit as st
import pandas as pd

# Postavke aplikacije za 2026. godinu
st.set_page_config(page_title="Kojundžić Mesnica", page_icon="🥩", layout="wide")

# --- PREMIUM DIZAJN (Shopify/Glovo Stil) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .product-box {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #eee;
    }
    .stButton>button {
        background-color: #8B0000;
        color: white;
        border-radius: 25px;
        font-weight: bold;
        width: 100%;
        height: 3em;
        border: none;
    }
    .stButton>button:hover { background-color: #cc0000; transform: scale(1.02); }
    h1, h2, h3 { color: #333; }
    </style>
    """, unsafe_allow_index=True)

# --- LOGIKA KOŠARICE ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- VAŠ POPIS PROIZVODA ---
proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50, "jedinica": "kg", "slika": "images.unsplash.com"},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50, "jedinica": "kg", "slika": "images.unsplash.com"},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.20, "jedinica": "kg", "slika": "images.unsplash.com"},
    {"id": 4, "ime": "Buđola", "cijena": 19.50, "jedinica": "kg", "slika": "images.unsplash.com"},
    {"id": 5, "ime": "Dimljeni vrat", "cijena": 15.00, "jedinica": "kg", "slika": "images.unsplash.com"},
    {"id": 6, "ime": "Slavonska kobasica", "cijena": 14.50, "jedinica": "kg", "slika": "images.unsplash.com"},
    {"id": 7, "ime": "Domaća salama", "cijena": 16.00, "jedinica": "kg", "slika": "images.unsplash.com"},
    {"id": 8, "ime": "Čvarci", "cijena": 22.00, "jedinica": "kg", "slika": "images.unsplash.com"},
    {"id": 9, "ime": "Dimljene kosti", "cijena": 4.50, "jedinica": "kg", "slika": "images.unsplash.com"},
    {"id": 10, "ime": "Dimljeni hamburger", "cijena": 12.80, "jedinica": "kg", "slika": "images.unsplash.com"},
]

# --- IZBORNIK ---
with st.sidebar:
    st.markdown("## 🥩 Kojundžić Sisak")
    st.write("---")
    izbor = st.radio("IZBORNIK", ["🛍️ Trgovina", "🛒 Košarica", "🌾 Dobavljači", "🛡️ Higijena", "ℹ️ O nama"])
    st.write("---")
    st.caption("Verzija 2.0 (2026)")

# --- STRANICA: TRGOVINA ---
if izbor == "🛍️ Trgovina":
    st.title("Naša Ponuda")
    st.info("Minimalna narudžba je 1 kg po proizvodu.")
    
    cols = st.columns(2)
    for i, p in enumerate(proizvodi):
        with cols[i % 2]:
            st.markdown(f'<div class="product-box">', unsafe_allow_index=True)
            st.image(p["slika"], use_container_width=True)
            st.subheader(p["ime"])
            st.write(f"**{p['cijena']:.2f} €** / {p['jedinica']}")
            
            qty = st.number_input(f"Količina (kg)", min_value=0.0, step=0.5, key=f"q_{p['id']}")
            
            if st.button(f"DODAJ U KOŠARICU", key=f"b_{p['id']}"):
                if qty >= 1.0:
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.toast(f"Dodan {p['ime']}!", icon="✅")
                else:
                    st.error("Min. narudžba je 1kg.")
            st.markdown('</div>', unsafe_allow_index=True)

# --- STRANICA: KOŠARICA & DOSTAVA ---
elif izbor == "🛒 Košarica":
    st.title("Vaša Košarica")
    if not st.session_state.cart:
        st.info("Košarica je prazna.")
    else:
        ukupno = 0
        for s in st.session_state.cart:
            st.write(f"**{s['ime']}** ({s['qty']} kg) = {s['price']:.2f} €")
            ukupno += s['price']
        
        st.divider()
        st.subheader(f"UKUPNO: {ukupno:.2f} €")
        
        if st.button("🗑️ ISPRAZNI KOŠARICU"):
            st.session_state.cart = []
            st.rerun()

        st.write("### 🚚 Podaci za dostavu")
        with st.form("dostava"):
            ime = st.text_input("Ime i Prezime*")
            adr = st.text_input("Adresa (Sisak i okolica)*")
            tel = st.text_input("Broj mobitela*")
            nac = st.selectbox("Plaćanje", ["Pouzećem (Gotovina/Kartica)", "Internet bankarstvo"])
            if st.form_submit_button("ZAVRŠI NARUDŽBU"):
                if ime and adr and tel:
                    st.balloons()
                    st.success(f"HVALA NA KUPOVINI, {ime}!")
                    st.write(f"Vaša narudžba je zaprimljena. Zvat ćemo Vas na {tel}.")
                    st.session_state.cart = []
                else:
                    st.error("Ispunite obavezna polja.")

# --- OSTALE RUBRIKE ---
elif izbor == "🌾 Dobavljači":
    st.title("🚜 Lokalni Dobavljači")
    st.write("Svu stoku kupujemo na malim obiteljskim gospodarstvima u okolici Siska. Podržavamo domaće!")
    st.image("images.unsplash.com")

elif izbor == "🛡️ Higijena":
    st.title("🛡️ Sigurnost hrane")
    st.write("Primjenjujemo HACCP sustav i najviše higijenske standarde u 2026. godini.")

elif izbor == "ℹ️ O nama":
    st.title("📖 O nama")
    st.write("Mesnica Kojundžić - Tradicija i kvaliteta. Nalazimo se u Sisku, Trg branitelja 1.")
    map_data = pd.DataFrame({'lat': [45.485], 'lon': [16.373]})
    st.map(map_data)
