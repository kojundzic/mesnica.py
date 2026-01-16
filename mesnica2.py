import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- 1. POSTAVKE I PRIJEVODI ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛍️ TRGOVINA", "nav_horeca": "🏢 UGOSTITELJI", "nav_info": "🧼 HACCP & INFO",
        "title_sub": "MESNICA I PRERADA MESA | 2026.", "cart_title": "🛒 Vaša Košarica",
        "cart_empty": "Prazna. Dodajte artikle.", "note_vaga": "ℹ️ VAŽNO: Cijena je informativna (vaganje pri slanju).",
        "total": "Ukupno (cca)", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad/Mjesto*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "✅ POTVRDI NARUDŽBU", "btn_clear": "🗑️ Isprazni", "success": "Hvala! Narudžba poslana.",
        "unit_kg": "kg", "unit_pc": "kom", "horeca_info": "Za ugostitelje radimo po dogovoru.",
        "contact": "Kontakt", "loc": "Lokacija: Trg Josipa Mađerića 1, Sisak"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 HORECA", "nav_info": "🧼 HACCP & INFO",
        "title_sub": "BUTCHER SHOP & MEAT PROCESSING | 2026.", "cart_title": "🛒 Your Cart",
        "cart_empty": "Empty. Add items.", "note_vaga": "ℹ️ NOTE: Price is informative (weighing on dispatch).",
        "total": "Total (approx)", "form_name": "Full Name*", "form_tel": "Phone Number*",
        "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Street & House Number*",
        "btn_order": "✅ CONFIRM ORDER", "btn_clear": "🗑️ Clear Cart", "success": "Thank you! Order sent.",
        "unit_kg": "kg", "unit_pc": "pcs", "horeca_info": "Special production for restaurants & hotels.",
        "contact": "Contact", "loc": "Location: Trg Josipa Mađerića 1, Sisak"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 GASTRONOMIE", "nav_info": "🧼 HACCP & INFO",
        "title_sub": "METZGEREI & FLEISCHVERARBEITUNG | 2026.", "cart_title": "🛒 Warenkorb",
        "cart_empty": "Leer. Artikel hinzufügen.", "note_vaga": "ℹ️ INFO: Preis ist informativ (Wiegung beim Versand).",
        "total": "Gesamt (ca.)", "form_name": "Vor- und Nachname*", "form_tel": "Telefonnummer*",
        "form_city": "Stadt*", "form_zip": "Postleitzahl*", "form_addr": "Straße & Hausnummer*",
        "btn_order": "✅ BESTELLUNG BESTÄTIGEN", "btn_clear": "🗑️ Leeren", "success": "Danke! Bestellung gesendet.",
        "unit_kg": "kg", "unit_pc": "stk", "horeca_info": "Spezialproduktion für Gastronomie.",
        "contact": "Kontakt", "loc": "Standort: Trg Josipa Mađerića 1, Sisak"
    }
}

st.set_page_config(page_title="Kojundžić | 2026", page_icon="🥩", layout="wide")

# --- 2. LOGIKA ZA EMAIL (FIKSNO NA HRVATSKOM) ---
def posalji_email_vlasniku(ime, telefon, grad, ptt, adr, detalji_hr, ukupno, jezik_korisnika):
    # Poruka je uvijek na hrvatskom za vlasnika
    predmet = f"🥩 NOVA NARUDŽBA: {ime}"
    tijelo = f"""
    STIGLA JE NOVA NARUDŽBA IZ WEBSHOPA (2026.)
    -------------------------------------------
    Kupac: {ime}
    Telefon: {telefon}
    Adresa: {adr}, {ptt} {grad}
    
    NAPOMENA O JEZIKU: Kupac koristi jezik: {jezik_korisnika}
    (U slučaju kontakta, koristite ovaj jezik ako kupac ne govori hrvatski).
    
    NARUČENI ARTIKLI (Hrvatski nazivi):
    {detalji_hr}
    
    PRIBLIŽNI IZNOS: {ukupno} €
    -------------------------------------------
    """
    msg = MIMEText(tijelo)
    msg['Subject'] = predmet
    msg['From'] = MOJ_EMAIL
    msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT); server.starttls()
        server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

# --- 3. DIZAJN I ODABIR JEZIKA ---
col_logo, col_lang = st.columns([3, 1])
with col_lang:
    izabrani_jezik = st.selectbox("Language / Jezik", list(LANG_MAP.keys()))
    T = LANG_MAP[izabrani_jezik]

st.markdown(f"""<style>
    .stApp {{ background-color: #fdfdfd; }}
    .brand-name {{ color: #8B0000; font-size: 60px; font-weight: 900; text-align: center; text-transform: uppercase; margin-bottom:0px; }}
    .brand-sub {{ color: #333; font-size: 20px; text-align: center; font-weight: 600; margin-top:0px; margin-bottom: 35px; }}
    .product-card {{ background-color: white; border-radius: 12px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #eee; text-align: center; margin-bottom:10px; }}
    .stButton>button {{ background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%); color: white !important; font-weight: bold; border-radius: 10px; }}
</style>""", unsafe_allow_html=True)

if 'cart_dict' not in st.session_state: st.session_state.cart_dict = {}

# --- 4. PROIZVODI (S FIKSNIM HR KLJUČEM) ---
proizvodi = [
    {"id": 1, "hr_ime": "Dimljeni hamburger", "ime": {"HR 🇭🇷": "Dimljeni hamburger", "EN 🇬🇧": "Smoked Bacon", "DE 🇩🇪": "Geräucherter Speck"}, "cijena": 12.0, "tip": 0},
    {"id": 2, "hr_ime": "Slavonska kobasica", "ime": {"HR 🇭🇷": "Slavonska kobasica", "EN 🇬🇧": "Slavonian Sausage", "DE 🇩🇪": "Slawonische Wurst"}, "cijena": 16.0, "tip": 0},
    {"id": 3, "hr_ime": "Dimljeni buncek", "ime": {"HR 🇭🇷": "Dimljeni buncek", "EN 🇬🇧": "Smoked Pork Hock", "DE 🇩🇪": "Geräucherte Stelze"}, "cijena": 8.0, "tip": 1},
    {"id": 4, "hr_ime": "Panceta", "ime": {"HR 🇭🇷": "Panceta", "EN 🇬🇧": "Pancetta", "DE 🇩🇪": "Pancetta Speck"}, "cijena": 17.0, "tip": 0},
    {"id": 12, "hr_ime": "Čvarci", "ime": {"HR 🇭🇷": "Čvarci", "EN 🇬🇧": "Pork Cracklings", "DE 🇩🇪": "Grammeln"}, "cijena": 20.0, "tip": 0},
]

# --- 5. PRIKAZ TRGOVINE ---
izbor = st.sidebar.radio("MENU", [T["nav_shop"], T["nav_horeca"], T["nav_info"]])

if izbor == T["nav_shop"]:
    st.markdown('<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)
    
    col_t, col_k = st.columns([2, 1.2])
    with col_t:
        rows = st.columns(2)
        for idx, p in enumerate(proizvodi):
            p_vidljivo_ime = p["ime"][izabrani_jezik] # Ime koje kupac vidi
            p_hr_ime = p["hr_ime"] # Ime koje ide vama u mail
            
            with rows[idx % 2]:
                st.markdown(f'<div class="product-card"><b>{p_vidljivo_ime}</b>', unsafe_allow_html=True)
                lbl = f"€/{T['unit_pc'] if p['tip']==1 else T['unit_kg']}"
                st.markdown(f'<p style="color:#8B0000; font-weight:bold;">{p["cijena"]:.2f} {lbl}</p>', unsafe_allow_html=True)
                
                key = f"p_{p['id']}"
                step = 1.0 if p["tip"] == 1 else 0.5
                curr = st.session_state.cart_dict.get(p_hr_ime, {"qty": 0.0})["qty"]
                
                val = st.number_input(f"Qty {p_vidljivo_ime}", min_value=0.0, step=step, value=float(curr), key=key, label_visibility="collapsed")
                
                if p["tip"] == 0 and val == 0.5:
                    val = 1.0; st.session_state[key] = 1.0; st.rerun()
                
                # Ključ u sesiji je uvijek hrvatsko ime radi lakše obrade
                st.session_state.cart_dict[p_hr_ime] = {
                    "qty": val, 
                    "price": val * p["cijena"], 
                    "is_komad": p["tip"] == 1,
                    "p_ime_kupac": p_vidljivo_ime # Čuvamo i što je on vidio
                }
                st.markdown('</div>', unsafe_allow_html=True)

    with col_k:
        st.subheader(T["cart_title"])
        aktivni = {k: v for k, v in st.session_state.cart_dict.items() if v['qty'] > 0}
        if not aktivni:
            st.write(T["cart_empty"])
        else:
            st.info(T["note_vaga"])
            ukupno = 0
            detalji_hr = "" # Ovo gradimo za vaš e-mail
            
            for hr_ime, pod in aktivni.items():
                jed_kupac = T["unit_pc"] if pod['is_komad'] else T["unit_kg"]
                jed_hr = "kom" if pod['is_komad'] else "kg"
                
                # Kupac vidi prevedeno u košarici
                st.write(f"**{pod['p_ime_kupac']}**: {pod['qty']} {jed_kupac} ({pod['price']:.2f} €)")
                
                ukupno += pod['price']
                # Za vlasnika pišemo na hrvatskom
                detalji_hr += f"- {hr_ime}: {pod['qty']} {jed_hr}\n"
            
            st.markdown(f"### {T['total']}: {ukupno:.2f} €")
            ime = st.text_input(T["form_name"]); tel = st.text_input(T["form_tel"])
            grad = st.text_input(T["form_city"]); ptt = st.text_input(T["form_zip"]); adr = st.text_input(T["form_addr"])
            
            if st.button(T["btn_order"]):
                if ime and tel and grad and adr:
                    # Šaljemo detalje na hrvatskom i jezik koji je kupac koristio
                    if posalji_email_vlasniku(ime, tel, grad, ptt, adr, detalji_hr, f"{ukupno:.2f}", izabrani_jezik):
                        st.success(T["success"]); st.session_state.cart_dict = {}; st.balloons()
                        st.rerun()
                else: st.warning("!!!")

# --- OSTALE STRANICE ---
elif izbor == T["nav_horeca"]:
    st.title(T["nav_horeca"])
    st.write(T["horeca_info"])

elif izbor == T["nav_info"]:
    st.title(T["nav_info"])
    st.write(T["loc"])
    st.write(f"{T['contact']}: tomislavtomi90@gmail.com")
