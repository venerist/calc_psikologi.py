import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="PsychScore Calc", page_icon="🧠")

st.title("🧠 Kalkulator Skor Kepuasan Kerja")
st.write("Alat sederhana untuk mengukur tingkat kepuasan kerja berdasarkan indikator psikologi.")
st.markdown("---")

# Daftar Pertanyaan
pertanyaan = [
    "Saya merasa dihargai oleh atasan dan rekan kerja.",
    "Fasilitas di tempat kerja mendukung produktivitas saya.",
    "Saya memiliki keseimbangan antara pekerjaan dan kehidupan pribadi (Work-Life Balance).",
    "Kompensasi/Gaji yang saya terima sesuai dengan beban kerja.",
    "Saya melihat adanya peluang pengembangan karier di masa depan."
]

# Input User
skor_total = 0
st.subheader("Silahkan isi penilaian Anda:")
st.info("Skala 1 (Sangat Tidak Setuju) sampai 5 (Sangat Setuju)")

for i, p in enumerate(pertanyaan):
    jawaban = st.select_slider(f"{p}", options=[1, 2, 3, 4, 5], key=f"q{i}")
    skor_total += jawaban

st.markdown("---")

# Logika Tombol Hitung
if st.button("Lihat Hasil Interpretasi"):
    st.subheader(f"Total Skor Anda: {skor_total}")
    
    # Ambang batas skor (Total pertanyaan 5, max skor 25)
    if skor_total >= 21:
        st.success("### Kategori: SANGAT TINGGI\nAnda merasa sangat puas dan memiliki keterikatan (engagement) yang luar biasa dengan pekerjaan saat ini.")
    elif skor_total >= 16:
        st.info("### Kategori: TINGGI\nAnda merasa puas secara umum, namun mungkin ada detail kecil yang masih bisa ditingkatkan.")
    elif skor_total >= 11:
        st.warning("### Kategori: SEDANG\nKepuasan Anda berada di level rata-rata. Perlu diidentifikasi faktor apa yang membuat Anda merasa kurang maksimal.")
    else:
        st.error("### Kategori: RENDAH\nSkor ini menunjukkan adanya ketidakpuasan yang signifikan. Disarankan untuk berdiskusi dengan HR atau meninjau kembali lingkungan kerja Anda.")

st.caption("Dibuat untuk keperluan portofolio Analisis HR & Psikologi.")
