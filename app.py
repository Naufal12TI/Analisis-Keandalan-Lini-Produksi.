import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# CONFIG HALAMAN
st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")

# HEADER UTAMA
st.title("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

# --- 1. PENDAHULUAN
st.markdown("""
📌 **Masalah yang Dianalisis**
- Dalam lini perakitan otomotif, setiap mesin saling bergantung dalam susunan *sistem seri*.
- Kegagalan satu mesin saja dapat menghentikan seluruh proses produksi.

🎯 **Tujuan Analisis**
- Menghitung keandalan total sistem produksi.
- Mengidentifikasi *mata rantai terlemah*.
- Menyediakan dasar pengambilan keputusan perawatan berbasis data.
""")

st.divider()

# --- 2. PENJELASAN MODEL
with st.expander("📐 Konsep Model Matematis"):
    st.markdown("""
    Pada sistem seri, keandalan sistem dihitung sebagai hasil perkalian keandalan tiap komponen. 
    Jika satu komponen gagal, sistem gagal total.

    **Rumus umum sistem seri:**
    """)
    st.latex(r"R_s = \prod_{i=1}^{n} R_i")

    st.markdown("""
    Sistem ini sangat dipengaruhi oleh *komponen dengan keandalan terendah*. 
    Strategi pemeliharaan sebaiknya memprioritaskan komponen tersebut.

    📌 *Sumber teori: Reliability Engineering Handbook (Modarres et al.)*
    """)

st.divider()

# --- 3. INPUT DATA
st.subheader("🔧 Input Data: Keandalan per Mesin (%)")
st.caption("Silakan sesuaikan tingkat keandalan tiap mesin (dalam persen).")

col1, col2, col3, col4 = st.columns(4)
with col1:
    r1 = st.slider("Stamping", 80, 100, 98, 1)
with col2:
    r2 = st.slider("Welding", 80, 100, 99, 1)
with col3:
    r3 = st.slider("Painting", 80, 100, 96, 1)
with col4:
    r4 = st.slider("Assembly", 80, 100, 97, 1)

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

st.divider()

# --- 4. TABEL KEANDALAN PER MESIN
st.subheader("📊 Tabel Keandalan per Mesin")
df = pd.DataFrame({
    "Mesin": list(reliabilities.keys()),
    "Keandalan (%)": list(reliabilities.values())
})
st.table(df.style.format({"Keandalan (%)": "{:.0f}"}))

st.caption("📌 Tabel di atas menunjukkan keandalan masing-masing mesin secara individu.")

st.divider()

# --- 5. HASIL SISTEM
st.subheader("✅ Ringkasan Hasil Sistem")
col_total, col_fail = st.columns(2)
with col_total:
    st.metric(label="Keandalan Sistem", value=f"{Rs*100:.2f}%")
with col_fail:
    st.metric(label="Probabilitas Kegagalan", value=f"{fail_prob*100:.2f}%")

with st.expander("🔢 Detail Langkah Perhitungan"):
    st.markdown("""
    **Langkah-langkah:**
    1️⃣ Konversi persen ke desimal.
    2️⃣ Kalikan semua nilai keandalan.
    """)
    st.latex(
        rf"R_s = {ri_values[0]:.2f} \times {ri_values[1]:.2f} \times {ri_values[2]:.2f} \times {ri_values[3]:.2f} = {Rs:.4f}"
    )
    st.markdown(f"**Probabilitas Kegagalan:** 1 - R_s = {fail_prob:.4f}")

st.divider()

# --- 6. VISUALISASI GRAFIK
st.subheader("📈 Visualisasi Keandalan Komponen dan Sistem")
labels = list(reliabilities.keys()) + ["Sistem Total"]
values = list(ri_values) + [Rs]

colors = ['#3498db'] * len(ri_values)
weakest_idx = list(reliabilities.keys()).index(weakest_link)
colors[weakest_idx] = '#e74c3c'
colors.append('#9b59b6')

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(labels, values, color=colors)
ax.set_ylim(0.75, 1.01)
ax.set_ylabel('Keandalan (0-1)')
ax.set_title('Perbandingan Keandalan Komponen dan Sistem', fontsize=14)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2%}', ha='center', va='bottom', fontsize=10)

st.pyplot(fig)

with st.expander("🔎 Penjelasan Visualisasi"):
    st.markdown(f"""
    - **Bar Biru:** Komponen normal
    - **Bar Merah:** Mata rantai terlemah (**{weakest_link}**)
    - **Bar Ungu:** Keandalan sistem total

    Visualisasi membantu menunjukkan bagaimana keandalan sistem selalu lebih rendah daripada komponen terlemah.
    """)

st.divider()

# --- 7. INTERPRETASI BISNIS
st.subheader("💡 Interpretasi dan Wawasan")
st.markdown(f"""
✅ **Mata Rantai Terlemah:** Mesin **{weakest_link}** memiliki keandalan terendah (**{reliabilities[weakest_link]}%**).

📌 Karena sistem seri berhenti total jika satu mesin gagal, *peningkatan keandalan pada tahap ini akan memberikan dampak paling signifikan* pada keandalan keseluruhan sistem produksi.
""")

st.divider()

# --- 8. ANALISIS RISIKO
st.subheader("📋 Analisis Risiko")
if fail_prob > 0.10:
    st.error(f"**Kategori: Risiko Tinggi ({fail_prob*100:.2f}%)** - Diperlukan intervensi segera untuk mencegah potensi kerugian signifikan.")
elif fail_prob > 0.05:
    st.warning(f"**Kategori: Risiko Menengah ({fail_prob*100:.2f}%)** - Disarankan evaluasi ulang pada komponen kritis.")
else:
    st.success(f"**Kategori: Risiko Rendah ({fail_prob*100:.2f}%)** - Sistem relatif stabil, pemeliharaan rutin tetap diperlukan.")

st.divider()

# --- 9. REKOMENDASI
st.subheader("🛠️ Rekomendasi Strategi Perbaikan")
st.markdown(f"""
- Prioritaskan perawatan preventif pada mesin **{weakest_link}**.
- Standardisasi prosedur operasi untuk tahap **{weakest_link}**.
- Terapkan sistem pemantauan kondisi (*Condition Monitoring*).
- Pertimbangkan pelatihan operator untuk mengurangi human error.
- Jadwalkan evaluasi berkala untuk memverifikasi peningkatan keandalan.
""")

st.divider()

# --- 10. PENUTUP
st.subheader("✅ Saran Implementasi")
st.markdown("""
Analisis ini diharapkan menjadi acuan pengambilan keputusan strategis dalam perencanaan pemeliharaan lini produksi. 
Dengan fokus pada komponen kritis, perusahaan dapat meningkatkan keandalan sistem secara signifikan, mengurangi downtime, dan mengoptimalkan produktivitas.
""")

st.caption("📌 Dikembangkan oleh Naufal Khoirul Ibrahim - Matematika Terapan")
