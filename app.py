# eoq_app.py
import streamlit as st
import numpy as np

# Judul halaman
st.title("📦 Aplikasi Perhitungan EOQ (Economic Order Quantity)")

# Studi Kasus
with st.expander("ℹ️ Studi Kasus (Klik untuk lihat)"):
    st.markdown("""
    *Toko Sembako “Makmur Jaya”*  
    Toko “Makmur Jaya” menjual beras dengan permintaan tahunan 12.000 kg.  
    Biaya pemesanan tiap kali order Rp150.000, dan biaya penyimpanan per kg per tahun Rp1.000.  
    Pemilik ingin menghitung jumlah pemesanan optimal (EOQ) untuk menekan total biaya persediaan.
    """)

# Deskripsi Aplikasi & Rumus
with st.expander("💡 Deskripsi & Rumus (Klik untuk lihat)"):
    st.markdown(r"""
    Aplikasi ini menghitung *jumlah pemesanan optimal (EOQ)* yang meminimalkan total biaya persediaan.
    
    **Rumus EOQ:**
    $$
    EOQ = \sqrt{ \frac{2DS}{H} }
    $$
    - D = Permintaan tahunan (kg)
    - S = Biaya pemesanan per order (Rp)
    - H = Biaya penyimpanan per kg per tahun (Rp)
    
    **Contoh Perhitungan Manual:**
    $$
    EOQ = \sqrt{ \frac{2 \times 12,000 \times 150,000}{1,000} } = \sqrt{3,600,000} = 1,897.37 \text{ kg}
    $$
    Dengan nilai di atas, toko disarankan memesan sekitar **1.897 kg per order** agar total biaya persediaan minimum.
    """)

# Sidebar Input
st.sidebar.header("📌 Input Parameter")
D = st.sidebar.number_input("Permintaan tahunan (kg)", value=12000, min_value=1)
S = st.sidebar.number_input("Biaya pemesanan per order (Rp)", value=150000, min_value=1)
H = st.sidebar.number_input("Biaya penyimpanan per kg per tahun (Rp)", value=1000, min_value=1)

# Hitung EOQ
EOQ = np.sqrt((2 * D * S) / H)
num_orders = D / EOQ
total_ordering_cost = num_orders * S
average_inventory = EOQ / 2
total_holding_cost = average_inventory * H
total_cost = total_ordering_cost + total_holding_cost

# Hasil Perhitungan
st.header("✅ Hasil Perhitungan EOQ")
col1, col2 = st.columns(2)

with col1:
    st.metric("📦 Jumlah Pemesanan Optimal (EOQ)", f"{EOQ:.2f} kg")
    st.metric("📈 Jumlah Pesan per Tahun", f"{num_orders:.2f} kali")

with col2:
    st.metric("💰 Total Biaya Pemesanan", f"Rp {total_ordering_cost:,.0f}")
    st.metric("💰 Total Biaya Penyimpanan", f"Rp {total_holding_cost:,.0f}")

st.subheader("💵 Estimasi Total Biaya Persediaan")
st.success(f"Total biaya tahunan diperkirakan: Rp {total_cost:,.0f}")

# Penjelasan Singkat (untuk presentasi)
with st.expander("🗂️ Penjelasan Konsep (Klik untuk bantu presentasi)"):
    st.markdown("""
    - *EOQ (Economic Order Quantity)* adalah jumlah pembelian optimal yang meminimalkan total biaya persediaan.
    - Biaya total terdiri dari *biaya pemesanan* dan *biaya penyimpanan*.
    - Dengan menghitung EOQ, pemilik usaha bisa menekan biaya logistik dan membuat sistem persediaan lebih efisien.
    - Aplikasi ini dapat digunakan untuk simulasi berbagai skenario biaya dan permintaan.
    """)
