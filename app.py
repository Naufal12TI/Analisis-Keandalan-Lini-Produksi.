import streamlit as st
import math

st.title("📦 Aplikasi Perhitungan Economic Order Quantity (EOQ)")
st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")

# Penjelasan singkat dengan expander
with st.expander("ℹ️ Apa itu EOQ?"):
    st.markdown("""
    Economic Order Quantity (EOQ) adalah metode untuk menghitung jumlah pembelian optimal 
    agar biaya penyimpanan dan biaya pemesanan minimum.
    
    Rumus EOQ:
    \n
    $EOQ = \sqrt{ (2DS) / H }$
    \n
    - D = Permintaan tahunan (unit/tahun)
    - S = Biaya pesan per pesanan
    - H = Biaya simpan per unit per tahun
    """)

# Input section
st.header("1️⃣ Input Data")
col1, col2, col3 = st.columns(3)
with col1:
    D = st.number_input("Permintaan tahunan (D)", min_value=1, value=1000)
with col2:
    S = st.number_input("Biaya pesan per order (S)", min_value=1, value=50)
with col3:
    H = st.number_input("Biaya simpan per unit per tahun (H)", min_value=1, value=5)

# Hitung EOQ
if st.button("Hitung EOQ"):
    EOQ = math.sqrt((2 * D * S) / H)
    freq = D / EOQ
    cycle_time = 365 / freq

    st.header("2️⃣ Hasil Perhitungan")
    st.success(f"**EOQ (Jumlah Pemesanan Optimal): {EOQ:.2f} unit**")
    st.write(f"Frekuensi Pemesanan per Tahun: {freq:.2f} kali")
    st.write(f"Waktu Antar Pemesanan (hari): {cycle_time:.2f} hari")

    with st.expander("📈 Penjelasan Matematis"):
        st.markdown(f"""
        - Rumus EOQ digunakan untuk meminimalkan biaya total persediaan.
        - Dengan EOQ = √(2DS/H):
            - Permintaan tahunan (D) = {D}
            - Biaya pesan (S) = {S}
            - Biaya simpan (H) = {H}
        - Hasil EOQ ≈ {EOQ:.2f} unit.
        - Artinya setiap kali pesan, sebaiknya {EOQ:.2f} unit agar biaya total minimum.
        """)

st.caption("✅ Aplikasi sederhana ini membantu manajer gudang atau UKM menghitung strategi pemesanan yang lebih efisien.")
