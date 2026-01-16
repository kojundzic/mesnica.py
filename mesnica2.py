import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- 1. POSTAVKE ZA OBAVIJESTI ---
MOJ_EMAIL = "tomislavtomi90@gmail.com"
MOJA_LOZINKA = "czdx ndpg owzy wgqu" 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Postavke aplikacije za 2026. godinu
st.set_page_config(page_title="Kojundžić | Mesnica i Prerada mesa", page_icon="🥩", layout="wide")

# --- 2. LOGIKA ZA TIHO SLANJE NARUDŽBE VLASNIKU ---
def posalji_email_vlasniku(ime, telefon, drzava, grad, ptt, adr, detalji_narudzbe, ukupno):
    predmet = f"🥩 NOVA NARUDŽBA: {ime}"
    tijelo = f"""
    Stigla je nova narudžba putem weba!
    
    PODACI O KUPCU ZA DOSTAVU:
    -----------------------------------
    Ime i Prezime: {ime}
    Broj telefona: {telefon}
    Država: {drzava}
    Grad: {grad}
    Poštanski broj (PTT): {ptt}
    Adresa: {adr}
    
    DATUM NARUDŽBE: {datetime.now().strftime('%d.%m.%2026. %H:%M')}
    
    NARUČENI ARTIKLI:
    -----------------------------------
    {detalji_narudzbe}
    
    PRIBLIŽNI UKUPNI IZNOS: {ukupno} €
    
    (Napomena: Kupac je obaviješten da se točna cijena utvrđuje nakon vaganja.)
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
    except:
        return False

# --- 3. DIZAJN I STILIZACIJA ---
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .brand-name { color: #8B0000; font-size: 55px; font-weight: 900; text-align: center; text-transform: uppercase; margin-bottom:0px; }
    .brand-sub { color: #333; font-size: 22px; text-align: center; font-weight: 600; margin-top:0px; margin-bottom: 25px; }
    .product-card { background-color: white; border-radius: 12px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #eee; text-align: center; margin-bottom:10px; }
    .price-tag { color: #8B0000; font-size: 20px; font-weight: bold; margin-bottom: 10px; }
    .sidebar-cart { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #ddd; }
    .stButton>button { background: linear-gradient(135deg, #8B0000 0%, #4a0000 100%); color: white !important; font-weight: bold; border-radius: 50px; width: 100%; }
    .vaga-napomena { color: #444; font-weight: 500; font-size: 14px; text-align: center; margin-bottom: 15px; border: 1px solid #ddd; padding: 12px; border-radius: 8px; background-color: #fcfcfc; line-height: 1.5; }
    .u-box { background-color: #f8f9fa; padding: 30px; border-radius: 15px; border-left: 5px solid #8B0000; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

if 'cart_dict' not in st.session_state: st.session_state.cart_dict = {}

# --- 4. PODACI O PROIZVODIMA ---
proizvodi = [
    {"id": 1, "ime": "Dimljeni hamburger", "cijena": 12.0, "tip": 0},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.0, "tip": 1},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.0, "tip": 1},
    {"id": 4, "ime": "Slavonska kobasica", "cijena": 16.0, "tip": 0},
    {"id": 5, "ime": "Domaća salama", "cijena": 25.0, "tip": 0},
    {"id": 6, "ime": "Dimljene kosti", "cijena": 2.5, "tip": 0},
    {"id": 7, "ime": "Dimljene nogice, uši, rep - mix", "cijena": 2.5, "tip": 0},
    {"id": 8, "ime": "Panceta", "cijena": 17.0, "tip": 0},
    {"id": 9, "ime": "Dimljeni vrat bez kosti", "cijena": 15.0, "tip": 0},
    {"id": 10, "ime": "Dimljeni kremenadl bez kosti", "cijena": 15.0, "tip": 0},
    {"id": 11, "ime": "Buđola", "cijena": 20.0, "tip": 0},
    {"id": 12, "ime": "Čvarci", "cijena": 20.0, "tip": 0},
    {"id": 13, "ime": "Mast", "cijena": 3.0, "tip": 0},
]

# --- 5. LOGIKA KOŠARICE ---
def prikazi_kosaricu(col):
    with col:
        st.markdown('<div class="sidebar-cart">', unsafe_allow_html=True)
        st.subheader("🛒 Vaša Košarica")
        
        aktivni_artikli = {k: v for k, v in st.session_state.cart_dict.items() if v['qty'] > 0}
        
        if not aktivni_artikli:
            st.write("Vaša košarica je trenutno prazna. Počnite dodavati artikle pomoću znaka +.")
        else:
            st.markdown("""
            <div class="vaga-napomena">
                ℹ️ <b>Napomena:</b> Navedene cijene ispod artikala su točne, dok je iznos u košarici informativan i približan. 
                Točan iznos znat će se nakon vaganja, odnosno pri primitku paketa. 
                Prodavatelj će se truditi maksimalno pridržavati naručenih količina kako bi iznos informativne i prave cijene bio što točniji.
            </div>
            """, unsafe_allow_html=True)
            
            ukupno = sum(v['price'] for v in aktivni_artikli.values())
            detalji_za_email = ""
            for ime, podaci in aktivni_artikli.items():
                jedinica = "kom" if podaci['is_komad'] else "kg"
                st.write(f"**{ime}** - {podaci['qty']} {jedinica}")
                detalji_za_email += f"- {ime}: {podaci['qty']} {jedinica}\n"
            
            st.write("---")
            st.markdown(f"### Približno: {ukupno:.2f} €")
            
            st.markdown("#### Podaci za dostavu:")
            ime = st.text_input("Ime i Prezime*")
            telefon = st.text_input("Broj telefona (za kurirsku službu)*")
            col_geo1, col_geo2 = st.columns(2)
            grad = col_geo1.text_input("Grad*")
            ptt = col_geo2.text_input("Poštanski broj*")
            drzava = st.text_input("Država*", value="Hrvatska")
            adr = st.text_input("Ulica i kućni broj*")
            
            if st.button("✅ POTVRDI NARUDŽBU"):
                if ime and telefon and grad and ptt and adr:
                    with st.spinner('Slanje narudžbe...'):
                        if posalji_email_vlasniku(ime, telefon, drzava, grad, ptt, adr, detalji_za_email, f"{ukupno:.2f}"):
                            st.session_state.cart_dict = {}
                            st.success("🎉 Zaprimljeno! Točan iznos znat ćete nakon vaganja pri primitku paketa.")
                            st.balloons()
                        else:
                            st.error("Greška kod slanja.")
                else:
                    st.warning("Popunite sva polja!")
            
            if st.button("🗑️ Isprazni"):
                st.session_state.cart_dict = {}
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
    
    col_t, col_k = st.columns([2.0, 1.2])
    with col_t:
        t_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with t_cols[i % 2]:
                st.markdown(f'<div class="product-card"><h3>{p["ime"]}</h3>', unsafe_allow_html=True)
                labela = "€/kom*" if p["tip"] == 1 else "€/kg"
                st.markdown(f'<p class="price-tag">{p["cijena"]:.2f} {labela}</p>', unsafe_allow_html=True)
                
                pocetna = st.session_state.cart_dict.get(p["ime"], {"qty": 0.0})["qty"]
                
                # LOGIKA KORAKA:
                if p["tip"] == 1:
                    # Artikl na komade: krene od 0, korak je uvijek 1
                    step_val = 1.0
                else:
                    # Artikl na kg: ako je 0, prvi klik skače na 1.0, dalje ide po 0.5
                    step_val = 1.0 if pocetna == 0 else 0.5
                
                qty = st.number_input(f"Količina {p['ime']}", min_value=0.0, step=step_val, value=float(pocetna), key=f"inp_{p['id']}", label_visibility="collapsed")
                
                # Ažuriranje košarice u realnom vremenu
                st.session_state.cart_dict[p["ime"]] = {"qty": qty, "price": qty * p["cijena"], "is_komad": p["tip"] == 1}
                st.markdown('</div>', unsafe_allow_html=True)
    prikazi_kosaricu(col_k)

elif izbor == "🏢 ZA UGOSTITELJE":
    st.title("🏢 Ugostiteljska Ponuda i Partnerstva")
    st.markdown("""
    <div class="u-box">
        <h3>Tražite pouzdanog partnera za svoj objekt?</h3>
        <p style="font-size: 18px;">Na veće količine radimo i uslužnu proizvodnju po dogovoru, prilagođenu vašim recepturama.</p>
        <p style="font-size: 18px;">Javite nam se s povjerenjem:</p>
        <ul style="font-size: 18px; list-style-type: none; padding-left: 0;">
            <li>📞 <b>Mobitel:</b> +385 91 XXX XXXX</li>
            <li>📧 <b>E-mail:</b> tomislavtomi90@gmail.com</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif izbor == "🧼 HACCP":
    st.title("🧼 HACCP Sigurnost")
    st.success("✅ ODOBRENI OBJEKT BR. 2686")

elif izbor == "ℹ️ O NAMA":
    st.title("ℹ️ Kontakt")
    st.write(f"📍 **Adresa:** Trg Josipa Mađerića 1, Sisak")
    st.write(f"📧 **Email:** {MOJ_EMAIL}")

# --- FOOTER ---
st.write("---")
st.markdown('<p style="text-align: center; color: #777; font-size: 13px;">Navedene cijene ispod artikala su točne. Iznos u košarici je informativan i približan, a točan iznos znat će se nakon vaganja pri primitku paketa.</p>', unsafe_allow_html=True)
st.caption("© 2026. Mesnica Kojundžić Sisak")
