import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul & pengantar
st.title("🔗 Analisis Keandalan Lini Produksi")
st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")

st.markdown("""
Skenario Bisnis: Sebuah lini perakitan terdiri dari beberapa mesin yang beroperasi secara **seri**. 
Jika satu mesin berhenti, seluruh lini terhenti. 
Analisis ini menghitung keandalan total dan mengidentifikasi **'mata rantai terlemah'**.
""")

# Data komponen
mesin = ["Stamping", "Welding", "Painting", "Assembly"]
keandalan = [0.98, 0.99, 0.96, 0.97]

# Tampilkan tabel rapi
df = pd.DataFrame({"Mesin": mesin, "Keandalan": keandalan})
st.dataframe(df, use_container_width=True)

# Penjelasan rumus
st.header("🧮 Rumus Keandalan Sistem Seri")
st.latex(r"R_s = R_1 \times R_2 \times R_3 \times R_4")

# Hitung keandalan total
Rs = 1
for R in keandalan:
    Rs *= R

Rs_persen = round(Rs * 100, 1)
prob_fail = round(100 - Rs_persen, 1)

# Hasil
st.success(f"✅ Keandalan Sistem diperkirakan {Rs_persen:.1f}%, sehingga probabilitas kegagalan adalah {prob_fail:.1f}%.")

# Identifikasi mata rantai terlemah
min_R = min(keandalan)
index_min = keandalan.index(min_R)
terlemah = mesin[index_min]

st.warning(f"🔍 Mata Rantai Terlemah: **{terlemah}** ({min_R*100:.1f}%)")

# Visualisasi
st.header("📊 Visualisasi Keandalan Komponen")
colors = ["red" if i == index_min else "blue" for i in range(len(mesin))]

fig, ax = plt.subplots()
bars = ax.bar(mesin, [r*100 for r in keandalan], color=colors)
ax.axhline(y=Rs_persen, color="black", linestyle="--", linewidth=2, label=f"Keandalan Sistem ≈ {Rs_persen:.1f}%")

# Tambahkan label ke setiap bar
for bar, val in zip(bars, keandalan):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f"{val*100:.1f}%", ha='center')

ax.set_ylabel("Keandalan (%)")
ax.legend()
st.pyplot(fig)

# Kesimpulan
st.header("✅ Kesimpulan")
