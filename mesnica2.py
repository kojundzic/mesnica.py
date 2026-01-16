import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time

# --- 1. KONFIGURACIJA (ZAKLJUČANO) ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- 2. PRIJEVODI (ZAKLJUČANO) ---
LANG_MAP = {
    "HR 🇭🇷": {
        "nav_shop": "🛍️ TRGOVINA", "nav_horeca": "🏢 ZA UGOSTITELJE", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ O NAMA",
        "title_sub": "MESNICA I PRERADA MESA | 2026.", "cart_title": "🛒 Vaša Košarica",
        "cart_empty": "Vaša košarica je prazna.", 
        "note_vaga": "ℹ️ **Napomena:** Navedene cijene proizvoda su točne, dok je ukupni iznos u košarici informativan. Točan iznos bit će poznat nakon vaganja proizvoda. Konačan iznos znat ćete prilikom isporuke paketa, a mi ćemo se truditi da količine i informativni iznos budu što približniji stvarnom iznosu.",
        "total": "Približno", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "form_country": "Država*", "btn_order": "✅ POTVRDI NARUDŽBU", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom",
        "horeca_title": "Profesionalna usluga za restorane i hotele",
        "horeca_text": "Mesnica i prerada mesa Kojundžić nudi posebne pogodnosti:\n* **Uslužna proizvodnja:** Izrada po vašim recepturama.\n* **Veleprodajne cijene:** Za redovne isporuke.\n* **Dostava:** Vlastitim vozilima.",
        "horeca_mail": "Ostale informacije dostupne su putem e-mail adrese:",
        "haccp_title": "HACCP Standardi i Sigurnost",
        "haccp_text": "Naša proizvodnja u 2026. odvija se pod najstrožim sanitarnim uvjetima i HACCP sustavom sljedivosti.",
        "info_title": "Obiteljska tradicija i kvaliteta",
        "info_text": "Smješteni u srcu Siska, ponosni smo na dugogodišnje iskustvo. Naša se stoka kupuje isključivo na farmama malih proizvođača iz okolice Siska (Park prirode Lonjsko polje, Banovina, Posavina). Meso se priprema na tradicionalan način u modernom pogonu te se dimi isključivo izabranim drvetom kako bismo osigurali vrhunsku aromu i kvalitetu."
    },
    "EN 🇬🇧": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 FOR RESTAURANTS", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP & MEAT PROCESSING | 2026.", "cart_title": "🛒 Your Cart",
        "cart_empty": "Your cart is empty.", 
        "note_vaga": "Note: Final price will be known after weighing.",
        "total": "Approx.", "form_name": "Name*", "form_tel": "Phone*",
        "form_city": "City*", "form_zip": "ZIP*", "form_addr": "Address*",
        "form_country": "Country*", "btn_order": "✅ CONFIRM ORDER", "success": "Received!",
        "unit_kg": "kg", "unit_pc": "pcs",
        "horeca_title": "B2B Service", "horeca_text": "Special conditions for restaurants...",
        "horeca_mail": "Contact us via email:", "haccp_title": "HACCP Safety", "haccp_text": "Standards in 2026.",
        "info_title": "Tradition", "info_text": "Traditional meat processing in Sisak since 2026."
    }
}

st.set_page_config(page_title="Kojundžić | 2026", page_icon="🥩", layout="wide")

# --- 3. LOGIKA ZA EMAIL (ZAKLJUČANO) ---
def posalji_email(ime, telefon, grad, adr, detalji, ukupno, jezik, country, ptt):
    predmet = f"🥩 NOVA NARUDŽBA 2026: {ime}"
    tijelo = f"Kupac: {ime}\nTel: {telefon}\nDržava: {country}\nLokacija: {ptt} {grad}\nAdresa: {adr}\nJezik: {jezik}\n\nArtikli:\n{detalji}\n\nUkupno cca: {ukupno} €"
    msg = MIMEText(tijelo); msg['Subject'] = predmet; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

# --- 4. DIZAJN (ZAKLJUČANO) ---
st.markdown("""<style>
    .brand-name { color: #8B0000; font-size: 50px; font-weight: 900; text-align: center; margin:0; }
    .brand-sub { color: #333; font-size: 18px; text-align: center; margin-bottom: 25px; }
    .product-card { background: white; border-radius: 12px; padding: 15px; border: 1px solid #eee; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .qty-display { font-size: 20px; font-weight: bold; color: #8B0000; text-align: center; }
</style>""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 5. NAVIGACIJA (ZAKLJUČANO) ---
izabrani_jezik = st.sidebar.selectbox("Language / Jezik", list(LANG_MAP.keys()))
T = LANG_MAP[izabrani_jezik]
choice = st.sidebar.radio("Meni", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

# --- 6. TRGOVINA (DINAMIČKI DIO) ---
if choice == T["nav_shop"]:
    st.markdown(f'<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)

    col_proizvodi, col_desno = st.columns([2, 1])

    with col_proizvodi:
        proizvodi = [
            {"id": 1, "name": "Dimljeni hamburger", "price": 12.0, "type": "kg"},
            {"id": 2, "name": "Dimljeni buncek", "price": 8.0, "type": "pc"},
            {"id": 3, "name": "Dimljeni prsni vršci", "price": 9.0, "type": "pc"},
            {"id": 4, "name": "Slavonska kobasica", "price": 16.0, "type": "kg"},
            {"id": 5, "name": "Domaća salama", "price": 25.0, "type": "kg"},
            {"id": 6, "name": "Dimljene kosti", "price": 2.5, "type": "kg"},
            {"id": 7, "name": "Dimljene nogice/rep mix", "price": 2.5, "type": "kg"},
            {"id": 8, "name": "Panceta", "price": 17.0, "type": "kg"},
            {"id": 9, "name": "Dimljeni vrat (BK)", "price": 15.0, "type": "kg"},
            {"id": 10, "name": "Dimljeni kremenadl (BK)", "price": 15.0, "type": "kg"},
            {"id": 11, "name": "Dimljena pečenica", "price": 20.0, "type": "kg"},
            {"id": 12, "name": "Čvarci", "price": 10.0, "type": "pc"},
        ]

        sub_cols = st.columns(2)
        for idx, p in enumerate(proizvodi):
            with sub_cols[idx % 2]:
                st.markdown(f'<div class="product-card"><h4>{p["name"]}</h4><p>{p["price"]:.2f} €</p></div>', unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                
                # MINUS
                if c1.button("➖", key=f"m_{p['id']}"):
                    if p['id'] in st.session_state.cart:
                        step = 0.5 if p['type'] == 'kg' else 1
                        st.session_state.cart[p['id']] -= step
                        if st.session_state.cart[p['id']] <= 0: del st.session_state.cart[p['id']]
                        st.rerun()
                
                # PRIKAZ
                qty = st.session_state.cart.get(p['id'], 0.0)
                display_qty = int(qty) if qty == int(qty) else qty
                c2.markdown(f'<p class="qty-display">{display_qty}</p>', unsafe_allow_html=True)
                
                # PLUS (0 -> 1 -> +0.5 za kg)
                if c3.button("➕", key=f"p_{p['id']}"):
                    if p['id'] not in st.session_state.cart:
                        st.session_state.cart[p['id']] = 1.0
                    else:
                        step = 0.5 if p['type'] == 'kg' else 1
                        st.session_state.cart[p['id']] += step
                    st.rerun()

    with col_desno:
        st.subheader(T["cart_title"])
        total = 0.0
        txt_email = ""
        
        if not st.session_state.cart:
            st.info(T["cart_empty"])
        else:
            for pid, q in st.session_state.cart.items():
                p = next(x for x in proizvodi if x['id'] == pid)
                sub = q * p['price']
                total += sub
                st.write(f"✅ **{p['name']}**: {q} {T['unit_kg'] if p['type']=='kg' else T['unit_pc']} = {sub:.2f}€")
                txt_email += f"- {p['name']}: {q} {p['type']} ({sub:.2f}€)\n"
            st.markdown(f"### {T['total']}: {total:.2f} €")

        st.markdown("---")
        st.info(T["note_vaga"])
        
        with st.form("order_form"):
            st.markdown("##### Podaci za dostavu:")
            f_name = st.text_input(T["form_name"])
            f_tel = st.text_input(T["form_tel"])
            f_country = st.text_input(T["form_country"])
            f_city = st.text_input(T["form_city"])
            f_ptt = st.text_input(T["form_zip"])
            f_addr = st.text_input(T["form_addr"])
            
            if st.form_submit_button(T["btn_order"]):
                if not st.session_state.cart:
                    st.error("Košarica je prazna.")
                elif f_name and f_tel and f_city and f_addr:
                    if posalji_email(f_name, f_tel, f_city, f_addr, txt_email, total, izabrani_jezik, f_country, f_ptt):
                        st.success(T["success"])
                        st.session_state.cart = {}
                        time.sleep(2)
                        st.rerun()
                else:
                    st.error("❌ Ispunite sva polja sa *")

# --- 7. OSTALE RUBRIKE (ZAKLJUČANO) ---
elif choice == T["nav_horeca"]:
    st.title(T["horeca_title"]); st.write(T["horeca_text"])
    st.markdown("---"); st.info(f"📧 **{T['horeca_mail']}** {MOJ_EMAIL}")
elif choice == T["nav_haccp"]:
    st.title(T["haccp_title"]); st.success(T["haccp_text"])
elif choice == T["nav_info"]:
    st.title(T["info_title"]); st.write(T["info_text"])
    st.markdown("---"); st.markdown(f"📍 **Lokacija:** Sisak, Hrvatska\n\n📧 **Email:** {MOJ_EMAIL}")
