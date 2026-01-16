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
        "cart_empty": "Prazna. Dodajte artikle pomoću +", 
        "note_vaga": "ℹ️ <b>Napomena:</b> Navedene cijene ispod artikala su točne, dok je iznos u košarici informativan i približan. Točan iznos znat će se nakon vaganja pri primitku paketa.",
        "total": "Približno", "form_name": "Ime i Prezime*", "form_tel": "Broj telefona*",
        "form_city": "Grad*", "form_zip": "Poštanski broj*", "form_addr": "Ulica i kućni broj*",
        "btn_order": "✅ POTVRDI NARUDŽBU", "btn_clear": "🗑️ Isprazni", "success": "Zaprimljeno! Hvala vam.",
        "unit_kg": "kg", "unit_pc": "kom"
    },
    "EN 🇬🇧": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 FOR RESTAURANTS", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ ABOUT US",
        "title_sub": "BUTCHER SHOP & MEAT PROCESSING | 2026.", "cart_title": "🛒 Your Cart",
        "cart_empty": "Empty. Add items using +", 
        "note_vaga": "ℹ️ <b>Note:</b> Prices listed are accurate, but the cart total is informative and approximate. The exact total will be determined after weighing upon receipt.",
        "total": "Approximate total", "form_name": "Full Name*", "form_tel": "Phone Number*",
        "form_city": "City*", "form_zip": "ZIP Code*", "form_addr": "Street & House Number*",
        "btn_order": "✅ CONFIRM ORDER", "btn_clear": "🗑️ Clear", "success": "Received! Thank you.",
        "unit_kg": "kg", "unit_pc": "pcs"
    },
    "DE 🇩🇪": {
        "nav_shop": "🛍️ SHOP", "nav_horeca": "🏢 FÜR GASTRONOMIE", "nav_haccp": "🧼 HACCP", "nav_info": "ℹ️ ÜBER UNS",
        "title_sub": "METZGEREI & FLEISCHVERARBEITUNG | 2026.", "cart_title": "🛒 Warenkorb",
        "cart_empty": "Leer. Artikel mit + hinzufügen", 
        "note_vaga": "ℹ️ <b>Hinweis:</b> Die Preise sind korrekt, ali der Gesamtbetrag im Warenkorb ist informativ. Der genaue Betrag wird nach dem Wiegen bei Erhalt ermittelt.",
        "total": "Ungefährer Gesamtbetrag", "form_name": "Vor- und Nachname*", "form_tel": "Telefonnummer*",
        "form_city": "Stadt*", "form_zip": "Postleitzahl*", "form_addr": "Straße & Hausnummer*",
        "btn_order": "✅ BESTELLUNG BESTÄTIGEN", "btn_clear": "🗑️ Leeren", "success": "Eingegangen! Vielen Dank.",
        "unit_kg": "kg", "unit_pc": "stk"
    }
}

st.set_page_config(page_title="Kojundžić | Mesnica i Prerada", page_icon="🥩", layout="wide")

# --- 2. LOGIKA ZA EMAIL ---
def posalji_email_vlasniku(ime, telefon, grad, ptt, adr, detalji_hr, ukupno, jezik_korisnika):
    predmet = f"🥩 NOVA NARUDŽBA: {ime}"
    tijelo = f"""
    Stigla je nova narudžba putem weba!
    -----------------------------------
    PODACI O KUPCU ZA DOSTAVU:
    Ime i Prezime: {ime}
    Broj telefona: {telefon}
    Grad: {grad}
    Poštanski broj (PTT): {ptt}
    Adresa: {adr}
    
    JEZIK KUPCA: {jezik_korisnika}
    DATUM: {datetime.now().strftime('%d.%m.%2026. %H:%M')}
    
    NARUČENI ARTIKLI (Hrvatski):
    -----------------------------------
    {detalji_hr}
    
    UKUPNO (približno): {ukupno} €
    -----------------------------------
    """
    msg = MIMEText(tijelo); msg['Subject'] = predmet; msg['From'] = MOJ_EMAIL; msg['To'] = MOJ_EMAIL
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(); server.login(MOJ_EMAIL, MOJA_LOZINKA)
        server.sendmail(MOJ_EMAIL, MOJ_EMAIL, msg.as_string()); server.quit()
        return True
    except: return False

# --- 3. DIZAJN ---
izabrani_jezik = st.sidebar.selectbox("Language / Jezik", list(LANG_MAP.keys()))
T = LANG_MAP[izabrani_jezik]

st.markdown("""
<style>
    .brand-name { color: #8B0000; font-size: 60px; font-weight: 900; text-align: center; text-transform: uppercase; margin-bottom:0px; letter-spacing: 3px; }
    .brand-sub { color: #333; font-size: 20px; text-align: center; font-weight: 600; margin-top:0px; margin-bottom: 30px; }
    .product-card { background-color: white; border-radius: 10px; padding: 15px; border: 1px solid #eee; text-align: center; margin-bottom:15px; box-shadow: 2px 2px 8px rgba(0,0,0,0.05); }
    .vaga-napomena { color: #444; font-size: 13px; text-align: center; margin-bottom: 15px; border: 1px solid #ddd; padding: 10px; border-radius: 8px; background-color: #f9f9f9; line-height: 1.4; }
    .stButton>button { background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%); color: white !important; font-weight: bold; border-radius: 50px; }
    .section-img { border-radius: 15px; margin-bottom: 20px; width: 100%; object-fit: cover; height: 350px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

if 'cart' not in st.session_state: st.session_state.cart = {}

# --- 4. PROIZVODI ---
proizvodi = [
    {"id": 1, "hr_name": "Dimljeni hamburger", "name": {"HR 🇭🇷": "Dimljeni hamburger", "EN 🇬🇧": "Smoked Bacon", "DE 🇩🇪": "Geräucherter Speck"}, "price": 12.0, "type": "kg"},
    {"id": 2, "hr_name": "Dimljeni buncek", "name": {"HR 🇭🇷": "Dimljeni buncek", "EN 🇬🇧": "Smoked Pork Hock", "DE 🇩🇪": "Geräucherte Stelze"}, "price": 8.0, "type": "kom"},
    {"id": 3, "hr_name": "Dimljeni prsni vršci", "name": {"HR 🇭🇷": "Dimljeni prsni vršci", "EN 🇬🇧": "Smoked Rib Tips", "DE 🇩🇪": "Geräucherte Rippenspitzen"}, "price": 9.0, "type": "kom"},
    {"id": 4, "hr_name": "Slavonska kobasica", "name": {"HR 🇭🇷": "Slavonska kobasica", "EN 🇬🇧": "Slavonian Sausage", "DE 🇩🇪": "Slawonische Wurst"}, "price": 16.0, "type": "kg"},
    {"id": 5, "hr_name": "Domaća salama", "name": {"HR 🇭🇷": "Domaća salama", "EN 🇬🇧": "Homemade Salami", "DE 🇩🇪": "Hausgemachte Salami"}, "price": 25.0, "type": "kg"},
    {"id": 8, "hr_name": "Panceta", "name": {"HR 🇭🇷": "Panceta", "EN 🇬🇧": "Pancetta", "DE 🇩🇪": "Pancetta Speck"}, "price": 17.0, "type": "kg"},
    {"id": 12, "hr_name": "Čvarci", "name": {"HR 🇭🇷": "Čvarci", "EN 🇬🇧": "Pork Cracklings", "DE 🇩🇪": "Grammeln"}, "price": 20.0, "type": "kg"},
    {"id": 13, "hr_name": "Mast", "name": {"HR 🇭🇷": "Mast", "EN 🇬🇧": "Lard", "DE 🇩🇪": "Schweineschmalz"}, "price": 3.0, "type": "kg"}
]

# --- 5. NAVIGACIJA ---
izbor = st.sidebar.radio("IZBORNIK", [T["nav_shop"], T["nav_horeca"], T["nav_haccp"], T["nav_info"]])

if izbor == T["nav_shop"]:
    st.markdown('<p class="brand-name">KOJUNDŽIĆ</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="brand-sub">{T["title_sub"]}</p>', unsafe_allow_html=True)
    col_p, col_c = st.columns([2, 1.2])
    with col_p:
        p_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with p_cols[i % 2]:
                st.markdown(f'<div class="product-card"><b>{p["name"][izabrani_jezik]}</b><br>{p["price"]:.2f} € / {p["type"]}</div>', unsafe_allow_html=True)
                step = 1.0 if p["type"] == "kom" else 0.5
                q_key = f"qty_{p['id']}"
                curr = st.session_state.cart.get(p["hr_name"], {"qty": 0.0})["qty"]
                qty = st.number_input(f"K {p['id']}", min_value=0.0, step=step, value=float(curr), key=q_key, label_visibility="collapsed")
                if p["type"] == "kg" and qty == 0.5: qty = 1.0; st.session_state[q_key] = 1.0; st.rerun()
                st.session_state.cart[p["hr_name"]] = {"qty": qty, "price": qty * p["price"], "vidi": p["name"][izabrani_jezik], "type": p["type"]}

    with col_c:
        st.subheader(T["cart_title"])
        aktivni = {k: v for k, v in st.session_state.cart.items() if v['qty'] > 0}
        if not aktivni: st.info(T["cart_empty"])
        else:
            st.markdown(f'<div class="vaga-napomena">{T["note_vaga"]}</div>', unsafe_allow_html=True)
            total = 0; detalji_hr = ""
            for hr_ime, pod in aktivni.items():
                st.write(f"**{pod['vidi']}**: {pod['qty']} {pod['type']} ({pod['price']:.2f} €)")
                total += pod['price']; detalji_hr += f"- {hr_ime}: {pod['qty']} {pod['type']}\n"
            st.write("---"); st.markdown(f"### {T['total']}: {total:.2f} €")
            ime = st.text_input(T["form_name"]); tel = st.text_input(T["form_tel"]); grad = st.text_input(T["form_city"]); ptt = st.text_input(T["form_zip"]); adr = st.text_input(T["form_addr"])
            if st.button(T["btn_order"]):
                if ime and tel and grad and adr:
                    if posalji_email_vlasniku(ime, tel, grad, ptt, adr, detalji_hr, f"{total:.2f}", izabrani_jezik):
                        st.success(T["success"]); st.session_state.cart = {}; st.balloons(); st.rerun()
                else: st.warning("Popunite polja!")

elif izbor == T["nav_horeca"]:
    st.image("https://images.unsplash.com", caption=T["nav_horeca"], use_container_width=True)
    st.title(T["nav_horeca"])
    st.subheader("Profesionalna usluga za restorane i hotele")
    st.markdown("""
    Mesnica i prerada mesa Kojundžić nudi posebne pogodnosti za ugostiteljske objekte:
    * **Uslužna proizvodnja:** Izrada suhomesnatih proizvoda prema vašim specifičnim recepturama.
    * **Veleprodajne cijene:** Konkurentne cijene prilagođene redovnim isporukama.
    * **Kvaliteta i kontinuitet:** Strogo kontrolirano domaće porijeklo i stabilna kvaliteta kroz cijelu godinu.
    * **Dostava:** Na veće količine mogućnost dostave vlastitim vozilima.
    
    Za sve upite i dogovore oko suradnje kontaktirajte nas direktno na: **tomislavtomi90@gmail.com**
    """)

elif izbor == T["nav_haccp"]:
    st.image("https://images.unsplash.com", caption=T["nav_haccp"], use_container_width=True)
    st.title(T["nav_haccp"])
    st.success("### ✅ ODOBRENI OBJEKT BR. 2686")
    st.markdown("""
    Naša proizvodnja se odvija pod najstrožim sanitarnim uvjetima u skladu s europskim normama:
    1. **Sljedivost:** Svaki komad mesa ima jasno vidljivo porijeklo i kontroliran put do vašeg stola.
    2. **Sigurnost:** Sustav HACCP osigurava da se svaki korak proizvodnje prati i dokumentira.
    3. **Tradicija i Higijena:** Spajamo starinske načine dimljenja s najsuvremenijim higijenskim standardima.
    """)

elif izbor == T["nav_info"]:
    st.image("https://images.unsplash.com", caption=T["nav_info"], use_container_width=True)
    st.title(T["nav_info"])
    st.write("### Obiteljska tradicija i kvaliteta")
    st.markdown("""
    Smješteni u srcu Siska, ponosni smo na dugogodišnje iskustvo u obradi i preradi mesa. 
    Sve naše proizvode radimo s posebnom pažnjom, koristeći tradicionalne metode soljenja i dimljenja na drvima bukve i graba.
    
    **Porijeklo sirovine:**
    Posebno smo ponosni na suradnju s lokalnim proizvođačima. Naša se stoka kupuje isključivo na farmama i poljoprivrednim 
    gospodarstvima malih proizvođača iz neposredne okolice Siska, obuhvaćajući područja:
    * **Park prirode Lonjsko polje**
    * **Banovina**
    * **Posavina**
    
    Time osiguravamo vrhunsku svježinu, podržavamo lokalno gospodarstvo i garantiramo ispašu na ekološki čistim pašnjacima.
    
    ---
    📍 **Lokacija:** Trg Josipa Mađerića 1, 44000 Sisak  
    📧 **Kontakt:** tomislavtomi90@gmail.com  
    ⏰ **Godina:** U 2026. nastavljamo tradiciju vrhunskog okusa.
    """)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Kojundžić Mesnica i Prerada")
