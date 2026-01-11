import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title='Analyze Your Data', page_icon='📊', layout='wide')

st.title('📊 Analyze Your Data')
st.write('📁 Upload A **CSV** Or An **Excel** File To Explore Your Data Interactively!')

# for uploading file
uploaded_file = st.file_uploader('Upload A CSV Or An Excel File', type=['CSV','xlsx'])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file, engine='openpyxl')
        # Task1: allow user to also submit in xlsx
        # converting bool columns as str
        bool_cols = data.select_dtypes(include=['bool']).columns
        data[bool_cols] = data[bool_cols].astype('str')
    except Exception as e:
        st.error('Could Not Read Excel / CSV File. Please Check The File Format.')
        st.exception(e)
        st.stop()

    st.success('✅ File Uploaded Successfully!')
    st.write('### Preview Of Data')
    st.dataframe(data.head())

    st.write('### 📋 Data Overview')
    st.write('Number Of Rows: ',data.shape[0])
    st.write('Number Of Columns: ',data.shape[1])
    st.write('Number Of Missing Values: ',data.isnull().sum().sum())
    st.write('Number Of Duplicate Records: ',data.duplicated().sum())

    st.write('### 🗄️ Complete Summary Of Dataset')
    deet = io.StringIO()
    data.info(buf=deet)
    i = deet.getvalue()
    st.text(i)

    st.write('### 📈 Statistical Summary Of Dataset')
    st.dataframe(data.describe())

    st.write('### 📈 Statistical Summary For Non-Numerical features Of Dataset')
    non_num = data.select_dtypes(exclude=['number'])
    if non_num.empty:
        st.write("This Data Does Not Contain Non-Numerical Data")
    else:
        st.dataframe(data.describe(include=['bool','object']))
    # create IF code if for data set that doesn't have numerical
    # ORIGINAL code: st.dataframe(data.describe(include=['bool','object']))

    st.write('### 🗳️ Select The Desired Columns For Analysis')
    selected_columns = st.multiselect('Choose Columns', data.columns.tolist())

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.info('No Columns Selected. Showing Full Dataset')
        st.dataframe(data.head())

    st.write('### 📈 Data Visualization')
    st.write('Select **Columns** For Data Visualization')
    columns = data.columns.tolist()
    x_axis=st.selectbox('Select Column For X-Azis', options=columns)
    y_axis=st.selectbox('Select Column For Y-Axis', options=columns)

    # Create Buttons For Diff Diff Charts
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        line_btn = st.button('Line Graph')
    with col2:
        scatter_btn = st.button('Scatter Graph')
    with col3:
        bar_btn = st.button('Bar Graph')
    with col4:
        heatmap_btn = st.button('Heatmap')
    with col5:
        pie_btn = st.button('Pie Chart')
    
    if line_btn:
        st.write('### Showing A Line Graph')
        fig,ax = plt.subplots()
        ax.plot(data[x_axis], data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_xlabel(x_axis)
        ax.set_title(f'Line Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)

    if scatter_btn:
        st.write('### Showing A Scatter Graph')
        fig,ax = plt.subplots()
        ax.scatter(data[x_axis], data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Scatter Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)

    if bar_btn:
        st.write('### Showing A Bar Graph')
        grouped = data.groupby(x_axis)[y_axis].mean()
        fig, ax = plt.subplots()
        ax.bar(grouped.index, grouped.values)
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Bar Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)

    if heatmap_btn:
        st.write('### Showing A Heatmap')
        corr = data.select_dtypes(include='number').corr()
        fig, ax = plt.subplots()
        cax = ax.imshow(corr)
        fig.colorbar(cax)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha='right')
        ax.set_yticklabels(corr.columns)
        st.pyplot(fig)

    if pie_btn:
        st.write('### Showing A Pie Chart')
        counts = data[x_axis].value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
        ax.set_title(f'Distribution of {x_axis}')
        st.pyplot(fig)
else:
    st.info('Please Upload A CSV Or An Excel File To Get Started')