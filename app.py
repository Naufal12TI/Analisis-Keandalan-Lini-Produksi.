import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")
st.header("🛠️ Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

col1, col2 = st.columns([1.5, 2])

with col1:
    st.markdown("""
    **Skenario Bisnis:**
    Lini perakitan terdiri dari mesin-mesin yang beroperasi secara seri. Jika satu mesin gagal, seluruh proses terhenti. Tujuan analisis ini adalah menghitung keandalan total dan mengidentifikasi *mata rantai terlemah*.
    """)

    st.caption("Gunakan slider untuk menyesuaikan tingkat keandalan mesin (dalam persen).")
    with st.container(border=True):
        st.subheader("🔧 Keandalan per Mesin (%)")
        r1 = st.slider("Stamping", 80, 100, 98, 1)
        r2 = st.slider("Welding", 80, 100, 99, 1)
        r3 = st.slider("Painting", 80, 100, 96, 1)
        r4 = st.slider("Assembly", 80, 100, 97, 1)

    with st.expander("🔢 Penjelasan & Proses Perhitungan (Matematika Terapan)"):
        st.markdown("""
        Keandalan sistem seri dihitung dengan rumus:
        - Sistem seri sangat bergantung pada komponen terlemah.
        - Jika salah satu gagal, sistem gagal total.
        Rumus umum:
        """)
        st.latex(r''' R_s = R_1 \times R_2 \times \dots \times R_n = \prod_{i=1}^{n} R_i ''')

        r1f, r2f, r3f, r4f = [r/100 for r in (r1, r2, r3, r4)]
        keandalan_sistem = np.prod([r1f, r2f, r3f, r4f])
        prob_kegagalan = 1 - keandalan_sistem

        reliabilities = {'Stamping': r1f, 'Welding': r2f, 'Painting': r3f, 'Assembly': r4f}
        weakest_link_name = min(reliabilities, key=reliabilities.get)
        weakest_link_value = reliabilities[weakest_link_name]

        st.markdown(f"""
        Substitusi nilai:
        - R1 (Stamping) = {r1f:.2f}
        - R2 (Welding) = {r2f:.2f}
        - R3 (Painting) = {r3f:.2f}
        - R4 (Assembly) = {r4f:.2f}

        Perhitungan:
        """)
        st.latex(fr"R_s = {r1f:.2f} \times {r2f:.2f} \times {r3f:.2f} \times {r4f:.2f} = {keandalan_sistem:.4f}")
        st.markdown(f"**Keandalan Sistem ($R_s$)** = **{keandalan_sistem:.2%}**")
        st.markdown(f"**Probabilitas Kegagalan** = **{prob_kegagalan:.2%}** (karena 1 - $R_s$).")

with col2:
    st.subheader("💡 Hasil dan Wawasan Bisnis")
    st.info(f"""
    **📌 Analisis Komponen Kritis:**
    Mesin **{weakest_link_name}** memiliki keandalan terendah (**{weakest_link_value:.1%}**), sehingga menjadi *mata rantai terlemah* dalam sistem seri.
    Karena sistem berhenti jika satu mesin gagal, fokus peningkatan keandalan pada tahap ini akan berdampak langsung pada peningkatan keandalan total.
    Direkomendasikan program perawatan preventif intensif, standardisasi SOP, dan penerapan sistem pemantauan kondisi.
    """)

    col1_res, col2_res = st.columns(2)
    with col1_res:
        st.metric(label="📈 Keandalan Total", value=f"{keandalan_sistem:.2%}")
    with col2_res:
        st.metric(label="📉 Probabilitas Kegagalan", value=f"{prob_kegagalan:.2%}", delta_color="inverse")

    with st.container(border=True):
        st.markdown("### 📋 Analisis Risiko (Matematika Terapan):")
        st.markdown(f"""
        - **Probabilitas kegagalan sistem** dihitung sebagai:
            \n\( 1 - R_s = {1 - keandalan_sistem:.4f} \)
            \nSehingga probabilitas kegagalan = **{prob_kegagalan:.2%}**.
        - Berdasarkan nilai ini, sistem dikategorikan sebagai:
        """)
        dampak = prob_kegagalan * 100
        if dampak > 10:
            st.error(f"""
            **Kategori: Sangat Berisiko ({dampak:.1f}%)**
            
            - Potensi downtime signifikan yang mempengaruhi output produksi.
            - Disarankan redesign lini, peningkatan spesifikasi mesin, dan perencanaan redundansi.
            """)
        elif dampak > 5:
            st.warning(f"""
            **Kategori: Risiko Menengah ({dampak:.1f}%)**
            
            - Evaluasi ulang mesin kritis sangat disarankan.
            - Fokus pada peningkatan keandalan komponen terlemah melalui perawatan preventif dan monitoring kondisi.
            """)
        else:
            st.success(f"""
            **Kategori: Risiko Rendah ({dampak:.1f}%)**
            
            - Sistem relatif stabil.
            - Tetap diperlukan pemeliharaan berkala dan inspeksi untuk menjaga performa.
            """)

    st.markdown("#### Visualisasi Keandalan Komponen dan Sistem")
    labels = list(reliabilities.keys()) + ["SISTEM TOTAL"]
    values = list(reliabilities.values()) + [keandalan_sistem]

    fig, ax = plt.subplots(figsize=(10, 5))
    bar_colors = ['#87CEEB'] * len(reliabilities)
    weakest_idx = list(reliabilities.keys()).index(weakest_link_name)
    bar_colors[weakest_idx] = '#FF6347'
    bar_colors.append('#9370DB')

    bars = ax.bar(labels, values, color=bar_colors)
    ax.set_ylabel('Tingkat Keandalan (%)')
    ax.set_title('Perbandingan Keandalan Komponen dan Sistem', fontsize=16)
    ax.set_ylim(0.75, 1.01)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2%}', ha='center', va='bottom', fontsize=10)
    st.pyplot(fig)

    with st.container(border=True):
        st.markdown("""
        **🔍 Penjelasan Grafik:**
        - **Bar Biru**: Komponen normal.
        - **Bar Merah**: Komponen dengan keandalan terendah (mata rantai terlemah).
        - **Bar Ungu**: Keandalan sistem total.

        Perhatikan bahwa keandalan sistem selalu lebih rendah dari komponen terlemah.
        Meningkatkan keandalan komponen kritis berdampak besar pada sistem.
        """)

st.divider()
st.caption("Naufal Khoirul Ibrahim")
