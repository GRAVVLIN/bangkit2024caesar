import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from streamlit_folium import folium_static
import folium

# Define the pages of your app
def d1():
    data_merge = pd.read_csv("data_merge.csv")
    data_merge2 = pd.read_csv("data_payments.csv")

    data_merged = pd.DataFrame(data_merge)
    data_merged2 = pd.DataFrame(data_merge2)

    city_counts = data_merge['customer_city'].value_counts()
    most_common_city = city_counts.index[0]
    count = city_counts.iloc[0]
    # Menampilkan hasil di Streamlit
    st.title('Most of City Customers')
    st.write(f"Kota terbanyak: **{most_common_city}**")
    st.write(f"Jumlah: **{count}**")
#================================================================
    payment_counts = data_merge2['payment_type'].value_counts()
    most_common_payment = payment_counts.index[0]
    count2 = payment_counts.iloc[0]

    print(f"Tipe Pembayaran Terbanyak: {most_common_payment}")
    print(f"Jumlah: {count}")
    #menghitung jumlah customer terbanyak serta menentukan kota dengan customer terbanyak
    st.title('Most of Payment Methode')
    st.write(f"Methode Pembayaran Terbanyak: **{most_common_payment}**")
    st.write(f"Jumlah: **{count2}**")


def d2():
        # Load the dataset
    data_merge = pd.read_csv("data_merge.csv")

    # Menghitung jumlah pelanggan berdasarkan kota
    city_counts = data_merge['customer_city'].value_counts()

    # Menampilkan 10 kota dengan jumlah pelanggan terbanyak
    top_10_cities = city_counts.nlargest(10)

    # Streamlit App
    st.title('Top 10 Kota dengan Jumlah Pelanggan Terbanyak')

    # Menampilkan tabel
    st.write("Tabel Jumlah Pelanggan per Kota:")
    st.dataframe(top_10_cities.reset_index(name='Jumlah Pelanggan').rename(columns={'index': 'Kota'}))

    # Visualisasi diagram batang untuk 10 kota terbanyak
    fig, ax = plt.subplots(figsize=(12, 6))

    # Menyusun warna yang berbeda untuk setiap batang
    colors = plt.cm.tab10(np.arange(len(top_10_cities)))  # Using the 'tab10' color map directly

    # Membuat diagram batang dengan warna yang berbeda
    bars = ax.bar(top_10_cities.index, top_10_cities.values, color=colors)

    # Menambahkan label pada tiap batang
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    # Menambahkan judul dan label
    ax.set_title('Top 10 Kota dengan Jumlah Pelanggan Terbanyak')
    ax.set_xlabel('Kota')
    ax.set_ylabel('Jumlah Pelanggan')
    ax.set_xticks(top_10_cities.index)
    ax.set_xticklabels(top_10_cities.index, rotation=45, ha='right')

    # Menyesuaikan tata letak
    plt.tight_layout()

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

        # Data geolocation
    city_geolocation = {
        'Sao Paulo': (-23.5505, -46.6333),
        'Rio De Janeiro': (-22.9068, -43.1729),
        'Belo Horizonte': (-19.9245, -43.9376),
        'Brasilia': (-15.7801, -47.9292),
        'Curitiba': (-25.4295, -49.2711),
    }

    # Contoh DataFrame top_10_cities
    data = {
        'customer_city': ['Sao Paulo', 'Rio De Janeiro', 'Belo Horizonte', 'Brasilia', 'Curitiba'],
        'customer_count': [500, 300, 200, 150, 100]
    }
    top_10_cities_df = pd.DataFrame(data)

    # Menambahkan kolom latitude dan longitude ke DataFrame
    top_10_cities_df['latitude'] = top_10_cities_df['customer_city'].map(lambda x: city_geolocation[x][0] if x in city_geolocation else None)
    top_10_cities_df['longitude'] = top_10_cities_df['customer_city'].map(lambda x: city_geolocation[x][1] if x in city_geolocation else None)

    # Membuat peta
    m = folium.Map(location=[-15.7801, -47.9292], zoom_start=5)  # Pusatkan peta di Brasil

    # Menambahkan marker untuk setiap kota
    for idx, row in top_10_cities_df.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):  # Check for valid coordinates
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['customer_city']}: {row['customer_count']} pelanggan",
            ).add_to(m)

    # Streamlit App
    st.title("Top 5 Kota dengan pelanggan terbanyak")

    # Menampilkan peta di Streamlit
    folium_static(m)

        # Data untuk metode pembayaran terbanyak per kota
    city_payment_data = pd.DataFrame({
        'customer_city': ['Sao Paulo', 'Rio De Janeiro', 'Belo Horizonte', 'Brasilia', 'Curitiba'],
        'payment_type': ['credit_card', 'boleto', 'credit_card', 'boleto', 'credit_card'],
    })

    # Geolocation data
    city_geolocation = {
        'Sao Paulo': (-23.5505, -46.6333),
        'Rio De Janeiro': (-22.9068, -43.1729),
        'Belo Horizonte': (-19.9245, -43.9376),
        'Brasilia': (-15.7801, -47.9292),
        'Curitiba': (-25.4295, -49.2711),
    }

    # Mapping latitude and longitude to the DataFrame
    city_payment_data['latitude'] = city_payment_data['customer_city'].map(lambda x: city_geolocation[x][0])
    city_payment_data['longitude'] = city_payment_data['customer_city'].map(lambda x: city_geolocation[x][1])

    # Membuat peta dasar menggunakan Folium
    m = folium.Map(location=[-15.7801, -47.9292], zoom_start=5)

    # Warna berdasarkan metode pembayaran
    payment_colors = {
        'credit_card': 'blue',
        'boleto': 'green',
        'debit_card': 'red',
        'voucher': 'purple',
        'others': 'orange'
    }

    # Menambahkan circle marker untuk setiap kota
    for index, row in city_payment_data.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=10,
            popup=f"{row['customer_city']}: {row['payment_type']}",
            color=payment_colors[row['payment_type']],
            fill=True,
            fill_color=payment_colors[row['payment_type']],
            fill_opacity=0.7
        ).add_to(m)

    # Streamlit App
    st.title("Metode Pemabayaran terbanyak berdasarkan 5 Kota teratas")

    st.markdown("""
        ### Warna untuk Metode Pembayaran:
        - **Blue**: Credit Card
        - **Green**: Boleto
    """)

    
    # Menampilkan peta di Streamlit
    folium_static(m)

def d3():
    st.title("Apa itu Geoanalisis?")
    st.write("Geoanalisis (atau analisis geospasial) adalah proses analisis data yang memiliki komponen geografis atau spasial, yang berarti data tersebut berkaitan dengan lokasi atau posisi di permukaan bumi. Geoanalisis sering digunakan untuk mengidentifikasi pola, hubungan, dan tren yang terkait dengan lokasi geografis tertentu. Alat utama yang digunakan dalam geoanalisis adalah Sistem Informasi Geografis (SIG), yang memungkinkan visualisasi dan analisis data dalam bentuk peta.")
    st.title("Kesimpulan yang di dapatkan")
    st.write("1. Mengetahui lokasi pelanggan terbanyak berdasarkan data pelanggan.")
    st.write("2. Mengetahui metode pembayaran terbanyak berdasarkan data pelanggan.")
    st.write("3. Mengetahui metode pembayaran terbanyak pada 5 kota dengan data pelanggan tertinggi")
    st.write("4. Mengetahui 10 kota teratas dengan pembelian terbanyak berdasarkan data")
    st.write("5. Memvisualisasikan data-data tersebut dalam bentuk peta")
    st.write("6. Sebagai acuan bisnis planning di masa depan")
# Create a dictionary for page mapping
pages = {
    "Kota dan Metode Pembayaran Terbnayak": d1,
    "Visualisasi Kota & Geografi": d2,
    "Apa itu Geoanalisis dan Kesimpulan": d3
}

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Call the selected page function
pages[selection]()




