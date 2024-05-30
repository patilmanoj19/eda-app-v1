import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, chi2_contingency, anderson
from wordcloud import WordCloud

# Function to perform univariate analysis
def univariate_analysis(data, selected_column):
    st.subheader("Univariate Analysis")
    # Display histogram
    st.write("### Histogram")
    plt.hist(data[selected_column], bins=20, color='skyblue', edgecolor='black')
    st.pyplot()

    # Display distribution plot
    st.write("### Distribution Plot")
    sns.distplot(data[selected_column], hist=True, kde=True, color='blue')
    st.pyplot()

    # Additional analysis tasks can be added here

# Function to perform bivariate analysis
def bivariate_analysis(data, selected_column1, selected_column2):
    st.subheader("Bivariate Analysis")
    # Display scatter plot
    st.write("### Scatter Plot")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=selected_column1, y=selected_column2, data=data)
    st.pyplot()

    # Additional analysis tasks can be added here

# Function to perform multivariate analysis
def multivariate_analysis(data, selected_columns):
    st.subheader("Multivariate Analysis")
    # Display heatmap
    st.write("### Heatmap")
    sns.heatmap(data[selected_columns].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    st.pyplot()

    # Additional analysis tasks can be added here

def main():
    st.title("Exploratory Data Analysis (EDA)")

    # Upload dataset
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data.head())

        # Display basic information about the dataset
        st.write("### Basic Information")
        st.write(data.info())

        # Select variable for analysis
        selected_column = st.selectbox("Select a variable for analysis", data.columns)

        # Perform univariate analysis
        univariate_analysis(data, selected_column)

        # Perform bivariate analysis (select two variables)
        if st.checkbox("Perform Bivariate Analysis"):
            selected_column1 = st.selectbox("Select first variable", data.columns)
            selected_column2 = st.selectbox("Select second variable", data.columns)
            bivariate_analysis(data, selected_column1, selected_column2)

        # Perform multivariate analysis
        if st.checkbox("Perform Multivariate Analysis"):
            selected_columns = st.multiselect("Select variables for analysis", data.columns)
            multivariate_analysis(data, selected_columns)

# Execute the main function
if __name__ == "__main__":
    main()
