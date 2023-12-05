import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

# --- READ DATA ---
mitra = pd.read_pickle('data/mitra.pkl')

# --- ROW 1 ---
st.write('# Dasbor Mitra BPS Kota Sungai Penuh')
st.write("""Mitra Statistik adalah ujung tombak kualitas data statistik. Seiring dengan meningkatnya 
         kualitas dan kuantitas survei, maka diperlukan dasbor Mitra Statistik BPS Kota Sungai Penuh 
         untuk merekrut Mitra terbaik untuk pekerjaan Sensus dan Survei di BPS""")

st.divider()
col3, col4 = st.columns(2)

## --- INPUT SELECT ---
input_select = col3.selectbox(
    label='Pilih Kabupaten/Kota Asal Pendaftar',
    options=mitra['city'].unique()
)

## --- INPUT SLIDER ---
input_slider = col4.slider(
    label='Pilih Rentang Usia',
    min_value=mitra['age'].min(),
    max_value=mitra['age'].max(),
    value=[20,50]
)

min_slider = input_slider[0]
max_slider = input_slider[1]

# --- ROW 4 ---
col5, col6 = st.columns(2)

## --- BARPLOT ---
# data: barplot
mitra = mitra[mitra['city'] == input_select]
df_kec = pd.crosstab(index=mitra.district, columns='Total', colnames=[None])
df_kec = df_kec.reset_index()

# plot: barplot
plot_gen = px.bar(df_kec.sort_values(by='Total',ascending=False), x='district', y='Total', 
                   labels = {'district' : 'Kecamatan',
                             'Total' : 'Jumlah Mitra'})

col5.write(f'### Jumlah Mitra dengan KTP {input_select}  ') # f-string
col5.plotly_chart(plot_gen, use_container_width=True)

## --- MULTIVARIATE ---
# data: multivariate
employ_age = mitra[mitra['age'].between(left=min_slider, right=max_slider)]
dept_gender = pd.crosstab(index=employ_age['Pendidikan'],
                          columns=employ_age['Jenis Kelamin'],
                          colnames=[None])
dept_gender_melt = dept_gender.melt(ignore_index=False, var_name='Jenis Kelamin', value_name='num_people')
dept_gender_melt = dept_gender_melt.reset_index()

# plot: multivariate
plot_dept = px.bar(dept_gender_melt.sort_values(by='num_people'), 
                   x="num_people", y="Pendidikan", 
                   color="Jenis Kelamin", 
                   barmode='group',
                   labels = {'num_people' : 'Jumlah Mitra',
                             'Pendidikan' : 'Pendidikan',
                             'Jenis Kelamin': 'Jenis Kelamin'}
                             )

col6.write(f'### Jumlah Mitra KTP {input_select} Menurut Pendidikan dan Jenis Kelamin, Umur {min_slider} s/d {max_slider} Tahun')
col6.plotly_chart(plot_dept, use_container_width=True)

# --- ROW 7 ---
col6, col7 = st.columns(2)

input_slider_ujian = col7.slider(
    label='Pilih Rentang Nilai',
    min_value=0,
    max_value=100,
    value= [70,95]
)

min_ujian_slider = input_slider_ujian[0]
max_ujian_slider = input_slider_ujian[1]

nilai_gen = mitra.pivot_table(index='generation',values='Nilai Ujian',aggfunc='mean').round(2)\
    .sort_values(by='Nilai Ujian')
nilai_gen_melt = nilai_gen.reset_index()
plot_nilai_gen = px.bar(nilai_gen_melt, x='generation',y='Nilai Ujian',
       barmode='group',
                   labels = {'generation' : 'Generasi',
                             'Nilai Ujian' : 'Nilai Ujian'}
                             )
col6.write(f'### Rata-rata Nilai Ujian Mitra KTP {input_select} Menurut Generasi') # f-string
col6.plotly_chart(plot_nilai_gen, use_container_width=True)



filter_mitra = mitra[(mitra['Nilai Ujian'] >= min_ujian_slider) & 
                           (mitra['Nilai Ujian'] <= max_ujian_slider)]
col7.write(f'### Daftar Mitra KTP {input_select} Terpilih')
col7.table(filter_mitra)