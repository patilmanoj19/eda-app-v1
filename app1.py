import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to perform EDA
def perform_eda(df):
    # Display basic dataset information
    st.subheader("Basic Dataset Information")
    st.write("Variable names:", df.columns.tolist())
    st.write("Shape of the dataset:", df.shape)
    st.write("Dataset Information:")
    st.write(df.info())

    # Display missing values
    st.subheader("Missing Values")
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    st.write("Missing values by columns in percentage:")
    st.write(missing_percentage)
    
    # Summary statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # Separate categorical and numerical variables
    categorical_vars = df.select_dtypes(include=['object']).columns.tolist()
    numerical_vars = df.select_dtypes(exclude=['object']).columns.tolist()

    # Univariate analysis
    st.subheader("Univariate Analysis")
    for col in numerical_vars:
        st.write(f"### {col}")
        st.write("Histogram:")
        st.pyplot(plt.hist(df[col], bins='auto', color='blue', alpha=0.7))
        st.write("KDE Plot:")
        sns.kdeplot(df[col], color='green', shade=True, alpha=0.3)
        st.pyplot()
        st.write("Box Plot:")
        st.pyplot(sns.boxplot(df[col]))

    for col in categorical_vars:
        st.write(f"### {col}")
        st.write("Value Counts:")
        st.write(df[col].value_counts())
        st.write("Bar Plot:")
        st.pyplot(sns.countplot(data=df, x=col))
        st.write("Pie Chart:")
        st.pyplot(plt.pie(df[col].value_counts(), labels=df[col].value_counts().index, autopct='%1.1f%%'))

    # Bivariate Analysis
    st.subheader("Bivariate Analysis")
    # Crosstab for categorical variables
    categorical_cols = st.multiselect("Select categorical variables for cross-tabulation:", categorical_vars)
    if len(categorical_cols) == 2:
        st.write("Cross-tabulation:")
        st.write(pd.crosstab(df[categorical_cols[0]], df[categorical_cols[1]]))
    else:
        st.write("Please select exactly 2 categorical variables for cross-tabulation.")

# Main function
def main():
    st.title("Exploratory Data Analysis (EDA) App")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('xls', 'xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return
        perform_eda(df)

if __name__ == "__main__":
    main()
