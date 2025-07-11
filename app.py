st.markdown("## 3️⃣ 🔧 Input & Tabel Keandalan Mesin")
st.caption("⚙️ Silakan atur keandalan mesin di slider kiri. Tabel kanan otomatis menyesuaikan.")

col_slider, col_table = st.columns(2)

with col_slider:
    st.subheader("🎚️ Slider Input")
    r1 = st.slider("Stamping", 80, 100, 98, 1)
    r2 = st.slider("Welding", 80, 100, 99, 1)
    r3 = st.slider("Painting", 80, 100, 96, 1)
    r4 = st.slider("Assembly", 80, 100, 97, 1)
    st.caption("✅ Geser untuk simulasi perawatan atau peningkatan keandalan.")

with col_table:
    st.subheader("📊 Tabel Ringkasan")
    st.table({
        "Mesin": ["Stamping", "Welding", "Painting", "Assembly"],
        "Keandalan (%)": [r1, r2, r3, r4]
    })
    st.caption("✅ Tabel ini membantu memastikan input sudah sesuai.")
