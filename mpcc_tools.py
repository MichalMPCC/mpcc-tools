import streamlit as st
import matplotlib.pyplot as plt

# -------------------------------
# Języki
lang = st.sidebar.selectbox("Wybierz język / Select language", ["PL", "ENG"])
is_pl = lang == "PL"

def _(pl, en):
    return pl if is_pl else en

# -------------------------------
# Sidebar i nagłówek
st.set_page_config(page_title="MPCC Tools", layout="wide")
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.markdown("**Kontakt:** [michal@mpcc.pl](mailto:michal@mpcc.pl)")
st.sidebar.markdown("**Instagram:** [@mpcc.pl](https://www.instagram.com/mpcc.pl/)")

st.title(_("🧠 MPCC Tools – Kalkulatory treningowe", "🧠 MPCC Tools – Training Calculators"))

# -------------------------------
# Zakładki
tab_names = [
    _("Strefy mocy (FTP)", "Power Zones (FTP)"),
    _("Strefy tętna (HR)", "Heart Rate Zones"),
    _("W/kg i poziom sportowy", "W/kg and Performance Level"),
    _("Kalorie z treningu", "Training Calorie Estimator"),
    _("CTL / ATL / TSB", "Fitness / Fatigue / Form"),
    _("Struktura tygodnia 80/20", "Weekly 80/20 Split"),
    _("Zakres Sweet Spot", "Sweet Spot Range"),
    _("Check Readiness", "Daily Readiness Check"),
    _("PRO vs Ty", "PRO vs You")
]

tabs = st.tabs(tab_names)

# -------------------------------
# Zakładka 1 – FTP Zones
with tabs[0]:
    st.header(_("Strefy mocy", "Power Zones"))
    ftp = st.number_input(_("Wprowadź FTP (w watach)", "Enter FTP (Watts)"), 100, 500, 250)
    st.write("###", _("Strefy:", "Zones:"))
    zones = {
        _("Strefa 1 (Recovery)", "Zone 1 (Recovery)"): (0, 0.55),
        _("Strefa 2 (Endurance)", "Zone 2 (Endurance)"): (0.56, 0.75),
        _("Strefa 3 (Tempo)", "Zone 3 (Tempo)"): (0.76, 0.90),
        _("Strefa 4 (Lactate Threshold)", "Zone 4 (Threshold)"): (0.91, 1.05),
        _("Strefa 5 (VO2max)", "Zone 5 (VO2max)"): (1.06, 1.20),
        _("Strefa 6 (Anaerobic)", "Zone 6 (Anaerobic)"): (1.21, 1.50),
        _("Strefa 7 (Neuromuscular)", "Zone 7 (Neuromuscular)"): (1.51, 2.5),
    }
    for name, (low, high) in zones.items():
        st.write(f"{name}: {int(low*ftp)} – {int(high*ftp)} W")

# -------------------------------
# Zakładka 2 – HR Zones
with tabs[1]:
    st.header(_("Strefy tętna", "Heart Rate Zones"))
    hr_max = st.number_input(_("Wprowadź HRmax", "Enter HRmax"), 100, 220, 190)
    st.write("###", _("Strefy:", "Zones:"))
    hr_zones = {
        "Zone 1": (0.5, 0.6),
        "Zone 2": (0.6, 0.7),
        "Zone 3": (0.7, 0.8),
        "Zone 4": (0.8, 0.9),
        "Zone 5": (0.9, 1.0)
    }
    for zone, (low, high) in hr_zones.items():
        st.write(f"{zone}: {int(low*hr_max)} – {int(high*hr_max)} bpm")

# -------------------------------
# Zakładka 3 – W/kg
with tabs[2]:
    st.header(_("W/kg i poziom", "W/kg and Performance Level"))
    ftp = st.number_input(_("FTP (W)", "FTP (W)"), 100, 500, 250, key="ftp_wkg")
    weight = st.number_input(_("Waga (kg)", "Weight (kg)"), 40.0, 120.0, 70.0)
    wkg = ftp / weight
    st.metric("W/kg", f"{wkg:.2f}")
    if wkg < 2.5:
        level = _("Początkujący", "Beginner")
    elif wkg < 3.2:
        level = _("Amator", "Amateur")
    elif wkg < 4.0:
        level = _("Zaawansowany", "Advanced")
    elif wkg < 5.0:
        level = _("Ekspert / PRO", "Expert / PRO")
    else:
        level = _("Światowa czołówka", "World Class")
    st.success(_("Poziom: ", "Level: ") + level)

# -------------------------------
# Zakładka 4 – Kalorie
with tabs[3]:
    st.header(_("Kalorie z treningu", "Training Calories"))
    avg_power = st.number_input(_("Średnia moc (W)", "Avg Power (W)"), 100, 400, 200)
    duration = st.number_input(_("Czas treningu (min)", "Training time (min)"), 10, 300, 60)
    efficiency = 0.23
    kcal = avg_power * (duration * 60) / efficiency / 1000
    st.metric(_("Spalone kalorie", "Calories Burned"), f"{kcal:.0f} kcal")

# -------------------------------
# Zakładka 5 – CTL / ATL / TSB
with tabs[4]:
    st.header(_("Forma i zmęczenie", "Form and Fatigue"))
    ctl = st.number_input("CTL (Chronic Load)", 0, 200, 60)
    atl = st.number_input("ATL (Acute Load)", 0, 200, 80)
    tsb = ctl - atl
    st.metric("TSB (Form)", f"{tsb:+.0f}")

# -------------------------------
# Zakładka 6 – 80/20
with tabs[5]:
    st.header(_("Struktura tygodnia 80/20", "80/20 Weekly Structure"))
    weekly_hours = st.number_input(_("Czas tygodniowy (h)", "Weekly hours"), 3, 30, 10)
    low = weekly_hours * 0.8
    high = weekly_hours * 0.2
    st.write(_("Treningi niskiej intensywności (Z1/Z2):", "Low intensity (Z1/Z2):"), f"{low:.1f} h")
    st.write(_("Treningi wysokiej intensywności (Z3+):", "High intensity (Z3+):"), f"{high:.1f} h")

# -------------------------------
# Zakładka 7 – Sweet Spot
with tabs[6]:
    st.header(_("Zakres Sweet Spot", "Sweet Spot Range"))
    ftp = st.number_input("FTP", 100, 500, 250, key="ftp_ss")
    low = 0.84 * ftp
    high = 0.97 * ftp
    st.write(f"Sweet Spot: {int(low)} – {int(high)} W")

# -------------------------------
# Zakładka 8 – Readiness
with tabs[7]:
    st.header(_("Check Readiness", "Sprawdź gotowość"))
    hrv = st.slider("HRV (ms)", 20, 150, 70)
    sleep = st.slider(_("Sen (h)", "Sleep (h)"), 0, 12, 7)
    mood = st.slider(_("Samopoczucie (1–10)", "Mood (1–10)"), 1, 10, 7)
    score = hrv/100 + sleep/10 + mood/10
    st.metric(_("Wynik gotowości", "Readiness Score"), f"{score:.2f}")
    if score < 2.5:
        st.warning(_("Zalecany odpoczynek lub lekki trening", "Recovery or light session recommended"))
    else:
        st.success(_("Można trenować zgodnie z planem", "Ready to train as planned"))

# -------------------------------
# Zakładka 9 – PRO vs Ty
with tabs[8]:
    st.header(_("PRO vs Ty", "PRO vs You"))
    your_wkg = st.number_input("Twój W/kg", 1.0, 7.0, 3.5, 0.1)
    pro_wkg = 6.4
    percent = your_wkg / pro_wkg * 100
    st.metric("% PRO", f"{percent:.1f}%")
    if percent < 50:
        comment = _("Spora różnica – skup się na bazie i systematyczności.", "Big gap – build base and consistency.")
    elif percent < 70:
        comment = _("Jesteś na dobrej drodze!", "You're on the right track!")
    else:
        comment = _("Świetny poziom – zbliżasz się do elity.", "Great level – close to elite.")
    st.info(comment)
