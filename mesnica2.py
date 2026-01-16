import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- 1. KONFIGURACIJA I PRIJEVODI (ZAKLJUČANO) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛍️ TRGOVINA", "nav_horeca": "🏢 ZA UGOSTITELJE", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA | 2026.", "cart_title": "🛒 Vaša Košarica",
        "cart_empty": "Prazna. Dodajte artikle.", 
        "note_vaga": """ℹ️ <b>Napomena:</b> Navedene cijene su točne, dok je iznos u košarici informativan. 
                     Točan iznos znat će se nakon vaganja. Konačan iznos znati ćete kada vam paket stigne, 
                     a mi ćemo se truditi da količine i informativni iznos bude što točniji pravom iznosu.""",
        "total": "Približno", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "form_country": "Država*", "btn_order": "✅ POTVRDI NARUDŽBU", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom"
    }
}

st.set_page_config(page_title="Kojundžić | 2026", page_icon="🥩", layout="wide")

# --- 2. LOGIKA ZA EMAIL (ZAKLJUČANO) ---
def posalji_email_vlasniku(ime, telefon, grad, adr, detalji_hr, ukupno, jezik_korisnika, country, ptt):
    predmet = f"🥩 NOVA NARUDŽBA: {ime}"
    tijelo = f"Kupac: {ime}\nTel: {telefon}\nDržava: {country}\nGrad: {grad} ({ptt})\nAdresa: {adr}\n\nArtikli:\n{detalji_hr}\n\nUkupno: {ukupno} €"
    msg = MIMEText(tijelo); msg['Subject'] = predmet; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

# --- 3. DIZAJN I NAVIGACIJA (ZAKLJUČANO) ---
izabrani_jezik = st.sidebar.selectbox("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[izabrani_jezik]
menu = [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]]
choice = st.sidebar.radio("Navigacija", menu, label_visibility="collapsed")

st.markdown(f"""<style>
    .brand-name {{ color: #8B0000; font-size: 55px; font-weight: 900; text-align: center; text-transform: uppercase; margin:0; }}
    .brand-sub {{ color: #333; font-size: 18px; text-align: center; font-weight: 600; margin-bottom: 25px; }}
    .product-card {{ background: white; border-radius: 12px; padding: 15px; border: 1px solid #eee; text-align: center; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); transition: 0.3s; }}
    .product-img {{ border-radius: 8px; width: 100%; height: 180px; object-fit: cover; margin-bottom: 10px; }}
    .stButton>button {{ 
        background-color: white !important; 
        color: #8B0000 !important; 
        border: 1px solid #8B0000 !important; 
        border-radius: 10px !important;
        width: 100%;
        transition: 0.2s;
    }}
    .stButton>button:hover {{ background-color: #8B0000 !important; color: white !important; }}
    .qty-display {{ font-size: 20px; font-weight: 700; color: #4a0000; text-align: center; padding-top: 5px; }}
</style>""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 4. TRGOVINA (ISPRAVLJENI SVI ERRORI) ---
if choice == T["nav_shop"]:
    st.markdown(f'<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)

    proizvodi = [
        {"id": 1, "hr_name": "Dimljeni hamburger", "price": 12.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 2, "hr_name": "Dimljeni buncek", "price": 8.0, "type": "pc", "img": "https://images.unsplash.com"},
        {"id": 3, "hr_name": "Dimljeni prsni vršci", "price": 9.0, "type": "pc", "img": "https://images.unsplash.com"},
        {"id": 4, "hr_name": "Slavonska kobasica", "price": 16.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 5, "hr_name": "Domaća salama", "price": 25.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 6, "hr_name": "Dimljene kosti", "price": 2.5, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 7, "hr_name": "Dimljene nogice, uši, rep - mix", "price": 2.5, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 8, "hr_name": "Panceta", "price": 17.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 9, "hr_name": "Dimljeni vrat bez kosti", "price": 15.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 10, "hr_name": "Dimljeni kremenadl bez kosti", "price": 15.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 11, "hr_name": "Buđola", "price": 20.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 12, "hr_name": "Čvarci", "price": 20.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 13, "hr_name": "Mast", "price": 3.0, "type": "kg", "img": "https://images.unsplash.com"}
    ]

    # ISPRAVLJENO: st.columns(2) definira izgled (glavno vs košarica)
    col_main, col_cart = st.columns([2, 1])

    with col_main:
        inner_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with inner_cols[i % 2]:
                st.markdown(f"""<div class="product-card">
                    <img src="{p['img']}" class="product-img">
                    <h3>{p['hr_name']}</h3>
                    <p style="color:#666;">{p['price']:.2f} € / {T['unit_'+p['type']]}</p>
                </div>""", unsafe_allow_html=True)
                
                trenutna = st.session_state.cart.get(p['id'], 0.0)
                # ISPRAVLJENO: st.columns(3) za kontrole artikla
                c1, c2, c3 = st.columns(3)
                
                if c1.button("−", key=f"min_{p['id']}"):
                    if trenutna > 0:
                        skok = 1.0 if (p['type'] == "pc" or trenutna == 1.0) else 0.5
                        st.session_state.cart[p['id']] = max(0.0, trenutna - skok)
                        if st.session_state.cart[p['id']] == 0: del st.session_state.cart[p['id']]
                        st.rerun()
                
                c2.markdown(f'<p class="qty-display">{trenutna}</p>', unsafe_allow_html=True)
                
                if c3.button("＋", key=f"pls_{p['id']}"):
                    if p['type'] == "pc":
                        st.session_state.cart[p['id']] = trenutna + 1
                    else:
                        st.session_state.cart[p['id']] = 1.0 if trenutna == 0 else trenutna + 0.5
                    st.rerun()
                st.write("---")

    with col_cart:
        st.markdown(f"### {T['cart_title']}")
        st.info(T["note_vaga"], icon="ℹ️")
        st.write("---")

        suma = 0.0
        detalji_mail = ""
        
        if not st.session_state.cart:
            st.warning(T["cart_empty"])
        else:
            for pid, qty in list(st.session_state.cart.items()):
                p = next(x for x in proizvodi if x["id"] == pid)
                sub = p["price"] * qty
                suma += sub
                detalji_mail += f"- {p['hr_name']}: {qty} {p['type']}\n"
                st.markdown(f"**{p['hr_name']}**  \n{qty} {T['unit_'+p['type']]} = {sub:.2f} €")
            
            st.write("---")
            st.subheader(f"{T['total']}: {suma:.2f} €")

            with st.expander("📍 PODACI ZA DOSTAVU", expanded=True):
                with st.form("final_order"):
                    f_ime = st.text_input(T["form_name"])
                    f_tel = st.text_input(T["form_tel"])
                    f_cty = st.text_input(T["form_country"], value="Hrvatska")
                    f_grad = st.text_input(T["form_city"])
                    f_ptt = st.text_input(T["form_zip"])
                    f_adr = st.text_input(T["form_addr"])
                    
                    if st.form_submit_button(T["btn_order"]):
                        # STRIKTNA PROVJERA
                        if f_ime and f_tel and f_cty and f_grad and f_ptt and f_adr:
                            if posalji_email_vlasniku(f_ime, f_tel, f_grad, f_adr, detalji_mail, suma, "HR 🇭🇷", f_cty, f_ptt):
                                st.success(T["success"]); st.session_state.cart = {}; st.balloons(); st.rerun()
                            else: 
                                st.error("Greška pri slanju.")
                        else: 
                            st.error("Narudžba nije poslana. Molimo ispunite SVA polja za dostavu.")

# --- 5. OSTALE RUBRIKE (ZAKLJUČANO) ---
elif choice == T["nav_horeca"]:
    st.header(T["horeca_title"]); st.markdown(T["horeca_text"])
elif choice == T["nav_haccp"]:
    st.header(T["haccp_title"]); st.markdown(T["haccp_text"])
elif choice == T["nav_info"]:
    st.header(T["info_title"]); st.markdown(T["info_text"]); st.map(data={'lat': [45.485], 'lon': [16.373]})
