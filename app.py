import streamlit as st
import pandas as pd

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Stress Assessment K3", layout="wide")

# ======================
# STYLE
# ======================
st.markdown("""
<style>
.block-container {
    max-width: 900px;
}
.question-box {
    padding: 12px;
    border-radius: 10px;
    background-color: #f8fafc;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.title("📋 Kuesioner Faktor Psikologi Kerja")
st.caption("Mengacu pada Permenaker No. 5 Tahun 2018 tentang K3 Lingkungan Kerja")

st.info("Silakan pilih jawaban sesuai kondisi kerja yang Anda alami dalam beberapa waktu terakhir.")

# ======================
# SKALA
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
# DATA (DESKRIPSI + SOAL PANJANG)
# ======================
kategori_data = {
    "TP": {
        "nama": "Ketidakpastian Peran",
        "deskripsi": "Kondisi dimana pekerja tidak memiliki kejelasan terkait tugas, tanggung jawab, dan harapan pekerjaan yang harus dilakukan.",
        "soal": [
            "Saya merasa tidak mendapatkan penjelasan yang jelas mengenai apa saja tugas dan tanggung jawab utama dalam pekerjaan saya.",
            "Saya sering mengalami kebingungan dalam menentukan prioritas pekerjaan yang harus diselesaikan terlebih dahulu.",
            "Saya tidak memahami secara jelas apa yang diharapkan oleh atasan terhadap hasil kerja saya.",
            "Instruksi kerja yang saya terima seringkali tidak lengkap atau kurang jelas.",
            "Peran dan fungsi saya dalam organisasi tidak dijelaskan secara rinci."
        ]
    },
    "KP": {
        "nama": "Konflik Peran",
        "deskripsi": "Kondisi dimana pekerja menerima tuntutan pekerjaan yang saling bertentangan atau tidak sejalan.",
        "soal": [
            "Saya menerima perintah kerja yang saling bertentangan dari atasan yang berbeda.",
            "Saya diminta melakukan pekerjaan yang tidak sesuai dengan tugas pokok saya.",
            "Saya mengalami konflik antara tuntutan dari dua pihak atau lebih dalam pekerjaan.",
            "Saya merasa tuntutan pekerjaan yang diberikan tidak selaras satu sama lain.",
            "Saya harus memenuhi ekspektasi yang berbeda dari beberapa pihak sekaligus."
        ]
    },
    "BBKuan": {
        "nama": "Beban Kerja Kuantitatif",
        "deskripsi": "Kondisi dimana jumlah pekerjaan yang harus diselesaikan melebihi kemampuan atau waktu yang tersedia.",
        "soal": [
            "Jumlah pekerjaan yang harus saya selesaikan terlalu banyak dalam waktu yang terbatas.",
            "Saya harus bekerja dengan kecepatan tinggi untuk menyelesaikan tugas.",
            "Saya sering merasa waktu kerja tidak cukup untuk menyelesaikan pekerjaan.",
            "Saya dihadapkan pada tenggat waktu yang sangat ketat.",
            "Saya sering harus bekerja lembur untuk menyelesaikan pekerjaan."
        ]
    },
    "BBKual": {
        "nama": "Beban Kerja Kualitatif",
        "deskripsi": "Kondisi dimana tingkat kesulitan pekerjaan melebihi kemampuan atau kompetensi pekerja.",
        "soal": [
            "Pekerjaan yang saya lakukan memiliki tingkat kesulitan yang tinggi.",
            "Saya merasa membutuhkan keterampilan tambahan untuk menyelesaikan pekerjaan.",
            "Saya sering merasa tidak mampu menyelesaikan tugas dengan baik.",
            "Pekerjaan saya menuntut konsentrasi yang sangat tinggi dalam waktu lama.",
            "Saya merasakan tekanan mental yang tinggi saat bekerja."
        ]
    },
    "PK": {
        "nama": "Pengembangan Karir",
        "deskripsi": "Kondisi terkait peluang pengembangan diri, pelatihan, dan kemajuan karir dalam pekerjaan.",
        "soal": [
            "Saya tidak melihat adanya peluang pengembangan karir di tempat kerja.",
            "Sistem promosi jabatan di perusahaan tidak jelas.",
            "Saya merasa karir saya tidak berkembang.",
            "Perusahaan kurang memberikan dukungan untuk pengembangan kompetensi.",
            "Saya jarang mendapatkan pelatihan yang relevan dengan pekerjaan."
        ]
    },
    "TJO": {
        "nama": "Tanggung Jawab Orang Lain",
        "deskripsi": "Kondisi dimana pekerja memiliki tanggung jawab terhadap pekerjaan atau keselamatan orang lain.",
        "soal": [
            "Saya bertanggung jawab atas hasil kerja orang lain.",
            "Kesalahan yang dilakukan orang lain berdampak pada pekerjaan saya.",
            "Saya harus mengawasi banyak orang dalam pekerjaan.",
            "Saya merasa terbebani oleh tanggung jawab terhadap tim.",
            "Saya harus memastikan pekerjaan orang lain berjalan dengan benar."
        ]
    }
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

    st.subheader("📊 Hasil")
    st.dataframe(df, use_container_width=True)

    st.bar_chart(df.set_index("Faktor")["Skor"])

    # ======================
    # DOWNLOAD EXCEL
    # ======================
    file_name = f"hasil_stres_{nama}.xlsx"

    st.download_button(
        label="📥 Download Excel",
        data=df.to_excel(index=False, engine="openpyxl"),
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
