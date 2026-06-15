import streamlit as st
import time

st.title("📊 Visualisasi Sorting")

# 1. Kontrol UI Input Data & Algoritma
col1, col2 = st.columns(2)
algo = col1.selectbox("Pilih Algoritma", ["Bubble Sort", "Selection Sort", "Insertion Sort"])
user_input = col2.text_input("Input Data (pisahkan koma)", "85, 60, 92, 75, 88")

# 2. Keterangan Algoritma Dinamis
if algo == "Bubble Sort":
    st.info("💡 **Bubble Sort**: Membandingkan elemen bersebelahan & menukarnya jika salah urutan. Elemen terbesar 'menggelembung' ke akhir.")
elif algo == "Selection Sort":
    st.info("💡 **Selection Sort**: Memilih elemen terkecil dari bagian yang belum terurut, lalu menukarnya ke posisi paling depan.")
elif algo == "Insertion Sort":
    st.info("💡 **Insertion Sort**: Bekerja seperti mengurutkan kartu; menyisipkan elemen satu per satu ke posisi yang tepat di bagian yang sudah terurut.")

# 3. Keamanan Input (Parsing Teks ke Angka)
try:
    data = [int(x.strip()) for x in user_input.split(",") if x.strip()]
except ValueError:
    st.error("Gagal! Pastikan Anda hanya memasukkan angka.")
    st.stop()

# 4. Area Gambar Grafik
chart = st.empty()
chart.bar_chart(data)

# 5. Tombol & Logika Sorting Utama
if st.button("Mulai Urutkan", type="primary"):
    n = len(data)
    
    if algo == "Bubble Sort":
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]  # Tukar posisi
                    chart.bar_chart(data)
                    time.sleep(0.2)
                    
    elif algo == "Selection Sort":
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]  # Tukar ke depan
            chart.bar_chart(data)
            time.sleep(0.2)
            
    elif algo == "Insertion Sort":
        for i in range(1, n):
            key = data[i]
            j = i - 1
            while j >= 0 and data[j] > key:
                data[j + 1] = data[j]  # Geser ke kanan
                j -= 1
                chart.bar_chart(data)
                time.sleep(0.2)
            data[j + 1] = key
            chart.bar_chart(data)
            time.sleep(0.2)
            
    st.success(f"Sorting Selesai! Hasil: {data}")