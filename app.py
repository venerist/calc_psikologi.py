import streamlit as st
import pandas as pd

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Stress Assessment", layout="wide")

# ======================
# STYLE (ENTERPRISE + CLEAN)
# ======================
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    max-width: 900px;
}
h1 {
    font-weight: 700;
}
.question-box {
    padding: 12px;
    border-radius: 10px;
    background-color: #f8fafc;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.title("📋 Kuesioner Stres Kerja")
st.caption("Permenaker No. 5 Tahun 2018")

st.info("Pilih angka yang paling sesuai dengan kondisi Anda")

# ======================
# SKALA (BIAR JELAS)
# ======================
st.markdown("""
**Skala Penilaian:**
- 1 = Tidak Pernah  
- 2 = Jarang  
- 3 = Kadang-kadang  
- 4 = Sering  
- 5 = Sangat Sering  
""")

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
        "Ekspektasi berbeda"
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
        "Memastikan pekerjaan orang lain"
    ])
}

# ======================
# INPUT IDENTITAS
# ======================
st.markdown("### 👤 Data Karyawan")

col1, col2 = st.columns(2)

with col1:
    nama = st.text_input("Nama")

with col2:
    dept = st.selectbox("Departemen", ["HR", "Finance", "IT", "Produksi"])

st.markdown("---")

# ======================
# INPUT PERTANYAAN
# ======================
jawaban = {}

for kode, (nama_kat, soal_list) in kategori_data.items():
    st.markdown(f"### 📌 {nama_kat}")

    for i, soal in enumerate(soal_list):
        key = f"{kode}_{i}"

        st.markdown(f"<div class='question-box'>{soal}</div>", unsafe_allow_html=True)

        jawaban[key] = st.radio(
            "",
            options=[1,2,3,4,5],
            horizontal=True,
            key=key
        )

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
st.markdown("---")

if st.button("🔍 Lihat Hasil"):

    hasil = {}

    for kode, (nama_kat, _) in kategori_data.items():
        skor = sum([jawaban[f"{kode}_{i}"] for i in range(5)])
        hasil[kode] = {
            "Faktor": nama_kat,
            "Skor": skor,
            "Kategori": klasifikasi(skor)
        }

    df = pd.DataFrame(hasil).T

    st.subheader("📊 Hasil")

    st.dataframe(df, use_container_width=True)

    st.bar_chart(df.set_index("Faktor")["Skor"])

    # PRIORITAS
    st.subheader("⚠️ Prioritas")

    high = df[df["Kategori"]=="Tinggi"]

    if not high.empty:
        for i in high.index:
            st.error(f"{df.loc[i,'Faktor']} → Risiko Tinggi")
    else:
        st.success("Tidak ada risiko tinggi")
