import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")

# =================================
# Judul & Pengantar
# =================================
st.title("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

st.markdown("""
📌 **Masalah yang Dianalisis**  
Lini perakitan dengan mesin-mesin saling bergantung (sistem seri). Jika satu mesin gagal, seluruh lini berhenti.  
🎯 **Tujuan:**  
- Menghitung keandalan total sistem.  
- Mengidentifikasi mata rantai terlemah.  
- Memberikan rekomendasi perbaikan berbasis hasil analisis.  
""")

st.divider()

# =================================
# INPUT + TABEL -> Dua Kolom
# =================================
col_input, col_table = st.columns(2)

with col_input:
    st.subheader("🔧 Input Data: Keandalan Mesin (%)")
    st.caption("Geser untuk mengatur keandalan mesin (dalam persen).")
    r1 = st.slider("Stamping", 80, 100, 98)
    r2 = st.slider("Welding", 80, 100, 99)
    r3 = st.slider("Painting", 80, 100, 96)
    r4 = st.slider("Assembly", 80, 100, 97)

with col_table:
    st.subheader("📊 Tabel Keandalan per Mesin")
    data = {
        "Mesin": ["Stamping", "Welding", "Painting", "Assembly"],
        "Keandalan (%)": [r1, r2, r3, r4]
    }
    st.table(data)

# =================================
# HASIL SISTEM + RISIKO -> Dua Kolom
# =================================
r_values = [r1/100, r2/100, r3/100, r4/100]
Rs = np.prod(r_values)
prob_fail = 1 - Rs

weakest_machine = min(zip(["Stamping", "Welding", "Painting", "Assembly"], r_values), key=lambda x: x[1])
weakest_name, weakest_val = weakest_machine

col_result, col_risk = st.columns(2)

with col_result:
    st.subheader("✅ Ringkasan Hasil Sistem")
    st.metric(label="📈 Keandalan Sistem", value=f"{Rs:.2%}")
    st.metric(label="📉 Probabilitas Kegagalan", value=f"{prob_fail:.2%}")
    st.caption("Keandalan sistem dihitung dengan mengalikan semua komponen. Sistem seri berhenti jika satu mesin gagal.")

with col_risk:
    st.subheader("📋 Analisis Risiko & Rekomendasi")
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
    **🛠️ Rekomendasi:**
    - Fokus perawatan pada mesin terlemah.
    - Terapkan preventive maintenance.
    - Standarkan SOP pada tahap kritis.
    - Condition monitoring (sensor).
    - Evaluasi periodik.
    """)

# =================================
# Detail Perhitungan (Expander)
# =================================
with st.expander("🔢 Detail Perhitungan (klik untuk buka/tutup)"):
    st.markdown("""
    ✅ Rumus Sistem Seri:
    """)
    st.latex(r''' R_s = \prod_{i=1}^{n} R_i ''')
    st.markdown(f"""
    - Stamping = {r_values[0]:.2f}  
    - Welding = {r_values[1]:.2f}  
    - Painting = {r_values[2]:.2f}  
    - Assembly = {r_values[3]:.2f}  
    """)
    st.latex(fr" R_s = {r_values[0]:.2f} \times {r_values[1]:.2f} \times {r_values[2]:.2f} \times {r_values[3]:.2f} = {Rs:.4f} ")
    st.markdown(f"✅ **Keandalan Sistem:** {Rs:.2%}  \n✅ **Probabilitas Kegagalan:** {prob_fail:.2%}")

# =================================
# Visualisasi Grafik
# =================================
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

# =================================
# Footer
# =================================
st.divider()
st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")
