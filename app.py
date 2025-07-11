import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="wide")
st.header("🔗 Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

col1, col2 = st.columns([1.5, 2])

with col1:
    st.markdown("""
    **Skenario Bisnis:**
    Sebuah lini perakitan terdiri dari beberapa mesin yang beroperasi secara seri. Jika satu mesin berhenti, seluruh lini terhenti. Analisis ini menghitung keandalan total dan mengidentifikasi 'mata rantai terlemah'.
    """)
    
    with st.container(border=True):
        st.subheader("🔧 Keandalan per Mesin")
        r1 = st.slider("Stamping (R1)", 0.80, 1.00, 0.98, 0.01)
        r2 = st.slider("Welding (R2)", 0.80, 1.00, 0.99, 0.01)
        r3 = st.slider("Painting (R3)", 0.80, 1.00, 0.96, 0.01)
        r4 = st.slider("Assembly (R4)", 0.80, 1.00, 0.97, 0.01)
    
    with st.expander("Penjelasan Rumus Model: Keandalan Sistem Seri"):
        st.markdown("""
        Keandalan sistem seri dihitung dengan mengalikan keandalan dari setiap komponennya.
        - **Keandalan (R):** Adalah probabilitas sebuah komponen atau sistem akan berfungsi dengan baik selama periode waktu tertentu.
        - **Sistem Seri:** Komponen-komponen yang tersusun berurutan. Jika salah satu saja gagal, maka seluruh sistem akan gagal. Akibatnya, keandalan sistem seri **selalu lebih rendah** daripada keandalan komponen terlemahnya.
        """)
        st.latex(r''' R_s = R_1 \times R_2 \times \dots \times R_n = \prod_{i=1}^{n} R_i ''')

    reliabilities = {'Stamping': r1, 'Welding': r2, 'Painting': r3, 'Assembly': r4}
    keandalan_sistem = np.prod(list(reliabilities.values()))
    weakest_link_name = min(reliabilities, key=reliabilities.get)
    weakest_link_value = reliabilities[weakest_link_name]
    
    with st.expander("Lihat Proses Perhitungan"):
        st.latex(fr"R_s = R_{{Stamping}} \times R_{{Welding}} \times R_{{Painting}} \times R_{{Assembly}}")
        st.latex(fr"R_s = {r1} \times {r2} \times {r3} \times {r4} = {keandalan_sistem:.4f}")
        st.markdown(f"**Keandalan Sistem ($R_s$)** adalah **{keandalan_sistem:.2%}**.")

with col2:
    st.subheader("💡 Hasil dan Wawasan Bisnis")
    st.warning(f"**Mata Rantai Terlemah:** Mesin **{weakest_link_name}** ({weakest_link_value:.1%}) adalah komponen paling berisiko. Prioritaskan perawatan dan perbaikan pada mesin ini untuk dampak terbesar.")

    col1_res, col2_res = st.columns(2)
    with col1_res:
         st.metric(label="📈 Keandalan Keseluruhan Lini", value=f"{keandalan_sistem:.2%}")
    with col2_res:
         st.metric(label="📉 Probabilitas Kegagalan Lini", value=f"{1 - keandalan_sistem:.2%}", delta_color="inverse")

    with st.container(border=True):
        st.markdown("**Analisis Dampak Kegagalan:**")
        dampak = (1 - keandalan_sistem) * 100
        if dampak > 10:
            st.error(f"- **Sangat Berisiko ({dampak:.1f}%):** Lini produksi kemungkinan besar akan sering berhenti, menyebabkan kerugian signifikan.")
        elif dampak > 5:
            st.warning(f"- **Risiko Menengah ({dampak:.1f}%):** Probabilitas kegagalan cukup tinggi. Perbaikan pada mesin terlemah sangat disarankan.")
        else:
            st.info(f"- **Risiko Rendah ({dampak:.1f}%):** Probabilitas kegagalan terkendali. Fokus pada perawatan rutin untuk mempertahankan kinerja.")

    # Grafik
    st.markdown("#### Visualisasi Dampak Keandalan Komponen")
    labels = list(reliabilities.keys())
    values = list(reliabilities.values())
    labels.append("SISTEM TOTAL")
    values.append(keandalan_sistem)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bar_colors = ['#87CEEB'] * len(reliabilities)
    weakest_idx = list(reliabilities.keys()).index(weakest_link_name)
    bar_colors[weakest_idx] = '#FF6347'
    bar_colors.append('#9370DB')

    bars = ax.bar(labels, values, color=bar_colors)
    ax.set_ylabel('Tingkat Keandalan (Reliability)')
    ax.set_title('Perbandingan Keandalan Komponen dan Sistem', fontsize=16)
    ax.set_ylim(min(0.75, min(values) * 0.95 if values else 0.75), 1.01)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2%}', ha='center', va='bottom', fontsize=10, color='black')
    st.pyplot(fig)

    with st.container(border=True):
        st.markdown("**🔍 Penjelasan Grafik:**")
        st.markdown("""
        Grafik ini menunjukkan bagaimana keandalan setiap mesin mempengaruhi keandalan seluruh lini produksi.
        - **Bar Biru & Merah:** Menunjukkan keandalan setiap mesin. Bar **merah** adalah mesin dengan keandalan terendah, yang menjadi **mata rantai terlemah**.
        - **Bar Ungu:** Menunjukkan keandalan total sistem. Perhatikan bagaimana nilainya selalu **lebih rendah** dari komponen terlemah sekalipun.

        **Kesimpulan:** Dalam sistem seri, keandalan keseluruhan sangat dipengaruhi oleh komponen yang paling tidak andal. Meningkatkan keandalan 'mata rantai terlemah' akan memberikan dampak terbesar pada peningkatan keandalan seluruh lini produksi.
        """)

# --- FOOTER ---
st.divider()
st.caption("Naufal Khoirul Ibrahim")
