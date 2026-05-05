import streamlit as st
import pandas as pd

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Stress Risk Assessment", layout="wide")

# ======================
# STYLE ENTERPRISE
# ======================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    font-weight: 600;
}
.stDataFrame {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.title("📊 Stress Risk Assessment Dashboard")
st.caption("Permenaker No. 5 Tahun 2018 - K3 Psikologi Kerja")

# ======================
# DATA 30 ITEM
# ======================
kategori_data = {
    "TP": ("Ketidakpastian Peran", [
        "Tidak jelas tanggung jawab",
        "Bingung prioritas kerja",
        "Tidak tahu ekspektasi kerja",
        "Instruksi tidak jelas",
        "Peran tidak terdefinisi"
    ]),
    "KP": ("Konflik Peran", [
        "Perintah bertentangan",
        "Tugas di luar tanggung jawab",
        "Konflik antar atasan",
        "Tuntutan bertabrakan",
        "Ekspektasi berbeda-beda"
    ]),
    "BBKuan": ("Beban Kuantitatif", [
        "Volume kerja terlalu banyak",
        "Harus kerja cepat",
        "Kekurangan waktu",
        "Deadline ketat",
        "Sering lembur"
    ]),
    "BBKual": ("Beban Kualitatif", [
        "Pekerjaan terlalu sulit",
        "Butuh skill tinggi",
        "Merasa tidak mampu",
        "Butuh konsentrasi tinggi",
        "Tekanan mental tinggi"
    ]),
    "PK": ("Pengembangan Karir", [
        "Tidak ada peluang karir",
        "Promosi tidak jelas",
        "Karir stagnan",
        "Kurang dukungan pengembangan",
        "Minim pelatihan"
    ]),
    "TJO": ("Tanggung Jawab Orang Lain", [
        "Bertanggung jawab atas orang lain",
        "Kesalahan orang lain berdampak",
        "Mengawasi banyak orang",
        "Beban tim tinggi",
        "Harus memastikan pekerjaan orang lain"
    ])
}

# ======================
# BUILD GRID DATA
# ======================
rows = []
mapping = []

for kode, (nama, soal_list) in kategori_data.items():
    for soal in soal_list:
        rows.append({
            "Faktor": nama,
            "Pertanyaan": soal,
            "Skor": 3
        })
        mapping.append(kode)

df_input = pd.DataFrame(rows)

# ======================
# INPUT IDENTITAS
# ======================
col1, col2 = st.columns(2)

with col1:
    nama_user = st.text_input("Nama Karyawan")

with col2:
    departemen = st.selectbox("Departemen", ["HR", "Finance", "IT", "Produksi"])

# ======================
# GRID INPUT
# ======================
st.subheader("📝 Kuesioner (Pilih Skala 1–5)")

edited_df = st.data_editor(
    df_input,
    column_config={
        "Skor": st.column_config.SelectboxColumn(
            "Skala",
            options=[1,2,3,4,5],
            required=True
        )
    },
    hide_index=True,
    use_container_width=True
)

st.caption("1 = Tidak Pernah | 5 = Sangat Sering")

# ======================
# FUNCTION
# ======================
def klasifikasi(skor):
    if skor <= 9:
        return "Rendah"
    elif skor <= 24:
        return "Sedang"
    else:
        return "Tinggi"

# ======================
# PROSES
# ======================
if st.button("🔍 Analisa"):

    edited_df["Kode"] = mapping

    hasil = edited_df.groupby("Kode")["Skor"].sum().reset_index()

    nama_map = {k:v[0] for k,v in kategori_data.items()}
    hasil["Faktor"] = hasil["Kode"].map(nama_map)
    hasil["Kategori"] = hasil["Skor"].apply(klasifikasi)

    # ======================
    # OUTPUT
    # ======================
    st.subheader("📊 Hasil Analisis")

    st.dataframe(
        hasil[["Faktor","Skor","Kategori"]],
        use_container_width=True
    )

    # ======================
    # METRIC
    # ======================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Faktor", len(hasil))

    with col2:
        st.metric("Risiko Tinggi", (hasil["Kategori"]=="Tinggi").sum())

    with col3:
        st.metric("Rata-rata Skor", round(hasil["Skor"].mean(),1))

    # ======================
    # CHART
    # ======================
    st.subheader("📈 Visualisasi")
    st.bar_chart(hasil.set_index("Faktor")["Skor"])

    # ======================
    # PRIORITAS
    # ======================
    st.subheader("⚠️ Prioritas")

    high = hasil[hasil["Kategori"]=="Tinggi"]

    if not high.empty:
        for _, row in high.iterrows():
            st.error(f"{row['Faktor']} → Risiko Tinggi")
    else:
        st.success("Tidak ada risiko tinggi")

# ======================
# SIDEBAR
# ======================
st.sidebar.title("ℹ️ Informasi")
st.sidebar.write("Assessment psikologi kerja berbasis Permenaker")
st.sidebar.caption("HRGA System 2026")
