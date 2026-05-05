import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="HSE Psych Assessment",
    page_icon="🛡️",
    layout="centered"
)

# ==========================================
# 2. STYLE CSS (UI FIX & SIDEBAR TERANG)
# ==========================================
st.markdown("""
<style>
    /* Mengatur warna latar belakang aplikasi */
    .stApp { background-color: #f8fafc; }
    .block-container { max-width: 850px; padding-top: 2rem; }

    /* Sidebar Terang & Modern */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Warna Teks di Sidebar agar Kontras */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h3 {
        color: #1e293b !important;
    }

    /* Box Skala Penilaian di Sidebar */
    .scale-box {
        background-color: #f1f5f9;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
    }

    /* Kartu Soal */
    .question-card {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border-left: 6px solid #10b981; /* Hijau HSE */
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 10px;
    }
    .question-text { color: #334155; font-weight: 500; font-size: 16px; }

    /* Button Style */
    div.stButton > button:first-child {
        background-color: #10b981;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: bold;
        width: 100%;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. DATA STRUKTUR (PERMENAKER 5/2018)
# ==========================================
kategori_data = {
    "TP": {
        "nama": "Ketidakpastian Peran",
        "desc": "Ketidakjelasan mengenai tugas dan tanggung jawab.",
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
        "desc": "Adanya tuntutan pekerjaan yang saling bertentangan.",
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
        "desc": "Jumlah pekerjaan melebihi waktu atau kemampuan.",
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
        "desc": "Tingkat kesulitan pekerjaan yang tinggi.",
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
        "desc": "Peluang pengembangan dan kepastian karir.",
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
        "desc": "Beban tanggung jawab terhadap hasil kerja orang lain.",
        "soal": [
            "Saya bertanggung jawab atas orang lain.",
            "Kesalahan orang lain berdampak ke saya.",
            "Saya mengawasi banyak orang.",
            "Saya terbebani oleh tim.",
            "Saya harus memastikan pekerjaan orang lain."
        ]
    }
}

# ==========================================
# 4. SIDEBAR (SKALA PENILAIAN TERANG)
# ==========================================
with st.sidebar:
    st.markdown("# 🛡️ K3 Lingkungan Kerja")
    st.write("Sesuai Permenaker No. 5/2018")
    st.markdown("---")
    
    st.markdown("### 📊 Skala Penilaian")
    st.markdown("""
    <div class='scale-box'>
        <p style='color: #1e293b; margin-bottom: 5px;'><b>1:</b> Tidak Pernah</p>
        <p style='color: #1e293b; margin-bottom: 5px;'><b>2:</b> Jarang</p>
        <p style='color: #1e293b; margin-bottom: 5px;'><b>3:</b> Kadang-kadang</p>
        <p style='color: #1e293b; margin-bottom: 5px;'><b>4:</b> Sering</p>
        <p style='color: #1e293b; margin-bottom: 0px;'><b>5:</b> Sangat Sering</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Dibuat oleh Adam - Portofolio 2026")

# ==========================================
# 5. HEADER & IDENTITAS
# ==========================================
st.title("📋 Kuesioner Stres Kerja")
st.caption("Asesmen Faktor Psikologi Berdasarkan Permenaker No. 5 Tahun 2018")

with st.expander("👤 Identitas Karyawan", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap")
    with col2:
        dept = st.selectbox("Departemen", ["HRGA", "Finance", "IT", "Produksi", "Maintenance"])

st.markdown("---")

# ==========================================
# 6. INPUT JAWABAN (MODERN CARD UI)
# ==========================================
jawaban = {}
for kode, item in kategori_data.items():
    st.subheader(f"📌 {item['nama']}")
    st.caption(item["desc"])

    for i, soal in enumerate(item["soal"]):
        key = f"{kode}_{i}"
        
        # UI Card untuk Soal
        st.markdown(f"""
        <div class='question-card'>
            <div class='question-text'>{i+1}. {soal}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Input Radio
        jawaban[key] = st.radio(
            f"Label_{key}",
            options=[1, 2, 3, 4, 5],
            horizontal=True,
            key=key,
            label_visibility="collapsed"
        )
    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 7. FUNGSI KLASIFIKASI & PROSES
# ==========================================
def klasifikasi(skor):
    if skor <= 12: return "Rendah"
    elif skor <= 19: return "Sedang"
    else: return "Tinggi"

st.markdown("---")

if st.button("🔍 ANALISIS & DOWNLOAD HASIL"):
    if not nama:
        st.warning("⚠️ Mohon isi Nama Lengkap terlebih dahulu.")
    else:
        hasil_list = []
        for kode, item in kategori_data.items():
            # Menghitung total skor per kategori (5 soal x nilai jawaban)
            skor_kategori = sum([jawaban[f"{kode}_{i}"] for i in range(5)])
            
            hasil_list.append({
                "Nama": nama,
                "Departemen": dept,
                "Faktor": item["nama"],
                "Skor": skor_kategori,
                "Kategori": klasifikasi(skor_kategori)
            })

        df = pd.DataFrame(hasil_list)

        # Output Visual
        st.success(f"Analisis Selesai untuk {nama}")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.bar_chart(df.set_index("Faktor")["Skor"])
        with c2:
            st.write("**Ringkasan Kategori:**")
            st.dataframe(df.set_index("Faktor")[["Kategori"]], use_container_width=True)

        # Alert Prioritas
        st.subheader("⚠️ Fokus Prioritas")
        high_risk = df[df["Kategori"] == "Tinggi"]
        if not high_risk.empty:
            for f in high_risk["Faktor"]:
                st.error(f"Faktor {f} Terdeteksi Risiko Tinggi")
        else:
            st.success("Seluruh faktor berada dalam batas aman.")

        # Fitur Download Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Hasil_Asesmen')
        
        st.download_button(
            label="📥 Download Hasil (Excel)",
            data=output.getvalue(),
            file_name=f"Asesmen_K3_{nama}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
