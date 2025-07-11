# streamlit_app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Keandalan - Tab 4 (Naufal)", layout="centered")

st.title("Analisis Keandalan Lini Produksi")
st.header("Tab 4: Simulasi Monte Carlo")
st.subheader("Oleh: Naufal")

st.markdown("""
Simulasi Monte Carlo digunakan untuk memperkirakan keandalan sistem perakitan
dengan meniru distribusi waktu antar kerusakan.
""")

# Input jumlah simulasi
num_simulasi = st.number_input(
    "Masukkan Jumlah Simulasi",
    min_value=100,
    max_value=100000,
    value=1000,
    step=100
)

# Tombol untuk jalankan simulasi
if st.button("Jalankan Simulasi"):
    # Misal kita modelkan waktu antar kerusakan (mean = 10 jam)
    mean_waktu = 10
    hasil_simulasi = np.random.exponential(mean_waktu, num_simulasi)

    # Statistik
    rata_rata = np.mean(hasil_simulasi)
    st.success(f"Rata-rata waktu antar kerusakan hasil simulasi: {rata_rata:.2f} jam")

    # Tampilkan histogram
    fig, ax = plt.subplots()
    ax.hist(hasil_simulasi, bins=30, color='skyblue', edgecolor='black')
    ax.set_xlabel('Waktu Antar Kerusakan (jam)')
    ax.set_ylabel('Frekuensi')
    ax.set_title('Distribusi Simulasi Monte Carlo')
    st.pyplot(fig)

    # Data tabel opsional
    if st.checkbox("Tampilkan Data Simulasi"):
        st.write(hasil_simulasi)
