import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")

# =============================
# Judul & Studi Kasus
# =============================
st.title("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

st.markdown("""
📌 **Masalah:** Jika satu mesin gagal, seluruh lini berhenti.
🎯 **Tujuan:** Menghitung keandalan sistem & mengidentifikasi mesin terlemah untuk fokus perawatan.
""")

# =============================
# Input Data: Slider
# =============================
st.divider()
st.header("🔧 Input Data: Keandalan Mesin (%)")
st.caption("Geser untuk menentukan keandalan setiap mesin (dalam persen).")

col1, col2 = st.columns(2)
with col1:
    r1 = st.slider("Stamping", 80, 100, 98, 1)
    r2 = st.slider("Welding", 80, 100, 99, 1)
with col2:
    r3 = st.slider("Painting", 80, 100, 96, 1)
    r4 = st.slider("Assembly", 80, 100, 97, 1)

# =============================
# Tabel Keandalan Mesin
# =============================
st.divider()
st.subheader("📊 Tabel Keandalan per Mesin")
data = {
    "Mesin": ["Stamping", "Welding", "Painting", "Assembly"],
    "Keandalan (%)": [r1, r2, r3, r4]
}
st.table(data)

# =============================
# Rumus & Penjelasan (Expander)
# =============================
with st.expander("📐 Penjelasan Model & Rumus (klik untuk buka/tutup)"):
    st.markdown("""
    Sistem seri: Semua mesin harus andal. Jika satu gagal, sistem berhenti.
    Rumus keandalan sistem:
    """)
    st.latex(r''' R_s = \prod_{i=1}^{n} R_i ''')
    st.markdown("""
    ➜ **Interpretasi:** Sistem seri sangat sensitif pada mesin dengan keandalan terendah.
    """)

# =============================
# Hitung Keandalan Sistem
# =============================
st.divider()
st.header("✅ Ringkasan Hasil Sistem")
r_values = [r1/100, r2/100, r3/100, r4/100]
Rs = np.prod(r_values)
prob_fail = 1 - Rs

col_res1, col_res2 = st.columns(2)
col_res1.metric(label="📈 Keandalan Sistem", value=f"{Rs:.2%}")
col_res2.metric(label="📉 Probabilitas Kegagalan", value=f"{prob_fail:.2%}")

# =============================
# Detail Perhitungan (Expander)
# =============================
with st.expander("🔢 Detail Perhitungan (klik untuk buka/tutup)"):
    st.markdown("""
    1️⃣ Konversi persen ke desimal:  
    - Stamping = {:.2f}  
    - Welding = {:.2f}  
    - Painting = {:.2f}  
    - Assembly = {:.2f}  
    """.format(*r_values))
    st.markdown("""
    2️⃣ Hitung perkalian semua komponen:
    """)
    st.latex(fr" R_s = {r_values[0]:.2f} \times {r_values[1]:.2f} \times {r_values[2]:.2f} \times {r_values[3]:.2f} = {Rs:.4f} ")
    st.markdown(f"✅ **Keandalan Sistem:** {Rs:.2%}  \n✅ **Probabilitas Kegagalan:** {prob_fail:.2%}")

# =============================
# Analisis Risiko
# =============================
st.divider()
st.subheader("📋 Analisis Risiko & Rekomendasi")

weakest_machine = min(zip(["Stamping", "Welding", "Painting", "Assembly"], r_values), key=lambda x: x[1])
weakest_name, weakest_val = weakest_machine

if prob_fail > 0.10:
    risk_level = "🔴 Risiko Tinggi"
elif prob_fail > 0.05:
    risk_level = "🟠 Risiko Menengah"
else:
    risk_level = "🟢 Risiko Rendah"

st.markdown(f"""
✅ **Mata Rantai Terlemah:** {weakest_name} ({weakest_val:.0%})  
✅ **Kategori Risiko:** {risk_level} ({prob_fail:.2%})
""")

st.markdown("""
**🛠️ Rekomendasi Strategi Perbaikan:**
- Fokus perawatan pada mesin dengan keandalan terendah.
- Terapkan preventive maintenance intensif.
- Standarkan SOP pada tahap kritis.
- Pasang condition monitoring (sensor/pemantauan).
- Lakukan evaluasi periodik untuk verifikasi peningkatan.
""")

# =============================
# Visualisasi Grafik
# =============================
st.divider()
st.subheader("📊 Visualisasi Keandalan Komponen dan Sistem")

labels = ["Stamping", "Welding", "Painting", "Assembly", "SISTEM TOTAL"]
values = r_values + [Rs]

fig, ax = plt.subplots(figsize=(10, 5))
colors = ['#87CEEB'] * 4
colors[["Stamping", "Welding", "Painting", "Assembly"].index(weakest_name)] = '#FF6347'
colors.append('#9370DB')

bars = ax.bar(labels, values, color=colors)
ax.set_ylabel('Keandalan (%)')
ax.set_title('Perbandingan Keandalan Mesin dan Sistem')
ax.set_ylim(0.75, 1.01)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2%}', ha='center', va='bottom', fontsize=10)

st.pyplot(fig)

with st.expander("ℹ️ Penjelasan Grafik (klik untuk buka/tutup)"):
    st.markdown("""
    - **Bar biru:** Komponen normal.
    - **Bar merah:** Mesin dengan keandalan terendah.
    - **Bar ungu:** Keandalan sistem total.
    - Sistem seri berhenti jika satu mesin gagal ➜ mesin terlemah sangat menentukan.
    """)

# =============================
# Footer
# =============================
st.divider()
st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")
