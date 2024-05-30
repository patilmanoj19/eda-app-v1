import numpy as np
import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import matplotlib.pyplot as plt
import seaborn as sns

# Web App Title
st.markdown('''
# **The EDA App**

This is the **EDA App** created in Streamlit using the **pandas-profiling** library.

**Credit:** App built in `Python` + `Streamlit` by [Manojkumar Patil](https://www.linkedin.com/in/patilmanojkumar)

---
''')

# Upload CSV or Excel data
with st.sidebar.header('1. Upload your data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV or Excel file", type=["csv", "xlsx"])
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")

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
    univariate_analysis_choice = st.selectbox("Select analysis type:", ["Numerical", "Categorical"])
    if univariate_analysis_choice == "Numerical":
        for col in numerical_vars:
            st.write(f"### {col}")
            st.write("Histogram:")
            st.pyplot(plt.hist(df[col], bins='auto', color='blue', alpha=0.7))
            st.write("KDE Plot:")
            sns.kdeplot(df[col], color='green', shade=True, alpha=0.3)
            st.pyplot()
            st.write("Box Plot:")
            st.pyplot(sns.boxplot(df[col]))
    elif univariate_analysis_choice == "Categorical":
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
    bivariate_analysis_choice = st.selectbox("Select analysis type:", ["Categorical vs. Categorical", "Categorical vs. Numerical"])
    if bivariate_analysis_choice == "Categorical vs. Categorical":
        categorical_cols = st.multiselect("Select categorical variables for cross-tabulation:", categorical_vars)
        if len(categorical_cols) == 2:
            st.write("Cross-tabulation:")
            st.write(pd.crosstab(df[categorical_cols[0]], df[categorical_cols[1]]))
        else:
            st.write("Please select exactly 2 categorical variables for cross-tabulation.")
    elif bivariate_analysis_choice == "Categorical vs. Numerical":
        categorical_col = st.selectbox("Select a categorical variable:", categorical_vars)
        numerical_col = st.selectbox("Select a numerical variable:", numerical_vars)
        st.write("Box Plot:")
        st.pyplot(sns.boxplot(data=df, x=categorical_col, y=numerical_col))

# Main function
def main():
    if uploaded_file is not None:
        if uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('xls', 'xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return
        perform_eda(df)
    else:
        st.info('Awaiting for CSV or Excel file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            # Example data
            @st.cache_data
            def load_data():
                a = pd.DataFrame(
                    np.random.rand(100, 5),
                    columns=['a', 'b', 'c', 'd', 'e']
                )
                return a
            df = load_data()
            perform_eda(df)

if __name__ == "__main__":
    main()
