import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")

st.title("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

# ===== MASALAH & TUJUAN =====
with st.container(border=True):
    st.markdown("""
    ## 📌 Masalah & Tujuan Analisis
    Lini perakitan terdiri dari **mesin-mesin yang saling bergantung secara seri**.
    - ➜ Jika satu mesin gagal, **seluruh lini berhenti**.
    - ➜ Tujuan analisis ini:
      1. Hitung **keandalan total** sistem.
      2. Identifikasi **mata rantai terlemah**.
      3. Rekomendasi **perbaikan berbasis data**.

    💬 *Note Presenter:*  
    👉 Jelaskan ke dosen: kenapa sistem seri sensitif pada kegagalan satu mesin.  
    👉 Tunjukkan betapa penting menemukan "komponen kritis".
    """)

# ===== INPUT & TABEL SEBARIS =====
with st.container(border=True):
    st.markdown("## 🔧 Input & Tabel Keandalan Mesin (%)")
    st.caption("🎚️ Sesuaikan keandalan mesin pada slider (dalam %). Kanan muncul tabel ringkas.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎛️ Input Slider")
        r1 = st.slider("Stamping", 80, 100, 98)
        r2 = st.slider("Welding", 80, 100, 99)
        r3 = st.slider("Painting", 80, 100, 96)
        r4 = st.slider("Assembly", 80, 100, 97)
        st.markdown("""
        ℹ️ *Catatan untuk presenter:*  
        - Bisa jelaskan "slider ini simulasi keandalan mesin nyata".  
        - Tunjukkan jika menurunkan 1 mesin → pengaruh total.  
        """)
    with col2:
        st.markdown("### 📋 Tabel Keandalan per Mesin")
        st.table({
            "Mesin": ["Stamping", "Welding", "Painting", "Assembly"],
            "Keandalan (%)": [r1, r2, r3, r4]
        })

# ===== PERHITUNGAN MODEL =====
with st.container(border=True):
    st.markdown("## 📐 Konsep Model & Detail Perhitungan")
    st.markdown("""
    - Sistem seri berhenti jika satu mesin gagal.
    - Rumus **keandalan sistem seri**:
    """)
    st.latex(r"R_s = \prod_{i=1}^{n} R_i")

    r_values = [r1/100, r2/100, r3/100, r4/100]
    Rs = np.prod(r_values)
    prob_fail = 1 - Rs

    st.markdown("### 🔢 Perhitungan Contoh:")
    st.latex(
        fr"R_s = {r_values[0]:.2f} \times {r_values[1]:.2f} \times {r_values[2]:.2f} \times {r_values[3]:.2f} = {Rs:.4f}"
    )
    st.markdown(f"- ✅ **Keandalan Sistem:** {Rs:.2%}")
    st.markdown(f"- ✅ **Probabilitas Kegagalan:** {prob_fail:.2%}")

    st.markdown("""
    ℹ️ *Catatan untuk presenter:*  
    - Rumus penting buat dosen matematika terapan.  
    - Tegaskan bahwa sistem seri = semua mesin harus andal.  
    """)

# ===== VISUALISASI SEBARIS =====
with st.container(border=True):
    st.markdown("## 📊 Visualisasi Keandalan")
    col1, col2 = st.columns(2)

    # Komponen Individu
    with col1:
        st.markdown("#### 🔹 Keandalan Mesin Individu")
        weakest_idx = np.argmin(r_values)
        bar_colors = ['#87CEEB'] * 4
        bar_colors[weakest_idx] = '#FF6347'
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.bar(["Stamping", "Welding", "Painting", "Assembly"], r_values, color=bar_colors)
        ax1.set_ylim(0.75, 1.01)
        ax1.set_ylabel('Keandalan (%)')
        for i, v in enumerate(r_values):
            ax1.text(i, v, f"{v:.2%}", ha='center', va='bottom')
        st.pyplot(fig1)
        st.caption(f"✅ Bar merah menandai mesin terlemah: {['Stamping','Welding','Painting','Assembly'][weakest_idx]} ({r_values[weakest_idx]*100:.1f}%).")

    # Sistem Total
    with col2:
        st.markdown("#### 🔹 Keandalan Sistem Total")
        fig2, ax2 = plt.subplots(figsize=(3.5, 3))
        ax2.bar(["Sistem Total"], [Rs], color="#9370DB")
        ax2.set_ylim(0.75, 1.01)
        ax2.set_ylabel('Keandalan (%)')
        ax2.text(0, Rs, f"{Rs:.2%}", ha='center', va='bottom')
        st.pyplot(fig2)
        st.caption("✅ Sistem total adalah hasil kombinasi semua mesin dalam model seri.")

# ===== ANALISIS RISIKO =====
with st.container(border=True):
    st.markdown("## 📋 Analisis Risiko & Rekomendasi")
    kategori = "🟠 Risiko Menengah" if prob_fail > 0.05 else "🟢 Risiko Rendah"
    st.markdown(f"- **Kategori Risiko:** {kategori}")
    st.markdown(f"- **Probabilitas Kegagalan:** {prob_fail:.2%}")

    st.markdown("### 🛠️ Rekomendasi Strategi Perbaikan")
    st.markdown(f"""
    1. Fokus perawatan pada **{['Stamping','Welding','Painting','Assembly'][weakest_idx]}** (mata rantai terlemah).
    2. Preventive maintenance intensif.
    3. Standarkan SOP di tahap tersebut.
    4. Terapkan **condition monitoring**.
    5. Lakukan evaluasi berkala.
    """)
    st.markdown("""
    ℹ️ *Catatan untuk presenter:*  
    - Jelaskan bahwa peningkatan mesin terlemah → dampak besar ke sistem.  
    - Buat dosen lihat logika: tidak semua mesin harus 100%, cukup perbaiki yang lemah.  
    """)

st.divider()
st.caption("📌 Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")
