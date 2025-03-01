import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

huairou_df = pd.read_csv('dashboard/data.csv')

with st.sidebar:
    st.write("Istia Budi")
    st.write("istiabudi@gmail.com")

yearly_avg = huairou_df.groupby("year")[['PM2.5', 'PM10']].mean()

st.header("Air Quality Dataset - Huairou Station")

st.subheader("Bagaimana kondisi materi partikulat PM(2.5) dan PM(10) yang dimonitoring pada stasiun Huairou tiap tahun")
years = huairou_df["year"].unique()
selected_years = st.slider("Pilih rentang tahun:", int(years.min()), int(years.max()), (int(years.min()), int(years.max())))

filtered_data = yearly_avg.loc[selected_years[0]:selected_years[1]]

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_data, markers=True, ax=ax)
ax.set_title("Tren Tahunan PM₂.₅ dan PM₁₀ di Stasiun Huairou")
ax.set_xlabel("Tahun")
ax.set_ylabel("Konsentrasi (µg/m³)")
ax.legend(["PM₂.₅", "PM₁₀"])
ax.grid(True)
st.pyplot(fig)

with st.expander("Lihat Analisis"):
    st.write(
        """
        Kondisi materi partikulat yang dimonitoring pada stasiun Huairou dalam rentang 1 Maret 2013 hingga 28 Februari 2017 mengalami penurunan yang cukup baik. Artinya pemerintah Beijing cukup baik dalam melakukan mengurangi polusi udara.
"""
    )

st.subheader("Apakah jam sibuk mempengaruhi polusi udara dibanding tengah malam?")

huairou_df['time_category'] = 'Other'
huairou_df.loc[huairou_df['hour'].between(7, 9), 'time_category'] = 'Rush Hour (Morning)'
huairou_df.loc[huairou_df['hour'].between(17, 19), 'time_category'] = 'Rush Hour (Evening)'
huairou_df.loc[huairou_df['hour'].between(0, 4), 'time_category'] = 'Midnight'

st.title("Distribusi PM₂.₅ pada Jam Sibuk vs Tengah Malam")

selected_category = st.selectbox("Pilih kategori waktu:", ['All', 'Rush Hour (Morning)', 'Rush Hour (Evening)', 'Midnight'])

if selected_category != 'All':
    filtered_data = huairou_df[huairou_df['time_category'] == selected_category]
else:
    filtered_data = huairou_df

fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(data=filtered_data, x='PM2.5', hue='time_category', bins=30, kde=True, palette='coolwarm', element='step', common_norm=False, ax=ax)
ax.set_title('Distribusi PM2.5 pada Jam Sibuk vs Tengah Malam')
ax.set_xlabel('Konsentrasi PM2.5 (µg/m³)')
ax.set_ylabel('Frekuensi')
ax.grid(True)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(data=filtered_data, x='PM10', hue='time_category', bins=30, kde=True, palette='coolwarm', element='step', common_norm=False, ax=ax)
ax.set_title('Distribusi PM10 pada Jam Sibuk vs Tengah Malam')
ax.set_xlabel('Konsentrasi PM10 (µg/m³)')
ax.set_ylabel('Frekuensi')
ax.grid(True)

st.pyplot(fig)

with st.expander("Lihat Analisis"):
    st.write(
        """
        Jam sibuk tidak selalu meningkatkan polusi udara secara signifikan, karena distribusi Midnight dan Other masih cukup tinggi. Sumber polusi lain selain kendaraan mungkin lebih dominan, seperti aktivitas industri atau kondisi cuaca yang menyebabkan akumulasi polutan. Sebagian besar polusi udara berada di level rendah, tetapi ada outlier tinggi yang bisa disebabkan oleh faktor ekstrem.
        """
    )