import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Postavke aplikacije za 2026. godinu
st.set_page_config(page_title="Kojundžić | Mesnica i Prerada mesa", page_icon="🥩", layout="wide")

@st.cache_data
def load_image(url):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# --- DIZAJN I MARKETINŠKA PSIHOLOGIJA ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .brand-name { color: #8B0000; font-size: 70px; font-weight: 900; text-align: center; margin-bottom: 0px; text-transform: uppercase; letter-spacing: 5px; line-height: 1; }
    .brand-sub { color: #333; font-size: 28px; text-align: center; margin-top: 0px; margin-bottom: 30px; font-weight: 600; letter-spacing: 2px; }
    
    .product-card { background-color: white; border-radius: 20px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #efefef; margin-bottom: 25px; text-align: center; }
    .price-tag { color: #8B0000; font-size: 24px; font-weight: bold; }
    
    .badge-bestseller { background-color: #FFD700; color: black; padding: 5px 15px; border-radius: 50px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    .badge-chef { background-color: #8B0000; color: white; padding: 5px 15px; border-radius: 50px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    
    .stButton>button { background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%); color: white !important; border-radius: 50px; width: 100%; font-weight: bold; height: 3em; }
    .sidebar-cart { background-color: #ffffff; padding: 25px; border-radius: 20px; border: 1px solid #eee; box-shadow: 0 5px 20px rgba(0,0,0,0.05); position: sticky; top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Inicijalizacija sesija
if 'cart' not in st.session_state: st.session_state.cart = []
if 'sales_tracker' not in st.session_state: st.session_state.sales_tracker = {}

# --- PODACI O PROIZVODIMA ---
proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50, "slika": "images.unsplash.com"},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50, "slika": "images.unsplash.com"},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.20, "slika": "images.unsplash.com"},
    {"id": 4, "ime": "Premium Buđola", "cijena": 19.50, "slika": "images.unsplash.com"},
    {"id": 5, "ime": "Dimljeni vrat", "cijena": 15.00, "slika": "images.unsplash.com"},
    {"id": 6, "ime": "Domaća salama", "cijena": 16.00, "slika": "images.unsplash.com"},
]

ugostitelji_ponuda = [
    {"id": 101, "ime": "Ćevapi (juneći)", "cijena": 12.00},
    {"id": 102, "ime": "Pljeskavice", "cijena": 11.50},
    {"id": 103, "ime": "Roštiljke / Debricinke", "cijena": 11.00},
    {"id": 104, "ime": "Šiš-ćevapi", "cijena": 12.50},
    {"id": 201, "ime": "Juneći biftek", "cijena": 35.00},
    {"id": 202, "ime": "Juneći ramstek s kosti", "cijena": 18.50},
    {"id": 203, "ime": "Juneći ramstek bez kosti", "cijena": 22.00},
    {"id": 204, "ime": "Teletina (but/plećka)", "cijena": 14.50},
]

najprodavaniji_artikl = None
if st.session_state.sales_tracker:
    najprodavaniji_artikl = max(st.session_state.sales_tracker, key=st.session_state.sales_tracker.get)

# --- FUNKCIJA ZA KOŠARICU ---
def prikazi_kosaricu(col):
    with col:
        st.markdown('<div class="sidebar-cart">', unsafe_allow_html=True)
        st.subheader("🛒 Vaša Košarica")
        if not st.session_state.cart:
            st.write("Prazna.")
        else:
            ukupno = sum(i['price'] for i in st.session_state.cart)
            email_lista = ""
            for item in st.session_state.cart:
                st.write(f"**{item['ime']}** ({item['qty']}kg)")
                email_lista += f"- {item['ime']}: {item['qty']}kg%0D%0A"
            st.write("---")
            st.markdown(f"### Ukupno: {ukupno:.2f} €")
            if st.button("🗑️ Isprazni"):
                st.session_state.cart = []
                st.rerun()
            st.write("---")
            ime = st.text_input("Ime i Prezime*")
            mob = st.text_input("Mobitel*")
            adr = st.text_input("Adresa, Grad, PTT*")
            if st.button("✅ POŠALJI NARUDŽBU"):
                if ime and mob and adr:
                    predmet = f"Narudžba - {ime}"
                    tijelo = f"Nova narudžba od: {ime}%0D%0A"
                    tijelo += f"Mobitel: {mob}%0D%0A"
                    tijelo += f"Adresa: {adr}%0D%0A---%0D%0A"
                    tijelo += email_lista
                    tijelo += f"---%0D%0AUKUPNO: {ukupno:.2f} EUR"
                    mail_url = f"mailto:narudzbe@kojundzic-meso.hr?subject={predmet}&body={tijelo}"
                    st.success("Narudžba spremna!")
                    st.markdown(f'<a href="{mail_url}" style="text-decoration:none;"><div style="background-color:#28a745;color:white;padding:10px;text-align:center;border-radius:10px;font-weight:bold;">📧 POŠALJI EMAIL</div></a>', unsafe_allow_html=True)
                else:
                    st.error("Popunite sva polja!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- NAVIGACIJA ---
with st.sidebar:
    st.markdown("## 🥩 IZBORNIK")
    izbor = st.radio("NAVIGACIJA", ["🛍️ TRGOVINA", "🏢 ZA UGOSTITELJE", "🚜 DOBAVLJAČI", "🧼 HACCP", "ℹ️ O NAMA"])
    st.write("---")
    st.caption("Sisak, 15. siječanj 2026.")

# --- STRANICE ---
if izbor == "🛍️ TRGOVINA":
    st.markdown('<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-sub">MESNICA I PRERADA MESA</p>', unsafe_allow_html=True)
    
    col_trgovina, col_kosarica = st.columns([2.5, 1])
    with col_trgovina:
        prod_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with prod_cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                if p['ime'] == "Domaća salama": st.markdown('<span class="badge-chef">⭐ PREPORUKA</span>', unsafe_allow_html=True)
                elif p['ime'] == najprodavaniji_artikl: st.markdown('<span class="badge-bestseller">🏆 NAJPRODAVANIJE</span>', unsafe_allow_html=True)
                
                st.markdown(f"### {p['ime']}")
                st.markdown(f"<div class='price-tag'>{p['cijena']:.2f} €/kg</div>", unsafe_allow_html=True)
                qty = st.number_input(f"Kg za {p['ime']}", 0.5, 50.0, 1.0, 0.5, key=f"q_{p['id']}")
                if st.button("DODAJ", key=f"b_{p['id']}"):
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.session_state.sales_tracker[p['ime']] = st.session_state.sales_tracker.get(p['ime'], 0) + qty
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    prikazi_kosaricu(col_kosarica)

elif izbor == "🏢 ZA UGOSTITELJE":
    st.title("🏢 Premium Ugostiteljska Ponuda")
    st.warning("⚠️ **Dostava:** Svježi program (ćevapi, bifteci) dostavljamo isključivo vlastitom hladnjačom.")
    
    col_u, col_k = st.columns([2.5, 1])
    with col_u:
        u_cols = st.columns(2)
        for i, r in enumerate(ugostitelji_ponuda):
            with u_cols[i % 2]:
                with st.expander(f"🛒 {r['ime']} - {r['cijena']:.2f} €/kg"):
                    # POSTAVKE: Početna 10kg, korak 2.5kg
                    qty_u = st.number_input(
                        f"Količina (kg)", 
                        min_value=10.0, 
                        max_value=1000.0, 
                        value=10.0, 
                        step=2.5, 
                        key=f"u_{r['id']}"
                    )
                    if st.button(f"DODAJ {r['ime']}", key=f"ub_{r['id']}"):
                        st.session_state.cart.append({"ime": r['ime'], "qty": qty_u, "price": qty_u * r['cijena']})
                        st.rerun()
    prikazi_kosaricu(col_k)

elif izbor == "🚜 DOBAVLJAČI":
    st.title("🚜 Porijeklo i Kvaliteta")
    st.info("Sva stoka se otkupljuje od malih OPG-ova iz okolice Siska (Banovina i Posavina).")
    st.write("- **Tradicionalan uzgoj** na otvorenom.")
    st.write("- **Hranjeno domaćom hranom** bez GMO-a.")

elif izbor == "🧼 HACCP":
    st.title("🧼 Sigurnost Hrane")
    st.success("✅ **Odobreni objekt br. 2686**")
    st.write("Proizvodnja se odvija pod strogim nadzorom HACCP sustava i veterinarske inspekcije.")

elif izbor == "ℹ️ O NAMA":
    st.title("ℹ️ O Mesnici Kojundžić")
    st.write("Obiteljska tvrtka posvećena tradiciji i vrhunskoj kvaliteti mesa od 1990-ih.")
    st.info("📍 Trg Josipa Mađerića 1, Sisak")
    st.map(pd.DataFrame({'lat': [45.4832], 'lon': [16.3761]}))

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026. Mesnica Kojundžić Sisak | Kvaliteta bez kompromisa")
