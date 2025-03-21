import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.markdown("""
    <style>
        .stMarkdown h1, .stMarkdown h2 {
            text-align: center;
        }
        p {
            font-size: 22px;
            font-weight: bold;
        }
        .stSelectbox {
            margin-bottom: 50px;
        }
    </style>
    """, unsafe_allow_html=True)

day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

st.markdown("<h1 style='text-align: center;'>Proyek Analisis Data</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Dashboard Bike Sharing Dataset</h2>", unsafe_allow_html=True)

chart_options = [
    "Perbandingan Jumlah Penyewaan Sepeda Tahun 2011 dan 2012",
    "Persentase Jumlah Penyewaan Sepeda pada Weekday dan Weekend",
    "Pengaruh Kecepatan Angin Terhadap Jumlah Penyewaan Sepeda",
    "Rata-Rata Jumlah Penyewaan Sepeda Untuk Setiap Jam",
    "Rata-Rata Jumlah Penyewaan Sepeda Untuk Setiap Hari"
]
selected_chart = st.selectbox("Silahkan pilih Data yang ingin diampilkan:", chart_options)


if selected_chart == "Perbandingan Jumlah Penyewaan Sepeda Tahun 2011 dan 2012":
    with st.container():
        st.markdown("<p>Perbandingan Jumlah Penyewaan Sepeda Tahun 2011 dan 2012</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
            selected_season = st.selectbox("Pilih Musim:", ["Semua"] + list(season_mapping.values()))

            filtered_df = day_df.copy()
            if selected_season != "Semua":
                filtered_df = filtered_df[filtered_df["season"].map(season_mapping) == selected_season]

            year_counts_df = filtered_df.groupby(by='yr').cnt.sum()
            year_counts_df.index = year_counts_df.index.map({0: 2011, 1: 2012})
            fig, ax = plt.subplots(figsize=(10, 5))
            year_counts_df.plot(kind='bar', ax=ax)
            ax.set_xticklabels(year_counts_df.index, rotation=0)
            ax.set_xlabel('Tahun')
            ax.set_ylabel('Jumlah Penyewaan Sepeda')
            ax.set_title('Jumlah Penyewaan Sepeda per Tahun')
            st.pyplot(fig)

        with col2:
            selected_year = st.selectbox("Pilih Tahun:", ["Semua", 2011, 2012])

            seasonal_counts = day_df.groupby(['yr', 'season'])['cnt'].sum().reset_index()
            seasonal_counts_pivot = seasonal_counts.pivot(index='season', columns='yr', values='cnt')
            seasonal_counts_pivot['selisih'] = seasonal_counts_pivot[1] - seasonal_counts_pivot[0]

            seasonal_counts_pivot = seasonal_counts_pivot.rename(index={1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

            if selected_year in [2011, 2012]:
                if selected_year == 2011:
                    year_col = 0
                else:
                    year_col = 1
            else:
                year_col = 'selisih'

            fig, ax = plt.subplots(figsize=(10, 5))
            seasonal_counts_pivot[year_col].plot(kind='line', ax=ax, color='red')
            ax.set_xlabel('Musim', size=12)
            ax.set_ylabel('Selisih Penyewaan Sepeda', size=12)
            ax.set_title('Selisih Penyewaan Sepeda per Musim')
            st.pyplot(fig)


elif selected_chart == "Persentase Jumlah Penyewaan Sepeda pada Weekday dan Weekend":
    with st.container():
        st.markdown("<p>Persentase Jumlah Penyewaan Sepeda pada Weekday dan Weekend</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            selected_year = st.selectbox("Pilih Tahun:", [2011, 2012])

        with col2:
            months = [
                "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                "Juli", "Agustus", "September", "Oktober", "November", "Desember"
            ]
            selected_month = st.selectbox("Pilih Bulan:", months)
            month_number = months.index(selected_month) + 1 

        filtered_df = day_df[(day_df["yr"] == [2011, 2012].index(selected_year)) & (day_df["mnth"] == month_number)]

        workingday_counts_df = filtered_df.groupby(by='workingday').cnt.sum()
        workingday_counts_df = workingday_counts_df.rename({0: 'Weekend', 1: 'Weekday'})

        fig, ax = plt.subplots(figsize=(10, 5))
        workingday_counts_df.plot(kind='pie', ax=ax, autopct='%1.1f%%')
        ax.set_ylabel('')
        ax.set_title('Perbandingan jumlah Penyewaan Sepeda pada Hari Libur dan Hari Kerja')
        st.pyplot(fig)

elif selected_chart == "Pengaruh Kecepatan Angin Terhadap Jumlah Penyewaan Sepeda":
    with st.container():
        st.markdown("<p>Pengaruh Kecepatan Angin Terhadap Jumlah Penyewaan Sepeda</p>", unsafe_allow_html=True)
        min_wind, max_wind = st.slider(
            "Pilih Rentang Kecepatan Angin:",
            min_value=float(day_df["windspeed"].min()),
            max_value=float(day_df["windspeed"].max()),
            value=(0.0, 1.0)
        )

        filtered_df = day_df[(day_df["windspeed"] >= min_wind) & (day_df["windspeed"] <= max_wind)]
        bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1]
        labels = ['0-0.1', '0.1-0.2', '0.2-0.3', '0.3-0.4', '0.4-0.5', '0.5+']
        filtered_df['windspeed_bin'] = pd.cut(filtered_df['windspeed'], bins=bins, labels=labels)

        windspeed_counts_df = filtered_df.groupby('windspeed_bin', observed=False)['cnt'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        windspeed_counts_df.plot(kind='bar', ax=ax)
        ax.set_xticklabels(windspeed_counts_df.index, rotation=0)
        ax.set_xlabel('Kecepatan Angin')
        ax.set_ylabel('Jumlah Penyewaan Sepeda')
        ax.set_title('Jumlah Penyewaan Sepeda berdasarkan Kecepatan Angin')
        st.pyplot(fig)

elif selected_chart == "Rata-Rata Jumlah Penyewaan Sepeda Untuk Setiap Jam":
    with st.container():
        st.markdown("<p>Rata-Rata Jumlah Penyewaan Sepeda Untuk Setiap Jam</p>", unsafe_allow_html=True)

        selected_day = st.selectbox("Pilih Hari:", ["Semua", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])
    
        filtered_df = hour_df.copy()
        if selected_day != "Semua":
            day_mapping = {"Minggu": 0, "Senin": 1, "Selasa": 2, "Rabu": 3, "Kamis": 4, "Jumat": 5, "Sabtu": 6}
            filtered_df = filtered_df[filtered_df["weekday"] == day_mapping[selected_day]]

        hour_counts_df = filtered_df.groupby(by='hr').cnt.mean()

        fig, ax = plt.subplots(figsize=(10, 5))
        hour_counts_df.plot(kind='line', ax=ax, color='green')
        ax.set_xticks(range(0, 24, 1))
        ax.set_xticklabels(range(0, 24), rotation=0)
        ax.set_xlabel('Jam', size=12)
        ax.set_ylabel('Rata-Rata Jumlah Penyewaan Sepeda', size=12)
        ax.set_title('Rata-Rata Jumlah Penyewaan Sepeda per Jam')
        st.pyplot(fig)

elif selected_chart == "Rata-Rata Jumlah Penyewaan Sepeda Untuk Setiap Hari":
    with st.container():
        st.markdown("<p>Rata-Rata Jumlah Penyewaan Sepeda Untuk Setiap Hari</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            selected_year = st.selectbox("Pilih Tahun:", ["Semua", 2011, 2012])

        with col2:
            season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
            selected_season = st.selectbox("Pilih Musim:", ["Semua"] + list(season_mapping.values()))

        filtered_df = day_df.copy()
        if selected_year in [2011, 2012]:
            filtered_df = filtered_df[filtered_df["yr"] == (selected_year - 2011)]

        if selected_season != "Semua":
            filtered_df = filtered_df[filtered_df["season"].map(season_mapping) == selected_season]


        weekday_counts_df = filtered_df.groupby(by='weekday').cnt.mean()
        weekday_counts_df = weekday_counts_df.rename({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'})
        fig, ax = plt.subplots(figsize=(10, 5))
        weekday_counts_df.plot(
            kind='pie',
            ax=ax,
            autopct='%1.2f%%',
            wedgeprops={'width': 0.6},
            textprops={'color': 'black', 'fontsize': 12}
            )
        ax.set_ylabel('')
        ax.set_title('Rata-Rata Jumlah Penyewaan Sepeda per Hari')
        st.pyplot(fig)