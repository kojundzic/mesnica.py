import streamlit as st
import pandas as pd

# Postavke aplikacije za 2026. godinu
st.set_page_config(page_title="Kojundžić Mesnica", page_icon="🥩", layout="wide")

# --- MODERNIZIRANI DIZAJN ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-box {
        background-color: white; padding: 20px; border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center;
        margin-bottom: 20px; border: 1px solid #eee;
    }
    .stButton>button {
        background-color: #8B0000; color: white; border-radius: 25px;
        font-weight: bold; width: 100%; height: 3.5em; border: none;
    }
    .stButton>button:hover { background-color: #cc0000; }
    h1, h2, h3 { color: #333; }
    </style>
    """, unsafe_allow_index=True)

# --- LOGIKA KOŠARICE ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- POPIS PROIZVODA (Ažurirano 2026.) ---
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
    izbor = st.sidebar.radio("IZBORNIK", ["🛍️ Ponuda mesa", "🛒 Moja košarica", "ℹ️ O nama"])

# --- STRANICA: TRGOVINA ---
if izbor == "🛍️ Ponuda mesa":
    st.title("Domaća ponuda")
    st.warning("🚛 Pakete šaljemo unutar Hrvatske i cijele Europske unije (EU).")
    cols = st.columns(2)
    for i, p in enumerate(proizvodi):
        with cols[i % 2]:
            st.markdown(f'<div class="product-box">', unsafe_allow_index=True)
            st.image(p["slika"], use_container_width=True)
            st.subheader(p["ime"])
            st.write(f"**{p['cijena']:.2f} €** / {p['jedinica']}")
            qty = st.number_input(f"Količina (kg)", min_value=0.0, step=0.5, key=f"q_{p['id']}")
            if st.button(f"DODAJ", key=f"b_{p['id']}"):
                if qty >= 1.0:
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.toast(f"Dodan {p['ime']}!", icon="✅")
                else: st.error("Min. narudžba je 1kg.")
            st.markdown('</div>', unsafe_allow_index=True)

# --- STRANICA: KOŠARICA I DOSTAVA ---
elif izbor == "🛒 Moja košarica":
    st.title("Vaša narudžba")
    if not st.session_state.cart:
        st.info("Košarica je prazna.")
    else:
        ukupno = 0
        for s in st.session_state.cart:
            st.write(f"**{s['ime']}** ({s['qty']} kg) = {s['price']:.2f} €")
            ukupno += s['price']
        st.divider()
        st.subheader(f"UKUPNO: {ukupno:.2f} €")

        st.write("### 🚚 Detalji za dostavu")
        # Odabir regije
        regija = st.radio("Kamo šaljemo paket?", ["Unutar Hrvatske", "Inozemstvo (Samo Europska unija - EU)"])
        
        with st.form("forma_narudzbe"):
            ime = st.text_input("Ime i Prezime*")
            adresa = st.text_input("Ulica i kućni broj*")
            grad_zip = st.text_input("Poštanski broj i Grad*")
            
            # Polje za zemlju se pojavljuje samo ako je odabrano inozemstvo
            zemlja = "Hrvatska"
            if regija == "Inozemstvo (Samo Europska unija - EU)":
                zemlja = st.text_input("Zemlja (npr. Njemačka, Austrija)*")
            
            mobitel = st.text_input("Broj mobitela (obavezno)*")
            
            # Prilagodba plaćanja
            if regija == "Unutar Hrvatske":
                nacin = st.selectbox("Način plaćanja", ["Pouzećem (kod dostave)", "Uplata na račun (prema ponudi)"])
            else:
                st.info("ℹ️ Za slanje u EU dostupna je isključivo uplata na račun prije slanja.")
                nacin = "Uplata na račun (Inozemna doznaka)"
            
            if st.form_submit_button("ZAVRŠI NARUDŽBU"):
                if ime and adresa and grad_zip and mobitel and (zemlja if regija != "Unutar Hrvatske" else True):
                    st.balloons()
                    st.success(f"HVALA NA NARUDŽBI!")
                    
                    # PRIPREMA PORUKE ZA WHATSAPP
                    tekst = f"Nova narudžba - {regija}:\n"
                    for s in st.session_state.cart: tekst += f"- {s['ime']} ({s['qty']}kg)\n"
                    tekst += f"\nUKUPNO: {ukupno:.2f}€\nKupac: {ime}\nAdresa: {adresa}, {grad_zip}\nZemlja: {zemlja}\nMob: {mobitel}\nPlacanje: {nacin}"
                    
                    # --- UPIŠI SVOJ BROJ OVDJE (primjer: 38591234567) ---
                    moj_broj = "38591234567" 
                    url_wa = f"wa.me{moj_broj}?text={tekst.replace(' ', '%20')}"
                    
                    st.markdown(f'<a href="{url_wa}" target="_blank"><button style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; width: 100%; border: none; font-weight: bold; cursor: pointer;">✅ POŠALJI NARUDŽBU NA WHATSAPP</button></a>', unsafe_allow_index=True)
                    st.warning("⚠️ Važno: Da bismo zaprimili narudžbu, kliknite na zeleni gumb iznad!")
                else:
                    st.error("Molimo ispunite sva polja označena s *.")

elif izbor == "ℹ️ O nama":
    st.title("O Mesnici Kojundžić")
    st.write("Sisak, Hrvatska. Tradicionalna obrada mesa s pašnjaka sisačke Posavine.")
    st.info("📍 Lokacija: Trg branitelja 1, Sisak")
    st.write("Radno vrijeme: Pon-Sub (07:00 - 15:00)")
