import streamlit as st
import pandas as pd
import datetime
import urllib.parse

# Configurazione della Pagina
st.set_page_config(
    page_title="Host Control 5.0 — Dimora San Giacomo",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema e Stile Customizzato (Coerente con il Brand Metodo Host5)
st.markdown("""
    <style>
    .main {
        background-color: #F8F9FA;
    }
    .stButton>button {
        background-color: #70AD47 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
    }
    .stButton>button:hover {
        background-color: #5F933B !important;
    }
    .kpi-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #2F5496;
        margin-bottom: 15px;
    }
    .whatsapp-badge {
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 🗃️ INIZIALIZZAZIONE STATO E DATI (DATABASE IN MEMORIA)
# ----------------------------------------------------
if "prenotazioni" not in st.session_state:
    st.session_state.prenotazioni = pd.DataFrame([
        {"ospite": "John Smith", "camera": "Camera Fuoco", "checkin": datetime.date(2026, 6, 1), "checkout": datetime.date(2026, 6, 5), "notti": 4, "ospiti": 2, "canale": "Airbnb", "lordo": 600.0, "cellulare": "+393471234567", "regione": "Lazio", "fascia_eta": "36-50"},
        {"ospite": "Jane Doe", "camera": "Camera Aria", "checkin": datetime.date(2026, 6, 8), "checkout": datetime.date(2026, 6, 12), "notti": 4, "ospiti": 2, "canale": "Booking.com", "lordo": 550.0, "cellulare": "+393471234567", "regione": "Estero", "fascia_eta": "26-35"},
        {"ospite": "Pierre Dubois", "camera": "Camera Terra", "checkin": datetime.date(2026, 6, 15), "checkout": datetime.date(2026, 6, 22), "notti": 7, "ospiti": 3, "canale": "Diretta", "lordo": 900.0, "cellulare": "+393471234567", "regione": "Estero", "fascia_eta": "51-65"},
        {"ospite": "Mario Rossi", "camera": "Camera Acqua", "checkin": datetime.date(2026, 6, 24), "checkout": datetime.date(2026, 6, 29), "notti": 5, "ospiti": 2, "canale": "Airbnb", "lordo": 870.0, "cellulare": "+393471234567", "regione": "Puglia", "fascia_eta": "36-50"},
        {"ospite": "Hans Müller", "camera": "Camera Fuoco", "checkin": datetime.date(2026, 7, 2), "checkout": datetime.date(2026, 7, 8), "notti": 6, "ospiti": 2, "canale": "Booking.com", "lordo": 950.0, "cellulare": "+393471234567", "regione": "Estero", "fascia_eta": "18-25"},
        {"ospite": "Sophie Martin", "camera": "Camera Aria", "checkin": datetime.date(2026, 7, 10), "checkout": datetime.date(2026, 7, 15), "notti": 5, "ospiti": 2, "canale": "Airbnb", "lordo": 850.0, "cellulare": "+393471234567", "regione": "Lombardia", "fascia_eta": "36-50"},
        {"ospite": "Carlos Gomez", "camera": "Camera Terra", "checkin": datetime.date(2026, 7, 20), "checkout": datetime.date(2026, 7, 25), "notti": 5, "ospiti": 2, "canale": "Diretta", "lordo": 1050.0, "cellulare": "+393471234567", "regione": "Estero", "fascia_eta": "26-35"},
        {"ospite": "Jean Dupont", "camera": "Camera Acqua", "checkin": datetime.date(2026, 8, 1), "checkout": datetime.date(2026, 8, 8), "notti": 7, "ospiti": 2, "canale": "Booking.com", "lordo": 1150.0, "cellulare": "+393471234567", "regione": "Estero", "fascia_eta": "51-65"},
        {"ospite": "Anna Bianchi", "camera": "Camera Fuoco", "checkin": datetime.date(2026, 8, 12), "checkout": datetime.date(2026, 8, 18), "notti": 6, "ospiti": 2, "canale": "Airbnb", "lordo": 1050.0, "cellulare": "+393471234567", "regione": "Puglia", "fascia_eta": "36-50"},
        {"ospite": "David Cohen", "camera": "Camera Aria", "checkin": datetime.date(2026, 8, 20), "checkout": datetime.date(2026, 8, 25), "notti": 5, "ospiti": 2, "canale": "Diretta", "lordo": 750.0, "cellulare": "+393471234567", "regione": "Veneto", "fascia_eta": "66+"}
    ])

if "spese" not in st.session_state:
    st.session_state.spese = pd.DataFrame([
        {"data": datetime.date(2026, 6, 5), "camera": "Camera Fuoco", "categoria": "Pulizie", "importo": 50.0, "note": "Pulizia di checkout ditta esterna"},
        {"data": datetime.date(2026, 6, 5), "camera": "Camera Fuoco", "categoria": "Lavanderia", "importo": 25.5, "note": "Lavaggio biancheria"},
        {"data": datetime.date(2026, 6, 12), "camera": "Camera Aria", "categoria": "Pulizie", "importo": 50.0, "note": "Pulizia checkout"},
        {"data": datetime.date(2026, 6, 12), "camera": "Camera Aria", "categoria": "Lavanderia", "importo": 25.0, "note": "Lavaggio biancheria"}
    ])

if "todo" not in st.session_state:
    st.session_state.todo = pd.DataFrame([
        {"data": datetime.date(2026, 8, 14), "area": "Camera Fuoco", "categoria": "Idraulica", "descrizione": "Riparazione perdita lavandino bagno", "stato": "🔴 Aperto", "costo": 80.0},
        {"data": datetime.date(2026, 8, 13), "area": "Camera Aria", "categoria": "Elettricità", "descrizione": "Sostituzione lampadina rooftop", "stato": "🟢 Completato", "costo": 15.0}
    ])

# Costanti di Configurazione
CAMERE = ["Camera Fuoco", "Camera Aria", "Camera Terra", "Camera Acqua", "Camera Etere", "Camera Luce"]
CATEGORIE_MANUTENZIONE = ["Idraulica", "Elettricità", "Pulizie", "Lavanderia", "Spesa Consumabili", "Pitturazione", "Altro"]
CANALI = ["Airbnb", "Booking.com", "Diretta"]
COMMISSIONI = {"Airbnb": 0.15, "Booking.com": 0.18, "Diretta": 0.0}
TASSA_SOGGIORNO = 1.00 # Barletta/Bisceglie
CEDOLARE_SECCA = 0.21
COSTI_FISSI_MENSILI = 315.00 # 3780€ / 12

# Link Recensioni (da Configurazione)
LINK_RECENSIONI = "https://g.page/r/your-google-review-link"

# ----------------------------------------------------
# 🏢 LOGICA DI BUSINESS & REVENUE MANAGEMENT
# ----------------------------------------------------
def calcola_kpi_periodo(start_date, end_date):
    df_filtered = st.session_state.prenotazioni[
        (st.session_state.prenotazioni["checkin"] >= start_date) &
        (st.session_state.prenotazioni["checkin"] <= end_date)
    ]
    tot_notti = df_filtered["notti"].sum()
    lordo = df_filtered["lordo"].sum()
    n_prenotazioni = len(df_filtered)
    
    occupazione_pct = (tot_notti / (len(CAMERE) * 90)) * 100 if n_prenotazioni > 0 else 0
    adr = lordo / tot_notti if tot_notti > 0 else 0
    revpar = adr * (occupazione_pct / 100) if tot_notti > 0 else 0
    
    return n_prenotazioni, tot_notti, lordo, occupazione_pct, adr, revpar

# ----------------------------------------------------
# 🖥️ STRUTTURA DEL FRONTEND (STREAMLIT)
# ----------------------------------------------------
st.title("🏨 Host Control 5.0 — Dimora San Giacomo B&B")
st.markdown("---")

# Layout con Sidebar di Configurazione Rapida
with st.sidebar:
    st.header("⚙️ Cabina di Regia")
    data_test = st.date_input("Data di Simulazione (OGGI):", datetime.date(2026, 8, 23))
    selettore_tempo = st.selectbox("Visualizza movimenti di:", ["DOMANI", "OGGI"])
    cellulare_staff = st.text_input("Cellulare Staff Pulizie:", "+393470000000")
    st.markdown("---")
    st.info("💡 **Metodo Host5**: La regola dei 5 minuti a sera per monitorare l'occupazione e proteggere i margini operativi reali.")

# Navigazione Principale tramite Tabs
tab_notif, tab_pren, tab_planning, tab_finanza, tab_todo = st.tabs([
    "💬 Notifiche WhatsApp",
    "📝 Prenotazioni",
    "📅 Planning & KPI 90GG",
    "📊 Bilancio Mensile",
    "🔧 To-Do & Manutenzioni"
])

# ----------------------------------------------------
# TAB 1: PLANCIA NOTIFICHE WHATSAPP (DYNAMIC CORE)
# ----------------------------------------------------
with tab_notif:
    st.subheader("💬 Plancia Comunicazioni Interattiva (Oggi per Domani)")
    
    # Calcolo data di riferimento
    data_movimento = data_test if selettore_tempo == "OGGI" else data_test + datetime.timedelta(days=1)
    st.warning(f"📅 Visualizzazione movimenti del giorno: **{data_movimento.strftime('%d/%m/%Y')}** (Selettore impostato su *{selettore_tempo}*)")
    
    # Griglia a 6 camere
    cols = st.columns(3)
    for idx, camera in enumerate(CAMERE):
        with cols[idx % 3]:
            st.markdown(f"### 🚪 {camera}")
            
            # Trova partenze (check-out corrispondenti alla data movimento)
            out_guest = st.session_state.prenotazioni[
                (st.session_state.prenotazioni["camera"] == camera) &
                (st.session_state.prenotazioni["checkout"] == data_movimento)
            ]
            
            # Trova arrivi (check-in corrispondenti alla data movimento)
            in_guest = st.session_state.prenotazioni[
                (st.session_state.prenotazioni["camera"] == camera) &
                (st.session_state.prenotazioni["checkin"] == data_movimento)
            ]
            
            is_out = len(out_guest) > 0
            is_in = len(in_guest) > 0
            
            # Caso 1: Cambio al volo (Out + In lo stesso giorno)
            if is_out and is_in:
                guest_out = out_guest.iloc[0]["ospite"]
                phone_out = out_guest.iloc[0]["cellulare"]
                guest_in = in_guest.iloc[0]["ospite"]
                phone_in = in_guest.iloc[0]["cellulare"]
                
                st.markdown("<span class='whatsapp-badge' style='background-color:#FFEB9C;color:#9C6500;'>🔄 CAMBIO AL VOLO</span>", unsafe_allow_html=True)
                st.write(f"👥 **OUT**: {guest_out} | **IN**: {guest_in}")
                st.info("⚠️ Avvisare lo staff per pulizia prioritaria (URGENTE) ed inviare guida e richiesta recensioni.")
                
                # Messaggio Staff Urgente
                msg_staff = f"Ciao! ⚠️ *URGENTE Cambio al Volo* {selettore_tempo.lower()} in *{camera}*! Check-out ore 10:00 e Check-in ore 15:00. Priorità massima. Grazie!"
                url_staff = f"https://wa.me/{cellulare_staff}?text={urllib.parse.quote(msg_staff)}"
                st.markdown(f"[[🧹 WA Staff URGENTE]]({url_staff})", unsafe_allow_html=True)
                
                # Messaggi Ospiti (Affiancati - Soluzione al Bug v30)
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    msg_in = f"Ciao {guest_in}! Ecco la tua Guida Digitale con check-in e info parcheggio: https://guida-terracielo.netlify.app"
                    url_in = f"https://wa.me/{phone_in}?text={urllib.parse.quote(msg_in)}"
                    st.markdown(f"[[🔑 Benvenuto {guest_in}]]({url_in})", unsafe_allow_html=True)
                with col_btn2:
                    msg_out = f"Ciao {guest_out}! Grazie del soggiorno. Ti sei trovato bene? Lasciaci una recensione qui: {LINK_RECENSIONI}"
                    url_out = f"https://wa.me/{phone_out}?text={urllib.parse.quote(msg_out)}"
                    st.markdown(f"[[⭐ Recensione {guest_out}]]({url_out})", unsafe_allow_html=True)
            
            # Caso 2: Solo check-out
            elif is_out:
                guest_out = out_guest.iloc[0]["ospite"]
                phone_out = out_guest.iloc[0]["cellulare"]
                
                st.markdown("<span class='whatsapp-badge' style='background-color:#C6EFCE;color:#006100;'>🟢 PARTENZA</span>", unsafe_allow_html=True)
                st.write(f"👥 **OUT**: {guest_out}")
                st.info(f"🧹 Checkout. Avvisare lo staff ed inviare link Recensioni a {guest_out}.")
                
                # Messaggio Staff Standard
                msg_staff = f"Ciao! {selettore_tempo.lower()} si libera la camera *{camera}* alle ore 10:00. Puoi procedere con le pulizie standard. Grazie!"
                url_staff = f"https://wa.me/{cellulare_staff}?text={urllib.parse.quote(msg_staff)}"
                st.markdown(f"[[🧹 WA Staff (Standard)]]({url_staff})", unsafe_allow_html=True)
                
                # Messaggio Ospite Recensione
                msg_out = f"Ciao {guest_out}! Grazie del soggiorno. Ti sei trovato bene? Lasciaci una recensione qui: {LINK_RECENSIONI}"
                url_out = f"https://wa.me/{phone_out}?text={urllib.parse.quote(msg_out)}"
                st.markdown(f"[[⭐ Richiedi Recensione]]({url_out})", unsafe_allow_html=True)
                
            # Caso 3: Solo check-in
            elif is_in:
                guest_in = in_guest.iloc[0]["ospite"]
                phone_in = in_guest.iloc[0]["cellulare"]
                
                st.markdown("<span class='whatsapp-badge' style='background-color:#FFC7CE;color:#9C0006;'>🔴 ARRIVO</span>", unsafe_allow_html=True)
                st.write(f"👥 **IN**: {guest_in}")
                st.info(f"🔑 Check-in. Inviare messaggio di Benvenuto e Guida Digitale a {guest_in}.")
                
                # Messaggio Ospite Benvenuto
                msg_in = f"Ciao {guest_in}! Benvenuto. Ecco la tua Guida Digitale con check-in e info parcheggio: https://guida-terracielo.netlify.app"
                url_in = f"https://wa.me/{phone_in}?text={urllib.parse.quote(msg_in)}"
                st.markdown(f"[[🔑 Invia Benvenuto & Guida]]({url_in})", unsafe_allow_html=True)
                
            # Caso 4: Vuota / Nessun Movimento
            else:
                st.markdown("<span class='whatsapp-badge' style='background-color:#E3E3E3;color:#7F7F7F;'>⚪ NESSUN MOVIMENTO</span>", unsafe_allow_html=True)
                st.write("-")
                st.write("😴 Tutto calmo. Nessuna azione richiesta per questo giorno.")
            st.markdown("---")

# ----------------------------------------------------
# TAB 2: REGISTRO PRENOTAZIONI
# ----------------------------------------------------
with tab_pren:
    st.subheader("📝 Registro Prenotazioni Attive")
    
    # Form per l'inserimento rapido di una nuova prenotazione
    with st.expander("➕ Inserisci Nuova Prenotazione"):
        col1, col2, col3 = st.columns(3)
        with col1:
            n_ospite = st.text_input("Nome Ospite:")
            c_camera = st.selectbox("Camera Dedicata:", CAMERE)
            c_canale = st.selectbox("Canale di Prenotazione:", CANALI)
        with col2:
            d_checkin = st.date_input("Data Check-in:", datetime.date(2026, 9, 1))
            d_checkout = st.date_input("Data Check-out:", datetime.date(2026, 9, 5))
            num_ospiti = st.number_input("Numero Ospiti:", min_value=1, max_value=6, value=2)
        with col3:
            p_lordo = st.number_input("Prezzo Lordo (€):", min_value=0.0, value=400.0)
            p_telefono = st.text_input("Telefono Ospite:", "+393471234567")
            p_regione = st.selectbox("Regione Provenienza:", ["Lazio", "Puglia", "Veneto", "Lombardia", "Estero"])
            
        if st.button("Salva Prenotazione nel Database"):
            if n_ospite:
                diff_notti = (d_checkout - d_checkin).days
                nuova_p = {
                    "ospite": n_ospite,
                    "camera": c_camera,
                    "checkin": d_checkin,
                    "checkout": d_checkout,
                    "notti": diff_notti,
                    "ospiti": num_ospiti,
                    "canale": c_canale,
                    "lordo": p_lordo,
                    "cellulare": p_telefono,
                    "regione": p_regione,
                    "fascia_eta": "36-50"
                }
                st.session_state.prenotazioni = pd.concat([st.session_state.prenotazioni, pd.DataFrame([nuova_p])], ignore_index=True)
                st.success("🎉 Prenotazione registrata con successo!")
            else:
                st.error("⚠️ Inserisci almeno il nome dell'ospite!")

    # Tabella delle prenotazioni con calcolo delle commissioni in tempo reale
    df_disp = st.session_state.prenotazioni.copy()
    df_disp["Commissioni (€)"] = df_disp.apply(lambda r: r["lordo"] * COMMISSIONI[r["canale"]], axis=1)
    df_disp["Tassa Soggiorno (€)"] = df_disp["notti"] * df_disp["ospiti"] * TASSA_SOGGIORNO
    df_disp["Cedolare (€)"] = (df_disp["lordo"] - df_disp["Commissioni (€)"]) * CEDOLARE_SECCA
    df_disp["Utile Netto (€)"] = df_disp["lordo"] - df_disp["Commissioni (€)"] - df_disp["Tassa Soggiorno (€)"] - df_disp["Cedolare (€)"]
    
    st.dataframe(df_disp.style.format({
        "lordo": "€{:.2f}",
        "Commissioni (€)": "€{:.2f}",
        "Tassa Soggiorno (€)": "€{:.2f}",
        "Cedolare (€)": "€{:.2f}",
        "Utile Netto (€)": "€{:.2f}"
    }), use_container_width=True)

# ----------------------------------------------------
# TAB 3: PLANNING VISIVO E KPI SULL'ORIZZONTE 90 GIORNI
# ----------------------------------------------------
with tab_planning:
    st.subheader("📅 Analisi Strategica Revenue & KPI (Saturazione a 90 Giorni)")
    
    # Orizzonte temporale predefinito (Giugno, Luglio, Agosto 2026)
    start_orizzonte = datetime.date(2026, 6, 1)
    end_orizzonte = datetime.date(2026, 8, 31)
    
    # Calcolo KPI
    n_pren, notti_occ, lordo_90, occ_90, adr_90, revpar_90 = calcola_kpi_periodo(start_orizzonte, end_orizzonte)
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        st.metric("Tasso Occupazione Medio", f"{occ_90:.1f}%")
    with col_kpi2:
        st.metric("Ricavo Lordo Generato", f"€{lordo_90:,.2f}")
    with col_kpi3:
        st.metric("Tariffa Media (ADR)", f"€{adr_90:.2f}")
    with col_kpi4:
        st.metric("RevPAR Struttura", f"€{revpar_90:.2f}")
        
    st.markdown("---")
    st.markdown("#### Vista Calendario Operativa (Controllo Rapido occupazione per camera)")
    
    # Creazione della matrice calendario a 90 giorni (da Giugno 2026 in poi)
    date_range = [start_orizzonte + datetime.timedelta(days=x) for x in range(90)]
    calendario_data = []
    
    for d in date_range:
        row = {"Data": d.strftime('%d/%m/%Y')}
        for camera in CAMERE:
            booking_found = st.session_state.prenotazioni[
                (st.session_state.prenotazioni["camera"] == camera) &
                (st.session_state.prenotazioni["checkin"] <= d) &
                (st.session_state.prenotazioni["checkout"] > d)
            ]
            if len(booking_found) > 0:
                row[camera] = f"🛌 {booking_found.iloc[0]['ospite']}"
            else:
                row[camera] = "🟢 Libera"
        calendario_data.append(row)
        
    df_cal = pd.DataFrame(calendario_data)
    st.dataframe(df_cal, use_container_width=True, height=400)

# ----------------------------------------------------
# TAB 4: BILANCIO MENSILE (FINANZA & CPOR)
# ----------------------------------------------------
with tab_finanza:
    st.subheader("📊 Analisi e Margini di Profitto Reale")
    
    # Calcolo dei dati finanziari mensili (Simulazione basata sui dati storici inseriti)
    giugno_lordo = st.session_state.prenotazioni[st.session_state.prenotazioni["checkin"].apply(lambda d: d.month == 6)]["lordo"].sum()
    luglio_lordo = st.session_state.prenotazioni[st.session_state.prenotazioni["checkin"].apply(lambda d: d.month == 7)]["lordo"].sum()
    agosto_lordo = st.session_state.prenotazioni[st.session_state.prenotazioni["checkin"].apply(lambda d: d.month == 8)]["lordo"].sum()
    
    giugno_var = st.session_state.spese[st.session_state.spese["data"].apply(lambda d: d.month == 6)]["importo"].sum()
    
    m_data = [
        {"Mese": "Giugno 2026", "Lordo (€)": giugno_lordo, "Commissioni (€)": giugno_lordo * 0.165, "Tasse (€)": giugno_lordo * 0.17, "Spese Camere (€)": giugno_var, "Costi Fissi (€)": COSTI_FISSI_MENSILI, "Utile Netto (€)": giugno_lordo - (giugno_lordo*0.335) - giugno_var - COSTI_FISSI_MENSILI},
        {"Mese": "Luglio 2026", "Lordo (€)": luglio_lordo, "Commissioni (€)": luglio_lordo * 0.165, "Tasse (€)": luglio_lordo * 0.17, "Spese Camere (€)": 180.0, "Costi Fissi (€)": COSTI_FISSI_MENSILI, "Utile Netto (€)": luglio_lordo - (luglio_lordo*0.335) - 180.0 - COSTI_FISSI_MENSILI},
        {"Mese": "Agosto 2026", "Lordo (€)": agosto_lordo, "Commissioni (€)": agosto_lordo * 0.165, "Tasse (€)": agosto_lordo * 0.17, "Spese Camere (€)": 135.5, "Costi Fissi (€)": COSTI_FISSI_MENSILI, "Utile Netto (€)": agosto_lordo - (agosto_lordo*0.335) - 135.5 - COSTI_FISSI_MENSILI}
    ]
    
    df_m = pd.DataFrame(m_data)
    df_m["Margine %"] = (df_m["Utile Netto (€)"] / df_m["Lordo (€)"]) * 100
    
    st.dataframe(df_m.style.format({
        "Lordo (€)": "€{:.2f}",
        "Commissioni (€)": "€{:.2f}",
        "Tasse (€)": "€{:.2f}",
        "Spese Camere (€)": "€{:.2f}",
        "Costi Fissi (€)": "€{:.2f}",
        "Utile Netto (€)": "€{:.2f}",
        "Margine %": "{:.1f}%"
    }), use_container_width=True)
    
    st.markdown("---")
    st.info("💡 **Che cos'è il CPOR (Costo per Camera Occupata)?** Rappresenta il costo vivo totale (Fissi + Variabili) per preparare una camera per l'ospite. Utilizza questo indicatore come soglia minima di sicurezza per non vendere mai sotto costo!")

# ----------------------------------------------------
# TAB 5: REGISTRO MANUTENZIONI & TO-DO
# ----------------------------------------------------
with tab_todo:
    st.subheader("🔧 Registro Manutenzioni Ordinari e Controllo Costi")
    
    # Form inserimento manutenzioni
    with st.expander("➕ Segnala Guasto o Manutenzione"):
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            t_area = st.selectbox("Seleziona Camera / Area:", CAMERE + ["Rooftop", "Terrazza", "Esterni"])
            t_cat = st.selectbox("Categoria Guasto:", CATEGORIE_MANUTENZIONE)
            t_desc = st.text_input("Descrizione Attività:")
        with col_t2:
            t_costo = st.number_input("Costo Intervento (€):", min_value=0.0, value=20.0)
            t_stato = st.selectbox("Stato Iniziale:", ["🔴 Aperto", "🟡 In Corso", "🟢 Completato"])
            
        if st.button("Salva Manutenzione"):
            nuovo_guasto = {
                "data": datetime.date.today(),
                "area": t_area,
                "categoria": t_cat,
                "descrizione": t_desc,
                "stato": t_stato,
                "costo": t_costo
            }
            st.session_state.todo = pd.concat([st.session_state.todo, pd.DataFrame([nuovo_guasto])], ignore_index=True)
            st.success("🔧 Manutenzione registrata con successo!")
            
    # Box indicatori To-Do in alto con subtotale
    col_t_kpi1, col_t_kpi2, col_t_kpi3, col_t_kpi4 = st.columns(4)
    with col_t_kpi1:
        st.metric("Lavori Aperti 🔴", len(st.session_state.todo[st.session_state.todo["stato"] == "🔴 Aperto"]))
    with col_t_kpi2:
        st.metric("Lavori In Corso 🟡", len(st.session_state.todo[st.session_state.todo["stato"] == "🟡 In Corso"]))
    with col_t_kpi3:
        st.metric("Lavori Completati 🟢", len(st.session_state.todo[st.session_state.todo["stato"] == "🟢 Completato"]))
    with col_t_kpi4:
        st.metric("Spesa Totale Manutenzioni", f"€{st.session_state.todo['costo'].sum():,.2f}")
        
    st.markdown("---")
    st.dataframe(st.session_state.todo, use_container_width=True)
