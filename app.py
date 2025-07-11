import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")
st.title("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

st.markdown("""
📌 **Masalah yang Dianalisis**
> Lini perakitan dengan mesin-mesin yang saling bergantung secara seri. Jika satu mesin gagal, seluruh lini berhenti.
""")

st.markdown("""
🎯 **Tujuan Analisis**
- Menghitung keandalan total sistem
- Mengidentifikasi mata rantai terlemah
- Memberikan rekomendasi perbaikan berbasis hasil analisis
""")

# ---------------------------------------------
st.markdown("## 1️⃣ 📐 Konsep Model Matematis")
with st.expander("Lihat Penjelasan Detail 📖", expanded=False):
    st.markdown("""
    Dalam sistem seri:
    - Keandalan sistem dihitung sebagai hasil perkalian keandalan semua komponen.
    - Jika satu mesin gagal, sistem berhenti total.
    
    Rumus umum:
    """)
    st.latex(r"R_s = \prod_{i=1}^{n} R_i")
    st.caption("✅ Sistem seri sangat sensitif pada komponen dengan keandalan terendah.")


# ---------------------------------------------
st.markdown("## 2️⃣ 🔧 Input Data")
st.caption("✅ Silakan atur keandalan tiap mesin (dalam persen).")

col_slider, col_table = st.columns(2)

with col_slider:
    st.subheader("🎚️ Slider Input Mesin")
    r1 = st.slider("Stamping", 80, 100, 98, 1)
    r2 = st.slider("Welding", 80, 100, 99, 1)
    r3 = st.slider("Painting", 80, 100, 96, 1)
    r4 = st.slider("Assembly", 80, 100, 97, 1)
    st.caption("💡 Geser untuk simulasi perawatan atau peningkatan keandalan.")

with col_table:
    st.subheader("📊 Tabel Ringkasan Input")
    st.table({
        "Mesin": ["Stamping", "Welding", "Painting", "Assembly"],
        "Keandalan (%)": [r1, r2, r3, r4]
    })
    st.caption("ℹ️ Tabel ini membantu memeriksa nilai input.")


# ---------------------------------------------
st.markdown("## 3️⃣ 🔢 Detail Perhitungan")
with st.expander("Lihat Langkah-langkah 📖", expanded=False):
    st.markdown("""
    1️⃣ Konversi persen ke desimal
    2️⃣ Hitung hasil perkalian semua komponen
    
    Contoh substitusi nilai:
    """)
    r1f, r2f, r3f, r4f = [r/100 for r in (r1, r2, r3, r4)]
    keandalan_sistem = np.prod([r1f, r2f, r3f, r4f])
    st.latex(fr"R_s = {r1f:.2f} \times {r2f:.2f} \times {r3f:.2f} \times {r4f:.2f} = {keandalan_sistem:.4f}")
    st.caption("✅ Probabilitas Kegagalan = 1 - R_s")


# ---------------------------------------------
st.markdown("## 4️⃣ ✅ Ringkasan Hasil Sistem")
col_result1, col_result2 = st.columns(2)
with col_result1:
    st.metric("📈 Keandalan Sistem", f"{keandalan_sistem:.2%}")
with col_result2:
    prob_kegagalan = 1 - keandalan_sistem
    st.metric("📉 Probabilitas Kegagalan", f"{prob_kegagalan:.2%}")

with st.container(border=True):
    dampak = prob_kegagalan * 100
    if dampak > 10:
        st.error(f"🛑 **Sangat Berisiko ({dampak:.1f}%):** Intervensi segera disarankan.")
    elif dampak > 5:
        st.warning(f"⚠️ **Risiko Menengah ({dampak:.1f}%):** Evaluasi ulang mesin kritis sangat disarankan.")
    else:
        st.success(f"✅ **Risiko Rendah ({dampak:.1f}%):** Sistem relatif stabil.")


# ---------------------------------------------
st.markdown("## 5️⃣ 📈 Visualisasi Komponen & Sistem")
st.caption("🔍 Perhatikan: Sistem seri akan berhenti jika satu mesin gagal.")

reliabilities = {
    'Stamping': r1f,
    'Welding': r2f,
    'Painting': r3f,
    'Assembly': r4f
}
weakest_link_name = min(reliabilities, key=reliabilities.get)
weakest_link_value = reliabilities[weakest_link_name]

col_graph_mesin, col_graph_sistem = st.columns(2)

with col_graph_mesin:
    st.subheader("🔹 Keandalan Mesin Individu")
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    colors = ['#87CEEB'] * 4
    colors[list(reliabilities.keys()).index(weakest_link_name)] = '#FF6347'
    ax1.bar(reliabilities.keys(), reliabilities.values(), color=colors)
    ax1.set_ylim(0.75, 1.01)
    ax1.set_ylabel('Keandalan')
    ax1.set_title('Komponen Individu')
    for i, v in enumerate(reliabilities.values()):
        ax1.text(i, v, f"{v:.2%}", ha='center', va='bottom', fontsize=9)
    st.pyplot(fig1)
    st.caption(f"✅ Bar merah: {weakest_link_name} ({weakest_link_value:.0%}) adalah *mata rantai terlemah*.")

with col_graph_sistem:
    st.subheader("🟣 Keandalan Sistem Total")
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.bar(['Sistem Total'], [keandalan_sistem], color='#9370DB')
    ax2.set_ylim(0.75, 1.01)
    ax2.set_ylabel('Keandalan')
    ax2.set_title('Sistem Seri')
    ax2.text(0, keandalan_sistem, f"{keandalan_sistem:.2%}", ha='center', va='bottom', fontsize=10)
    st.pyplot(fig2)
    st.caption(f"✅ Sistem total = {keandalan_sistem:.2%}. Fokus pada perbaikan mata rantai terlemah.")


# ---------------------------------------------
st.markdown("## 6️⃣ 📋 Rekomendasi Strategi Perbaikan")
with st.container(border=True):
    st.markdown(f"""
    - Fokuskan perawatan pada **{weakest_link_name}** (keandalan terendah).
    - Terapkan *preventive maintenance* intensif.
    - Standarkan SOP pada tahap **{weakest_link_name}**.
    - Pasang *condition monitoring* (sensor/pemantauan).
    - Lakukan evaluasi periodik untuk memverifikasi peningkatan keandalan.
    """)
    st.caption("✅ Strategi berbasis data untuk peningkatan keandalan sistem.")


st.divider()
st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")
