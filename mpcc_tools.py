# mpcc_tools.py (pełna aplikacja z zakładkami + CP/W′ + poprawionym logo)

import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

# Język
lang = st.sidebar.radio("Language / Język", ("PL", "EN"))
def _(pl, en): return pl if lang == "PL" else en

# Logo i tytuł
st.sidebar.image("logo.png", use_container_width=True)
st.title("MPCC Tools")

# Zakładki

tab_names = [
    _("Strefy mocy (FTP)", "Power Zones (FTP)"),
    _("Strefy tętna (HR)", "Heart Rate Zones"),
    _("W/kg i poziom sportowy", "W/kg and Performance Level"),
    _("CTL / ATL / TSB", "Fitness / Fatigue / Form"),
    _("Struktura tygodnia 80/20", "Weekly 80/20 Split"),
    _("Zakres Sweet Spot", "Sweet Spot Range"),
    _("Check Readiness", "Daily Readiness Check"),
    _("PRO Benchmark", "PRO Benchmark"),
    _("Critical Power i W′", "Critical Power & W′")
]

tabs = st.tabs(tab_names)

# Zakładka 1 – FTP
with tabs[0]:
    st.header(tab_names[0])
    ftp = st.number_input("FTP (W)", 100, 500, 250)
    zones = [0.55, 0.75, 0.90, 1.05, 1.20, 1.50, 1.70]
    labels = ["Z1 – Recovery", "Z2 – Endurance", "Z3 – Tempo", "Z4 – Threshold", "Z5 – VO2max", "Z6 – Anaerobic", "Z7 – Neuromuscular"]

    for i in range(len(zones)):
        zmin = int(ftp * (zones[i-1] if i > 0 else 0))
        zmax = int(ftp * zones[i])
        st.write(f"{labels[i]}: {zmin}–{zmax} W")

    st.caption("Z1: lekka regeneracja, Z2: baza tlenowa, Z3: tempo, Z4: FTP, Z5: VO2max, Z6: zrywy, Z7: sprinty")

# Zakładka 2 – HR
with tabs[1]:
    st.header(tab_names[1])
    hrmax = st.number_input("HR max", 120, 220, 190)
    st.write("Strefy tętna:")
    hr_zones = [(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]
    for i, (low, high) in enumerate(hr_zones):
        st.write(f"Z{i+1}: {int(hrmax*low)} – {int(hrmax*high)} bpm")
    st.caption("Z1: recovery, Z2: fatburn, Z3: endurance, Z4: próg, Z5: max")

# Zakładka 3 – W/kg
with tabs[2]:
    st.header(tab_names[2])
    ftp = st.number_input("FTP (W)", 100, 500, 250, key="ftp2")
    weight = st.number_input("Waga (kg)", 40.0, 120.0, 70.0)
    wkg = ftp / weight
    st.metric("W/kg", f"{wkg:.2f}")

# Zakładka 4 – CTL/ATL/TSB
with tabs[3]:
    st.header(tab_names[3])
    ctl = st.number_input("CTL", 0, 200, 70)
    atl = st.number_input("ATL", 0, 200, 65)
    tsb = ctl - atl
    st.metric("TSB (form)", f"{tsb:+.0f}")

# Zakładka 5 – 80/20
with tabs[4]:
    st.header(tab_names[4])
    total_hours = st.number_input("Godziny tygodniowo", 1, 40, 10)
    z1z2 = total_hours * 0.8
    z3plus = total_hours * 0.2
    st.metric("Z1–Z2 (80%)", f"{z1z2:.1f}h")
    st.metric("Z3+ (20%)", f"{z3plus:.1f}h")

# Zakładka 6 – Sweet Spot
with tabs[5]:
    st.header(tab_names[5])
    ftp = st.number_input("FTP (W)", 100, 500, 250, key="ftp3")
    s_min = ftp * 0.88
    s_max = ftp * 0.94
    st.write(f"Sweet Spot: {int(s_min)} – {int(s_max)} W")

# Zakładka 7 – Readiness
with tabs[6]:
    st.header(tab_names[6])
    sleep = st.slider("Sen (1–10)", 1, 10, 7)
    mood = st.slider("Samopoczucie (1–10)", 1, 10, 7)
    energy = st.slider("Energia (1–10)", 1, 10, 7)
    score = (sleep + mood + energy) / 3
    st.metric("Readiness Score", f"{score:.1f}/10")

# Zakładka 8 – PRO Benchmark (placeholder)
with tabs[7]:
    st.header(tab_names[7])
    st.markdown("W przygotowaniu...")

# Zakładka 9 – CP/W′
with tabs[8]:
    st.header(tab_names[8])

    st.markdown("""Wprowadź dane z dwóch testów, np. 3-min i 12-min. Obliczymy Twój próg CP oraz rezerwę beztlenową W′.""")

    time1 = st.number_input("Czas testu 1 (s)", 60, 1000, 180)
    power1 = st.number_input("Średnia moc testu 1 (W)", 100, 800, 380)

    time2 = st.number_input("Czas testu 2 (s)", 200, 2000, 720)
    power2 = st.number_input("Średnia moc testu 2 (W)", 100, 600, 310)

    if time2 == time1:
        st.warning("Czasy testów muszą się różnić")
    else:
        cp = (power2 * power1 * (time2 - time1)) / (power2 * time2 - power1 * time1)
        w_prime = (power1 - cp) * time1

        st.subheader("📊 Wyniki")
        st.metric("Critical Power (W)", f"{cp:.1f}")
        st.metric("W′ (J)", f"{w_prime:.0f}")

        if cp < 220:
            cp_level = "Niski CP – skup się na bazie tlenowej"
        elif cp < 280:
            cp_level = "Solidny CP – rozwijaj FTP i VO2max"
        else:
            cp_level = "Wysoki CP – świetna wydolność tlenowa"

        if w_prime < 12000:
            w_level = "Niska rezerwa – dodaj sprinty i VO2"
        elif w_prime < 18000:
            w_level = "Zrównoważony profil – rozwijaj próg"
        else:
            w_level = "Silna beztlenowość – dobra końcówka"

        st.success(cp_level)
        st.info(w_level)

        st.markdown("### Sugestie treningowe")
        st.markdown("- Z2 + SST 2x/tydzień")
        st.markdown("- VO2max 3–5 min")
        st.markdown("- Sprinty 15–30s")

        st.markdown("---")
        st.markdown("📩 Potrzebujesz planu? [Skontaktuj się z nami](mailto:michal@mpcc.pl)")

        cp_benchmark = [200, 250, 300]
        labels = ["Niski", "Średni", "Wysoki"]
        colors = ["#bbb", "#aaa", "#888"]

        fig, ax = plt.subplots()
        ax.bar(labels, cp_benchmark, color=colors, label="Benchmarki")
        ax.axhline(cp, color="red", linestyle="--", label="Twój CP")
        ax.set_ylabel("Watts")
        ax.set_title("Porównanie CP")
        ax.legend()
        st.pyplot(fig)
