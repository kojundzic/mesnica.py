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
        "title_sub": "MESNICA I PRERADA MESA | 2026.", "cart_title": "🛒 Vaša Košarica",
        "cart_empty": "Prazna. Dodajte artikle.", 
        "note_vaga": "ℹ️ <b>Napomena:</b> Navedene cijene su točne, dok je iznos u košarici informativan. Točan iznos znat će se nakon vaganja.",
        "total": "Približno", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "✅ POTVRDI NARUDŽBU", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom",
        "horeca_title": "Profesionalna usluga za restorane i hotele",
        "horeca_text": "Mesnica i prerada mesa Kojundžić nudi posebne pogodnosti za ugostiteljske objekte:\n* **Uslužna proizvodnja:** Izrada suhomesnatih proizvoda prema vašim recepturama.\n* **Veleprodajne cijene:** Konkurentne cijene prilagođene redovnim isporukama.\n* **Kvaliteta:** Strogo kontrolirano domaće porijeklo.\n* **Dostava:** Na veće količine dostava vlastitim vozilima.",
        "haccp_title": "HACCP Standardi i Sigurnost",
        "haccp_text": "Naša proizvodnja odvija se pod najstrožim sanitarnim uvjetima:\n1. **Sljedivost:** Jasno vidljivo porijeklo svakog komada.\n2. **Sigurnost:** HACCP sustav prati svaki korak.\n3. **Higijena:** Spoj tradicije i najsuvremenijih standarda.",
        "info_title": "Obiteljska tradicija i kvaliteta",
        "info_text": "Smješteni u srcu Siska, ponosni smo na dugogodišnje iskustvo. Naša se stoka kupuje isključivo na farmama malih proizvođača iz okolice Siska:\n* **Park prirode Lonjsko polje**\n* **Banovina**\n* **Posavina**"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 FOR RESTAURANTS", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP & MEAT PROCESSING | 2026.", "cart_title": "🛒 Your Cart",
        "cart_empty": "Empty. Add items.", 
        "note_vaga": "ℹ️ <b>Note:</b> Prices listed are accurate, but the cart total is informative. The exact total will be determined after weighing.",
        "total": "Approx. total", "form_name": "Full Name*", "form_tel": "Phone*",
        "form_city": "City*", "form_zip": "ZIP*", "form_addr": "Address*",
        "btn_order": "✅ CONFIRM ORDER", "success": "Received! Thank you.",
        "unit_kg": "kg", "unit_pc": "pcs",
        "horeca_title": "Professional service for restaurants and hotels",
        "horeca_text": "Kojundžić Butcher Shop offers special benefits for catering facilities:\n* **Custom production:** Meat products according to your recipes.\n* **Wholesale prices:** Competitive prices for regular deliveries.\n* **Quality:** Strictly controlled local origin.\n* **Delivery:** For larger quantities, delivery with our own vehicles.",
        "haccp_title": "HACCP Standards and Safety",
        "haccp_text": "Our production takes place under the strictest sanitary conditions:\n1. **Traceability:** Clearly visible origin of every piece.\n2. **Safety:** The HACCP system monitors every step.\n3. **Hygiene:** Tradition combined with modern standards.",
        "info_title": "Family tradition and quality",
        "info_text": "Located in the heart of Sisak, we are proud of our experience. Our livestock is purchased exclusively from small farms around Sisak:\n* **Lonjsko Polje Nature Park**\n* **Banovina region**\n* **Posavina region**"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 FÜR GASTRONOMIE", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI & FLEISCHVERARBEITUNG | 2026.", "cart_title": "🛒 Warenkorb",
        "cart_empty": "Leer. Artikel hinzufügen.", 
        "note_vaga": "ℹ️ <b>Info:</b> Die Preise sind korrekt, der Gesamtbetrag im Warenkorb ist jedoch nur ein Richtwert.",
        "total": "Gesamt ca.", "form_name": "Vor- und Nachname*", "form_tel": "Telefon*",
        "form_city": "Stadt*", "form_zip": "PLZ*", "form_addr": "Adresse*",
        "btn_order": "✅ BESTELLUNG BESTÄTIGEN", "success": "Eingegangen! Danke.",
        "unit_kg": "kg", "unit_pc": "stk",
        "horeca_title": "Professioneller Service für Gastronomie",
        "horeca_text": "Metzgerei Kojundžić bietet besondere Vorteile für Gastronomiebetriebe:\n* **Lohnfertigung:** Fleischprodukte nach Ihren Rezepten.\n* **Großhandelspreise:** Wettbewerbsfähige Preise für Lieferungen.\n* **Qualität:** Streng kontrollierte lokale Herkunft.\n* **Lieferung:** Bei größeren Mengen Lieferung mit eigenen Fahrzeugen.",
        "haccp_title": "HACCP-Standards und Sicherheit",
        "haccp_text": "Unsere Produktion findet unter strengsten sanitären Bedingungen statt:\n1. **Rückverfolgbarkeit:** Klar ersichtliche Herkunft jedes Stücks.\n2. **Sicherheit:** Das HACCP-System monitors every step.\n3. **Hygiene:** Tradition combined with modern standards.",
        "info_title": "Familientradition und kvalitet",
        "info_text": "Im Herzen von Sisak gelegen, sind wir stolz auf unsere Erfahrung. Unser Vieh wird ausschließlich von kleinen Bauernhöfen rund um Sisak gekauft:\n* **Naturpark Lonjsko Polje**\n* **Region Banovina**\n* **Region Posavina**"
    }
}

def posalji_email_vlasniku(ime, telefon, grad, adr, detalji_hr, ukupno, jezik_korisnika):
    predmet = f"🥩 NOVA NARUDŽBA: {ime}"
    tijelo = f"Kupac: {ime}\nTel: {telefon}\nGrad: {grad}\nAdresa: {adr}\n\nJezik kupca: {jezik_korisnika}\n\nArtikli:\n{detalji_hr}\n\nUkupno: {ukupno} €"
    msg = MIMEText(tijelo); msg['Subject'] = predmet; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

st.set_page_config(page_title="Kojundžić | 2026", page_icon="🥩", layout="wide")
izabrani_jezik = st.sidebar.selectbox("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[izabrani_jezik]
menu = [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]]
choice = st.sidebar.radio("Navigacija", menu, label_visibility="collapsed")

st.markdown(f"""<style>
    .brand-name {{ color: #8B0000; font-size: 55px; font-weight: 900; text-align: center; text-transform: uppercase; margin:0; }}
    .brand-sub {{ color: #333; font-size: 18px; text-align: center; font-weight: 600; margin-bottom: 25px; }}
    .product-card {{ background: white; border-radius: 12px; padding: 15px; border: 1px solid #eee; text-align: center; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); transition: 0.3s; }}
    .product-img {{ border-radius: 8px; width: 100%; height: 180px; object-fit: cover; margin-bottom: 10px; }}
    .stButton>button {{ background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%); color: white !important; font-weight: bold; border-radius: 50px; width: 100%; }}
</style>""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

# ==============================================================================
# SECTION 3: OTVORENO (Trgovina - Specijalna logika dodavanja)
# ==============================================================================
if choice == T["nav_shop"]:
    st.markdown(f'<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)

    proizvodi = [
        {"id": 1, "hr_name": "Dimljeni hamburger", "name": {"HR 🇭🇷": "Dimljeni hamburger", "EN 🇬🇧": "Smoked Bacon", "DE 🇩🇪": "Geräucherter Speck"}, "price": 12.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 2, "hr_name": "Dimljeni buncek", "name": {"HR 🇭🇷": "Dimljeni buncek", "EN 🇬🇧": "Smoked Pork Hock", "DE 🇩🇪": "Geräucherte Stelze"}, "price": 8.0, "type": "pc", "img": "https://images.unsplash.com"},
        {"id": 3, "hr_name": "Dimljeni prsni vršci", "name": {"HR 🇭🇷": "Dimljeni prsni vršci", "EN 🇬🇧": "Smoked Rib Tips", "DE 🇩🇪": "Geräucherte Rippenspitzen"}, "price": 7.5, "type": "pc", "img": "https://images.unsplash.com"},
        {"id": 4, "hr_name": "Slavonska kobasica", "name": {"HR 🇭🇷": "Slavonska kobasica", "EN 🇬🇧": "Slavonian Sausage", "DE 🇩🇪": "Slawonische Wurst"}, "price": 16.0, "type": "kg", "img": "https://images.unsplash.com"},
        {"id": 12, "hr_name": "Čvarci", "name": {"HR 🇭🇷": "Čvarci", "EN 🇬🇧": "Pork Cracklings", "DE 🇩🇪": "Grammeln"}, "price": 20.0, "type": "kg", "img": "https://images.unsplash.com"}
    ]

    col_main, col_cart = st.columns([2, 1])

    with col_main:
        inner_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with inner_cols[i % 2]:
                st.markdown(f"""<div class="product-card"><img src="{p['img']}" class="product-img"><h3>{p['name'][izabrani_jezik]}</h3>
                <p style="font-size: 20px; color: #8B0000; font-weight: bold;">{p['price']:.2f} € / {T['unit_'+p['type']]}</p></div>""", unsafe_allow_html=True)
                
                # LOGIKA: Komad +1 | KG: Prvi klik 1, ostali +0.5
                if st.button(f"➕ {p['name'][izabrani_jezik]}", key=f"add_{p['id']}"):
                    trenutna = st.session_state.cart.get(p['id'], 0.0)
                    if p['type'] == "pc":
                        st.session_state.cart[p['id']] = trenutna + 1
                    else:
                        st.session_state.cart[p['id']] = 1.0 if trenutna == 0 else trenutna + 0.5
                    st.rerun()

    with col_cart:
        st.markdown(f"### {T['cart_title']}")
        suma = 0.0
        lista_za_email = ""
        if not st.session_state.cart:
            st.info(T["cart_empty"])
        else:
            for pid, qty in list(st.session_state.cart.items()):
                p = next(x for x in proizvodi if x["id"] == pid)
                subtotal = p["price"] * qty
                suma += subtotal
                lista_za_email += f"- {p['hr_name']}: {qty} {p['type']}\n"
                
                c1, c2 = st.columns([4, 1])
                c1.write(f"**{p['name'][izabrani_jezik]}**\n{qty} {T['unit_'+p['type']]} = {subtotal:.2f} €")
                if c2.button("❌", key=f"rem_{pid}"):
                    del st.session_state.cart[pid]
                    st.rerun()
            
            st.write("---")
            st.markdown(T["note_vaga"], unsafe_allow_html=True)
            st.subheader(f"{T['total']}: {suma:.2f} €")
            
            with st.expander(T["btn_order"]):
                with st.form("narudzba"):
                    f_ime = st.text_input(T["form_name"])
                    f_tel = st.text_input(T["form_tel"])
                    f_grad = st.text_input(T["form_city"])
                    f_adr = st.text_input(T["form_addr"])
                    if st.form_submit_button(T["btn_order"]):
                        if f_ime and f_tel and f_grad and f_adr:
                            if posalji_email_vlasniku(f_ime, f_tel, f_grad, f_adr, lista_za_email, suma, izabrani_jezik):
                                st.success(T["success"]); st.session_state.cart = {}; st.balloons()
                            else: st.error("Greška kod slanja.")
                        else: st.warning("Popunite sva polja.")

# ==============================================================================
# SECTION 4: ZAKLJUČANO (Horeca, Haccp, Info)
# ==============================================================================
elif choice == T["nav_horeca"]:
    st.header(T["horeca_title"]); st.markdown(T["horeca_text"])
elif choice == T["nav_haccp"]:
    st.header(T["haccp_title"]); st.markdown(T["haccp_text"])
elif choice == T["nav_info"]:
    st.header(T["info_title"]); st.markdown(T["info_text"]); st.map(data={'lat': [45.485], 'lon': [16.373]})
