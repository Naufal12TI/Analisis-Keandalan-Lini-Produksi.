import streamlit as st
import numpy as np

st.set_page_config(page_title="Perhitungan EOQ - Toko Makmur", layout="centered")

st.title("📦 Perhitungan Economic Order Quantity (EOQ) - Toko Makmur Jaya")

st.markdown("""
Aplikasi ini membantu menghitung **jumlah pembelian optimal (EOQ)** untuk mengurangi biaya penyimpanan dan pemesanan.
""")

st.header("📌 Input Parameter")

D = st.number_input("Permintaan tahunan (kg)", min_value=1000, value=12000, step=1000)
S = st.number_input("Biaya pemesanan per order (Rp)", min_value=50000, value=150000, step=10000)
H = st.number_input("Biaya penyimpanan per kg per tahun (Rp)", min_value=500, value=1000, step=100)

st.divider()

st.header("📐 Rumus EOQ")
st.latex(r"EOQ = \sqrt{\frac{2DS}{H}}")

EOQ = np.sqrt((2 * D * S) / H)
n_order = D / EOQ
total_order_cost = n_order * S
avg_inventory = EOQ / 2
total_holding_cost = avg_inventory * H
total_cost = total_order_cost + total_holding_cost

st.subheader("✅ Hasil Perhitungan")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Jumlah Pembelian Optimal (EOQ)", value=f"{EOQ:,.2f} kg")
    st.metric(label="Jumlah Pemesanan per Tahun", value=f"{n_order:.2f} kali")
with col2:
    st.metric(label="Total Biaya Pemesanan", value=f"Rp {total_order_cost:,.0f}")
    st.metric(label="Total Biaya Penyimpanan", value=f"Rp {total_holding_cost:,.0f}")

st.success(f"💵 Estimasi Total Biaya Persediaan per Tahun: Rp {total_cost:,.0f}")

with st.expander("ℹ️ Penjelasan Konsep EOQ (bisa dibuka/tutup)"):
    st.markdown("""
    - EOQ membantu menentukan **jumlah pembelian optimal** untuk meminimalkan biaya persediaan.
    - Biaya total terdiri dari **biaya pemesanan** dan **biaya penyimpanan**.
    - Dengan membagi rata-rata stok (**EOQ/2**), kita menghitung biaya penyimpanan lebih realistis karena stok terus berkurang seiring waktu.
    """)

with st.expander("📌 Studi Kasus"):
    st.markdown("""
    **Toko Sembako Makmur Jaya**
    
    - Permintaan tahunan beras: 12.000 kg
    - Biaya pesan setiap kali order: Rp 150.000
    - Biaya penyimpanan: Rp 1.000 per kg per tahun

    Pemilik ingin mengetahui berapa kg sebaiknya dia pesan setiap kali agar total biaya persediaan paling rendah.
    """)

st.caption("Dikembangkan untuk tugas Matematika Terapan - EOQ")
