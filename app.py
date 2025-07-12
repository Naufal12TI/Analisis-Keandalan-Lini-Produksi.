import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Statistik Deskriptif Keandalan Mesin", layout="wide")

st.title("📊 Analisis Statistik Deskriptif Keandalan Mesin Produksi")
st.markdown("""
Aplikasi ini membantu menganalisis keandalan mesin pada lini produksi menggunakan **statistik deskriptif**.
""")

# 1️⃣ PENJELASAN
with st.expander("ℹ️ Penjelasan Singkat", expanded=True):
    st.markdown("""
    - Sistem produksi dengan mesin saling bergantung (*seri*).
    - Analisis keandalan tiap mesin (dalam %).
    - Identifikasi mesin dengan keandalan terendah (*outlier*).
    - Memberikan insight rekomendasi perbaikan.
    """)

# 2️⃣ INPUT & TABEL SAMPINGAN
st.subheader("1️⃣ Input Data Keandalan Mesin")
col_input, col_table = st.columns(2)

with col_input:
    st.caption("Silakan sesuaikan tingkat keandalan masing-masing mesin:")
    r1 = st.slider("Stamping", 80, 100, 98)
    r2 = st.slider("Welding", 80, 100, 99)
    r3 = st.slider("Painting", 80, 100, 96)
    r4 = st.slider("Assembly", 80, 100, 97)

with col_table:
    data_df = pd.DataFrame({
        'Mesin': ['Stamping', 'Welding', 'Painting', 'Assembly'],
        'Keandalan (%)': [r1, r2, r3, r4]
    })
    st.dataframe(data_df, use_container_width=True)

# 3️⃣ STATISTIK DESKRIPTIF
st.subheader("2️⃣ Hasil Statistik Deskriptif")
mean_val = np.mean([r1, r2, r3, r4])
min_val = min([r1, r2, r3, r4])
min_machine = data_df.iloc[data_df['Keandalan (%)'].idxmin()]['Mesin']

st.markdown(f"""
✅ **Rata-rata Keandalan Mesin:** {mean_val:.2f}%  
🚨 **Keandalan Terendah:** {min_val:.2f}% (Mesin {min_machine})
""")

# 4️⃣ VISUALISASI
st.subheader("3️⃣ Visualisasi Komponen & Sistem")
reliabilities = [r1/100, r2/100, r3/100, r4/100]
system_reliability = np.prod(reliabilities)

labels = ['Stamping', 'Welding', 'Painting', 'Assembly', 'Sistem Total']
values = [r/100 for r in [r1, r2, r3, r4]] + [system_reliability]
colors = ['#87CEEB']*4 + ['#9370DB']
colors[data_df['Keandalan (%)'].idxmin()] = '#FF6347'

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(labels, values, color=colors)
ax.set_ylim(0.75, 1.02)
ax.set_ylabel('Keandalan (dalam proporsi)')

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2%}', ha='center', va='bottom')

st.pyplot(fig)

with st.expander("💡 Penjelasan Grafik"):
    st.markdown("""
    - **Bar biru:** Komponen normal.
    - **Bar merah:** Mesin dengan keandalan terendah (*outlier*).
    - **Bar ungu:** Keandalan sistem total.
    """)

# 5️⃣ INSIGHT & SARAN
st.subheader("4️⃣ Insight & Rekomendasi")
st.markdown(f"""
✅ Sistem total memiliki keandalan **{system_reliability:.2%}**  
✅ Probabilitas kegagalan sistem: **{(1-system_reliability):.2%}**

**Rekomendasi:**
- Fokuskan perawatan pada mesin {min_machine}.
- Terapkan preventive maintenance & condition monitoring.
- Lakukan evaluasi periodik.
""")

st.caption("📌 Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")
