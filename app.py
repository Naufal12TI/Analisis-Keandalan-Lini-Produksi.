import streamlit as st
import numpy as np
import pandas as pd

# CONFIG HALAMAN
st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")

# HEADER UTAMA
st.title("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

# --- 1. PENDAHULUAN
st.markdown("""
📌 **Masalah yang Dianalisis**

Pada lini perakitan otomotif yang terdiri dari beberapa mesin saling bergantung (sistem seri), kegagalan satu mesin menyebabkan berhentinya seluruh lini produksi.

**🎯 Tujuan Analisis**
- Menghitung keandalan total sistem produksi.
- Mengidentifikasi *mata rantai terlemah*.
- Memberikan rekomendasi perbaikan berbasis hasil analisis.
""")

st.divider()

# --- 2. PENJELASAN MODEL
with st.expander("📐 Konsep Model Matematis"):
    st.markdown("""
    Dalam sistem seri, keandalan sistem dihitung sebagai perkalian keandalan tiap komponen. Jika satu mesin gagal, seluruh sistem berhenti.

    **Rumus:**
    """)
    st.latex(r"R_s = \prod_{i=1}^{n} R_i")
    st.markdown("""
    Sistem seri sangat sensitif pada komponen dengan keandalan terendah. Identifikasi *mata rantai terlemah* menjadi kunci strategi perawatan.
    """)

st.divider()

# --- 3. INPUT USER
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

# --- 4. PERHITUNGAN KEANDALAN
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

# --- 5. TABEL KEANDALAN PER MESIN
st.subheader("📊 Tabel Keandalan per Mesin")
df = pd.DataFrame({
    "Mesin": list(reliabilities.keys()),
    "Keandalan (%)": list(reliabilities.values())
})
st.table(df.style.format({"Keandalan (%)": "{:.0f}"}))

st.divider()

# --- 6. RINGKASAN HASIL SISTEM
st.subheader("✅ Ringkasan Hasil Sistem")
col_total, col_fail = st.columns(2)
with col_total:
    st.metric(label="Keandalan Sistem", value=f"{Rs*100:.2f}%")
with col_fail:
    st.metric(label="Probabilitas Kegagalan", value=f"{fail_prob*100:.2f}%")

with st.expander("🔢 Detail Perhitungan"):
    st.markdown("""
    **Langkah-langkah Perhitungan:**
    1️⃣ Konversi persen ke desimal.  
    2️⃣ Hitung perkalian semua komponen.
    """)
    st.latex(
        rf"R_s = {ri_values[0]:.2f} \times {ri_values[1]:.2f} \times {ri_values[2]:.2f} \times {ri_values[3]:.2f} = {Rs:.4f}"
    )
    st.markdown(f"**Probabilitas Kegagalan:** 1 - R_s = {fail_prob:.4f}")

st.divider()

# --- 7. INTERPRETASI BISNIS
st.subheader("💡 Interpretasi dan Wawasan")
st.markdown(f"""
✅ **Mata Rantai Terlemah:** Mesin **{weakest_link}** memiliki keandalan terendah (**{reliabilities[weakest_link]}%**).

Karena sistem seri akan berhenti jika satu mesin gagal, *peningkatan keandalan pada tahap ini memberikan dampak terbesar* terhadap keandalan keseluruhan sistem.
""")

st.divider()

# --- 8. ANALISIS RISIKO
st.subheader("📋 Analisis Risiko")
if fail_prob > 0.10:
    st.error(f"**Kategori: Risiko Tinggi ({fail_prob*100:.2f}%)** - Perlunya intervensi segera untuk mencegah kerugian signifikan.")
elif fail_prob > 0.05:
    st.warning(f"**Kategori: Risiko Menengah ({fail_prob*100:.2f}%)** - Evaluasi ulang komponen kritis sangat disarankan.")
else:
    st.success(f"**Kategori: Risiko Rendah ({fail_prob*100:.2f}%)** - Sistem relatif stabil, namun pemeliharaan rutin tetap penting.")

st.divider()

# --- 9. REKOMENDASI
st.subheader("🛠️ Rekomendasi Strategi Perbaikan")
st.markdown(f"""
- Fokuskan program perawatan preventif pada mesin **{weakest_link}**.
- Standarkan SOP untuk proses **{weakest_link}**.
- Terapkan sistem pemantauan kondisi (*Condition Monitoring*).
- Pertimbangkan pelatihan operator untuk mengurangi human error.
- Lakukan evaluasi periodik untuk memverifikasi peningkatan keandalan.
""")

# FOOTER
st.caption("📌 Dikembangkan oleh Naufal Khoirul Ibrahim - Matematika Terapan")
