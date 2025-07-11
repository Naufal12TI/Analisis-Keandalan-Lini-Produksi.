import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")

st.title("🛠️ Analisis Keandalan Lini Produksi")
st.caption("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

with st.expander("📌 1️⃣ Masalah & Tujuan Analisis", expanded=False):
    st.markdown("""
    **Masalah:** Pada lini perakitan sistem seri, jika satu mesin gagal, seluruh proses berhenti.
    
    **Tujuan Analisis:**
    - Menghitung keandalan total sistem produksi
    - Mengidentifikasi *mata rantai terlemah*
    - Memberikan rekomendasi berbasis hasil analisis
    """)

with st.expander("📐 2️⃣ Konsep Sistem Seri & Rumus", expanded=False):
    st.markdown("""
    Dalam sistem seri, semua komponen saling bergantung. Kegagalan satu mesin menyebabkan sistem gagal total.
    
    **Rumus keandalan sistem:**
    """)
    st.latex(r"R_s = \prod_{i=1}^{n} R_i")
    st.markdown("""
    ➜ Sistem seri sangat sensitif pada komponen dengan keandalan terendah.  
    ➜ Fokus pada peningkatan mesin terlemah memberikan dampak terbesar.
    """)

# Input & Tabel berdampingan
st.markdown("### 🔧 3️⃣ Input Data: Keandalan Mesin (%)")
col_input, col_table = st.columns(2)

with col_input:
    st.subheader("🎚️ Input Slider")
    st.caption("Atur nilai keandalan masing-masing mesin:")
    r1 = st.slider("Stamping", 80, 100, 98, 1)
    r2 = st.slider("Welding", 80, 100, 99, 1)
    r3 = st.slider("Painting", 80, 100, 96, 1)
    r4 = st.slider("Assembly", 80, 100, 97, 1)

with col_table:
    st.subheader("📊 Tabel Keandalan per Mesin")
    st.table({
        "Mesin": ["Stamping", "Welding", "Painting", "Assembly"],
        "Keandalan (%)": [r1, r2, r3, r4]
    })

# Hitung nilai
r1f, r2f, r3f, r4f = [r/100 for r in (r1, r2, r3, r4)]
keandalan_sistem = np.prod([r1f, r2f, r3f, r4f])
prob_kegagalan = 1 - keandalan_sistem
reliabilities = {
    "Stamping": r1f,
    "Welding": r2f,
    "Painting": r3f,
    "Assembly": r4f
}
weakest_link_name = min(reliabilities, key=reliabilities.get)
weakest_link_value = reliabilities[weakest_link_name]

# Ringkasan hasil
st.markdown("### ✅ 4️⃣ Ringkasan Hasil Sistem")
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(label="📈 Keandalan Sistem", value=f"{keandalan_sistem:.2%}")
with col_res2:
    st.metric(label="📉 Probabilitas Kegagalan", value=f"{prob_kegagalan:.2%}")

with st.expander("🔎 Penjelasan Singkat", expanded=False):
    st.markdown(f"""
    ➜ Sistem seri = semua mesin saling tergantung.  
    ➜ Mesin dengan keandalan terendah yaitu **{weakest_link_name}** ({weakest_link_value:.0%}) menjadi *mata rantai lemah*.  
    ➜ Meningkatkan keandalan di bagian ini → berdampak langsung pada sistem.
    """)

# Visualisasi Mesin Individu
st.markdown("### 📈 5️⃣ Visualisasi Komponen")
st.caption(f"✅ Bar merah = mesin dengan keandalan terendah yaitu {weakest_link_name} ({weakest_link_value:.0%}).")

fig1, ax1 = plt.subplots(figsize=(8,4))
colors = ['#87CEEB'] * 4
colors[list(reliabilities.keys()).index(weakest_link_name)] = '#FF6347'
ax1.bar(reliabilities.keys(), reliabilities.values(), color=colors)
ax1.set_ylim(0.75, 1.01)
ax1.set_ylabel('Keandalan')
ax1.set_title('Keandalan Mesin Individu')
for i, v in enumerate(reliabilities.values()):
    ax1.text(i, v, f"{v:.2%}", ha='center', va='bottom')
st.pyplot(fig1)

# Visualisasi Sistem Total
st.markdown("### 🟣 6️⃣ Visualisasi Sistem Total")
st.caption("✅ Keandalan sistem total selalu lebih rendah dari komponen terlemah.")
fig2, ax2 = plt.subplots(figsize=(4,4))
ax2.bar(['Sistem Total'], [keandalan_sistem], color='#9370DB')
ax2.set_ylim(0.75, 1.01)
ax2.set_ylabel('Keandalan')
ax2.set_title('Keandalan Sistem Total')
ax2.text(0, keandalan_sistem, f"{keandalan_sistem:.2%}", ha='center', va='bottom')
st.pyplot(fig2)

# Analisis Risiko & Rekomendasi
st.markdown("### 📋 7️⃣ Analisis Risiko & Rekomendasi")
risk_category = "🟢 Rendah" if prob_kegagalan <= 0.05 else ("🟠 Menengah" if prob_kegagalan <= 0.10 else "🔴 Tinggi")
st.info(f"**Kategori Risiko: {risk_category} ({prob_kegagalan:.2%})**")

with st.expander("💡 Strategi Perbaikan yang Disarankan", expanded=False):
    st.markdown(f"""
    - Fokus perawatan preventif pada **{weakest_link_name}**.
    - Standardisasi SOP untuk proses {weakest_link_name}.
    - Terapkan pemantauan kondisi (Condition Monitoring).
    - Pertimbangkan pelatihan operator untuk mengurangi human error.
    - Lakukan evaluasi periodik untuk memverifikasi peningkatan keandalan.
    """)

st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")
