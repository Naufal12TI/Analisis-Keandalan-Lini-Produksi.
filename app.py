# eoq_app_v2.py
import streamlit as st
import numpy as np

# Judul halaman
st.title("📦 Aplikasi Perhitungan EOQ (Economic Order Quantity)")

# Studi Kasus
with st.expander("ℹ Studi Kasus (Klik untuk lihat)"):
    st.markdown("""
    *Toko Sembako “Makmur Jaya”*  
    Toko ini menjual beras dengan permintaan tahunan sebesar **12.000 kg**.  
    Biaya pemesanan setiap kali order adalah **Rp150.000**, dan biaya penyimpanan per kg per tahun adalah **Rp1.000**.  
    Pemilik ingin menghitung jumlah pemesanan optimal (EOQ) untuk menekan total biaya persediaan.
    """)

# Deskripsi Aplikasi dan Rumus
with st.expander("💡 Deskripsi & Rumus (Klik untuk lihat)"):
    st.markdown("""
    Aplikasi ini menghitung *jumlah pemesanan optimal (EOQ)* yang meminimalkan total biaya persediaan.

    ### Rumus EOQ:
    $$
    EOQ = \sqrt{\frac{2DS}{H}}
    $$
    - **D** = Permintaan tahunan (kg)
    - **S** = Biaya pemesanan per order (Rp)
    - **H** = Biaya penyimpanan per kg per tahun (Rp)

    ### Contoh Perhitungan Manual:
    Misalnya:
    - D = 12.000 kg
    - S = Rp150.000
    - H = Rp1.000

    Maka:
    $$
    EOQ = \sqrt{\frac{2 \times 12000 \times 150000}{1000}} = \sqrt{3.600.000} = 1897.37\text{ kg}
    $$

    Jadi, jumlah pemesanan optimal adalah sekitar **1.897 kg** per order.
    """)

# Sidebar Input
st.sidebar.header("📌 Input Parameter")
D = st.sidebar.number_input("Permintaan tahunan (kg)", value=12000, min_value=1)
S = st.sidebar.number_input("Biaya pemesanan per order (Rp)", value=150000, min_value=1)
H = st.sidebar.number_input("Biaya penyimpanan per kg per tahun (Rp)", value=1000, min_value=1)

# Hitung EOQ
EOQ = np.sqrt((2 * D * S) / H)
num_orders = D / EOQ
ordering_cost = num_orders * S
avg_inventory = EOQ / 2
holding_cost = avg_inventory * H
total_cost = ordering_cost + holding_cost

# Hasil Perhitungan
st.header("✅ Hasil Perhitungan EOQ")
col1, col2 = st.columns(2)

with col1:
    st.metric("📦 Jumlah Pemesanan Optimal (EOQ)", f"{EOQ:.2f} kg")
    st.metric("📈 Jumlah Pesan per Tahun", f"{num_orders:.2f} kali")

with col2:
    st.metric("💰 Total Biaya Pemesanan", f"Rp {ordering_cost:,.0f}")
    st.metric("💰 Total Biaya Penyimpanan", f"Rp {holding_cost:,.0f}")

st.subheader("💵 Estimasi Total Biaya Persediaan")
st.success(f"Total biaya tahunan diperkirakan: Rp {total_cost:,.0f}")

# Penjelasan Konsep
with st.expander("🗂 Penjelasan Konsep (Klik untuk bantu presentasi)"):
    st.markdown("""
    - *EOQ (Economic Order Quantity)* adalah metode untuk menghitung jumlah pemesanan paling optimal agar biaya tidak membengkak.
    - Dengan EOQ, kita mencari keseimbangan antara *biaya pemesanan* dan *biaya penyimpanan*.
    - Terlalu sering pesan = biaya pesan mahal.  
      Terlalu banyak stok = biaya simpan mahal.
    - EOQ membantu cari titik optimal dari dua biaya itu.
    """)
