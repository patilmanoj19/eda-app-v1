import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Web App Title
st.markdown('''
# **The Simple EDA App**

This is the **Simple EDA App** created in Streamlit for basic data exploration.

**Credit:** App built in `Python` + `Streamlit` by [Manojkumar Patil](https://www.linkedin.com/in/patilmanojkumar)

---
''')

# File uploader
with st.sidebar.header('1. Upload your CSV or Excel file'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=["csv", "xlsx"])
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")

# Load data
def load_data(file):
    if file is not None:
        try:
            df = pd.read_csv(file)
        except Exception as e:
            df = pd.read_excel(file)
        return df
    return None

# Function to display basic dataset information
def display_basic_info(df):
    st.subheader("Basic Dataset Information")
    st.write("Variable names:", df.columns.tolist())
    st.write("Shape of the dataset:", df.shape)
    st.write("Dataset Information:")
    buffer = pd.DataFrame(df.dtypes, columns=['dtype']).reset_index()
    buffer.columns = ['Column', 'Data Type']
    buffer['Missing Values'] = df.isnull().sum().values
    buffer['Missing Values (%)'] = ((df.isnull().sum() / len(df)) * 100).values
    st.dataframe(buffer)

# Function to display missing values
def display_missing_values(df):
    st.subheader("Missing Values")
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    st.write("Missing values by columns in percentage:")
    st.write(missing_percentage)

# Function to display summary statistics
def display_summary_statistics(df):
    st.subheader("Summary Statistics")
    st.write(df.describe())

# Main function
def main():
    df = load_data(uploaded_file)
    
    if df is not None:
        st.header('**Input DataFrame**')
        st.write(df)
        st.write('---')

        display_basic_info(df)
        st.write('---')
        
        display_missing_values(df)
        st.write('---')
        
        display_summary_statistics(df)
    else:
        st.info('Awaiting for file to be uploaded.')

# Run main function
if __name__ == '__main__':
    main()
