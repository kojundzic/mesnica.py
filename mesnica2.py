import streamlit as st
import pandas as pd

# Postavke aplikacije za siječanj 2026.
st.set_page_config(page_title="Kojundžić Mesnica", page_icon="🥩", layout="wide")

# --- MODERNI PREMIUM DIZAJN ---
st.markdown("""
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
        font-weight: 600; width: 100%; height: 3.5em; transition: all 0.3s;
    }
    .stButton>button:hover { background: linear-gradient(135deg, #cc0000 0%, #8B0000 100%); }
    h1, h2, h3 { color: #1a1a1a; font-weight: 800 !important; }
    [data-testid="stSidebar"] { background-color: #1a1a1a; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_index=True)

# --- LOGIKA KOŠARICE ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- VAŠ POPIS PROIZVODA (ISKLJUČIVO NA KG) ---
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
    st.markdown("<h2 style='text-align: center;'>🥩 KOJUNDŽIĆ</h2>", unsafe_allow_index=True)
    st.write("---")
    izbor = st.sidebar.radio("NAVIGACIJA", ["🛍️ TRGOVINA", "🛒 KOŠARICA", "ℹ️ O NAMA & KONTAKT"])
    st.write("---")
    st.caption("Sisak, Hrvatska | 2026")

# --- STRANICA: TRGOVINA ---
if izbor == "🛍️ TRGOVINA":
    st.title("Domaća Ponuda")
    st.info("ℹ️ **Napomena o vaganju:** Svi proizvodi prodaju se na kilograme. Prodavatelj će se pokušati držati što bliže traženoj količini, a točan iznos znat će se nakon vaganja.")
    
    cols = st.columns(2)
    for i, p in enumerate(proizvodi):
        with cols[i % 2]:
            st.markdown(f'<div class="product-card">', unsafe_allow_index=True)
            st.image(p["slika"], use_container_width=True)
            st.markdown(f"### {p['ime']}")
            st.markdown(f"<p style='color: #8B0000; font-size: 20px; font-weight: bold;'>{p['cijena']:.2f} € / kg</p>", unsafe_allow_index=True)
            qty = st.number_input(f"Količina (kg)", min_value=0.0, step=0.1, key=f"q_{p['id']}", format="%.1f")
            if st.button(f"DODAJ U KOŠARICU", key=f"b_{p['id']}"):
                if qty >= 0.5:
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.toast(f"Dodan {p['ime']}!", icon="✅")
                else: st.error("Min. narudžba je 0.5 kg.")
            st.markdown('</div>', unsafe_allow_index=True)

# --- STRANICA: KOŠARICA ---
elif izbor == "🛒 KOŠARICA":
    st.title("Vaša Narudžba")
    if not st.session_state.cart:
        st.info("Košarica je prazna.")
    else:
        ukupno = 0
        detalji_mail = ""
        for s in st.session_state.cart:
            col_a, col_b = st.columns()
            col_a.write(f"**{s['ime']}** ({s['qty']} kg)")
            col_b.write(f"{s['price']:.2f} €")
            ukupno += s['price']
            detalji_mail += f"- {s['ime']}: {s['qty']} kg%0D%0A"
        
        st.markdown("---")
        st.markdown(f"<h2 style='text-align: right;'>Informativno: {ukupno:.2f} €</h2>", unsafe_allow_index=True)
        st.caption("Točan iznos plaćate nakon vaganja (pouzećem ili uplatom). Dostava unutar EU.")

        with st.form("forma_narudzbe"):
            st.markdown("### 🚚 Podaci za dostavu")
            ime = st.text_input("Ime i Prezime*")
            adr = st.text_input("Adresa, poštanski broj i Grad*")
            mob = st.text_input("Broj mobitela*")
            regija = st.selectbox("Regija dostave", ["Hrvatska", "Inozemstvo (EU)"])
            zemlja = st.text_input("Država (samo za EU)*") if regija == "Inozemstvo (EU)" else "Hrvatska"
            
            if st.form_submit_button("PRIPREMI NARUDŽBU"):
                if ime and adr and mob:
                    MOJ_GMAIL = "tomislavtomi90@gmail.com"
                    subjekt = f"Nova narudzba - {ime}"
                    tijelo = f"Kupac: {ime}%0D%0AMobitel: {mob}%0D%0AAdresa: {adr}%0D%0ADrzava: {zemlja}%0D%0A%0D%0AStavke:%0D%0A{detalji_mail}%0D%0AInformativno ukupno: {ukupno:.2f} EUR"
                    mail_link = f"mailto:{MOJ_GMAIL}?subject={subjekt}&body={tijelo}"
                    
                    st.success("✅ Narudžba spremna za slanje!")
                    st.markdown(f"""
                        <a href="{mail_link}">
                            <button style="background-color: #25D366; color: white; padding: 15px; border-radius: 12px; width: 100%; border: none; font-size: 18px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                                POŠALJI NARUDŽBU E-MAILOM 📧
                            </button>
                        </a>
                        """, unsafe_allow_index=True)
                else:
                    st.error("Ispunite obavezna polja.")

# --- STRANICA: O NAMA ---
elif izbor == "ℹ️ O NAMA & KONTAKT":
    st.title("Tradicija Kojundžić")
    st.write("**Mesnica i prerada mesa Kojundžić** obiteljski je obrt iz Siska. Naš fokus je na kvaliteti, domaćem uzgoju i tradicionalnom dimljenju.")
    st.divider()
    st.subheader("📍 Kontakt i Lokacija")
    st.write("**Adresa:** Trg Josipa Mađerića 1, 44000 Sisak")
    st.write("**E-mail:** tomislavtomi90@gmail.com")
    sisak_map = pd.DataFrame({'lat': [45.483], 'lon': [16.376]})
    st.map(sisak_map)
    st.info("🛡️ HACCP kontrola 2026.")
