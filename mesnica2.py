import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- 1. POSTAVKE ZA OBAVIJESTI ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu"  # Tvoja lozinka aplikacije
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Postavke aplikacije za 2026. godinu
st.set_page_config(page_title="Kojundžić | Mesnica i Prerada mesa", page_icon="🥩", layout="wide")

# --- 2. LOGIKA ZA TIHO SLANJE NARUDŽBE VLASNIKU ---
def posalji_email_vlasniku(ime, mob, adr, detalji_narudzbe, ukupno):
    predmet = f"🥩 NOVA NARUDŽBA: {ime}"
    tijelo = f"""
    Stigla je nova narudžba putem weba!
    
    KUPAC: {ime}
    MOBITEL: {mob}
    ADRESA: {adr}
    DATUM: {datetime.now().strftime('%d.%m.%2026. %H:%M')}
    
    NARUČENI ARTIKLI:
    {detalji_narudzbe}
    
    UKUPNO ZA NAPLATU: {ukupno} €
    """
    msg = MIMEText(tijelo)
    msg['Subject'] = predmet
    msg['From'] = MOJ_EMAIL
    msg['To'] = MOJ_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

# --- 3. DIZAJN ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .brand-name { color: #8B0000; font-size: 55px; font-weight: 900; text-align: center; text-transform: uppercase; margin-bottom:0px; }
    .brand-sub { color: #333; font-size: 22px; text-align: center; font-weight: 600; margin-top:0px; margin-bottom: 25px; }
    .product-card { background-color: white; border-radius: 12px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #eee; text-align: center; margin-bottom:10px; }
    .price-tag { color: #8B0000; font-size: 20px; font-weight: bold; }
    .sidebar-cart { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #ddd; }
    .stButton>button { background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%); color: white !important; font-weight: bold; border-radius: 50px; }
    </style>
    """, unsafe_allow_html=True)

if 'cart' not in st.session_state: st.session_state.cart = []

# --- 4. PODACI ---
proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50},
    {"id": 3, "ime": "Premium Buđola", "cijena": 19.50},
    {"id": 4, "ime": "Dimljeni vrat", "cijena": 15.00},
    {"id": 5, "ime": "Domaća salama", "cijena": 16.00},
    {"id": 6, "ime": "Dimljeni prsni vršci", "cijena": 9.20},
]

ugostitelji_ponuda = [
    {"id": 101, "ime": "Ćevapi (juneći)", "cijena": 12.00},
    {"id": 102, "ime": "Pljeskavice", "cijena": 11.50},
    {"id": 103, "ime": "Šiš-ćevapi", "cijena": 12.50},
    {"id": 201, "ime": "Juneći biftek", "cijena": 35.00},
    {"id": 202, "ime": "Juneći ramstek s kosti", "cijena": 18.50},
]

# --- 5. LOGIKA KOŠARICE ---
def prikazi_kosaricu(col):
    with col:
        st.markdown('<div class="sidebar-cart">', unsafe_allow_html=True)
        st.subheader("🛒 Vaša Košarica")
        if not st.session_state.cart:
            st.write("Prazna.")
        else:
            ukupno = sum(i['price'] for i in st.session_state.cart)
            detalji_za_email = ""
            for item in st.session_state.cart:
                st.write(f"**{item['ime']}** - {item['qty']}kg")
                detalji_za_email += f"- {item['ime']}: {item['qty']}kg\n"
            
            st.write("---")
            st.markdown(f"### Ukupno: {ukupno:.2f} €")
            
            ime = st.text_input("Ime i Prezime*")
            mob = st.text_input("Mobitel*")
            adr = st.text_input("Adresa dostave*")
            
            if st.button("✅ POTVRDI NARUDŽBU"):
                if ime and mob and adr:
                    with st.spinner('Slanje narudžbe...'):
                        if posalji_email_vlasniku(ime, mob, adr, detalji_za_email, f"{ukupno:.2f}"):
                            st.session_state.cart = []
                            st.success("🎉 Zaprimljeno! Javit ćemo Vam se ubrzo.")
                            st.balloons()
                        else:
                            st.error("Greška kod slanja. Provjerite vezu ili nas nazovite.")
                else:
                    st.warning("Molimo popunite sva polja!")
            
            if st.button("🗑️ Isprazni"):
                st.session_state.cart = []
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. STRANICE ---
with st.sidebar:
    st.markdown("## 🥩 IZBORNIK")
    izbor = st.radio("NAVIGACIJA", ["🛍️ TRGOVINA", "🏢 ZA UGOSTITELJE", "🧼 HACCP", "ℹ️ O NAMA"])
    st.write("---")
    st.caption(f"Sisak, {datetime.now().strftime('%d.%m.%2026.')}")

if izbor == "🛍️ TRGOVINA":
    st.markdown('<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-sub">MESNICA I PRERADA MESA SISAK</p>', unsafe_allow_html=True)
    
    col_t, col_k = st.columns([2.2, 1])
    with col_t:
        t_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with t_cols[i % 2]:
                st.markdown(f'<div class="product-card"><h3>{p["ime"]}</h3><p class="price-tag">{p["cijena"]:.2f} €/kg</p></div>', unsafe_allow_html=True)
                qty = st.number_input(f"Kg za {p['ime']}", 0.5, 50.0, 1.0, 0.5, key=f"p_{p['id']}", label_visibility="collapsed")
                if st.button(f"Dodaj u košaricu", key=f"btn_{p['id']}"):
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.rerun()
    prikazi_kosaricu(col_k)

elif izbor == "🏢 ZA UGOSTITELJE":
    st.title("🏢 Ugostiteljska Ponuda")
    st.warning("Minimalna količina 10kg, korak 2.5kg.")
    col_u, col_k = st.columns([2.2, 1])
    with col_u:
        for r in ugostitelji_ponuda:
            with st.expander(f"🛒 {r['ime']} - {r['cijena']:.2f} €/kg"):
                qty_u = st.number_input("Odaberite kg", 10.0, 1000.0, 10.0, 2.5, key=f"u_{r['id']}")
                if st.button(f"DODAJ {r['ime'].upper()}", key=f"ub_{r['id']}"):
                    st.session_state.cart.append({"ime": r['ime'], "qty": qty_u, "price": qty_u * r['cijena']})
                    st.rerun()
    prikazi_kosaricu(col_k)

elif izbor == "🧼 HACCP":
    st.title("🧼 HACCP Sigurnost")
    st.success("✅ ODOBRENI OBJEKT BR. 2686")
    st.write("Svi proizvodi prolaze strogu kontrolu kvalitete i sljedivosti.")

elif izbor == "ℹ️ O NAMA":
    st.title("ℹ️ Kontakt i Lokacija")
    st.write("📍 **Adresa:** Trg Josipa Mađerića 1, Sisak")
    st.write("📞 **Mobitel:** +385 91 XXX XXXX")
    st.write(f"📧 **Email:** {MOJ_EMAIL}")
    st.write("---")
    st.info("Obiteljska tradicija prerade mesa na domaći način.")

# --- FOOTER ---
st.write("---")
st.caption("© 2026. Mesnica Kojundžić Sisak")
