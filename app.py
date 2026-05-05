import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# 1. KONFIGURASI & THEME
# ==========================================
st.set_page_config(
    page_title="HSE Psych Assessment",
    page_icon="📋",
    layout="centered"
)

# Kustom CSS untuk memperbaiki UI yang membosankan
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .block-container { max-width: 900px; padding-top: 2rem; }
    
    /* Judul & Subtitle */
    .main-title { color: #1e293b; font-weight: 800; font-size: 2.5rem; margin-bottom: 0.5rem; }
    .sub-title { color: #64748b; font-size: 1.1rem; margin-bottom: 2rem; }
    
    /* Kartu Soal */
    .question-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #10b981; /* Hijau HSE */
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 15px;
    }
    .question-text { color: #334155; font-weight: 500; font-size: 16px; margin-bottom: 10px; }
    
    /* Sidebar info */
    section[data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    
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
# 2. SIDEBAR & DATA STRUKTUR
# ==========================================
with st.sidebar:
    st.markdown("# 🛡️ K3 Lingkungan Kerja")
    st.write("Sesuai Permenaker No. 5/2018")
    st.markdown("---")
    st.markdown("### 📊 Skala Penilaian")
    st.info("1: Tidak Pernah\n\n2: Jarang\n\n3: Kadang-kadang\n\n4: Sering\n\n5: Sangat Sering")

kategori_data = {
    "TP": {"nama": "Ketidakpastian Peran", "desc": "Ketidakjelasan tanggung jawab.", "soal": ["Saya tidak mendapatkan penjelasan jelas mengenai tugas.", "Saya bingung menentukan prioritas.", "Saya tidak memahami ekspektasi atasan.", "Instruksi kerja sering tidak jelas.", "Peran saya tidak terdefinisi."]},
    "KP": {"nama": "Konflik Peran", "desc": "Tuntutan pekerjaan bertentangan.", "soal": ["Saya menerima perintah yang bertentangan.", "Saya diminta melakukan pekerjaan di luar tugas.", "Saya mengalami konflik antar atasan.", "Tuntutan pekerjaan saling bertabrakan.", "Ekspektasi dari berbagai pihak berbeda."]},
    "BBKuan": {"nama": "Beban Kuantitatif", "desc": "Volume kerja melebihi waktu.", "soal": ["Pekerjaan saya terlalu banyak.", "Saya harus bekerja sangat cepat.", "Waktu kerja tidak cukup.", "Deadline sangat ketat.", "Saya sering lembur."]},
    "BBKual": {"nama": "Beban Kualitatif", "desc": "Tingkat kesulitan tinggi.", "soal": ["Pekerjaan saya sulit.", "Saya butuh skill tambahan.", "Saya merasa tidak mampu menyelesaikan tugas.", "Pekerjaan butuh konsentrasi tinggi.", "Saya merasa tekanan mental tinggi."]},
    "PK": {"nama": "Pengembangan Karir", "desc": "Peluang pengembangan diri.", "soal": ["Tidak ada peluang karir.", "Promosi tidak jelas.", "Karir stagnan.", "Kurang dukungan pengembangan.", "Jarang pelatihan."]},
    "TJO": {"nama": "Tanggung Jawab Orang Lain", "desc": "Beban mengawasi tim.", "soal": ["Saya bertanggung jawab atas orang lain.", "Kesalahan orang lain berdampak ke saya.", "Saya mengawasi banyak orang.", "Saya terbebani oleh tim.", "Saya harus memastikan pekerjaan orang lain."]}
}

# ==========================================
# 3. HEADER & IDENTITAS
# ==========================================
st.markdown("<div class='main-title'>Kuesioner Stres Kerja</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Identifikasi Faktor Psikologi Berdasarkan Regulasi K3</div>", unsafe_allow_html=True)

with st.expander("👤 Data Karyawan", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap")
    with col2:
        dept = st.selectbox("Departemen", ["HRGA", "Finance", "IT", "Produksi", "Maintenance"])

st.markdown("---")

# ==========================================
# 4. INPUT JAWABAN (KARTU UI)
# ==========================================
jawaban = {}
for kode, item in kategori_data.items():
    st.subheader(f"📌 {item['nama']}")
    st.caption(item["desc"])

    for i, soal in enumerate(item["soal"]):
        key = f"{kode}_{i}"
        # Styling kartu soal
        st.markdown(f"""
        <div class='question-card'>
            <div class='question-text'>{i+1}. {soal}</div>
        </div>
        """, unsafe_allow_html=True)
        
        jawaban[key] = st.radio(
            f"Skala penilaian untuk: {soal}", # Hidden by label_visibility
            options=[1, 2, 3, 4, 5],
            horizontal=True,
            key=key,
            label_visibility="collapsed"
        )
    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5. LOGIKA & OUTPUT
# ==========================================
def klasifikasi(skor):
    if skor <= 12: return "Rendah"
    elif skor <= 19: return "Sedang"
    else: return "Tinggi"

if st.button("🔍 ANALISIS & DOWNLOAD HASIL"):
    if not nama:
        st.warning("Silahkan isi nama terlebih dahulu.")
    else:
        hasil = []
        for kode, item in kategori_data.items():
            skor = sum([jawaban[f"{kode}_{i}"] for i in range(5)])
            hasil.append({
                "Faktor": item["nama"],
                "Skor": skor,
                "Kategori": klasifikasi(skor)
            })

        df = pd.DataFrame(hasil)

        # Layout Hasil
        st.success(f"Analisis Selesai untuk {nama} (Dept: {dept})")
        
        col_res1, col_res2 = st.columns([2, 1])
        with col_res1:
            st.bar_chart(df.set_index("Faktor")["Skor"])
        with col_res2:
            st.dataframe(df.set_index("Faktor")[["Kategori"]])

        # Prioritas Masalah
        high_risk = df[df["Kategori"] == "Tinggi"]
        if not high_risk.empty:
            st.error("### ⚠️ PRIORITAS TINDAK LANJUT")
            for f in high_risk["Faktor"]:
                st.write(f"- {f}")
        else:
            st.success("✅ Semua faktor dalam batas aman.")

        # Download Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Hasil')
        
        st.download_button(
            label="📥 Download Laporan Excel",
            data=output.getvalue(),
            file_name=f"Hasil_K3_{nama}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
