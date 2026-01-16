import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ==============================================================================
# SECTION 1 & 2: ZAKLJUČANO (Konfiguracija, Email, Dizajn, Prijevodi, Navigacija)
# ==============================================================================
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛍️ TRGOVINA", "nav_horeca": "🏢 ZA UGOSTITELJE", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA | PREMIUM QUALITY | 2026.", "cart_title": "VAŠ IZBOR",
        "cart_empty": "Košarica je prazna. Istražite našu ponudu.", 
        "note_vaga": "ℹ️ *Točan iznos bit će potvrđen nakon vaganja.*",
        "total": "UKUPNO", "form_name": "Ime i Prezime*", "form_tel": "Kontakt telefon*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Adresa i kućni broj*",
        "form_country": "Država*", "btn_order": "DOVRŠI NARUDŽBU", "success": "NARUDŽBA POSLANA! Hvala na povjerenju.",
        "unit_kg": "kg", "unit_pc": "kom"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 B2B SERVICE", "nav_haccp": "🧼 STANDARDS", "nav_info": "ℹ️ TRADITION",
        "title_sub": "BUTCHER SHOP | PREMIUM QUALITY | 2026.", "cart_title": "YOUR SELECTION",
        "cart_empty": "Your cart is empty. Explore our selection.", 
        "note_vaga": "ℹ️ *Final amount confirmed after weighing.*",
        "total": "TOTAL", "form_name": "Full Name*", "form_tel": "Phone Number*",
        "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Address*",
        "form_country": "Country*", "btn_order": "COMPLETE ORDER", "success": "ORDER SENT! Thank you.",
        "unit_kg": "kg", "unit_pc": "pcs"
    }
}

def posalji_email_vlasniku(ime, telefon, grad, adr, detalji_hr, ukupno, jezik_korisnika, country, ptt):
    predmet = f"🥩 NOVA PREMIUM NARUDŽBA: {ime}"
    tijelo = f"Kupac: {ime}\nTel: {telefon}\nLokacija: {adr}, {ptt} {grad}, {country}\nJezik: {jezik_korisnika}\n\nNARUČENO:\n{detalji_hr}\n\nUKUPNO: {ukupno} €"
    msg = MIMEText(tijelo); msg['Subject'] = predmet; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

st.set_page_config(page_title="Kojundžić Premium | 2026", page_icon="🥩", layout="wide")
izabrani_jezik = st.sidebar.selectbox("Language / Jezik", list(LANG_MAP.keys()))
T = LANG_MAP[izabrani_jezik]
menu = [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]]
choice = st.sidebar.radio("Navigation", menu, label_visibility="collapsed")

# GLOBALNI PREMIUM DIZAJN
st.markdown(f"""<style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="st-"] {{ font-family: 'Inter', sans-serif; }}
    .brand-name {{ color: #4a0000; font-size: 65px; font-weight: 900; text-align: center; letter-spacing: -2px; margin-bottom: -10px; }}
    .brand-sub {{ color: #888; font-size: 14px; text-align: center; letter-spacing: 3px; font-weight: 400; text-transform: uppercase; margin-bottom: 40px; }}
    
    .product-card {{ background: #ffffff; border-radius: 20px; padding: 0px; border: 1px solid #f0f0f0; transition: 0.4s; }}
    .product-img {{ border-radius: 20px 20px 0 0; width: 100%; height: 220px; object-fit: cover; }}
    .product-info {{ padding: 20px; text-align: left; }}
    
    .stButton>button {{ 
        border-radius: 12px; border: 1px solid #4a0000 !important; color: #4a0000 !important; 
        background: transparent !important; font-weight: 600; width: 100%; transition: 0.3s;
    }}
    .stButton>button:hover {{ background: #4a0000 !important; color: white !important; box-shadow: 0 10px 20px rgba(74,0,0,0.2); }}
    
    .cart-summary {{ background: #fdfdfd; border-left: 1px solid #eee; padding: 20px; height: 100%; }}
    .total-price {{ font-size: 32px; font-weight: 900; color: #4a0000; text-align: right; }}
</style>""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

# ==============================================================================
# SECTION 3: EKSPERTNO SUČELJE TRGOVINE (Marketing & Psihologija)
# ==============================================================================
if choice == T["nav_shop"]:
    st.markdown(f'<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)

    proizvodi = [
        {"id": 1, "hr_name": "Dimljeni hamburger", "name": {"HR 🇭🇷": "Dimljeni hamburger", "EN 🇬🇧": "Smoked Bacon"}, "price": 12.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 2, "hr_name": "Dimljeni buncek", "name": {"HR 🇭🇷": "Dimljeni buncek", "EN 🇬🇧": "Smoked Pork Hock"}, "price": 8.0, "type": "pc", "img": "https://images.unsplash.com"},
        {"id": 3, "hr_name": "Dimljeni prsni vršci", "name": {"HR 🇭🇷": "Dimljeni prsni vršci", "EN 🇬🇧": "Smoked Rib Tips"}, "price": 7.5, "type": "pc", "img": "https://images.unsplash.com"},
        {"id": 4, "hr_name": "Slavonska kobasica", "name": {"HR 🇭🇷": "Slavonska kobasica", "EN 🇬🇧": "Slavonian Sausage"}, "price": 16.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 12, "hr_name": "Čvarci", "name": {"HR 🇭🇷": "Čvarci", "EN 🇬🇧": "Pork Cracklings"}, "price": 20.0, "type": "kg", "img": "https://images.unsplash.com"}
    ]

    main_col, cart_col = st.columns([2.5, 1], gap="large")

    with main_col:
        st.markdown("### ARTISAN PONUDA")
        st.write("---")
        inner_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with inner_cols[i % 2]:
                st.markdown(f"""<div class="product-card">
                    <img src="{p['img']}" class="product-img">
                    <div class="product-info">
                        <h2 style="margin:0; font-size:22px; color:#111;">{p['name'][izabrani_jezik]}</h2>
                        <p style="color:#888; margin-top:5px; font-weight:700;">{p['price']:.2f} € / {T['unit_'+p['type']]}</p>
                    </div>
                </div>""", unsafe_allow_html=True)
                
                # Kontrole kolicine
                trenutna = st.session_state.cart.get(p['id'], 0.0)
                ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 1.5, 1])
                
                if ctrl_col1.button("−", key=f"sub_{p['id']}"):
                    if trenutna > 0:
                        skok = 1.0 if (p['type'] == "pc" or trenutna == 1.0) else 0.5
                        st.session_state.cart[p['id']] = max(0.0, trenutna - skok)
                        if st.session_state.cart[p['id']] == 0: del st.session_state.cart[p['id']]
                        st.rerun()

                ctrl_col2.markdown(f"<div style='text-align:center; font-weight:900; font-size:18px; padding-top:8px;'>{trenutna}</div>", unsafe_allow_html=True)

                if ctrl_col3.button("＋", key=f"add_{p['id']}"):
                    if p['type'] == "pc":
                        st.session_state.cart[p['id']] = trenutna + 1
                    else:
                        st.session_state.cart[p['id']] = 1.0 if trenutna == 0 else trenutna + 0.5
                    st.rerun()
                st.write("") # Razmak

    with cart_col:
        st.markdown(f"### {T['cart_title']}")
        st.write("---")
        suma = 0.0
        lista_za_email = ""
        
        if not st.session_state.cart:
            st.caption(T["cart_empty"])
        else:
            for pid, qty in list(st.session_state.cart.items()):
                p = next(x for x in proizvodi if x["id"] == pid)
                sub = p["price"] * qty
                suma += sub
                lista_za_email += f"- {p['hr_name']}: {qty} {p['type']}\n"
                
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span><b>{qty}x</b> {p['name'][izabrani_jezik]}</span>
                    <span>{sub:.2f} €</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.write("---")
            st.markdown(f"<p style='margin:0; color:#888;'>{T['total']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='total-price'>{suma:.2f} €</p>", unsafe_allow_html=True)
            st.caption(T["note_vaga"])
            
            with st.container():
                st.write("")
                with st.expander("OSOBNI PODACI ZA DOSTAVU", expanded=False):
                    with st.form("premium_order"):
                        f_ime = st.text_input(T["form_name"])
                        f_tel = st.text_input(T["form_tel"])
                        f_cty = st.text_input(T["form_country"], value="Hrvatska")
                        f_grad = st.text_input(T["form_city"])
                        f_ptt = st.text_input(T["form_zip"])
                        f_adr = st.text_input(T["form_addr"])
                        
                        btn = st.form_submit_button(T["btn_order"])
                        if btn:
                            if f_ime and f_tel and f_grad and f_adr:
                                if posalji_email_vlasniku(f_ime, f_tel, f_grad, f_adr, lista_za_email, suma, izabrani_jezik, f_cty, f_ptt):
                                    st.success(T["success"]); st.session_state.cart = {}; st.balloons()
                                else: st.error("Greška sustava.")
                            else: st.warning("Popunite obavezna polja (*)")

# ==============================================================================
# SECTION 4: ZAKLJUČANO (Horeca, Haccp, Info)
# ==============================================================================
elif choice == T["nav_horeca"]:
    st.header(T["horeca_title"]); st.markdown(T["horeca_text"])
elif choice == T["nav_haccp"]:
    st.header(T["haccp_title"]); st.markdown(T["haccp_text"])
elif choice == T["nav_info"]:
    st.header(T["info_title"]); st.markdown(T["info_text"]); st.map(data={'lat': [45.485], 'lon': [16.373]})
