import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")

# Judul utama
st.title("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

# 1. Pendahuluan
st.markdown("""
**📌 Masalah yang Dianalisis:**
Pada lini perakitan otomotif yang terdiri dari beberapa mesin saling bergantung (*sistem seri*), kegagalan satu mesin menyebabkan berhentinya seluruh lini produksi.

**🎯 Tujuan Analisis:**
- Menghitung keandalan total sistem.
- Mengidentifikasi *mata rantai terlemah*.
- Memberikan rekomendasi perbaikan berbasis hasil perhitungan.
""")

st.divider()

# 2. Penjelasan Model
with st.expander("📐 Konsep Model dan Rumus"):
    st.markdown("""
    **Model Sistem Seri:**
    - Sistem seri berhenti jika satu mesin gagal.
    - Keandalan sistem = hasil perkalian keandalan semua komponen.

    **Rumus Umum:**
    """)
    st.latex(r"R_s = \prod_{i=1}^{n} R_i")
    st.markdown("""
    Sistem seri bergantung pada *mata rantai terlemah*. Dengan memahami ini, kita bisa menentukan strategi perawatan yang paling berdampak.
    """)

st.divider()

# 3. Input Keandalan Mesin
st.subheader("🔧 Input Data: Keandalan per Mesin (%)")
st.caption("Gunakan slider untuk menyesuaikan tingkat keandalan mesin (dalam persen).")

col1, col2, col3, col4 = st.columns(4)
with col1:
    r1 = st.slider("Stamping", 80, 100, 98, 1)
with col2:
    r2 = st.slider("Welding", 80, 100, 99, 1)
with col3:
    r3 = st.slider("Painting", 80, 100, 96, 1)
with col4:
    r4 = st.slider("Assembly", 80, 100, 97, 1)

# 4. Hitung Keandalan Sistem
ri_values = [r1/100, r2/100, r3/100, r4/100]
Rs = np.prod(ri_values)
fail_prob = 1 - Rs
reliabilities = {
    "Stamping": r1,
    "Welding": r2,
    "Painting": r3,
    "Assembly": r4
}
weakest_link = min(reliabilities, key=reliabilities.get)

# 5. Tabel Keandalan Mesin (tanpa sistem total!)
st.subheader("📊 Tabel Keandalan per Mesin")
df = pd.DataFrame({
    "Komponen": list(reliabilities.keys()),
    "Keandalan (%)": list(reliabilities.values())
})
st.table(df)

# 6. Ringkasan Hasil Sistem
st.subheader("✅ Ringkasan Hasil Sistem")
col_total, col_fail = st.columns(2)
with col_total:
    st.metric(label="Keandalan Sistem", value=f"{Rs*100:.2f}%")
with col_fail:
    st.metric(label="Probabilitas Kegagalan", value=f"{fail_prob*100:.2f}%")

with st.expander("🔢 Detail Perhitungan"):
    st.markdown("""
    **Langkah-langkah:**
    1. Ubah persen ke desimal.
    2. Hitung: 
    """)
    st.latex(
        rf"R_s = {ri_values[0]:.2f} \times {ri_values[1]:.2f} \times {ri_values[2]:.2f} \times {ri_values[3]:.2f} = {Rs:.4f}"
    )
    st.markdown(f"**Probabilitas Kegagalan:** 1 - R_s = {fail_prob:.4f}")

st.divider()

# 7. Interpretasi Bisnis
st.subheader("💡 Interpretasi dan Wawasan Bisnis")
st.markdown(f"""
**Mata Rantai Terlemah:** Mesin **{weakest_link}** memiliki keandalan terendah (**{reliabilities[weakest_link]}%**).

Karena sistem seri berhenti total jika satu mesin gagal, peningkatan keandalan pada tahap ini memberikan dampak paling besar terhadap keandalan keseluruhan.
""")

# 8. Analisis Risiko
st.subheader("📋 Analisis Risiko")
if fail_prob > 0.10:
    st.error(f"**Kategori: Risiko Tinggi ({fail_prob*100:.2f}%)**")
    st.markdown("- Disarankan intervensi segera.")
elif fail_prob > 0.05:
    st.warning(f"**Kategori: Risiko Menengah ({fail_prob*100:.2f}%)**")
    st.markdown("- Evaluasi ulang komponen kritis sangat disarankan.")
else:
    st.success(f"**Kategori: Risiko Rendah ({fail_prob*100:.2f}%)**")
    st.markdown("- Sistem relatif stabil, teruskan pemeliharaan rutin.")

# 9. Rekomendasi Strategi
st.subheader("🛠️ Rekomendasi Strategi Perbaikan")
st.markdown(f"""
- Fokuskan perawatan preventif intensif pada mesin **{weakest_link}**.
- Standardisasi SOP untuk proses **{weakest_link}**.
- Terapkan sistem pemantauan kondisi (Condition Monitoring).
- Lakukan evaluasi periodik untuk mengukur peningkatan keandalan.
""")

st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim - Matematika Terapan")
