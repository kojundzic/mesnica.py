import streamlit as st
import pd
import requests
from PIL import Image
from io import BytesIO

# Postavke aplikacije
st.set_page_config(page_title="Kojundžić Mesnica | Premium Selection", page_icon="🥩", layout="wide")

@st.cache_data
def load_image(url):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# --- MODERNI VIZUALNI IDENTITET (2026) ---
st.markdown(
    """
    <style>
    /* Glavna pozadina s blagim gradijentom */
    .stApp { background: linear-gradient(to bottom, #fdfdfd, #f4f4f4); }
    
    /* Hero sekcija */
    .hero-section {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('images.unsplash.com');
        background-size: cover; background-position: center;
        padding: 60px; border-radius: 30px; text-align: center; color: white; margin-bottom: 40px;
    }
    
    /* Kartice proizvoda - moderni Glassmorphism */
    .product-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    .product-card:hover { transform: translateY(-10px); box-shadow: 0 15px 40px rgba(139,0,0,0.15); }
    
    /* Gumbi */
    .stButton>button {
        background: #8B0000; color: white !important; border-radius: 50px;
        border: none; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
    }
    
    /* Bočna košarica */
    .sidebar-cart {
        background: white; padding: 25px; border-radius: 20px;
        border: 1px solid #eee; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, 
    unsafe_allow_html=True
)

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- PODACI ---
proizvodi = [
    {"id": 1, "ime": "Dimljena češnjovka", "cijena": 11.50, "slika": "images.unsplash.com"},
    {"id": 2, "ime": "Dimljeni buncek", "cijena": 8.50, "slika": "images.unsplash.com"},
    {"id": 3, "ime": "Dimljeni prsni vršci", "cijena": 9.20, "slika": "images.unsplash.com"},
    {"id": 4, "ime": "Premium Buđola", "cijena": 19.50, "slika": "images.unsplash.com"},
    {"id": 5, "ime": "Dimljeni vrat", "cijena": 15.00, "slika": "images.unsplash.com"},
    {"id": 6, "ime": "Slavonska kobasica", "cijena": 14.50, "slika": "images.unsplash.com"},
]

# --- NAVIGACIJA ---
with st.sidebar:
    st.markdown("## 🥩 KOJUNDŽIĆ")
    izbor = st.radio("MENU", ["🛍️ TRGOVINA", "🚜 DOBAVLJAČI", "🧼 HACCP", "ℹ️ KONTAKT"])
    st.write("---")
    st.caption("Sisak | Siječanj 2026.")

# --- TRGOVINA ---
if izbor == "🛍️ TRGOVINA":
    # Hero uvod
    st.markdown("""
        <div class="hero-section">
            <h1 style='color: white;'>Tradicija dima iz srca Posavine</h1>
            <p style='font-size: 1.2em;'>Domaće meso uzgojeno na prostranim pašnjacima okolice Siska.</p>
        </div>
    """, unsafe_allow_html=True)

    col_main, col_cart = st.columns([2.5, 1])

    with col_main:
        st.subheader("Naša selekcija")
        prod_cols = st.columns(2)
        for i, p in enumerate(proizvodi):
            with prod_cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                img = load_image(p["slika"])
                if img: st.image(img, use_container_width=True)
                st.markdown(f"### {p['ime']}")
                st.markdown(f"<h3 style='color: #8B0000;'>{p['cijena']:.2f} €/kg</h3>", unsafe_allow_html=True)
                qty = st.number_input(f"Količina (kg)", 1.0, 20.0, 1.0, 0.5, key=f"q_{p['id']}")
                if st.button("DODAJ U KOŠARICU", key=f"b_{p['id']}"):
                    st.session_state.cart.append({"ime": p['ime'], "qty": qty, "price": qty * p['cijena']})
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    with col_cart:
        st.markdown('<div class="sidebar-cart">', unsafe_allow_html=True)
        st.subheader("🛒 Vaša Narudžba")
        if not st.session_state.cart:
            st.write("Vaša košarica čeka prve domaće proizvode.")
        else:
            ukupno = sum(item['price'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"**{item['ime']}** | {item['qty']}kg")
            st.write("---")
            st.markdown(f"## Ukupno: {ukupno:.2f} €")
            if st.button("🗑️ ISPRAZNI"):
                st.session_state.cart = []
                st.rerun()
            
            st.write("---")
            ime = st.text_input("Ime i Prezime*")
            mob = st.text_input("Mobitel*")
            adr = st.text_input("Adresa*")
            if st.button("✅ ZAVRŠI NARUDŽBU"):
                if ime and mob and adr:
                    # Logika za e-mail link
                    st.success("Spremno za slanje!")
                    st.markdown("*(Mail se otvara automatski)*")
        st.markdown('</div>', unsafe_allow_html=True)

# --- DOBAVLJAČI (S MODERNIM SLIKAMA) ---
elif izbor == "🚜 DOBAVLJAČI":
    st.title("🚜 Prirodni uzgoj i naši partneri")
    
    # Slika stoke u prirodi
    img_vrava = "images.unsplash.com" # Slika krava na pašnjaku
    st.image(img_vrava, caption="Slobodna ispaša u Lonjskom polju", use_container_width=True)
    
    st.markdown("""
    ### Od pašnjaka do vašeg stola
    Vjerujemo da vrhunsko meso dolazi samo iz suživota s prirodom. Svu našu stoku nabavljamo od malih OPG-ova s područja:
    *   **Banovine:** Brdski predjeli s čistim zrakom i bogatom ispašom.
    *   **Posavine:** Tradicija uzgoja koja traje stoljećima.
    *   **Parka prirode Lonjsko polje:** Gdje životinje žive u skladu s prirodnim ciklusima poplava i slobodne ispaše.
    """)
    
    # Dodatna slika životinja
    img_svinje = "images.unsplash.com" # Slika domaćih životinja
    st.image(img_svinje, caption="Tradicija uzgoja u Posavini", use_container_width=True)

# --- HACCP ---
elif izbor == "🧼 HACCP":
    st.title("Higijena i Sigurnost")
    st.info("Pogon za preradu mesa registriran pod brojem: **2686**")
    st.markdown("""
    Naš pogon koristi najsuvremenije sustave nadzora **HACCP**. 
    Svaki komad mesa je sljediv, od trenutka otkupa od OPG-a do trenutka kada stigne na Vaš prag. 
    Sigurnost i čistoća su temelj našeg poslovanja od prvog dana.
    """)

# --- KONTAKT ---
elif izbor == "ℹ️ KONTAKT":
    st.title("Posjetite nas u Sisku")
    st.markdown("""
    Pozivamo Vas da nas posjetite u našoj mesnici i uvjerite se u kvalitetu na licu mjesta.
    *   **Adresa:** Trg Josipa Mađerića 1, 44000 Sisak
    *   **E-mail:** tomislavtomi90@gmail.com
    """)
    st.map(pd.DataFrame({'lat': [45.4832], 'lon': [16.3761]}))
