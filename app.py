# app.py
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan Lini Produksi", layout="centered")

# Judul dan Identitas
st.title("🔗 Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")
st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim | Matematika Terapan 2025")

# Penjelasan Skenario
st.markdown("""
Skenario Bisnis: Sebuah lini perakitan terdiri dari beberapa mesin yang beroperasi secara **seri**. Jika satu mesin berhenti, seluruh lini terhenti.  
Analisis ini menghitung keandalan total dan mengidentifikasi 'mata rantai terlemah'.
""")

# Data Keandalan Mesin
st.header("🔧 Keandalan per Mesin")
mesin = ["Stamping", "Welding", "Painting", "Assembly"]
keandalan = [0.98, 0.99, 0.96, 0.97]

data_table = {"Mesin": mesin, "Keandalan": keandalan}
st.table(data_table)

# Hitung Keandalan Sistem Seri
Rs = 1
for R in keandalan:
    Rs *= R

Rs_persen = Rs * 100
prob_fail = 100 - Rs_persen

# Identifikasi Mata Rantai Terlemah
min_R = min(keandalan)
index_min = keandalan.index(min_R)
terlemah = mesin[index_min]

# Hasil Perhitungan
st.header("📈 Hasil Analisis")
st.markdown(f"""
- **Keandalan Sistem (Rs):** {Rs_persen:.2f}%
- **Probabilitas Kegagalan:** {prob_fail:.2f}%
- **Mata Rantai Terlemah:** {terlemah} ({min_R * 100:.1f}%)
""")

st.info(
    f"💡 *Saran:* Prioritaskan perawatan pada mesin **{terlemah}** untuk dampak perbaikan terbesar."
)

# Visualisasi Grafik
st.subheader("🔍 Visualisasi Keandalan Komponen")

colors = ["blue" if i != index_min else "red" for i in range(len(mesin))]
plt.figure(figsize=(8, 5))
bars = plt.bar(mesin, [r * 100 for r in keandalan], color=colors)
plt.axhline(y=Rs_persen, color="purple", linestyle="--", label=f"Keandalan Sistem ~ {Rs_persen:.1f}%")
plt.xlabel("Mesin")
plt.ylabel("Keandalan (%)")
plt.title("Keandalan Setiap Mesin dan Sistem")
plt.legend()
st.pyplot(plt)

# Kesimpulan
st.header("✅ Kesimpulan")
st.markdown("""
Dalam sistem seri, keandalan keseluruhan sangat dipengaruhi oleh komponen yang paling tidak andal.  
Meningkatkan keandalan **'mata rantai terlemah'** akan memberikan dampak terbesar pada peningkatan keandalan seluruh lini produksi.
""")

