import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")

# ==========================
# Judul & Pengantar Awal
# ==========================
st.title("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

st.markdown("""
📌 **Masalah yang Dianalisis**  
Lini perakitan dengan mesin-mesin saling bergantung (sistem seri). Jika satu mesin gagal, seluruh lini berhenti.  

🎯 **Tujuan:**  
1. Menghitung keandalan total sistem.  
2. Mengidentifikasi mata rantai terlemah.  
3. Memberikan rekomendasi perbaikan.
""")

st.divider()

# ==========================
# SLIDER (kiri) + TABEL (kanan) dalam kolom
# ==========================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("1️⃣ Input Keandalan Mesin")
    st.caption("Atur nilai keandalan tiap mesin dalam persen:")
    with st.container(border=True):
        r1 = st.slider("Stamping", 80, 100, 98)
        r2 = st.slider("Welding", 80, 100, 99)
        r3 = st.slider("Painting", 80, 100, 96)
        r4 = st.slider("Assembly", 80, 100, 97)

with col2:
    with st.expander("📊 Tabel Keandalan Mesin"):
        st.subheader("2️⃣ Ringkasan Input")
        st.table({
            "Mesin": ["Stamping", "Welding", "Painting", "Assembly"],
            "Keandalan (%)": [r1, r2, r3, r4]
        })

# ==========================
# PERHITUNGAN MODEL
# ==========================
r_vals = [r1/100, r2/100, r3/100, r4/100]
Rs = np.prod(r_vals)
P_fail = 1 - Rs
weakest_name, weakest_val = min(zip(["Stamping", "Welding", "Painting", "Assembly"], r_vals), key=lambda x: x[1])

# ==========================
# HASIL SISTEM + RISIKO
# ==========================
st.divider()
col3, col4 = st.columns(2)

with col3:
    st.subheader("3️⃣ Hasil Perhitungan")
    st.metric(label="Keandalan Sistem", value=f"{Rs:.2%}")
    st.metric(label="Probabilitas Kegagalan", value=f"{P_fail:.2%}")
    st.caption("Hasil ini diperoleh dari perkalian keandalan seluruh mesin.")

with col4:
    st.subheader("4️⃣ Analisis Risiko & Rekomendasi")
    kategori = "🟠 Risiko Menengah" if P_fail > 0.05 else "🟢 Risiko Rendah"
    st.markdown(f"""
    ✅ **Mata Rantai Terlemah:** {weakest_name} ({weakest_val:.0%})  
    ✅ **Kategori Risiko:** {kategori} ({P_fail:.2%})
    """)
    st.markdown("""
    **Saran Perbaikan:**
    - Fokuskan perawatan pada mesin **Painting**.
    - Terapkan maintenance preventif & sensor.
    - Standardisasi SOP dan pelatihan operator.
    """)

# ==========================
# EXPANDER DETAIL PERHITUNGAN
# ==========================
with st.expander("🔍 Penjelasan Detail Perhitungan"):
    st.markdown("""
    - Model: Sistem Seri ➜ semua mesin harus berfungsi.
    - Rumus:  
    """)
    st.latex(r"R_s = \prod_{i=1}^{n} R_i")
    st.markdown(f"""
    Substitusi nilai:  
    R_s = {r_vals[0]:.2f} × {r_vals[1]:.2f} × {r_vals[2]:.2f} × {r_vals[3]:.2f} = {Rs:.4f}  
    Probabilitas kegagalan = 1 - R_s = {P_fail:.4f}
    """)

# ==========================
# GRAFIK & PENJELASAN
# ==========================
st.divider()
st.subheader("5️⃣ Visualisasi Komponen & Sistem")

labels = ["Stamping", "Welding", "Painting", "Assembly", "SISTEM"]
values = r_vals + [Rs]
colors = ['#87CEEB'] * 4
colors[["Stamping", "Welding", "Painting", "Assembly"].index(weakest_name)] = '#FF6347'
colors.append('#9370DB')

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(labels, values, color=colors)
ax.set_ylim(0.75, 1.01)
ax.set_ylabel("Tingkat Keandalan")
ax.set_title("Perbandingan Keandalan Mesin dan Sistem")
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{bar.get_height():.2%}", ha='center', va='bottom')
st.pyplot(fig)

with st.expander("📘 Penjelasan Grafik"):
    st.markdown("""
    - Bar merah: komponen terlemah.
    - Bar ungu: total keandalan sistem.
    - Sistem seri sangat sensitif terhadap 1 titik lemah.
    """)

# ==========================
# FOOTER
# ==========================
st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")
