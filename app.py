import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO  # Import StringIO for buffering info output

# Web App Title
st.markdown('''
# **EDA App**

This is the **EDA App** created in Streamlit for basic data exploration.

**Credit:** App built in `Python` + `Streamlit` by [Manojkumar Patil](https://www.linkedin.com/in/patilmanojkumar)

---
''')

# File uploader
with st.sidebar.header('Upload your CSV or Excel file'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=["csv", "xlsx"])
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/patilmanoj19/eda-app-v1/main/Bangalore_Price_Data_Wheat.csv)
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
    
    buffer = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes,
        'Missing Values': df.isnull().sum(),
        'Missing Values (%)': (df.isnull().sum() / len(df)) * 100
    }).reset_index(drop=True)
    
    st.dataframe(buffer)
    
    # Using StringIO to capture df.info() output
    buffer = StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    
    st.subheader("Summary Statistics")
    st.write(df.describe())

# Function to display histograms and KDE plots for numeric variables
def plot_numeric_data(df):
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    st.subheader("Numeric Data Distribution")
    for col in numeric_columns:
        st.write(f"**{col}**")
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        
        sns.histplot(df[col], kde=True, ax=ax[0])
        ax[0].set_title(f'Histogram of {col}')
        
        sns.kdeplot(df[col], ax=ax[1])
        ax[1].set_title(f'KDE Plot of {col}')
        
        st.pyplot(fig)

# Function to display value counts bar plot for categorical variables
def plot_categorical_data(df):
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    st.subheader("Categorical Data Distribution")
    for col in categorical_columns:
        st.write(f"**{col}**")
        fig, ax = plt.subplots(figsize=(8, 4))
        
        sns.countplot(y=df[col], order=df[col].value_counts().index, ax=ax)
        ax.set_title(f'Value Counts of {col}')
        
        st.pyplot(fig)

# Function to display the correlation matrix
def plot_correlation_matrix(df):
    st.subheader("Correlation Matrix")
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])
    corr_matrix = numeric_columns.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Matrix')
    
    st.pyplot(fig)

# Main function
def main():
    df = load_data(uploaded_file)
    
    if df is not None:
        st.header('**Input DataFrame**')
        st.write(df.head())
        st.write('---')

        display_basic_info(df)
        st.write('---')
        
        plot_numeric_data(df)
        st.write('---')
        
        plot_categorical_data(df)
        st.write('---')

        plot_correlation_matrix(df)
        st.write('---')
                 
    else:
        st.info('Awaiting for CSV/Excel file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            # Example data
            @st.cache_data
            def load_example_data():
                return pd.read_csv('https://raw.githubusercontent.com/patilmanoj19/eda-app-v1/main/Bangalore_Price_Data_Wheat.csv')
            
            example_df = load_example_data()
            st.write(example_df.head())
            st.write('---')

            display_basic_info(example_df)
            st.write('---')
            
            plot_numeric_data(example_df)
            st.write('---')
            
            plot_categorical_data(example_df)
            st.write('---')

            plot_correlation_matrix(example_df)
            st.write('---')

# Run main function
if __name__ == '__main__':
    main()
