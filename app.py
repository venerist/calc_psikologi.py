import streamlit as st
import pandas as pd
from io import BytesIO

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Stress Assessment K3",
    layout="centered"
)

# ======================
# STYLE
# ======================
st.markdown("""
<style>
.block-container {
    max-width: 850px;
}
.question-box {
    padding: 12px;
    border-radius: 10px;
    background-color: #f1f5f9;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.title("📋 Kuesioner Stres Kerja")
st.caption("Berdasarkan Permenaker No. 5 Tahun 2018 (K3 Lingkungan Kerja)")

st.info("Pilih jawaban sesuai kondisi kerja yang Anda alami.")

# ======================
# SKALA
# ======================
st.markdown("""
**Skala Penilaian:**
1 = Tidak Pernah  
2 = Jarang  
3 = Kadang-kadang  
4 = Sering  
5 = Sangat Sering  
""")

# ======================
# DATA PERTANYAAN
# ======================
kategori_data = {
    "TP": {
        "nama": "Ketidakpastian Peran",
        "deskripsi": "Ketidakjelasan mengenai tugas, tanggung jawab, dan ekspektasi pekerjaan.",
        "soal": [
            "Saya tidak mendapatkan penjelasan yang jelas mengenai tugas pekerjaan saya.",
            "Saya bingung menentukan prioritas pekerjaan.",
            "Saya tidak memahami ekspektasi atasan.",
            "Instruksi kerja sering tidak jelas.",
            "Peran saya dalam pekerjaan tidak terdefinisi."
        ]
    },
    "KP": {
        "nama": "Konflik Peran",
        "deskripsi": "Adanya tuntutan pekerjaan yang saling bertentangan.",
        "soal": [
            "Saya menerima perintah yang bertentangan.",
            "Saya diminta melakukan pekerjaan di luar tugas saya.",
            "Saya mengalami konflik antar atasan.",
            "Tuntutan pekerjaan saling bertabrakan.",
            "Ekspektasi dari berbagai pihak berbeda."
        ]
    },
    "BBKuan": {
        "nama": "Beban Kerja Kuantitatif",
        "deskripsi": "Jumlah pekerjaan melebihi waktu atau kemampuan.",
        "soal": [
            "Pekerjaan saya terlalu banyak.",
            "Saya harus bekerja sangat cepat.",
            "Waktu kerja tidak cukup.",
            "Deadline sangat ketat.",
            "Saya sering lembur."
        ]
    },
    "BBKual": {
        "nama": "Beban Kerja Kualitatif",
        "deskripsi": "Tingkat kesulitan pekerjaan tinggi.",
        "soal": [
            "Pekerjaan saya sulit.",
            "Saya butuh skill tambahan.",
            "Saya merasa tidak mampu menyelesaikan tugas.",
            "Pekerjaan butuh konsentrasi tinggi.",
            "Saya merasa tekanan mental tinggi."
        ]
    },
    "PK": {
        "nama": "Pengembangan Karir",
        "deskripsi": "Peluang pengembangan dan karir.",
        "soal": [
            "Tidak ada peluang karir.",
            "Promosi tidak jelas.",
            "Karir stagnan.",
            "Kurang dukungan pengembangan.",
            "Jarang pelatihan."
        ]
    },
    "TJO": {
        "nama": "Tanggung Jawab Orang Lain",
        "deskripsi": "Tanggung jawab terhadap pekerjaan orang lain.",
        "soal": [
            "Saya bertanggung jawab atas orang lain.",
            "Kesalahan orang lain berdampak ke saya.",
            "Saya mengawasi banyak orang.",
            "Saya terbebani oleh tim.",
            "Saya harus memastikan pekerjaan orang lain."
        ]
    }
}

# ======================
# IDENTITAS
# ======================
st.markdown("### 👤 Data Karyawan")

nama = st.text_input("Nama")
dept = st.selectbox("Departemen", ["HR", "Finance", "IT", "Produksi"])

st.markdown("---")

# ======================
# INPUT JAWABAN
# ======================
jawaban = {}

for kode, item in kategori_data.items():
    st.markdown(f"### 📌 {item['nama']}")
    st.caption(item["deskripsi"])

    for i, soal in enumerate(item["soal"]):
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

if st.button("🔍 Proses & Download"):

    hasil = []

    for kode, item in kategori_data.items():
        skor = sum([jawaban[f"{kode}_{i}"] for i in range(5)])

        hasil.append({
            "Nama": nama,
            "Departemen": dept,
            "Faktor": item["nama"],
            "Skor": skor,
            "Kategori": klasifikasi(skor)
        })

    df = pd.DataFrame(hasil)

    # ======================
    # OUTPUT
    # ======================
    st.subheader("📊 Hasil Analisis")
    st.dataframe(df, use_container_width=True)

    st.bar_chart(df.set_index("Faktor")["Skor"])

    # ======================
    # PRIORITAS
    # ======================
    st.subheader("⚠️ Prioritas")

    high = df[df["Kategori"] == "Tinggi"]

    if not high.empty:
        for _, row in high.iterrows():
            st.error(f"{row['Faktor']} → Risiko Tinggi")
    else:
        st.success("Tidak ada risiko tinggi")

    # ======================
    # DOWNLOAD EXCEL (FIX)
    # ======================
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Hasil')

    excel_data = output.getvalue()

    st.download_button(
        label="📥 Download Excel",
        data=excel_data,
        file_name=f"hasil_stres_{nama}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
