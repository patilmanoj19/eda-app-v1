import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

dataframe = None

def upload_file(file):
    global dataframe
    if file.name.endswith('.csv'):
        dataframe = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        dataframe = pd.read_excel(file)
    return {"filename": file.name}

def do_eda():
    global dataframe
    if dataframe is None:
        return {"error": "No file uploaded"}

    st.title("Exploratory Data Analysis")
    st.write("## DataFrame Info")
    st.write(dataframe.info())
    st.write("## DataFrame Description")
    st.write(dataframe.describe())

    st.write("## Univariate Analysis")
    for column in dataframe.select_dtypes(include=['float64', 'int64']).columns:
        st.write(f"### {column}")
        st.write(dataframe[column].describe())
        plt.hist(dataframe[column])
        plt.xlabel(column)
        plt.ylabel("Frequency")
        st.pyplot()

        plt.figure()
        plt.title(f"{column} Distribution")
        plt.xlabel(column)
        plt.ylabel("Density")
        dataframe[column].plot.kde()
        st.pyplot()

    st.write("## Bivariate Analysis")
    numeric_columns = dataframe.select_dtypes(include=['float64', 'int64']).columns
    for i, column1 in enumerate(numeric_columns):
        for j, column2 in enumerate(numeric_columns):
            if i != j:
                st.write(f"### {column1} vs {column2}")
                plt.scatter(dataframe[column1], dataframe[column2])
                plt.xlabel(column1)
                plt.ylabel(column2)
                st.pyplot()

    return {"status": "EDA completed"}

# Streamlit UI
st.sidebar.title("Upload File")
file = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx"])

if file is not None:
    upload_file(file)
    if st.sidebar.button("Perform EDA"):
        do_eda()
