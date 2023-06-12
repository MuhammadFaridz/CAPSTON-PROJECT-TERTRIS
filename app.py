import streamlit as st
import pandas as pd
import altair as alt
import matplotlib
matplotlib.use('Agg')
import numpy as np

import matplotlib.pyplot as plt
from scipy import stats
from PIL import Image

#content-start
st.set_page_config(layout="wide")
st.title('FORECASTING OF ENERGY CONSUMPTION AND CO2 EMISSIONS IN INDONESIA, FOR SUSTAINABLE ENERGY DECISION MAKING')
#st.write('sumber data : https://yearbook.enerdata.net/ ')
st.write('https://www.linkedin.com/in/mhd-farid/')
st.write('oleh : **Muhammad Farid**')

#image = Image.open('polusikota.JPG')
#st.image(image, caption='https://pixabay.com/id/photos/pembangkit-listrik-3431136/')
#st.write('Negara indonesia menggunakan minyak, gas dan batu bara sebagai sumber utama pembangkit listrik. hal tersebut telah menjadikan polusi udara sebagai risiko utama bagi kesehatan masyarakat dan telah meningkatkan emisi karbon dioksida (CO2) terkait energi. Menurut WHO (2020), pada tahun 2016 diperkirakan 2,4 juta kematian dini disebabkan oleh polusi uara. masalah yang dihadapi saat ini adalah Peningkatan emisi Karbon Dioksida (CO2) akibat penggunaan sumber minyak, gas dan batubara untuk pembangkit listrik. dan Menipisnya sumber daya yang langka (yaitu minyak, gas dan batu bara). bagaimana prediksi konsumsi energi kedepannya untuk indonesia? dan bagaimana solusinya?  ')

df = pd.read_excel("C:/Users/ASUS/Downloads/ENERGI_INDONESIA.xlsx")
#df

import altair as alt
import streamlit as st
import pandas as pd
import pmdarima as pm
import pandas as pd



# Mengubah tipe data kolom Tahun menjadi integer
df['Tahun'] = pd.to_datetime(df['Tahun'], format='%Y').dt.year

# Menentukan model dengan menggunakan metode Auto ARIMA
model = pm.auto_arima(df['Konsumsi_Energi'], start_p=1, start_q=1,
                      test='adf',       # Menentukan jenis uji hipotesis
                      max_p=3, max_q=3, # Nilai maksimum untuk p dan q
                      m=1,              # Periode data (1 untuk data tahunan)
                      d=None,           # Nilai yang digunakan untuk differencing (None untuk otomatis)
                      seasonal=False,   # Non-seasonal data
                      start_P=0,        # Awal nilai seasonal P
                      D=0,              # Nilai yang digunakan untuk seasonal differencing
                      trace=True,       # Tampilkan langkah-langkah model
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)   # Pencarian parameter secara iteratif

# Melatih model ARIMA dengan parameter terbaik
model_fit = model.fit(df['Konsumsi_Energi'])

# Sidebar - Input jumlah tahun prediksi
n_years = st.sidebar.number_input('Masukkan Jumlah Tahun Prediksi', min_value=1, max_value=50, value=5)

# Mengambil data konsumsi energi terakhir
last_energy_consumption = df['Konsumsi_Energi'].iloc[-1]

# Melakukan prediksi untuk n tahun ke depan
forecast = model_fit.predict(n_periods=n_years)

# Membuat DataFrame untuk hasil prediksi
prediksi_df = pd.DataFrame({'Tahun': range(df['Tahun'].max() + 1, df['Tahun'].max() + n_years + 1),
                            'Prediksi_Konsumsi_Energi': forecast})

# Menampilkan hasil prediksi
st.write('Hasil Prediksi Konsumsi Energi:')
st.write(prediksi_df)



# CHART 1
# Sidebar - Year range slider
start_year = st.sidebar.slider("Pilih Tahun Awal", min_value=int(df["Tahun"].min()), max_value=int(df["Tahun"].max()), value=int(df["Tahun"].min()), step=1)
end_year = st.sidebar.slider("Pilih Tahun Akhir", min_value=int(df["Tahun"].min()), max_value=int(df["Tahun"].max()), value=int(df["Tahun"].max()), step=1)
# Filter data based on selected year range
filtered_df = df[(df["Tahun"] >= start_year) & (df["Tahun"] <= end_year)]
# Melt the dataframe to convert it into long format
melted_df = filtered_df.melt(id_vars='Tahun', value_vars=['Produksi_Energi', 'Konsumsi_Energi'], var_name='Jenis', value_name='Energi (Mtoe)')
# Create Altair chart
chart1 = alt.Chart(melted_df).mark_bar().encode(
    x='Tahun',
    y='Energi (Mtoe)',
    color='Jenis',
    tooltip=['Tahun', 'Jenis', 'Energi (Mtoe)']
).properties(
    width=600,
    height=400,
    title='Pertumbuhan Produksi dan Konsumsi Energi'
)
# Display the chart
st.altair_chart(chart1, use_container_width=True)
st.write('konsumsi energi di Indonesia mengalami peningkatan dari tahun ke tahun. Insight ini mengindikasikan bahwa permintaan energi terus meningkat seiring dengan pertumbuhan ekonomi dan populasi. Rekomendasi yang dapat diberikan adalah untuk mengembangkan strategi pengelolaan energi yang efisien dan berkelanjutan guna menghadapi permintaan energi yang terus meningkat.')




#CHART 2
# Create Altair chart
chart2 = alt.Chart(filtered_df).transform_fold(
    ['Produksi_Listrik', 'Konsumsi_Listrik'],
    as_=['Jenis', 'Jumlah (TWh)']
).mark_line(point=True).encode(
    x='Tahun:O',
    y=alt.Y('Jumlah (TWh):Q', title='Jumlah (TWh)'),
    color=alt.Color('Jenis:N', legend=alt.Legend(title=''),
                    scale=alt.Scale(scheme='category10')),
    tooltip=['Tahun:O', 'Jenis:N', alt.Tooltip('Jumlah (TWh):Q', title='Jumlah (TWh)')]
).properties(
    width=600,
    height=400,
    title='Produksi dan Konsumsi Listrik (TWh)'
).configure_title(
    align='center'
)

# Display the chart
st.altair_chart(chart2, use_container_width=True)
st.write('Produksi dan konsumsi listrik terus meningkat dari tahun ke tahun. Ini mencerminkan peningkatan aksesibilitas listrik dan kebutuhan energi listrik yang semakin besar di Indonesia.')





# Bar plot
chart3 = alt.Chart(filtered_df).transform_fold(
    ['Kontribusi_Energi_Terbarukan_Untuk_Total_Energi_Listrik(%)', 'Kontribusi_Energi_Angin_Matahari_Untuk_Total_Energi_Listrik(%)'],
    as_=['Energi', 'Kontribusi (%)']
).mark_bar().encode(
    x='Tahun:O',
    y='Kontribusi (%):Q',
    color='Energi:N',
    tooltip=['Tahun:O', 'Energi:N', 'Kontribusi (%):Q']
).properties(
    width=600,
    height=400,
    title='Kontribusi Energi Terbarukan Energi Angin dan Matahari dalam Produksi Listrik'
).configure_title(
    align='center'
)
# Display the chart
st.altair_chart(chart3, use_container_width=True)
st.write('persentase kontribusi energi terbarukan dalam produksi listrik. Insight ini menunjukkan bahwa seiring berjalannya waktu, kontribusi energi terbarukan dalam sektor listrik telah meningkat secara bertahap. Rekomendasi yang dapat diberikan adalah untuk terus mendorong pengembangan dan investasi dalam energi terbarukan guna mengurangi ketergantungan pada sumber energi konvensional yang terbatas dan berdampak negatif pada lingkungan.kontribusi energi terbarukan dalam produksi listrik yang meningkat seiring waktu. Ini menunjukkan upaya untuk beralih ke sumber energi yang lebih berkelanjutan dan ramah lingkungan.')


# CHART 4
chart4 = alt.Chart(filtered_df).transform_fold(
    ['Produksi_Batubara_Lignit', 'Konsumsi_Batubara_Lignit'],
    as_=['Jenis', 'Jumlah (Mt)'
]).mark_line(point=True).encode(
    x='Tahun:O',
    y=alt.Y('Jumlah (Mt):Q', title='Jumlah (Mt)'),
    color=alt.Color('Jenis:N', legend=alt.Legend(title=''),
                    scale=alt.Scale(scheme='category10')),
    tooltip=['Tahun:O', 'Jenis:N', alt.Tooltip('Jumlah (Mt):Q', title='Jumlah (Mt)')]
).properties(
    width=600,
    height=400,
    title='Produksi dan Konsumsi Batubara dan Lignit'
).configure_title(
    align='center'
)
# Display the chart
st.altair_chart(chart4, use_container_width=True)
st.write('Produksi dan konsumsi batubara dan ligint mengalami fluktuasi sepanjang tahun')



# CHART 5
chart5 = alt.Chart(filtered_df).mark_line(point=True, color='red').encode(
    x='Tahun:O',
    y=alt.Y('Emisi_Co2_Dari_Bahan_Bakar:Q', title='Jumlah Emisi CO2'),
    tooltip=['Tahun:O', alt.Tooltip('Emisi_Co2_Dari_Bahan_Bakar:Q', title='Jumlah Emisi CO2')]
)
# Overlay area plot
area = alt.Chart(filtered_df).mark_area(color='red', opacity=0.2).encode(
    x='Tahun:O',
    y='Emisi_Co2_Dari_Bahan_Bakar:Q'
)
# Combine the line chart and area plot
chart5 = (chart5 + area).configure_title(
    align='center'
).properties(
    width=600,
    height=400,
    title='Emisi CO2 dari Pembakaran Bahan Bakar (MtCO2)'
)
# Display the chart
st.altair_chart(chart5, use_container_width=True)
st.write(' Emisi CO2 dari pembakaran bahan bakar mengalami peningkatan seiring dengan peningkatan produksi dan konsumsi energi. Ini menekankan pentingnya pengelolaan emisi gas rumah kaca dalam upaya menjaga lingkungan dan mengurangi dampak perubahan iklim.  emisi CO2 dari pembakaran bahan bakar dapat menjadi pemacu untuk mengurangi emisi tersebut. Rekomendasi yang dapat diberikan adalah meningkatkan efisiensi penggunaan bahan bakar, mengadopsi teknologi ramah lingkungan dalam sektor transportasi dan industri, dan mendorong penggunaan energi terbarukan dalam sektor energi.')




# Chart 6
chart6 = alt.Chart(filtered_df).mark_line(point=True, color='Orage').encode(
    x='Tahun:O',
    y=alt.Y('Faktor_Emisi_Co2:Q', title='Faktor Emisi CO2'),
    tooltip=['Tahun:O', alt.Tooltip('Faktor_Emisi_Co2:Q', title='Faktor Emisi CO2')]
)
# Overlay area plot
area = alt.Chart(filtered_df).mark_area(color='Orange', opacity=0.2).encode(
    x='Tahun:O',
    y='Faktor_Emisi_Co2:Q'
)
# Combine the line chart and area plot
chart6 = (chart6 + area).configure_title(
    align='center'
).properties(
    width=600,
    height=400,
    title='Faktor Emisi CO2 Rata-rata (MtCO2)'
)
# Display the chart
st.altair_chart(chart6, use_container_width=True)
st.write('Faktor emisi CO2 rata-rata menunjukkan tingkat emisi CO2 yang dihasilkan per satuan energi yang diproduksi atau dikonsumsi. Perhatian terhadap faktor emisi ini penting untuk memantau efisiensi dan dampak lingkungan dari sektor energi.')





# char 7  Create correlation matrix
correlation_matrix = df.drop(columns=['Tahun']).corr().reset_index().melt('index')
# Create Altair chart
chart7 = alt.Chart(correlation_matrix).mark_rect().encode(
    x='index:O',
    y='variable:O',
    color=alt.Color('value:Q', scale=alt.Scale(scheme='Oranges'), title='Korelasi'),
    tooltip=['index:O', 'variable:O', 'value:Q']
).properties(
    width=600,
    height=400,
    title='Heatmap Korelasi Variabel terhadap Emisi CO2'
)
# Display the chart
st.altair_chart(chart7, use_container_width=True)




# Chart 8
chart8 = alt.Chart(filtered_df).mark_circle(size=100, opacity=0.8).encode(
    x=alt.X('Konsumsi_Batubara_Lignit:Q', title='Konsumsi Batubara Lignit'),
    y=alt.Y('Emisi_Co2_Dari_Bahan_Bakar:Q', title='Emisi CO2'),
    color=alt.Color('Tahun:O', scale=alt.Scale(scheme='oranges'), title='Tahun'),
    tooltip=['Konsumsi_Batubara_Lignit:Q', 'Emisi_Co2_Dari_Bahan_Bakar:Q', 'Tahun:O']
).properties(
    width=600,
    height=400,
    title='Hubungan Konsumsi Batubara Lignit terhadap Emisi CO2'
)
# Display the chart
st.altair_chart(chart8, use_container_width=True)
st.write('korelasi positif yang kuat antara konsumsi batu bara dan lignit dengan emisi CO2, ini mungkin menunjukkan bahwa peningkatan produksi dan konsumsi bahan bakar fosil berkontribusi pada emisi CO2.')


# Chart 9
chart9 = alt.Chart(filtered_df).mark_circle(size=100, opacity=0.8).encode(
    x=alt.X('Kontribusi_Energi_Terbarukan_Untuk_Total_Energi_Listrik(%):Q', title='Kontribusi_Energi_Terbarukan_Untuk_Total_Energi_Listrik(%)'),
    y=alt.Y('Emisi_Co2_Dari_Bahan_Bakar:Q', title='Emisi CO2'),
    color=alt.Color('Tahun:O', scale=alt.Scale(scheme='Blues'), title='Tahun'),
    tooltip=['Kontribusi_Energi_Terbarukan_Untuk_Total_Energi_Listrik(%):Q', 'Emisi_Co2_Dari_Bahan_Bakar:Q', 'Tahun:O']
).properties(
    width=600,
    height=400,
    title='Hubungan Kontribusi_Energi_Terbarukan Untuk Total Energi Listrik(%) terhadap Emisi CO2'
)
# Display the chart
st.altair_chart(chart9, use_container_width=True)
st.write('peningkatan pangsa energi terbarukan dalam produksi listrik berhubungan dengan pengurangan emisi CO2 dari sektor energi. terdapat korelasi negatif yang kuat antara pangsa energi terbarukan dan emisi CO2, ini dapat menunjukkan bahwa peningkatan penggunaan energi terbarukan berkontribusi pada pengurangan emisi CO2.')




# Chart 10
chart10 = alt.Chart(filtered_df).mark_circle(size=100, opacity=0.8).encode(
    x=alt.X('Faktor_Emisi_Co2:Q', title='Faktor_Emisi_Co2'),
    y=alt.Y('Emisi_Co2_Dari_Bahan_Bakar:Q', title='Emisi CO2'),
    color=alt.Color('Tahun:O', scale=alt.Scale(scheme='Blues'), title='Tahun'),
    tooltip=['Faktor_Emisi_Co2:Q', 'Emisi_Co2_Dari_Bahan_Bakar:Q', 'Tahun:O']
).properties(
    width=600,
    height=400,
    title='Hubungan Faktor Emisi Co2 terhadap Emisi CO2'
)
# Display the chart
st.altair_chart(chart10, use_container_width=True)
st.write(' faktor emisi CO2 rata-rata memiliki pengaruh pada emisi CO2 sektor energi')




# Chart 11
chart11 = alt.Chart(filtered_df).mark_circle(size=100, opacity=0.8).encode(
    x=alt.X('Konsumsi_Listrik:Q', title='Konsumsi_Listrik'),
    y=alt.Y('Emisi_Co2_Dari_Bahan_Bakar:Q', title='Emisi CO2'),
    color=alt.Color('Tahun:O', scale=alt.Scale(scheme='Blues'), title='Tahun'),
    tooltip=['Konsumsi_Listrik:Q', 'Emisi_Co2_Dari_Bahan_Bakar:Q', 'Tahun:O']
).properties(
    width=600,
    height=400,
    title='Hubungan Konsumsi Listrik terhadap Emisi CO2'
)
# Display the chart
st.altair_chart(chart11, use_container_width=True)
st.write('korelasi positif dengan emisi CO2 yang tinggi, ini mungkin menunjukkan bahwa konsumsi energi listrik masih bergantung pada sumber energi yang beremisi tinggi.')






st.title('SOLUSI')
import streamlit as st
from PIL import Image

def display_image_with_caption(image_path, caption):
    img = Image.open(image_path)
    framed_img = add_image_frame(img)
    st.image(framed_img, caption=caption, use_column_width=True)

def add_image_frame(image):
    frame_width = 10
    frame_color = 'white'
    framed_image = Image.new('RGB', (image.width + 2*frame_width, image.height + 2*frame_width), frame_color)
    framed_image.paste(image, (frame_width, frame_width))
    return framed_image

# Daftar gambar dan caption
images = [
    {'path': 'WhirlpoolTurbine.jfif','header': 'Whirlpool Turbine', 'caption': 'Dapat memberi daya puluhan rumah selama 24 jam dan menghasilkan 5 kwh sampai 500 kwh'},
    {'path': 'BUNGA.jfif','header': 'Smart Flower', 'caption': 'Menggunakan sistem pelacakan matahari untuk efisiensi yang lebih tinggi'},
    {'path': 'FloatingSolarPlant.jfif','header': 'Floating Solar Plan', 'caption': 'enggunakan air untuk mendinginkan panel'},
    {'path': 'KineticStep.jfif','header': 'Kinetic Step', 'caption': 'Menghasilkan 7KW per langkah'}
]

# Menampilkan empat kolom gambar dengan caption
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader(images[0]['header'])
    display_image_with_caption(images[0]['path'], images[0]['caption'])

with col2:
    st.subheader(images[1]['header'])
    display_image_with_caption(images[1]['path'], images[1]['caption'])

with col3:
    st.subheader(images[2]['header'])
    display_image_with_caption(images[2]['path'], images[2]['caption'])

with col4:
    st.subheader(images[3]['header'])
    display_image_with_caption(images[3]['path'], images[3]['caption'])









