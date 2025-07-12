import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Aplikasi Statistik Deskriptif", layout="wide")

# -----------------------------------
# 1️⃣ Judul & Deskripsi
# -----------------------------------
st.title("📊 Aplikasi Simulasi Statistik Deskriptif")
st.markdown("""
Aplikasi ini digunakan untuk menghitung **mean, median, modus, varians, dan standar deviasi** dari dataset yang diinput.

✅ Cocok untuk tugas Matematika Terapan.  
✅ Bisa input manual atau upload CSV.  
✅ Disertai visualisasi boxplot / histogram.
""")

# -----------------------------------
# 2️⃣ Input Data
# -----------------------------------
st.header("1️⃣ Input Data")
input_mode = st.radio("Pilih cara input data:", ["Manual", "Upload CSV"], horizontal=True)

if input_mode == "Manual":
    manual_data = st.text_area("Masukkan data (pisahkan dengan koma)", "70, 75, 80, 85, 90")
    try:
        data_list = [float(i.strip()) for i in manual_data.split(",")]
        df = pd.DataFrame({"Data": data_list})
    except:
        st.error("Pastikan input berupa angka dipisah koma.")
        st.stop()

else:
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File berhasil diupload.")
    else:
        st.warning("Silakan upload file CSV untuk melanjutkan.")
        st.stop()

# -----------------------------------
# 3️⃣ Tabel Data Input
# -----------------------------------
st.subheader("2️⃣ Tabel Data")
st.dataframe(df, use_container_width=True)

# -----------------------------------
# 4️⃣ Ringkasan Statistik
# -----------------------------------
st.subheader("3️⃣ Ringkasan Statistik Deskriptif")

if 'Data' in df.columns:
    data_col = df['Data']
else:
    data_col = df.iloc[:,0]

mean_val = np.mean(data_col)
median_val = np.median(data_col)
mode_val = data_col.mode().iloc[0]
var_val = np.var(data_col, ddof=1)
std_val = np.std(data_col, ddof=1)

col1, col2, col3 = st.columns(3)
col1.metric("Mean", f"{mean_val:.2f}")
col2.metric("Median", f"{median_val:.2f}")
col3.metric("Mode", f"{mode_val:.2f}")

col4, col5 = st.columns(2)
col4.metric("Varians", f"{var_val:.2f}")
col5.metric("Standar Deviasi", f"{std_val:.2f}")

# -----------------------------------
# 5️⃣ Penjelasan Konsep Matematis
# -----------------------------------
with st.expander("📐 Penjelasan Konsep & Rumus"):
    st.markdown("""
    **📌 Konsep Statistik Dasar**
    - Mean = Rata-rata
    - Median = Nilai tengah
    - Modus = Nilai yang paling sering muncul
    - Varians = Rata-rata kuadrat selisih dari mean
    - Standar Deviasi = Akar kuadrat varians
    
    **🔢 Rumus:**
    - Mean:  \\( \\bar{x} = \\frac{1}{n} \\sum_{i=1}^n x_i \\)
    - Varians:  \\( s^2 = \\frac{1}{n-1} \\sum_{i=1}^n (x_i - \\bar{x})^2 \\)
    - Standar Deviasi:  \\( s = \\sqrt{s^2} \\)
    
    📌 Interpretasi:
    - Nilai varians & SD tinggi = Data tersebar lebar.
    - Nilai varians & SD rendah = Data homogen.
    """)

# -----------------------------------
# 6️⃣ Visualisasi Boxplot & Histogram
# -----------------------------------
st.subheader("4️⃣ Visualisasi Data")
plot_type = st.selectbox("Pilih jenis grafik", ["Boxplot", "Histogram"])

fig, ax = plt.subplots()
if plot_type == "Boxplot":
    sns.boxplot(y=data_col, ax=ax)
    ax.set_title("Boxplot Data")
else:
    sns.histplot(data_col, bins=10, kde=True, ax=ax)
    ax.set_title("Histogram Data")
st.pyplot(fig)

# -----------------------------------
# 7️⃣ Footer / Credit
# -----------------------------------
st.markdown("---")
st.caption("Dikembangkan oleh Naufal Khoirul Ibrahim – Matematika Terapan")
