import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")

# ------------------------ Judul & Tujuan ------------------------
st.header("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

st.markdown("""
📌 **Masalah yang Dianalisis**  
Lini perakitan dengan mesin-mesin yang saling bergantung secara seri. Jika satu mesin gagal, seluruh lini berhenti.

🎯 **Tujuan Analisis**  
- Menghitung keandalan total sistem  
- Mengidentifikasi mata rantai terlemah  
- Memberikan rekomendasi perbaikan berbasis hasil analisis
""")

# ------------------------ Input Data ------------------------
st.divider()
st.subheader("🔧 Input Data: Keandalan per Mesin (%)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    r1 = st.slider("Stamping", 80, 100, 98)
with col2:
    r2 = st.slider("Welding", 80, 100, 99)
with col3:
    r3 = st.slider("Painting", 80, 100, 96)
with col4:
    r4 = st.slider("Assembly", 80, 100, 97)

# Konversi ke desimal
r_values = [r1, r2, r3, r4]
r_decimal = [r/100 for r in r_values]
komponen = ["Stamping", "Welding", "Painting", "Assembly"]

# ------------------------ Tabel Input ------------------------
df = pd.DataFrame({
    "Mesin": komponen,
    "Keandalan (%)": r_values
})
st.markdown("✅ **Tabel Keandalan per Mesin**")
st.table(df)

# ------------------------ Perhitungan ------------------------
st.divider()
st.subheader("📐 Konsep Model Matematis & Perhitungan")

with st.expander("🔢 Detail Perhitungan"):
    st.latex(r"R_s = \prod_{i=1}^{n} R_i")
    st.markdown("- Sistem seri sangat sensitif pada komponen terlemah.")
    st.markdown("1️⃣ Konversi persen ke desimal")
    st.markdown("2️⃣ Kalikan semua komponen")

    keandalan_sistem = np.prod(r_decimal)
    st.latex(fr"R_s = {r_decimal[0]:.2f} \times {r_decimal[1]:.2f} \times {r_decimal[2]:.2f} \times {r_decimal[3]:.2f} = {keandalan_sistem:.4f}")
    st.markdown(f"**Keandalan Sistem ($R_s$):** {keandalan_sistem:.2%}")
    st.markdown(f"**Probabilitas Kegagalan:** {1 - keandalan_sistem:.2%}")

# Cari komponen terlemah
weakest_idx = np.argmin(r_decimal)
weakest_name = komponen[weakest_idx]
weakest_value = r_values[weakest_idx]

# ------------------------ Grafik Sampingan ------------------------
st.divider()
st.subheader("📊 Visualisasi Keandalan Komponen dan Sistem")

col_grafik1, col_grafik2 = st.columns(2)

with col_grafik1:
    st.markdown("**🔹 Keandalan Mesin Individu**")
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    bar_colors = ['#87CEEB'] * 4
    bar_colors[weakest_idx] = '#FF6347'
    ax1.bar(komponen, r_decimal, color=bar_colors)
    ax1.set_ylim(0.75, 1.01)
    ax1.set_ylabel('Keandalan (%)')
    ax1.set_title('Komponen Individu')
    for i, v in enumerate(r_decimal):
        ax1.text(i, v + 0.005, f"{v:.2%}", ha='center')
    st.pyplot(fig1)
    st.caption(f"✅ Bar merah = mesin terlemah yaitu **{weakest_name} ({weakest_value}%)**.")

with col_grafik2:
    st.markdown("**🔹 Keandalan Sistem Total**")
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.bar(["Sistem Total"], [keandalan_sistem], color='#9370DB')
    ax2.set_ylim(0.75, 1.01)
    ax2.set_ylabel('Keandalan (%)')
    ax2.set_title('Sistem Total')
    ax2.text(0, keandalan_sistem + 0.005, f"{keandalan_sistem:.2%}", ha='center')
    st.pyplot(fig2)
    st.caption("✅ Sistem total = hasil kombinasi semua mesin dalam model seri.")

# ------------------------ Risiko ------------------------
st.divider()
st.subheader("📋 Analisis Risiko & Rekomendasi")

prob_fail = 1 - keandalan_sistem
if prob_fail > 0.10:
    kategori = "🔴 Risiko Tinggi"
elif prob_fail > 0.05:
    kategori = "🟠 Risiko Menengah"
else:
    kategori = "🟢 Risiko Rendah"

st.markdown(f"**Kategori Risiko:** {kategori}")
st.metric(label="Probabilitas Kegagalan", value=f"{prob_fail:.2%}")

st.subheader("🛠️ Rekomendasi Strategi Perbaikan")
st.markdown(f"""
- Fokus perawatan pada **{weakest_name}** (keandalan terendah).  
- Terapkan **preventive maintenance** intensif  
- Standarkan SOP pada tahap {weakest_name}  
- Pasang **condition monitoring** (sensor/pemantauan)  
- Lakukan **evaluasi periodik** untuk verifikasi peningkatan  
""")

st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")
