import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- 1. KONFIGURACIJA I KOMPLETNI PRIJEVODI ---
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
        "note_vaga": "ℹ️ <b>Note:</b> Prices are accurate, but the cart total is informative. The exact total will be known after weighing.",
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
        "haccp_text": "Unsere Produktion findet unter strengsten sanitären Bedingungen statt:\n1. **Rückverfolgbarkeit:** Klar ersichtliche Herkunft jedes Stücks.\n2. **Sicherheit:** Das HACCP-System überwacht jeden Schritt.\n3. **Hygiene:** Tradition kombiniert mit modernsten Standards.",
        "info_title": "Familientradition und Qualität",
        "info_text": "Im Herzen von Sisak gelegen, sind wir stolz auf unsere Erfahrung. Unser Vieh wird ausschließlich von kleinen Bauernhöfen rund um Sisak gekauft:\n* **Naturpark Lonjsko Polje**\n* **Region Banovina**\n* **Region Posavina**"
    }
}

st.set_page_config(page_title="Kojundžić | 2026", page_icon="🥩", layout="wide")

# --- 2. EMAIL FUNKCIJA (VLASNIKU NA HRVATSKOM) ---
def posalji_email_vlasniku(ime, telefon, grad, ptt, adr, detalji_hr, ukupno, jezik_korisnika):
    predmet = f"🥩 NOVA NARUDŽBA: {ime}"
    tijelo = f"Kupac: {ime}\nTel: {telefon}\nGrad: {grad}\nAdresa: {adr}\n\nJezik kupca: {jezik_korisnika}\n\nArtikli:\n{detalji_hr}\n\nUkupno: {ukupno} €"
    msg = MIMEText(tijelo); msg['Subject'] = predmet; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

# --- 3. JEZIK I DIZAJN ---
izabrani_jezik = st.sidebar.selectbox("Jezik / Language", list(LANG_MAP.keys()))
T = LANG_MAP[izabrani_jezik]

st.markdown(f"""<style>
    .brand-name {{ color: #8B0000; font-size: 55px; font-weight: 900; text-align: center; text-transform: uppercase; margin:0; }}
    .brand-sub {{ color: #333; font-size: 18px; text-align: center; font-weight: 600; margin-bottom: 25px; }}
    .product-card {{ background: white; border-radius: 10px; padding: 15px; border: 1px solid #eee; text-align: center; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
    .stButton>button {{ background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%); color: white !important; font-weight: bold; border-radius: 50px; }}
</style>""", unsafe_allow_html=True)

# --- 4. PROIZVODI ---
proizvodi = [
    {"id": 1, "hr_name": "Dimljeni hamburger", "name": {"HR 🇭🇷": "Dimljeni hamburger", "EN 🇬🇧": "Smoked Bacon", "DE 🇩🇪": "Geräucherter Speck"}, "price": 12.0, "type": "kg"},
    {"id": 2, "hr_name": "Dimljeni buncek", "name": {"HR 🇭🇷": "Dimljeni buncek", "EN 🇬🇧": "Smoked Pork Hock", "DE 🇩🇪": "Geräucherte Stelze"}, "price": 8.0, "type": "kom"},
    {"id": 4, "hr_name": "Slavonska kobasica", "name": {"HR 🇭🇷": "Slavonska kobasica", "EN 🇬🇧": "Slavonian Sausage", "DE 🇩🇪": "Slawonische Wurst"}, "price": 16.0, "type": "kg"},
    {"id": 12, "hr_name": "Čvarci", "name": {"HR 🇭🇷": "Čvarci", "EN 🇬🇧": "Pork Cracklings", "DE 🇩🇪": "Grammeln"}, "price": 20.0, "type": "kg"}
]

# --- 5. NAVIGACIJA ---
izbor = st.sidebar.radio("IZBORNIK", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

if izbor == T["nav_shop"]:
    st.markdown('<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)
    col_p, col_c = st.columns([2, 1.2])
    narudzba = {}
    with col_p:
        p_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            vidi_ime = p["name"][izabrani_jezik]
            with p_cols[i % 2]:
                st.markdown(f'<div class="product-card"><b>{vidi_ime}</b><br>{p["price"]:.2f} € / {T["unit_pc"] if p["type"]=="kom" else T["unit_kg"]}</div>', unsafe_allow_html=True)
                step = 1.0 if p["type"] == "kom" else 0.5
                qty = st.number_input(f"Q_{p['id']}", min_value=0.0, step=step, key=f"q_{p['id']}", label_visibility="collapsed")
                if p["type"] == "kg" and qty == 0.5: qty = 1.0
                if qty > 0: narudzba[p["hr_name"]] = {"qty": qty, "price": qty * p["price"], "vidi": vidi_ime, "unit": T["unit_pc"] if p["type"]=="kom" else T["unit_kg"]}

    with col_c:
        st.subheader(T["cart_title"])
        if not narudzba: st.info(T["cart_empty"])
        else:
            st.markdown(f'<div style="background:#f9f9f9; padding:10px; border-radius:8px; font-size:13px; border:1px solid #ddd; margin-bottom:15px;">{T["note_vaga"]}</div>', unsafe_allow_html=True)
            total = 0; detalji_hr = ""
            for hr_ime, pod in narudzba.items():
                st.write(f"**{pod['vidi']}**: {pod['qty']} {pod['unit']} ({pod['price']:.2f} €)")
                total += pod['price']; detalji_hr += f"- {hr_ime}: {pod['qty']} {p['type']}\n"
            st.write("---"); st.markdown(f"### {T['total']}: {total:.2f} €")
            ime = st.text_input(T["form_name"]); tel = st.text_input(T["form_tel"]); grad = st.text_input(T["form_city"]); adr = st.text_input(T["form_addr"])
            if st.button(T["btn_order"]):
                if ime and tel and grad and adr:
                    if posalji_email_vlasniku(ime, tel, grad, "", adr, detalji_hr, f"{total:.2f}", izabrani_jezik):
                        st.success(T["success"]); st.balloons()
                else: st.warning("!")

elif izbor == T["nav_horeca"]:
    st.image("https://cdn.pixabay.com", use_container_width=True)
    st.title(T["nav_horeca"])
    st.subheader(T["horeca_title"])
    st.markdown(T["horeca_text"])
    st.info(f"Email: tomislavtomi90@gmail.com")

elif izbor == T["nav_haccp"]:
    st.image("https://cdn.pixabay.com", use_container_width=True)
    st.title(T["nav_haccp"])
    st.success(f"### ✅ {T['haccp_text'] if izabrani_jezik == 'HR 🇭🇷' else 'APPROVED ESTABLISHMENT NO. 2686'}")
    st.markdown(T["haccp_text"])

elif izbor == T["nav_info"]:
    st.image("https://cdn.pixabay.com", use_container_width=True)
    st.title(T["nav_info"])
    st.subheader(T["info_title"])
    st.markdown(T["info_text"])
    st.markdown(f"--- \n📍 **Sisak, Trg Josipa Mađerića 1** \n📧 tomislavtomi90@gmail.com")

st.sidebar.caption("© 2026 Kojundžić Mesnica")
