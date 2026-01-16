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
        "nav_shop": "🛍️ TRGOVINA", "nav_horeca": "🏢 ZA UGOSTITELJE", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA | 2026.", "cart_title": "🛒 Vaša Košarica",
        "cart_empty": "Prazna. Dodajte artikle pomoću +", "note_vaga": "ℹ️ VAŽNO: Cijena je informativna. Točan iznos znat će se nakon vaganja pri primitku paketa.",
        "total": "Približno", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "✅ POTVRDI NARUDŽBU", "btn_clear": "🗑️ Isprazni", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom", 
        "horeca_text": "Za ugostiteljske objekte radimo uslužnu proizvodnju po dogovoru.",
        "haccp_text": "ODOBRENI OBJEKT BR. 2686",
        "info_text": "Trg Josipa Mađerića 1, Sisak"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 FOR RESTAURANTS", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP & MEAT PROCESSING | 2026.", "cart_title": "🛒 Your Cart",
        "cart_empty": "Empty. Add items using +", "note_vaga": "ℹ️ NOTE: Prices are informative. The exact amount will be known after weighing upon receipt.",
        "total": "Approximate total", "form_name": "Full Name*", "form_tel": "Phone Number*",
        "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Street & House Number*",
        "btn_order": "✅ CONFIRM ORDER", "btn_clear": "🗑️ Clear", "success": "Received! Thank you.",
        "unit_kg": "kg", "unit_pc": "pcs", 
        "horeca_text": "We offer custom production for restaurants and hotels by agreement.",
        "haccp_text": "APPROVED ESTABLISHMENT NO. 2686",
        "info_text": "Trg Josipa Mađerića 1, Sisak, Croatia"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 FÜR GASTRONOMIE", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI & FLEISCHVERARBEITUNG | 2026.", "cart_title": "🛒 Warenkorb",
        "cart_empty": "Leer. Artikel mit + hinzufügen", "note_vaga": "ℹ️ INFO: Die Preise sind informativ. Der genaue Betrag steht nach dem Wiegen fest.",
        "total": "Ungefährer Gesamtbetrag", "form_name": "Vor- und Nachname*", "form_tel": "Telefonnummer*",
        "form_city": "Stadt*", "form_zip": "Postleitzahl*", "form_addr": "Straße & Hausnummer*",
        "btn_order": "✅ BESTELLUNG BESTÄTIGEN", "btn_clear": "🗑️ Leeren", "success": "Eingegangen! Vielen Dank.",
        "unit_kg": "kg", "unit_pc": "stk", 
        "horeca_text": "Für Gastronomiebetriebe führen wir Lohnfertigung nach Vereinbarung durch.",
        "haccp_text": "ZUGELASSENER BETRIEB NR. 2686",
        "info_text": "Trg Josipa Mađerića 1, Sisak, Kroatien"
    }
}

st.set_page_config(page_title="Kojundžić | Mesnica i Prerada", page_icon="🥩", layout="wide")

# --- 2. LOGIKA ZA EMAIL (FIKSNO NA HRVATSKOM) ---
def posalji_email_vlasniku(ime, telefon, grad, ptt, adr, detalji_hr, ukupno, jezik_korisnika):
    predmet = f"🥩 NOVA NARUDŽBA: {ime}"
    tijelo = f"""
    Stigla je nova narudžba putem weba! (Siječanj 2026.)
    -----------------------------------
    Kupac: {ime}
    Telefon: {telefon}
    Adresa: {adr}, {ptt} {grad}
    
    JEZIK KUPCA: {jezik_korisnika}
    
    NARUČENI ARTIKLI (Hrvatski):
    -----------------------------------
    {detalji_hr}
    
    PRIBLIŽNI IZNOS: {ukupno} €
    -----------------------------------
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

# --- 3. ODABIR JEZIKA ---
col_logo_space, col_lang_picker = st.columns([3, 1])
with col_lang_picker:
    izabrani_jezik = st.selectbox("Izaberite jezik / Select Language", list(LANG_MAP.keys()))
    T = LANG_MAP[izabrani_jezik]

# --- 4. DIZAJN (CSS) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #fdfdfd; }}
    .brand-name {{ color: #8B0000; font-size: 70px; font-weight: 900; text-align: center; text-transform: uppercase; margin-bottom:0px; letter-spacing: 5px; }}
    .brand-sub {{ color: #333; font-size: 22px; text-align: center; font-weight: 600; margin-top:0px; margin-bottom: 35px; letter-spacing: 2px; }}
    .product-card {{ background-color: white; border-radius: 12px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #eee; text-align: center; margin-bottom:10px; }}
    .price-tag {{ color: #8B0000; font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
    .stButton>button {{ background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%); color: white !important; font-weight: bold; border-radius: 50px; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

if 'cart_dict' not in st.session_state: st.session_state.cart_dict = {}

# --- 5. PODACI O PROIZVODIMA ---
proizvodi = [
    {"id": 1, "hr_ime": "Dimljeni hamburger", "ime": {"HR 🇭🇷": "Dimljeni hamburger", "EN 🇬🇧": "Smoked Bacon", "DE 🇩🇪": "Geräucherter Speck"}, "cijena": 12.0, "tip": 0},
    {"id": 2, "hr_ime": "Dimljeni buncek", "ime": {"HR 🇭🇷": "Dimljeni buncek", "EN 🇬🇧": "Smoked Pork Hock", "DE 🇩🇪": "Geräucherte Stelze"}, "cijena": 8.0, "tip": 1},
    {"id": 3, "hr_ime": "Dimljeni prsni vršci", "ime": {"HR 🇭🇷": "Dimljeni prsni vršci", "EN 🇬🇧": "Smoked Rib Tips", "DE 🇩🇪": "Geräucherte Rippenspitzen"}, "cijena": 9.0, "tip": 1},
    {"id": 4, "hr_ime": "Slavonska kobasica", "ime": {"HR 🇭🇷": "Slavonska kobasica", "EN 🇬🇧": "Slavonian Sausage", "DE 🇩🇪": "Slawonische Wurst"}, "cijena": 16.0, "tip": 0},
    {"id": 5, "hr_ime": "Domaća salama", "ime": {"HR 🇭🇷": "Domaća salama", "EN 🇬🇧": "Homemade Salami", "DE 🇩🇪": "Hausgemachte Salami"}, "cijena": 25.0, "tip": 0},
    {"id": 6, "hr_ime": "Dimljene kosti", "ime": {"HR 🇭🇷": "Dimljene kosti", "EN 🇬🇧": "Smoked Bones", "DE 🇩🇪": "Geräucherte Knochen"}, "cijena": 2.5, "tip": 0},
    {"id": 7, "hr_ime": "Dimljene nogice, uši, rep - mix", "ime": {"HR 🇭🇷": "Dimljene nogice, uši, rep - mix", "EN 🇬🇧": "Smoked Trotters, Ears, Tail - Mix", "DE 🇩🇪": "Geräucherte Füße, Ohren, Schwanz - Mix"}, "cijena": 2.5, "tip": 0},
    {"id": 8, "hr_ime": "Panceta", "ime": {"HR 🇭🇷": "Panceta", "EN 🇬🇧": "Pancetta", "DE 🇩🇪": "Pancetta Speck"}, "cijena": 17.0, "tip": 0},
    {"id": 9, "hr_ime": "Dimljeni vrat bez kosti", "ime": {"HR 🇭🇷": "Dimljeni vrat bez kosti", "EN 🇬🇧": "Smoked Boneless Neck", "DE 🇩🇪": "Geräucherter Schopf (ohne Knochen)"}, "cijena": 15.0, "tip": 0},
    {"id": 10, "hr_ime": "Dimljeni kremenadl bez kosti", "ime": {"HR 🇭🇷": "Dimljeni kremenadl bez kosti", "EN 🇬🇧": "Smoked Boneless Loin", "DE 🇩🇪": "Geräuchertes Karree (ohne Knochen)"}, "cijena": 15.0, "tip": 0},
    {"id": 11, "hr_ime": "Buđola", "ime": {"HR 🇭🇷": "Buđola", "EN 🇬🇧": "Budjola (Dried Neck)", "DE 🇩🇪": "Budjola (Getrockneter Schopf)"}, "cijena": 20.0, "tip": 0},
    {"id": 12, "hr_ime": "Čvarci", "ime": {"HR 🇭🇷": "Čvarci", "EN 🇬🇧": "Pork Cracklings", "DE 🇩🇪": "Grammeln"}, "cijena": 20.0, "tip": 0},
    {"id": 13, "hr_ime": "Mast", "ime": {"HR 🇭🇷": "Mast", "EN 🇬🇧": "Lard", "DE 🇩🇪": "Schweineschmalz"}, "cijena": 3.0, "tip": 0},
]

# --- 6. NAVIGACIJA I STRANICE ---
izbor = st.sidebar.radio("NAVIGACIJA", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

if izbor == T["nav_shop"]:
    st.markdown('<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)
    
    col_t, col_k = st.columns([2, 1.2])
    with col_t:
        rows = st.columns(2)
        for idx, p in enumerate(proizvodi):
            p_vidljivo_ime = p["ime"][izabrani_jezik]
            p_hr_ime = p["hr_ime"]
            with rows[idx % 2]:
                st.markdown(f'<div class="product-card"><h3>{p_vidljivo_ime}</h3>', unsafe_allow_html=True)
                lbl = f"€/{T['unit_pc'] if p['tip']==1 else T['unit_kg']}"
                st.markdown(f'<p class="price-tag">{p["cijena"]:.2f} {lbl}</p>', unsafe_allow_html=True)
                
                key = f"p_{p['id']}"
                step = 1.0 if p["tip"] == 1 else 0.5
                curr = st.session_state.cart_dict.get(p_hr_ime, {"qty": 0.0})["qty"]
                
                val = st.number_input(f"Kol. {p_vidljivo_ime}", min_value=0.0, step=step, value=float(curr), key=key, label_visibility="collapsed")
                
                if p["tip"] == 0 and val == 0.5:
                    val = 1.0; st.session_state[key] = 1.0; st.rerun()
                
                st.session_state.cart_dict[p_hr_ime] = {"qty": val, "price": val * p["cijena"], "is_komad": p["tip"] == 1, "p_ime_kupac": p_vidljivo_ime}
                st.markdown('</div>', unsafe_allow_html=True)

    with col_k:
        st.subheader(T["cart_title"])
        aktivni = {k: v for k, v in st.session_state.cart_dict.items() if v['qty'] > 0}
        if not aktivni:
            st.write(T["cart_empty"])
        else:
            st.info(T["note_vaga"])
            ukupno = 0; detalji_hr = ""
            for hr_ime, pod in aktivni.items():
                jed_kupac = T["unit_pc"] if pod['is_komad'] else T["unit_kg"]
                jed_hr = "kom" if pod['is_komad'] else "kg"
                st.write(f"**{pod['p_ime_kupac']}** - {pod['qty']} {jed_kupac}")
                ukupno += pod['price']
                detalji_hr += f"- {hr_ime}: {pod['qty']} {jed_hr}\n"
            
            st.write("---")
            st.markdown(f"### {T['total']}: {ukupno:.2f} €")
            ime = st.text_input(T["form_name"]); tel = st.text_input(T["form_tel"])
            grad = st.text_input(T["form_city"]); ptt = st.text_input(T["form_zip"]); adr = st.text_input(T["form_addr"])
            
            if st.button(T["btn_order"]):
                if ime and tel and grad and adr:
                    if posalji_email_vlasniku(ime, tel, grad, ptt, adr, detalji_hr, f"{ukupno:.2f}", izabrani_jezik):
                        st.success(T["success"]); st.session_state.cart_dict = {}; st.balloons(); st.rerun()
                else: st.warning("!")

elif izbor == T["nav_horeca"]:
    st.title(T["nav_horeca"])
    st.write(T["horeca_text"])
    st.write("Kontakt: tomislavtomi90@gmail.com")

elif izbor == T["nav_haccp"]:
    st.title(T["nav_haccp"])
    st.success(f"✅ {T['haccp_text']}")

elif izbor == T["nav_info"]:
    st.title(T["nav_info"])
    st.write(T["info_text"])

st.sidebar.markdown("---")
st.sidebar.caption("© 2026. Kojundžić Mesnica i Prerada")
