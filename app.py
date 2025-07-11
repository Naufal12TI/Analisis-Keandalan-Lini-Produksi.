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

    with st.expander("🔢 Penjelasan & Proses Perhitungan"):
        st.markdown("""
        Keandalan sistem seri dihitung dengan mengalikan keandalan masing-masing komponen.
        - Sistem seri sangat bergantung pada komponen terlemah.
        - Jika salah satu gagal, sistem gagal total.
        """)
        st.latex(r''' R_s = R_1 \times R_2 \times \dots \times R_n = \prod_{i=1}^{n} R_i ''')

        r1f, r2f, r3f, r4f = [r/100 for r in (r1, r2, r3, r4)]
        keandalan_sistem = np.prod([r1f, r2f, r3f, r4f])
        reliabilities = {'Stamping': r1f, 'Welding': r2f, 'Painting': r3f, 'Assembly': r4f}
        weakest_link_name = min(reliabilities, key=reliabilities.get)
        weakest_link_value = reliabilities[weakest_link_name]

        st.latex(fr"R_s = {r1f:.2f} \times {r2f:.2f} \times {r3f:.2f} \times {r4f:.2f} = {keandalan_sistem:.4f}")
        st.markdown(f"**Keandalan Sistem ($R_s$)** adalah **{keandalan_sistem:.2%}**.")

with col2:
    st.subheader("💡 Hasil dan Wawasan Bisnis")
    st.warning(f"🚨 Komponen Kritis: Mesin **{weakest_link_name}** hanya memiliki keandalan **{weakest_link_value:.1%}**. Fokus perawatan pada komponen ini untuk dampak maksimal.")

    col1_res, col2_res = st.columns(2)
    with col1_res:
        st.metric(label="📈 Keandalan Total", value=f"{keandalan_sistem:.2%}")
    with col2_res:
        prob_kegagalan = 1 - keandalan_sistem
        st.metric(label="📉 Probabilitas Kegagalan", value=f"{prob_kegagalan:.2%}", delta_color="inverse")

    with st.container(border=True):
        st.markdown("**📋 Analisis Risiko:**")
        dampak = prob_kegagalan * 100
        if dampak > 10:
            st.error(f"- **Sangat Berisiko ({dampak:.1f}%):** Potensi kerugian signifikan. Intervensi segera disarankan.")
        elif dampak > 5:
            st.warning(f"- **Risiko Menengah ({dampak:.1f}%):** Evaluasi ulang mesin kritis sangat disarankan.")
        else:
            st.info(f"- **Risiko Rendah ({dampak:.1f}%):** Sistem relatif stabil, tetap lakukan pemeliharaan.")

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
