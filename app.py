import streamlit as st
import pandas as pd

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Diagnosa Stres Kerja K3", layout="wide")

st.title("🏢 Diagnosa Faktor Psikologi Kerja")
st.caption("Mengacu pada Permenaker No. 5 Tahun 2018 (K3 Lingkungan Kerja)")

st.info("Skala 1 = Tidak Pernah | 5 = Sangat Sering")

# ======================
# DATA 30 ITEM (6 FAKTOR)
# ======================
kategori_data = {
    "TP": {
        "nama": "Ketidakpastian Peran",
        "soal": [
            "Saya tidak jelas apa yang menjadi tanggung jawab saya.",
            "Saya bingung dengan prioritas pekerjaan saya.",
            "Saya tidak tahu apa yang diharapkan dari pekerjaan saya.",
            "Saya sering menerima instruksi yang tidak jelas.",
            "Peran saya dalam pekerjaan tidak terdefinisi dengan baik."
        ]
    },
    "KP": {
        "nama": "Konflik Peran",
        "soal": [
            "Saya menerima perintah yang saling bertentangan.",
            "Saya diminta melakukan pekerjaan di luar tanggung jawab saya.",
            "Saya mengalami konflik antara dua atasan.",
            "Saya merasa tuntutan pekerjaan bertabrakan.",
            "Saya harus memenuhi ekspektasi yang berbeda-beda."
        ]
    },
    "BBKuan": {
        "nama": "Beban Kerja Kuantitatif",
        "soal": [
            "Volume pekerjaan saya terlalu banyak.",
            "Saya harus bekerja sangat cepat.",
            "Saya sering kehabisan waktu untuk menyelesaikan pekerjaan.",
            "Deadline pekerjaan terlalu ketat.",
            "Saya harus lembur untuk menyelesaikan pekerjaan."
        ]
    },
    "BBKual": {
        "nama": "Beban Kerja Kualitatif",
        "soal": [
            "Pekerjaan saya terlalu sulit.",
            "Saya membutuhkan keterampilan yang belum saya kuasai.",
            "Saya sering merasa tidak mampu menyelesaikan tugas.",
            "Pekerjaan membutuhkan konsentrasi tinggi.",
            "Saya merasa tekanan mental dari pekerjaan."
        ]
    },
    "PK": {
        "nama": "Pengembangan Karir",
        "soal": [
            "Saya tidak melihat peluang karir.",
            "Promosi di tempat kerja tidak jelas.",
            "Saya merasa karir saya stagnan.",
            "Pengembangan diri tidak didukung perusahaan.",
            "Saya tidak mendapat pelatihan yang cukup."
        ]
    },
    "TJO": {
        "nama": "Tanggung Jawab Orang Lain",
        "soal": [
            "Saya bertanggung jawab atas pekerjaan orang lain.",
            "Kesalahan orang lain berdampak pada saya.",
            "Saya harus mengawasi banyak orang.",
            "Saya merasa terbebani oleh tanggung jawab tim.",
            "Saya harus memastikan pekerjaan orang lain benar."
        ]
    }
}

# ======================
# INPUT USER
# ======================
jawaban = {}

for kode, item in kategori_data.items():
    with st.expander(f"📌 {item['nama']}", expanded=False):
        for i, soal in enumerate(item["soal"]):
            key = f"{kode}_{i}"
            jawaban[key] = st.slider(
                soal,
                min_value=1,
                max_value=5,
                value=3
            )

st.markdown("---")

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
if st.button("🔍 Proses Diagnosa"):

    hasil = {}

    for kode, item in kategori_data.items():
        skor = sum([
            jawaban[f"{kode}_{i}"] for i in range(5)
        ])
        hasil[kode] = {
            "Nama": item["nama"],
            "Skor": skor,
            "Kategori": klasifikasi(skor)
        }

    df = pd.DataFrame(hasil).T

    st.subheader("📊 Hasil per Faktor")
    st.dataframe(df, use_container_width=True)

    # ======================
    # VISUAL
    # ======================
    st.subheader("📈 Grafik Skor")
    st.bar_chart(df["Skor"])

    # ======================
    # PRIORITAS
    # ======================
    st.subheader("⚠️ Prioritas Risiko")

    tinggi = df[df["Kategori"] == "Tinggi"]

    if not tinggi.empty:
        for i in tinggi.index:
            st.error(f"{df.loc[i,'Nama']} → Risiko Tinggi, perlu tindakan segera")
    else:
        st.success("Tidak ada faktor risiko tinggi")

    # ======================
    # INSIGHT
    # ======================
    st.subheader("💡 Insight")

    for i in df.index:
        skor = df.loc[i, "Skor"]
        nama = df.loc[i, "Nama"]

        if skor > 24:
            st.error(f"{nama}: Beban kritis, perlu intervensi segera")
        elif skor >= 10:
            st.warning(f"{nama}: Perlu monitoring & evaluasi")
        else:
            st.success(f"{nama}: Kondisi aman")

# ======================
# SIDEBAR
# ======================
st.sidebar.header("Tentang")
st.sidebar.write("Tools ini digunakan untuk analisis stres kerja berbasis K3.")
st.sidebar.caption("HRGA System - 2026")
